# ytbrf package initialization

import os
import sys
import argparse
import re
from ytbrf.config import ConfigManager
from ytbrf.youtube import YouTubeProcessor
from rich.console import Console
from rich.progress import Progress
import yaml

__version__ = '0.1.0'

def ensure_output_dir(processor):
    """Ensure the output directory exists and return its path."""
    output_dir = os.path.expanduser(processor.config.output.directory)
    os.makedirs(output_dir, exist_ok=True)
    return output_dir


def get_output_path(processor, filename=None, user_output=None):
    """Get the output file path based on user output or generated filename.
    
    Args:
        processor: The YouTubeProcessor instance
        filename: The generated filename if user_output is not provided
        user_output: The user-specified output path
        
    Returns:
        The full output path
    """
    output_dir = ensure_output_dir(processor)
    
    if user_output:
        return user_output
    else:
        return os.path.join(output_dir, filename)


def is_url(input_string):
    """Determine if the input string is a URL or a file path.
    
    Args:
        input_string: The string to check
        
    Returns:
        True if the input is a URL, False if it's likely a file path
    """
    # Simple regex pattern to match URLs
    url_pattern = re.compile(
        r'^(?:http|https)://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?: [A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S*)?'
        r'(?:#\S*)?$', re.IGNORECASE)
    
    # Check if it's a URL
    if url_pattern.match(input_string):
        return True
    
    # Check if it's a YouTube URL (special case for youtu.be short links)
    # Make the check case-insensitive and handle URLs without protocol
    input_lower = input_string.lower()
    if ('youtu.be/' in input_lower or 'youtube.com/' in input_lower or 
        input_lower.startswith('youtu.be') or input_lower.startswith('youtube.com')):
        return True
    
    # Otherwise, assume it's a file path
    return False


def extract_youtube_video_id(url):
    """Extract YouTube video ID from URL.
    
    Args:
        url: YouTube URL
        
    Returns:
        Video ID string if found, None otherwise
    """
    # Pattern to match YouTube video IDs
    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',  # Standard youtube.com URLs
        r'youtu\.be/([0-9A-Za-z_-]{11})',  # Short youtu.be URLs
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None


def process_input_source(processor, input_source, console, output_path=None, temp_output_file_wo_ext=None):
    """Unified function to process both YouTube URLs and local media files."""
    if is_url(input_source):
        print(f"[INFO] Getting transcript for YouTube URL: {input_source}...")
        metadata = processor.get_video_metadata(input_source)
        
        # Use video title as temp filename if not provided to avoid conflicts
        if temp_output_file_wo_ext is None:
            import re
            import random
            import string
            # Generate random fallback if video title is unavailable
            random_fallback = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
            video_title = metadata.get('title', random_fallback)
            # Sanitize video title for safe filename usage by replacing forbidden characters with underscores
            temp_output_file_wo_ext = re.sub(r'[<>:"/\\|?*]', '_', video_title)
        
        if metadata.get('has_transcript'):
            # Get transcript directly from YouTube
            transcript = processor.get_transcript(metadata['id'])
            language = metadata.get('language', 'en')
            print("[INFO] Successfully retrieved transcript from YouTube.")
        else:
            # Download and transcribe if no transcript is available
            print("[INFO] No transcript available on YouTube. Downloading audio and transcribing...")
            audio_path, _ = processor.download_audio(input_source, temp_output_file_wo_ext)
            print(f"[INFO] Audio downloaded to: {audio_path}")
            transcript, language = processor.transcribe_audio(audio_path)
            print("[INFO] Transcription complete.")
            
            # Clean up temporary files
            cleanup_temp_files(temp_output_file_wo_ext, console)
        
        # Create output filename and metadata
        filename = f"{metadata['title']}-{language}.txt"
        metadata_title = metadata['title']
    else:
        # Process local media file
        print(f"[INFO] Processing local media file: {input_source}...")
        transcript, language = processor.transcribe_audio(input_source)
        print("[INFO] Transcription complete.")
        
        # Create output filename and metadata
        metadata_title = os.path.splitext(os.path.basename(input_source))[0]
        filename = f"{metadata_title}-{language}.txt"
    
    # Use provided output path or generate one
    if output_path is None:
        output_path = get_output_path(processor, filename)
    
    # Save transcript to file
    with open(output_path, "w") as f:
        f.write(transcript)
    
    print(f"[INFO] Transcript saved to {output_path}")
    return transcript, language, metadata_title


def transcribe_media_file(processor, media_path, console):
    """Process audio or video file and return transcript."""
    return process_input_source(processor, media_path, console)


