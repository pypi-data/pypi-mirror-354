"""
Audio Scribe - Professional Audio Transcription Tool

Main entry point for the Audio Scribe transcription system.
Provides a comprehensive CLI interface for audio transcription using
Whisper speech recognition and Pyannote speaker diarization.

Author: Gurasis Osahan
Organization: GenomicOps
License: Apache-2.0
"""

import sys
import logging
import warnings
import argparse
import readline
from pathlib import Path
from datetime import datetime

from audio_scribe.config import TranscriptionConfig
from audio_scribe.models import TranscriptionPipeline
from audio_scribe.auth import TokenManager, get_token
from audio_scribe.utils import DependencyManager, complete_path

# Import version information
try:
    from audio_scribe import __version__
except ImportError:
    __version__ = "unknown"

# Configure professional logging
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    datefmt=LOG_DATE_FORMAT,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("audio_scribe.log", mode="a", encoding="utf-8"),
    ],
)

logger = logging.getLogger(__name__)


def setup_argument_parser():
    """
    Configure and return the command-line argument parser.

    Returns:
        argparse.ArgumentParser: Configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog="audio-scribe",
        description=(
            "Audio Scribe - Professional audio transcription tool utilizing "
            "OpenAI Whisper for speech recognition and Pyannote for speaker diarization. "
            "Processes audio files to generate accurate, timestamped transcripts with "
            "speaker identification."
        ),
        epilog=(
            "For more information and documentation, visit: "
            "https://gitlab.genomicops.cloud/innovation-hub/audio-scribe"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Version information
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="Display version information and exit",
    )

    # Core functionality arguments
    parser.add_argument(
        "--audio",
        type=Path,
        metavar="PATH",
        help=(
            "Path to the input audio file for transcription. "
            "Supports common audio formats (WAV, MP3, MP4, FLAC, etc.). "
            "If not provided, you will be prompted to enter the path interactively."
        ),
    )

    parser.add_argument(
        "--output",
        type=Path,
        metavar="DIRECTORY",
        help=(
            "Output directory for transcription results and temporary files. "
            "Creates timestamped subdirectories to organize outputs. "
            "Default: ./transcripts/YYYYMMDD/"
        ),
    )

    # Authentication and configuration
    parser.add_argument(
        "--token",
        metavar="TOKEN",
        help=(
            "HuggingFace API token for accessing Pyannote models. "
            "Required for speaker diarization functionality. "
            "Overrides any previously saved token. "
            "Obtain from: https://huggingface.co/settings/tokens"
        ),
    )

    parser.add_argument(
        "--delete-token",
        action="store_true",
        help=(
            "Remove any stored HuggingFace token from the system keyring and exit. "
            "Useful for switching between different HuggingFace accounts or "
            "clearing credentials for security purposes."
        ),
    )

    # Model and processing options
    parser.add_argument(
        "--whisper-model",
        default="base.en",
        choices=[
            "tiny",
            "tiny.en",
            "base",
            "base.en",
            "small",
            "small.en",
            "medium",
            "medium.en",
            "large",
            "turbo",
        ],
        metavar="MODEL",
        help=(
            "Whisper model for speech recognition (default: base.en). "
            "Larger models provide better accuracy but require more processing time and memory. "
            "English-specific models (.en) are optimized for English-only content. "
            "Available: tiny, tiny.en, base, base.en, small, small.en, medium, medium.en, large, turbo"
        ),
    )

    # Debug and development options
    parser.add_argument(
        "--show-warnings",
        action="store_true",
        help=(
            "Enable display of library warnings during processing. "
            "Warnings are suppressed by default to provide cleaner output. "
            "Enable for debugging or development purposes."
        ),
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging output for detailed processing information",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress non-essential output messages",
    )

    return parser


def configure_logging(verbose: bool, quiet: bool):
    """
    Configure logging levels based on user preferences.

    Args:
        verbose (bool): Enable verbose logging
        quiet (bool): Enable quiet mode
    """
    if quiet and verbose:
        logger.warning("Both --quiet and --verbose specified. Using verbose mode.")
        quiet = False

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled")
    elif quiet:
        logging.getLogger().setLevel(logging.WARNING)
    else:
        logging.getLogger().setLevel(logging.INFO)


def initialize_environment():
    """
    Initialize the application environment and dependencies.

    Returns:
        bool: True if initialization successful, False otherwise
    """
    logger.info("Initializing Audio Scribe environment")

    # Verify system dependencies
    if not DependencyManager.verify_dependencies():
        logger.error("Dependency verification failed")
        return False

    # Configure tab completion for file paths
    try:
        readline.set_completer_delims(" \t\n;")
        readline.set_completer(complete_path)
        readline.parse_and_bind("tab: complete")
        logger.debug("Tab completion configured successfully")
    except Exception as e:
        logger.warning(f"Failed to configure tab completion: {e}")

    return True


def get_audio_file_path(provided_path: Path | None = None) -> Path:
    """
    Get and validate the audio file path from user input or arguments.

    Args:
        provided_path (Path, optional): Path provided via command line

    Returns:
        Path: Validated audio file path
    """
    audio_path = provided_path

    while not audio_path or not audio_path.exists():
        try:
            audio_path_str = input(
                "\nEnter path to audio file (Tab for autocomplete): "
            ).strip()

            if not audio_path_str:
                logger.warning("No path provided. Please enter a valid file path.")
                continue

            audio_path = Path(audio_path_str)

            if not audio_path.exists():
                logger.error(
                    f"File '{audio_path}' not found. Please verify the path and try again."
                )

        except KeyboardInterrupt:
            logger.info("\nOperation cancelled by user")
            sys.exit(0)
        except Exception as e:
            logger.error(f"Error processing file path: {e}")

    logger.info(f"Audio file validated: {audio_path}")
    return audio_path


def main():
    """
    Main entry point for the Audio Scribe CLI application.

    Orchestrates the complete transcription workflow including:
    - Argument parsing and validation
    - Environment initialization
    - Authentication management
    - Model initialization
    - Audio file processing
    """
    # Parse command line arguments
    parser = setup_argument_parser()
    args = parser.parse_args()

    # Configure logging based on user preferences
    configure_logging(args.verbose, args.quiet)

    # Handle token deletion request
    if args.delete_token:
        token_manager = TokenManager()
        success = token_manager.delete_token()
        if success:
            logger.info("HuggingFace token successfully removed")
        else:
            logger.error("Failed to remove HuggingFace token")
        sys.exit(0 if success else 1)

    # Display startup information
    if not args.quiet:
        print(f"Audio Scribe v{__version__}")
        print("Initializing transcription environment...")
        sys.stdout.flush()

    # Configure warning display
    if not args.show_warnings:
        warnings.filterwarnings(
            "ignore", category=UserWarning, module=r"pyannote\.audio"
        )
        warnings.filterwarnings("ignore", category=FutureWarning, module="whisper")
        logger.debug("Library warnings suppressed")
    else:
        warnings.resetwarnings()
        logger.debug("Library warnings enabled")

    # Initialize environment
    if not initialize_environment():
        logger.critical("Environment initialization failed")
        sys.exit(1)

    # Configure output directory
    output_dir = args.output or (
        Path("transcripts") / datetime.now().strftime("%Y%m%d")
    )
    logger.info(f"Output directory: {output_dir}")

    # Initialize transcription configuration
    config = TranscriptionConfig(
        output_directory=output_dir, whisper_model=args.whisper_model
    )

    # Initialize transcription pipeline
    logger.info("Initializing transcription pipeline")
    pipeline = TranscriptionPipeline(config)

    # Handle authentication
    token_manager = TokenManager()
    hf_token = args.token or get_token(token_manager)

    if not hf_token:
        logger.error(
            "HuggingFace token required for speaker diarization. "
            "Provide via --token argument or interactive prompt."
        )
        sys.exit(1)

    # Initialize models
    logger.info("Loading speech recognition and diarization models")
    if not pipeline.initialize_models(hf_token):
        logger.error("Model initialization failed")
        sys.exit(1)

    # Get and validate audio file
    audio_path = get_audio_file_path(args.audio)

    # Process the audio file
    logger.info("Starting transcription process")
    if not args.quiet:
        print("Processing audio file. This may take several minutes...")
        sys.stdout.flush()

    try:
        success = pipeline.process_file(audio_path)
        if success:
            logger.info("Transcription completed successfully")
            if not args.quiet:
                print(f"Transcription completed. Results saved to: {output_dir}")
        else:
            logger.error("Transcription process failed")
            sys.exit(1)

    except KeyboardInterrupt:
        logger.info("Transcription interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unexpected error during transcription: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
