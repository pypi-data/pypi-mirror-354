import os
import shutil

import googleapiclient.discovery
from typing import Optional, Dict, Any, Tuple
import yt_dlp
import time
from functools import wraps
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from rich.console import Console
from rich.progress import Progress
import platform
import subprocess
from openai import OpenAI
import requests
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle

from .config import Config
import whisper
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from huggingface_hub.utils import EntryNotFoundError
from huggingface_hub import try_to_load_from_cache, _CACHED_NO_EXIST

console = Console()

WHISPER_CPP_REQUIRED_AUDIO_RATE = 16000

class YouTubeAPIError(Exception):
    """Base exception for YouTube API errors"""
    pass

class APIQuotaExceededError(YouTubeAPIError):
    """Raised when YouTube API quota is exhausted"""
    pass

class VideoUnavailableError(YouTubeAPIError):
    """Raised when video is unavailable or restricted"""
    pass

def retry(retries: int = 3, delay: int = 5, exceptions: tuple = (Exception,)):
    """Decorator for retrying API calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= retries:
                        raise
                    time.sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class YouTubeProcessor:
    def __init__(self, config: Config):
        self.config = config
        self.youtube = None
        self.credentials = None
        
        # Try OAuth authentication first, then fall back to API key
        oauth_file_path = os.path.expanduser(config.youtube.oauth_client_secrets_file) if config.youtube.oauth_client_secrets_file else None
        if oauth_file_path and os.path.exists(oauth_file_path):
            try:
                self.youtube = self._build_oauth_service()
                console.print("[green]Successfully authenticated with OAuth 2.0[/green]")
            except Exception as e:
                console.print(f"[yellow]OAuth authentication failed: {str(e)}. Falling back to API key.[/yellow]")
                self._try_api_key_auth()
        elif config.youtube.api_key:
            self._try_api_key_auth()
        else:
            console.print("[yellow]Warning: Neither OAuth credentials nor YouTube API key is configured. Some features will be limited.[/yellow]")
    
    def _try_api_key_auth(self):
        """Try to authenticate using API key."""
        try:
            self.youtube = build('youtube', 'v3', developerKey=self.config.youtube.api_key)
            console.print("[green]Successfully authenticated with API key[/green]")
        except HttpError as e:
            if e.resp.status == 403:
                raise APIQuotaExceededError("YouTube API quota exceeded") from e
            raise YouTubeAPIError(f"YouTube API connection failed: {str(e)}") from e
    
    def _build_oauth_service(self):
        """Build YouTube service using OAuth 2.0 authentication."""
        console.print("[blue]Starting OAuth 2.0 authentication process...[/blue]")
        
        # Define the scopes required for YouTube Data API
        # Note: youtube.force-ssl is required for caption downloads
        SCOPES = [
            'https://www.googleapis.com/auth/youtube.readonly',
            'https://www.googleapis.com/auth/youtube.force-ssl',
            'https://www.googleapis.com/auth/youtubepartner'
        ]
        console.print(f"[blue]Required scopes: {', '.join(SCOPES)}[/blue]")
        
        # Validate and load OAuth client secrets file
        secrets_file = os.path.expanduser(self.config.youtube.oauth_client_secrets_file)
        console.print(f"[blue]Loading OAuth client secrets from: {secrets_file}[/blue]")
        
        if not os.path.exists(secrets_file):
            raise YouTubeAPIError(f"OAuth client secrets file not found: {secrets_file}")
        
        # Load and validate client secrets file content
        try:
            import json
            with open(secrets_file, 'r') as f:
                secrets_data = json.load(f)
            
            # Validate the structure of the client secrets file
            if 'installed' in secrets_data:
                client_info = secrets_data['installed']
                console.print("[green]✓ Found 'installed' application type in client secrets[/green]")
            elif 'web' in secrets_data:
                client_info = secrets_data['web']
                console.print("[yellow]⚠ Found 'web' application type - this may cause issues with desktop authentication[/yellow]")
            else:
                raise YouTubeAPIError("Invalid client secrets file format - missing 'installed' or 'web' section")
            
            # Log client information (without exposing sensitive data)
            client_id = client_info.get('client_id', '')
            if client_id:
                # Show only first and last few characters for security
                masked_client_id = f"{client_id[:12]}...{client_id[-8:]}" if len(client_id) > 20 else "[MASKED]"
                console.print(f"[blue]Client ID: {masked_client_id}[/blue]")
            else:
                raise YouTubeAPIError("Client ID not found in secrets file")
            
            if 'client_secret' in client_info:
                console.print("[green]✓ Client secret found in secrets file[/green]")
            else:
                raise YouTubeAPIError("Client secret not found in secrets file")
            
            console.print(f"[blue]Auth URI: {client_info.get('auth_uri', 'Not specified')}[/blue]")
            console.print(f"[blue]Token URI: {client_info.get('token_uri', 'Not specified')}[/blue]")
            
        except json.JSONDecodeError as e:
            raise YouTubeAPIError(f"Invalid JSON in client secrets file: {str(e)}")
        except Exception as e:
            raise YouTubeAPIError(f"Error reading client secrets file: {str(e)}")
        
        creds = None
        # Token file stores the user's access and refresh tokens
        token_file = os.path.expanduser('~/.config/ytbrf/token.pickle')
        console.print(f"[blue]Token storage location: {token_file}[/blue]")
        
        # Load existing credentials if available
        if os.path.exists(token_file):
            console.print("[blue]Loading existing OAuth tokens...[/blue]")
            try:
                with open(token_file, 'rb') as token:
                    creds = pickle.load(token)
                console.print("[green]✓ Successfully loaded existing OAuth tokens[/green]")
                
                # Check token validity
                if creds.valid:
                    console.print("[green]✓ Existing tokens are valid[/green]")
                elif creds.expired:
                    console.print("[yellow]⚠ Existing tokens are expired[/yellow]")
                else:
                    console.print("[yellow]⚠ Existing tokens are invalid[/yellow]")
                    
            except Exception as e:
                console.print(f"[yellow]Failed to load existing tokens: {str(e)}[/yellow]")
                creds = None
        else:
            console.print("[blue]No existing OAuth tokens found[/blue]")
        
        # If there are no (valid) credentials available, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                console.print("[blue]Attempting to refresh expired tokens...[/blue]")
                try:
                    creds.refresh(Request())
                    console.print("[green]✓ Successfully refreshed OAuth credentials[/green]")
                except Exception as e:
                    console.print(f"[yellow]Failed to refresh credentials: {str(e)}. Starting new authentication flow...[/yellow]")
                    creds = None
            
            if not creds:
                console.print("[blue]Starting new OAuth authentication flow...[/blue]")
                console.print("[yellow]A browser window will open for authentication. Please complete the authorization process.[/yellow]")
                
                try:
                    flow = InstalledAppFlow.from_client_secrets_file(secrets_file, SCOPES)
                    creds = flow.run_local_server(port=0)
                    console.print("[green]✓ Successfully completed OAuth authentication flow[/green]")
                except Exception as e:
                    raise YouTubeAPIError(f"OAuth authentication failed: {str(e)}")
            
            # Save the credentials for the next run
            console.print("[blue]Saving OAuth tokens for future use...[/blue]")
            try:
                os.makedirs(os.path.dirname(token_file), exist_ok=True)
                with open(token_file, 'wb') as token:
                    pickle.dump(creds, token)
                console.print(f"[green]✓ OAuth tokens saved to {token_file}[/green]")
            except Exception as e:
                console.print(f"[yellow]Warning: Failed to save tokens: {str(e)}[/yellow]")
        
        # Final validation
        if not creds or not creds.valid:
            raise YouTubeAPIError("Failed to obtain valid OAuth credentials")
        
        console.print("[blue]Building YouTube API service with OAuth credentials...[/blue]")
        self.credentials = creds
        
        try:
            service = build('youtube', 'v3', credentials=creds)
            console.print("[green]✓ Successfully created YouTube API service with OAuth authentication[/green]")
            return service
        except Exception as e:
            raise YouTubeAPIError(f"Failed to build YouTube service: {str(e)}")

    def get_video_info(self, url: str) -> Dict[str, Any]:
        """Extract video information using yt-dlp."""
        try:
            with yt_dlp.YoutubeDL() as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'id': info['id'],
                    'title': info['title'],
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', ''),
                    'description': info.get('description', ''),
                    'thumbnail': info.get('thumbnail', ''),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'upload_date': info.get('upload_date', ''),
                }
        except Exception as e:
            console.print(f"[red]Error extracting video info: {str(e)}[/red]")
            raise

    @retry(retries=3, delay=5, exceptions=(APIQuotaExceededError, HttpError))
    def get_transcript(self, video_id: str) -> Optional[str]:
        """Try to get transcript from YouTube API."""
        if not self.youtube:
            console.print("[yellow]Cannot get transcript: YouTube API not available[/yellow]")
            return None

        try:
            console.print(f"[blue]Requesting captions list for video ID: {video_id}[/blue]")
            
            # Print full request context before API call
            console.print("[cyan]═══ API REQUEST CONTEXT ═══[/cyan]")
            console.print(f"[cyan]Method: captions().list[/cyan]")
            console.print(f"[cyan]Parameters:[/cyan]")
            console.print(f"[cyan]  - part: 'snippet'[/cyan]")
            console.print(f"[cyan]  - videoId: '{video_id}'[/cyan]")
            console.print(f"[cyan]Service object: {type(self.youtube)}[/cyan]")
            console.print(f"[cyan]Credentials valid: {self.credentials.valid if hasattr(self, 'credentials') and self.credentials else 'No credentials'}[/cyan]")
            if hasattr(self, 'credentials') and self.credentials:
                console.print(f"[cyan]Token: {self.credentials.token[:20] if self.credentials.token else 'No token'}...[/cyan]")
                console.print(f"[cyan]Scopes: {self.credentials.scopes if hasattr(self.credentials, 'scopes') else 'No scopes info'}[/cyan]")
            console.print("[cyan]═══════════════════════════[/cyan]")
            
            transcript_list = self.youtube.captions().list(
                part="snippet",
                videoId=video_id
            ).execute()
            
            console.print(f"[blue]API Response - transcript_list: {transcript_list}[/blue]")
            console.print(f"[blue]Number of caption items found: {len(transcript_list.get('items', []))}[/blue]")
            
            if not transcript_list['items']:
                console.print("[yellow]No caption items found in the response[/yellow]")
                return None
            
            # Print details about available captions
            for i, item in enumerate(transcript_list['items']):
                console.print(f"[blue]Caption {i}: ID={item['id']}, Language={item['snippet'].get('language', 'unknown')}, Name={item['snippet'].get('name', 'unknown')}[/blue]")
                
            # Select the best caption: prioritize captions where language equals name
            best_caption = None
            for item in transcript_list['items']:
                language = item['snippet'].get('language', '')
                name = item['snippet'].get('name', '')
                if language == name and language:  # Language equals name and both are non-empty
                    best_caption = item
                    console.print(f"[green]Found optimal caption where language equals name: {language}[/green]")
                    break
            
            # If no optimal caption found, use the first available one
            if not best_caption:
                best_caption = transcript_list['items'][0]
                console.print(f"[yellow]No optimal caption found, using first available caption[/yellow]")
            
            caption_id = best_caption['id']
            console.print(f"[blue]Downloading transcript with caption ID: {caption_id}[/blue]")
            
            # Print full request context before download API call
            console.print("[cyan]═══ DOWNLOAD API REQUEST CONTEXT ═══[/cyan]")
            console.print(f"[cyan]Method: captions().download[/cyan]")
            console.print(f"[cyan]Parameters:[/cyan]")
            console.print(f"[cyan]  - id: '{caption_id}'[/cyan]")
            console.print(f"[cyan]  - tfmt: 'srt'[/cyan]")
            console.print(f"[cyan]Service object: {type(self.youtube)}[/cyan]")
            console.print(f"[cyan]Credentials valid: {self.credentials.valid if hasattr(self, 'credentials') and self.credentials else 'No credentials'}[/cyan]")
            if hasattr(self, 'credentials') and self.credentials:
                console.print(f"[cyan]Token: {self.credentials.token[:20] if self.credentials.token else 'No token'}...[/cyan]")
                console.print(f"[cyan]Scopes: {self.credentials.scopes if hasattr(self.credentials, 'scopes') else 'No scopes info'}[/cyan]")
            console.print("[cyan]═══════════════════════════════════[/cyan]")
            
            transcript = self.youtube.captions().download(
                id=caption_id,
                tfmt='srt'
            ).execute()
            
            console.print(f"[blue]Downloaded transcript type: {type(transcript)}, length: {len(transcript) if transcript else 0}[/blue]")
            
            if isinstance(transcript, bytes):
                decoded_transcript = transcript.decode('utf-8')
                console.print(f"[blue]Decoded transcript length: {len(decoded_transcript)}[/blue]")
                console.print(f"[blue]First 200 characters of transcript: {decoded_transcript[:200]}...[/blue]")
                return decoded_transcript
            else:
                console.print(f"[blue]Transcript is not bytes, returning as-is: {transcript[:200] if transcript else 'None'}...[/blue]")
                return transcript
                
        except HttpError as e:
            console.print(f"[red]HttpError occurred: Status={e.resp.status}, Reason={e.resp.reason}[/red]")
            console.print(f"[red]Error details: {str(e)}[/red]")
            console.print(f"[red]Error content: {e.content if hasattr(e, 'content') else 'No content'}[/red]")
            return None
        except Exception as e:
            console.print(f"[red]Unexpected error in get_transcript: {type(e).__name__}: {str(e)}[/red]")
            return None

    def download_audio(self, url: str, output_filename_wo_ext: str = None) -> Tuple[str, str]:
        """Download audio from YouTube video.
        
        Returns:
            Tuple[str, str]: (audio_path, format)
        """
        video_info = self.get_video_info(url)
        if output_filename_wo_ext is None:
            output_filename_wo_ext = video_info['title']
        try:
            # First try with audio extraction
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessor_args': [
                    '-ar', str(WHISPER_CPP_REQUIRED_AUDIO_RATE)  # Set audio sampling rate to 16000 Hz
                ],
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': self.config.youtube.audio_format,
                    'preferredquality': self.config.youtube.audio_quality,
                }],
                'outtmpl': output_filename_wo_ext,
            }
            
            with Progress() as progress:
                task = progress.add_task("[cyan]Downloading audio...", total=None)
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    
                    # Get the actual output path (yt-dlp might modify it)
                    base_path = os.path.splitext(output_filename_wo_ext)[0]
                    audio_path = f"{base_path}.{self.config.youtube.audio_format}"
                    
                    return audio_path, self.config.youtube.audio_format
                except Exception as e:
                    if "ffprobe and ffmpeg not found" in str(e):
                        console.print("[yellow]ffmpeg not found. Falling back to direct download without audio extraction.[/yellow]")
                        # Fall back to direct download without audio extraction
                        ydl_opts = {
                            'format': 'bestaudio/best',
                            'outtmpl': output_filename_wo_ext,
                        }
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])
                        
                        # The format will be whatever yt-dlp downloaded
                        # We need to find the actual file that was created
                        for ext in ['mp4', 'webm', 'm4a', 'mp3']:
                            possible_path = f"{output_filename_wo_ext}.{ext}"
                            if os.path.exists(possible_path):
                                return possible_path, ext
                        
                        # If we can't find the file, raise the original error
                        raise
                    else:
                        raise
        except Exception as e:
            console.print(f"[red]Error downloading audio: {str(e)}[/red]")
            raise

    def check_video_availability(self, url: str) -> bool:
        """Check if the video is available and accessible."""
        try:
            with yt_dlp.YoutubeDL() as ydl:
                ydl.extract_info(url, download=False)
            return True
        except Exception as e:
            console.print(f"[red]Video is not available: {str(e)}[/red]")
            return False

    def get_video_metadata(self, url: str) -> Dict[str, Any]:
        """Get comprehensive video metadata including availability and transcript status."""
        if not self.check_video_availability(url):
            raise VideoUnavailableError("Video is not available or restricted")

        info = self.get_video_info(url)
        
        # Only check for transcript if YouTube API is available
        has_transcript = False
        if self.youtube:
            has_transcript = bool(self.get_transcript(info['id']))

        return {
            **info,
            'has_transcript': has_transcript,
            'needs_local_transcription': not has_transcript,
        }

    def _ensure_model_downloaded(self, model_name: str):
        # Check if model is cached locally, if not, download it
        try:
            _ = try_to_load_from_cache(model_name, 'config.json')
        except EntryNotFoundError:
            # Download model and tokenizer
            AutoTokenizer.from_pretrained(model_name)
            AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def summarize(self, text: str, model_name: str = None) -> str:
        summary_cfg = self.config.summary
        model_name = getattr(summary_cfg, "model", "gpt-3.5-turbo")
        console.print(f"[yellow]Summarization model selected: {model_name}[/yellow]")                 

        if getattr(summary_cfg, "type", None) == "openai":
            headers = {"Authorization": f"Bearer {summary_cfg.api_key}", "Content-Type": "application/json"}
            system_prompt = "You are a helpful AI assistant that summarizes text based on given instructions."

            user_prompt = f'''
{summary_cfg.prompt}

{text.strip()}
'''
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": text.strip()}
                ],
                "temperature": 0.2
            }
            from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential
            
            @retry(
                retry=retry_if_exception(lambda e: isinstance(e, requests.exceptions.HTTPError) 
                                        and 400 <= e.response.status_code < 500),
                stop=stop_after_attempt(3),
                wait=wait_exponential(multiplier=1, min=2, max=10)
            )
            def _retry_openai_request():
                response = requests.post(f"{summary_cfg.server_url}/chat/completions", 
                                       json=payload, headers=headers)
                response.raise_for_status()
                return response
            
            response = _retry_openai_request()
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

        self._ensure_model_downloaded(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        input_text = f"summarize: {text.strip()}"
        inputs = tokenizer(input_text, return_tensors="pt", max_length=2048, truncation=True)
        summary_ids = model.generate(**inputs, max_length=256, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary

    def translate(self, text: str, src_lang: str, tgt_lang: str, model_name: str = None) -> str:
        summary_cfg = self.config.summary
        if getattr(summary_cfg, "type", None) == "openai":
            import requests
            headers = {"Authorization": f"Bearer {summary_cfg.api_key}", "Content-Type": "application/json"}
            model_name = getattr(summary_cfg, "model", "gpt-3.5-turbo")
            payload = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that translates text."},
                    {"role": "user", "content": f"Translate the following text from {src_lang} to {tgt_lang}: {text.strip()}"}
                ],
                "temperature": 0.2
            }
            response = requests.post(f"{summary_cfg.server_url}/chat/completions", json=payload, headers=headers)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        # Default: HuggingFace Transformers
        if model_name is None:
            console.print("[yellow]No translation model specified. Using default model: t5-base[/yellow]")
            model_name = "t5-base"
        self._ensure_model_downloaded(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        if "mt5" in model_name.lower():
            translate_input = f"{text.strip()}"
            forced_bos_token_id = None
            if hasattr(tokenizer, "lang_code_to_id") and tgt_lang in tokenizer.lang_code_to_id:
                forced_bos_token_id = tokenizer.lang_code_to_id[tgt_lang]
            inputs = tokenizer(translate_input, return_tensors="pt", max_length=512, truncation=True)
            gen_kwargs = {"max_length": 256, "num_beams": 4, "early_stopping": True}
            if forced_bos_token_id is not None:
                gen_kwargs["forced_bos_token_id"] = forced_bos_token_id
            translated_ids = model.generate(**inputs, **gen_kwargs)
            translated = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
            import re
            translated = re.sub(r"<extra_id_\\d+>", "", translated).strip()
        elif "nllb" in model_name.lower():
            tokenizer.src_lang = src_lang
            translate_input = text.strip()
            forced_bos_token_id = None
            if hasattr(tokenizer, "lang_code_to_id") and tgt_lang in tokenizer.lang_code_to_id:
                forced_bos_token_id = tokenizer.lang_code_to_id[tgt_lang]
            inputs = tokenizer(translate_input, return_tensors="pt", max_length=512, truncation=True)
            gen_kwargs = {"max_length": 256, "num_beams": 4, "early_stopping": True}
            if forced_bos_token_id is not None:
                gen_kwargs["forced_bos_token_id"] = forced_bos_token_id
            translated_ids = model.generate(**inputs, **gen_kwargs)
            translated = tokenizer.batch_decode(translated_ids, skip_special_tokens=True)[0]
        else:
            translate_input = f"translate {src_lang} to {tgt_lang}: {text.strip()}"
            inputs = tokenizer(translate_input, return_tensors="pt", max_length=512, truncation=True)
            translated_ids = model.generate(**inputs, max_length=256, num_beams=4, early_stopping=True)
            translated = tokenizer.decode(translated_ids[0], skip_special_tokens=True)
        return translated

    def transcribe_audio(self, audio_path: str) -> tuple[str, str]:
        if self.config.transcription.method == "whisper-cpp":
            return self._transcribe_whisper_cpp(audio_path)
        elif self.config.transcription.method == "whisper-python":
            return self._transcribe_whisper_python(audio_path)
        elif self.config.transcription.method == "faster-whisper":
            return self._transcribe_faster_whisper(audio_path)
            
    def _subprocess_stream(self, command):
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in process.stdout:
            print(line, end="")
        process.wait()
        
    def _transcribe_whisper_cpp(self, audio_path: str) -> tuple[str, str]:
        # call whisper-cpp CLI locally to transcribe audio file into text
        
        # convert given audio file to wave format 16kHz using ffmpeg. Do this using local ffmpeg executable
        # and use the same ffmpeg executable that is used by yt-dlp

        # Track if we created a new wave file that might need cleanup
        created_wave_file = False
        wave_file_path = None

        # if audio_path is not a wave file, convert it to wave file
        if audio_path.endswith(".wav"):
            wave_file_path = audio_path
        else:
            console.print(f"ytbrf Converting {audio_path} to wave file")
            
            # detect if ffmpeg is installed and if not, raise an error
            if shutil.which("ffmpeg") is None:
                raise ValueError("ffmpeg not found. Please install ffmpeg or provide the path to ffmpeg in the config file.")

            # Construct the output wave file path
            wave_file_path = audio_path.rsplit('.', 1)[0] + ".wav"
            created_wave_file = True
            # Run the ffmpeg command
            command = ['ffmpeg', '-i', audio_path, '-ar', '16000', wave_file_path]
            # run the command and stream the stdout and stderr to the console
            console.print(f"Converting {audio_path} to {wave_file_path} with ffmpeg")
            result = subprocess.run(command, check=True, capture_output=False, text=True)
            if result.returncode != 0:
                console.print(f"Error converting file {audio_path} to wave")
                os.exit(1)
            audio_path = wave_file_path
        
        # Construct the output wave file path
        output_file_path_wo_ext = audio_path.rsplit('.', 1)[0]
        txt_file_path = output_file_path_wo_ext + ".txt"

        # check if txt_file_path exists and if it does, delete it
        if os.path.exists(output_file_path_wo_ext):
            os.remove(output_file_path_wo_ext)

        # Run the whisper-cpp command
        model_path = self.config.transcription.models_dir + "/ggml-" + self.config.transcription.model + ".bin"
        source_lang = self.config.transcription.force_language
        if source_lang is None:
            source_lang = "auto"
        command = ["whisper-cpp", '-f', wave_file_path, '-otxt', '-m', model_path, '-l', source_lang, '-of', output_file_path_wo_ext]
        # Add -nt flag (no timestamps) if timestamp is False
        if not self.config.transcription.timestamp:
            command.append('-nt')
        result = subprocess.run(command, check=True, capture_output=False, text=True)
        # Read the transcript from the output file
        with open(txt_file_path, 'r') as f:
            transcript = f.read()

        # Delete the txt file
        os.remove(txt_file_path)

        # Note: We don't delete the wave file here anymore, it will be handled by the process_video method
        # to ensure it's only deleted after the entire process completes successfully
        
        # Return the transcript, the language detected from whisper-cpp, and the wave file path if we created one
        return transcript, "auto"
        
    def _transcribe_faster_whisper(self, audio_path: str) -> tuple[str, str]:
        import faster_whisper
        model = faster_whisper.WhisperModel(self.config.transcription.model, device=self.device, compute_type="float16")
        segments, info = model.transcribe(audio_path)
        
        transcript = ""
        for segment in segments:
            transcript += segment.text + " "

        detected_lang = info.language
        
        # Note: We don't delete any intermediate files here
        # Cleanup will be handled by the process_video method after successful completion
        
        return transcript, detected_lang        

    def _transcribe_whisper_python(self, audio_path: str) -> tuple[str, str]:     
        console.print(f"[green]Loading Whisper model: {self.config.transcription.model}[/green]")
        model = whisper.load_model(self.config.transcription.model)
        console.print(f"[green]Transcribing audio file: {audio_path}[/green]")
        result = model.transcribe(audio_path)
        transcript = result["text"]
        detected_lang = result["language"]
    
        console.print(f"[green]Transcription complete. Detected language: {detected_lang}[/green]")
    
        # Derive video title from audio file name
        video_title = os.path.splitext(os.path.basename(audio_path))[0]
    
        # Ensure output directory exists
        output_dir = os.path.expanduser(self.config.output.directory)
        os.makedirs(output_dir, exist_ok=True)
        
        # Save transcript to a file in the output directory
        output_filename = f"{video_title}-{detected_lang}.txt"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(transcript)
        
        # Note: We don't delete any intermediate files here
        # Cleanup will be handled by the process_video method after successful completion
    
        return transcript, detected_lang

    def process_video(self, url: str) -> Dict[str, Any]:
        """Process video to get transcript and metadata."""
        metadata = self.get_video_metadata(url)
        transcript = metadata.get('has_transcript')
        intermediate_files = []

        try:
            if not transcript:
                # Use video title as base filename to avoid conflicts when multiple commands run simultaneously
                import re
                import random
                import string
                # Generate random fallback if video title is unavailable
                random_fallback = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                video_title = metadata.get('title', random_fallback)
                # Sanitize filename to remove invalid characters
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', video_title)
                
                # Download audio
                audio_path, audio_format = self.download_audio(url, safe_title)
                intermediate_files.append(audio_path)
                
                # If we downloaded a non-wav file and will convert it, track both files
                if audio_format != "wav":
                    wav_path = audio_path.rsplit('.', 1)[0] + ".wav"
                    if os.path.exists(wav_path):
                        intermediate_files.append(wav_path)
                
                # Transcribe audio
                transcript, language = self.transcribe_audio(audio_path)
                metadata['transcript'] = transcript
                metadata['language'] = language
                
                # Add any output text files that might have been created
                txt_path = audio_path.rsplit('.', 1)[0] + ".txt"
                if os.path.exists(txt_path):
                    intermediate_files.append(txt_path)
            
            # Process completed successfully, now clean up intermediate files if configured
            if self.config.transcription.delete_intermediate_files:
                for file_path in intermediate_files:
                    if os.path.exists(file_path):
                        try:
                            os.remove(file_path)
                            console.print(f"[green]Removed intermediate file: {file_path}[/green]")
                        except Exception as e:
                            console.print(f"[yellow]Warning: Could not remove file {file_path}: {str(e)}[/yellow]")
            
            return metadata
        except Exception as e:
            # If any error occurs, we don't delete the intermediate files
            # so they can be used for debugging or resuming the process
            console.print(f"[red]Error during video processing: {str(e)}[/red]")
            console.print(f"[yellow]Intermediate files were preserved for debugging: {', '.join(intermediate_files)}[/yellow]")
            raise

    def get_transcript_or_audio(self, url: str) -> Optional[str]:
        """Download subtitles with the smallest audio file using yt-dlp."""
        try:
            with yt_dlp.YoutubeDL({'writesubtitles': True, 'writeautomaticsub': True, 'format': 'worstaudio'}) as ydl:
                ydl.download([url])
                return 'Subtitles and audio downloaded'
        except Exception as e:
            console.print(f"[red]Error downloading subtitles and audio: {str(e)}[/red]")
            return None