def transcribe_from_youtube_url(processor, url, temp_output_file_wo_ext, console):
    """Process a YouTube URL for transcription."""
    print(f"[INFO] Processing YouTube URL: {url}")
    print("[INFO] Starting video processing...")
    return process_input_source(processor, url, console, temp_output_file_wo_ext=temp_output_file_wo_ext)





def cleanup_temp_files(temp_output_file_wo_ext, console):
    """Remove temporary audio files."""
    for fmt in ['mp3', 'wav']:
        tmp_file_path = f"{temp_output_file_wo_ext}.{fmt}"
        if os.path.exists(tmp_file_path):
            console.print(f"Removing temp file {tmp_file_path}")
            os.remove(tmp_file_path)


def summarize_text(processor, transcript, language, metadata_title):
    """Summarize the transcript using the processor's summarize method."""
    print("[INFO] Summarizing transcript...")
    summary = processor.summarize(transcript)
    summary_filename = f"{metadata_title}-{language}-summary.txt"
    summary_file_path = get_output_path(processor, summary_filename)
    with open(summary_file_path, "w") as f:
        f.write(summary)
    print(f"[INFO] Summarization complete. Summary saved to {summary_file_path}")
    return summary


def translate_text(processor, text, src_language, tgt_language, output_filename):
    """Translate the text using the processor's translate method."""
    if tgt_language != src_language and tgt_language != "auto":
        print(f"[INFO] Translating text from {src_language} to {tgt_language}...")
        translated_text = processor.translate(text, src_lang=src_language, tgt_lang=tgt_language)
        translated_file_path = get_output_path(processor, output_filename)
        with open(translated_file_path, "w") as f:
            f.write(translated_text)
        print(f"[INFO] Translation complete. Translated text saved to {translated_file_path}")
        return translated_text
    else:
        print("[INFO] No translation needed (target language is the same as source or set to 'auto').")
        return None





def cmd_all(args, processor, config, console):
    """Run the complete process (default)."""
    # Generate a random 6-character string to avoid conflicts
    import random
    import string
    
    # Get the input source (either URL or media file)
    input_source = args.input
    
    if not input_source:
        print("Usage: ytbrf all <YouTube URL or media file path>")
        sys.exit(1)
    
    # Determine temp_output_file_wo_ext based on input type
    if is_url(input_source):
        # Try to extract YouTube video ID
        video_id = extract_youtube_video_id(input_source)
        if video_id:
            temp_output_file_wo_ext = video_id
        else:
            # Fallback to random string if video ID extraction fails
            temp_output_file_wo_ext = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    else:
        # For local files, use the base filename without extension
        import os
        temp_output_file_wo_ext = os.path.splitext(os.path.basename(input_source))[0]
    
    # Automatically detect if the input is a URL or a file path
    if is_url(input_source):
        transcript, language, metadata_title = transcribe_from_youtube_url(processor, input_source, temp_output_file_wo_ext, console)
    else:
        # Assume it's a file path
        transcript, language, metadata_title = transcribe_media_file(processor, input_source, console)
    
    # Generate summary in source language
    summary = summarize_text(processor, transcript, language, metadata_title)
    
    # Check if source language differs from target language
    target_language = config.summary.target_language
    if target_language != language and target_language != "auto":
        print(f"[INFO] Source language ({language}) differs from target language ({target_language}). Generating additional files...")
        
        # Translate transcript using existing function
        translated_transcript_filename = f"{metadata_title}-{target_language}.txt"
        translated_transcript = translate_text(processor, transcript, language, target_language, translated_transcript_filename)
        
        # Translate summary to target language
        summary_target_filename = f"{metadata_title}-{target_language}-summary.txt"
        translate_text(processor, summary, language, target_language, summary_target_filename)
    else:
        # Save existing summary to file when languages are the same
        summary_filename = f"{metadata_title}-summary.txt"
        summary_path = get_output_path(processor, summary_filename)
        with open(summary_path, "w") as f:
            f.write(summary)
        print(f"[INFO] Summary saved to {summary_path}")


def cmd_audio(args, processor, console):
    """Download audio only from YouTube URL."""
    url = args.url
    
    # Create output filename and get output path
    if args.output:
        output_path = args.output
    else:
        # Use video ID or title as filename
        metadata = processor.get_video_metadata(url)
        filename = f"{metadata['title']}.mp3"
        output_path = get_output_path(processor, filename)
    
    print(f"[INFO] Downloading audio from {url}...")
    audio_path, _ = processor.download_audio(url, output_path)
    print(f"[INFO] Audio downloaded to {audio_path}")


