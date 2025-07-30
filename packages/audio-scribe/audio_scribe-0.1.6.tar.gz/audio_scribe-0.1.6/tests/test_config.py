"""Tests for configuration management."""

from src.audio_scribe.config import TranscriptionConfig


def test_transcription_config_defaults(tmp_dir):
    """Test default configuration initialization."""
    cfg = TranscriptionConfig(output_directory=tmp_dir)

    assert cfg.output_directory == tmp_dir
    assert cfg.whisper_model == "base.en"
    assert cfg.diarization_model == "pyannote/speaker-diarization-3.1"
    # Device is either 'cuda' or 'cpu'
    assert cfg.device in ("cuda", "cpu")
    assert cfg.temp_directory.exists()
    assert cfg.temp_directory == tmp_dir / "temp"


def test_transcription_config_custom(tmp_dir):
    """Test custom configuration initialization."""
    custom_temp = tmp_dir / "custom_temp"
    cfg = TranscriptionConfig(
        output_directory=tmp_dir,
        whisper_model="medium",
        diarization_model="pyannote/test-model",
        temp_directory=custom_temp,
        device="cpu",
    )

    assert cfg.whisper_model == "medium"
    assert cfg.diarization_model == "pyannote/test-model"
    assert cfg.device == "cpu"
    assert cfg.temp_directory == custom_temp
    assert cfg.temp_directory.exists()


def test_directory_creation(tmp_dir):
    """Test that directories are created if they don't exist."""
    deep_output = tmp_dir / "deep" / "nested" / "output"
    deep_temp = tmp_dir / "deep" / "nested" / "temp"

    TranscriptionConfig(output_directory=deep_output, temp_directory=deep_temp)

    assert deep_output.exists()
    assert deep_temp.exists()
