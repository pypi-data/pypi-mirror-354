"""Configuration management for Audio Scribe."""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import torch


@dataclass
class TranscriptionConfig:
    """Configuration settings for the transcription pipeline."""

    output_directory: Path
    whisper_model: str = "base.en"
    diarization_model: str = "pyannote/speaker-diarization-3.1"
    temp_directory: Optional[Path] = None
    device: Optional[str] = None

    def __post_init__(self):
        # Use CUDA if available, else fall back to CPU
        self.device = self.device or ("cuda" if torch.cuda.is_available() else "cpu")
        # Default temp directory inside the output directory
        self.temp_directory = self.temp_directory or (self.output_directory / "temp")
        # Ensure directories exist
        self.temp_directory.mkdir(parents=True, exist_ok=True)
        self.output_directory.mkdir(parents=True, exist_ok=True)