def cmd_transcribe(args, processor, console):
    """Transcribe from audio or video file and output text file."""
    media_path = args.media_path
    
    # Create output filename and get output path
    filename = f"{os.path.splitext(os.path.basename(media_path))[0]}-transcript.txt"
    output_path = get_output_path(processor, filename, args.output)
    
    print(f"[INFO] Transcribing audio/video file {media_path}...")
    transcript, language = processor.transcribe_audio(media_path)
    with open(output_path, "w") as f:
        f.write(transcript)
    print(f"[INFO] Transcription complete. Transcript saved to {output_path}")


def cmd_translate(args, processor, console):
    """Translate a text file from one language to another."""
    input_file = args.input_file
    src_lang = args.src_lang
    tgt_lang = args.tgt_lang
    
    # Create output filename and get output path
    filename = f"{os.path.splitext(os.path.basename(input_file))[0]}-translated-{tgt_lang}.txt"
    output_path = get_output_path(processor, filename, args.output)
    
    print(f"[INFO] Translating {input_file} from {src_lang} to {tgt_lang}...")
    with open(input_file, "r") as f:
        text = f.read()
    translated_text = processor.translate(text, src_lang=src_lang, tgt_lang=tgt_lang)
    with open(output_path, "w") as f:
        f.write(translated_text)
    print(f"[INFO] Translation complete. Translated text saved to {output_path}")


def cmd_summarize(args, processor, console):
    """Summarize given text in its original language."""
    input_file = args.input_file
    
    # Create output filename and get output path
    filename = f"{os.path.splitext(os.path.basename(input_file))[0]}-summary.txt"
    output_path = get_output_path(processor, filename, args.output)
    
    print(f"[INFO] Summarizing {input_file}...")
    with open(input_file, "r") as f:
        text = f.read()
    
    # Use processor.summarize directly since ratio is now embedded in the prompt
    summary = processor.summarize(text)
    with open(output_path, "w") as f:
        f.write(summary)
    print(f"[INFO] Summarization complete. Summary saved to {output_path}")


def cmd_transcript(args, processor, config, console):
    """Get transcript directly from YouTube or local media file."""
    input_source = args.input
    
    # Generate output path if specified
    output_path = None
    if args.output:
        if is_url(input_source):
            metadata = processor.get_video_metadata(input_source)
            language = metadata.get('language', 'en')
            filename = f"{metadata['title']}-{language}.txt"
        else:
            # For local files, we need to transcribe first to get language
            # So we'll let process_input_source handle the output path
            pass
        if args.output and is_url(input_source):
            output_path = get_output_path(processor, filename, args.output)
    
    # Get transcript and metadata
    transcript, language, metadata_title = process_input_source(processor, input_source, console, output_path)
    
    # Check if source language differs from target language
    target_language = config.summary.target_language
    if target_language != language and target_language != "auto":
        print(f"[INFO] Source language ({language}) differs from target language ({target_language}). Generating translated transcript...")
        
        # Translate transcript using existing function
        translated_transcript_filename = f"{metadata_title}-{target_language}.txt"
        translate_text(processor, transcript, language, target_language, translated_transcript_filename)
    
    return transcript, language, metadata_title


def ensure_config_exists(config_path=None, console=None):
    """Ensure the configuration file exists, creating it with defaults if necessary.
    
    Args:
        config_path: Optional path to config file. If None, uses ConfigManager's default path.
        console: Optional console for rich output. If None, uses print.
        
    Returns:
        str: The path to the config file
    """
    if config_path is None:
        config_manager = ConfigManager()
        config_path = config_manager.config_path
    
    if not os.path.exists(config_path):
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        config_manager = ConfigManager()
        default_config = config_manager._get_default_config()
        with open(config_path, "w") as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        message = f"Default config created at {config_path}. Please review and update it as needed."
        if console:
            console.print(f"[yellow]{message}[/yellow]")
        else:
            print(f"[INFO] {message}")
    
    return config_path


def cmd_config(args, processor, config, console):
    """Open the configuration file in an editor."""
    import subprocess
    import shutil
    
    # Ensure config exists and get its path
    config_path = ensure_config_exists()
    
    # Try different editors in order of preference
    editors = ["vim", "vi", "code"]
    editor_found = False
    
    for editor in editors:
        if shutil.which(editor):
            try:
                subprocess.run([editor, config_path], check=True)
                print(f"[INFO] Configuration file edited with {editor}: {config_path}")
                editor_found = True
                break
            except subprocess.CalledProcessError:
                print(f"[WARNING] Failed to open {editor}. Trying next editor...")
                continue
    
    # Fallback to system default editor (open command on macOS)
    if not editor_found:
        try:
            subprocess.run(["open", config_path], check=True)
            print(f"[INFO] Configuration file opened with system default editor: {config_path}")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"[ERROR] No suitable editor found. Please edit the config file manually at: {config_path}")


