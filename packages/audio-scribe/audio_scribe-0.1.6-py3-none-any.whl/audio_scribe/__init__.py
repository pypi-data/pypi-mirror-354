"""
Audio Scribe
-----------------
A Python package for transcribing audio files with speaker diarization
using Whisper and Pyannote.
"""

from audio_scribe.transcriber import main
from audio_scribe.models import TranscriptionPipeline, AudioProcessor
from audio_scribe.config import TranscriptionConfig
from audio_scribe.auth import TokenManager
from audio_scribe.utils import DependencyManager, complete_path

__version__ = "0.1.6"

__all__ = [
    "main",
    "TranscriptionPipeline",
    "TranscriptionConfig",
    "AudioProcessor",
    "TokenManager",
    "DependencyManager",
    "complete_path",
]