def main():
    console = Console()

    # Ensure config exists using utility function
    ensure_config_exists(console=console)

    # Check if the last argument is 'help' to handle cases like 'ytbrf transcribe help'
    if len(sys.argv) > 2 and sys.argv[-1] == 'help':
        # Reconstruct the arguments to use --help instead
        sys.argv[-1] = '--help'

    # Check if no arguments were provided - let it fall through to default 'all' behavior
    # (Removed automatic --help to allow default subcommand handling)

    parser = argparse.ArgumentParser(
        prog="ytbrf",  # Set the program name explicitly
        description="YouTube Brief: Summarize and translate YouTube videos or audio files."
    )
    subparsers = parser.add_subparsers(dest="command", required=False)

    # all: run the complete process
    parser_all = subparsers.add_parser("all", help="Run the complete process (default)")
    parser_all.add_argument("input", nargs="?", help="YouTube URL or path to local audio/video file")

    # audio: download audio only
    parser_audio = subparsers.add_parser("audio", help="Download audio only from YouTube URL")
    parser_audio.add_argument("url", help="YouTube URL")
    parser_audio.add_argument("-o", "--output", help="Output audio file path", default="output.mp3")

    # transcribe: transcribe from audio or video file path
    parser_transcribe = subparsers.add_parser("transcribe", help="Transcribe from audio or video file and output text file")
    parser_transcribe.add_argument("media_path", help="Path to audio or video file")
    parser_transcribe.add_argument("-o", "--output", help="Output transcript file path")

    # translate: translate a text file
    parser_translate = subparsers.add_parser("translate", help="Translate a text file from one language to another")
    parser_translate.add_argument("input_file", help="Input text file path")
    parser_translate.add_argument("-s", "--src-lang", help="Source language", default="auto")
    parser_translate.add_argument("-t", "--tgt-lang", help="Target language", required=True)
    parser_translate.add_argument("-o", "--output", help="Output translated file path")

    # summarize: summarize given text
    parser_summarize = subparsers.add_parser("summarize", help="Summarize given text in its original language")
    parser_summarize.add_argument("input_file", help="Input text file path")

    parser_summarize.add_argument("-o", "--output", help="Output summary file path")

    # transcript: get transcript directly from YouTube or local media file
    parser_transcript = subparsers.add_parser("transcript", help="Get transcript directly from YouTube or local media file")
    parser_transcript.add_argument("input", help="YouTube URL or path to local audio/video file")
    parser_transcript.add_argument("-o", "--output", help="Output transcript file path")

    # config: open configuration file in editor
    parser_config = subparsers.add_parser("config", help="Open configuration file in editor")

    # help: display help for a specific command
    parser_help = subparsers.add_parser("help", help="Display help information for commands")
    parser_help.add_argument("help_command", nargs="?", help="Command to get help for")

    # Parse arguments with fallback for invalid subcommands
    valid_commands = {'all', 'audio', 'transcribe', 'translate', 'summarize', 'transcript', 'config', 'help'}
    
    # Check if first argument is not a valid subcommand and handle accordingly
    if len(sys.argv) > 1 and sys.argv[1] not in valid_commands and not sys.argv[1].startswith('-'):
        console.print("[yellow]No subcommand specified. Assuming 'all' subcommand.[/yellow]")
        # Insert 'all' as the subcommand
        sys.argv.insert(1, 'all')
    
    args = parser.parse_args()
    
    # Handle case where no subcommand is provided - default to 'all'
    if args.command is None:
        console.print("[yellow]No subcommand specified. Assuming 'all' subcommand.[/yellow]")
        # Set default values for 'all' command
        args.command = "all"
        args.input = None
    
    # Handle help command
    if args.command == "help":
        if args.help_command:
            # Show help for specific command
            parser.parse_args([args.help_command, "--help"])
        else:
            # Show general help
            parser.parse_args(["--help"])
        return  # Exit after showing help
    
    config_manager = ConfigManager()
    config = config_manager._load_config()
    processor = YouTubeProcessor(config)

    # Command dispatcher
    command_handlers = {
        "all": cmd_all,
        "audio": cmd_audio,
        "transcribe": cmd_transcribe,
        "translate": cmd_translate,
        "summarize": cmd_summarize,
        "transcript": cmd_transcript,
        "config": cmd_config
    }
    
    # Execute the selected command
    command_handlers[args.command](args, processor, config, console)
    
