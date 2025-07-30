"""Tests for model handling and audio processing."""

import pytest
import threading
import warnings
from unittest.mock import patch, MagicMock, Mock
from pathlib import Path
from src.audio_scribe.models import (
    AudioProcessor,
    TranscriptionPipeline,
)
from src.audio_scribe.config import TranscriptionConfig


# ----------------
# Fixtures
# ----------------
@pytest.fixture
def config(tmp_dir):
    """Create a test configuration."""
    return TranscriptionConfig(output_directory=tmp_dir)


@pytest.fixture
def processor(config):
    """Create an AudioProcessor instance."""
    return AudioProcessor(config)


@pytest.fixture
def pipeline(config):
    """Create a TranscriptionPipeline instance."""
    return TranscriptionPipeline(config)


@pytest.fixture
def mock_wave_file():
    """Create a mock wave file for testing."""
    mock_wave = MagicMock()
    # Create a mock wave parameters object
    params = MagicMock()
    params.nchannels = 2
    params.sampwidth = 2
    params.framerate = 44100
    params.nframes = 44100 * 2  # 2 seconds of audio
    params.comptype = "NONE"
    params.compname = "not compressed"

    mock_wave.getparams.return_value = params
    mock_wave.getnframes.return_value = params.nframes
    mock_wave.readframes.return_value = b"fake_audio_data"

    # Set up frame position methods
    mock_wave.tell.return_value = 0
    mock_wave.setpos.return_value = None

    return mock_wave


# ----------------
# AudioProcessor Tests
# ----------------
def test_audio_processor_init(processor, config):
    """Test AudioProcessor initialization."""
    assert processor.config == config


def test_load_audio_segment_success(processor, tmp_dir, mock_wave_file):
    """Test successful audio segment loading."""
    input_path = Path(tmp_dir) / "input.wav"
    output_path = Path(tmp_dir) / "output.wav"

    with patch("wave.open", autospec=True) as mock_open:
        mock_output = MagicMock()
        # Configure mock to return different instances for input and output
        mock_open.return_value.__enter__.side_effect = [
            mock_wave_file,  # Input file
            mock_output,  # Output file
        ]

        result = processor.load_audio_segment(
            input_path, start_time=1.0, end_time=2.0, output_path=output_path
        )

        assert result is True

        # Verify correct method calls
        mock_wave_file.setpos.assert_called_once()
        mock_wave_file.readframes.assert_called_once()
        mock_output.setparams.assert_called_once_with(
            mock_wave_file.getparams.return_value
        )
        mock_output.writeframes.assert_called_once_with(
            mock_wave_file.readframes.return_value
        )


def test_load_audio_segment_invalid_file(processor, tmp_dir):
    """Test handling of invalid audio file."""
    input_path = Path(tmp_dir) / "nonexistent.wav"
    output_path = Path(tmp_dir) / "output.wav"

    result = processor.load_audio_segment(
        input_path, start_time=0.0, end_time=1.0, output_path=output_path
    )

    assert result is False


def test_load_audio_segment_invalid_times(processor, tmp_dir, mock_wave_file):
    """Test handling of invalid time parameters."""
    input_path = Path(tmp_dir) / "input.wav"
    output_path = Path(tmp_dir) / "output.wav"

    with patch("wave.open", autospec=True) as mock_open:
        mock_open.return_value.__enter__.return_value = mock_wave_file

        # Test end time beyond file duration
        result = processor.load_audio_segment(
            input_path,
            start_time=0.0,
            end_time=1000.0,  # Way beyond file length
            output_path=output_path,
        )

        assert result is True  # Should still work but clip to file length


# ----------------
# TranscriptionPipeline Tests
# ----------------
def test_pipeline_init(pipeline, config):
    """Test TranscriptionPipeline initialization."""
    assert pipeline.config == config
    assert pipeline.diarization_pipeline is None
    assert pipeline.whisper_model is None
    assert pipeline._running is False


@pytest.fixture
def mock_config():
    return TranscriptionConfig(
        output_directory=Path("test_output"),
        device="cpu",  # Explicitly set to CPU for testing
    )


@pytest.mark.cpu  # Mark this test as CPU-only
def test_initialize_models_success(mock_config):
    """Test successful model initialization with expected CPU warning."""
    with patch("whisper.load_model") as mock_whisper, patch(
        "pyannote.audio.Pipeline.from_pretrained"
    ) as mock_pipeline:

        # Configure mocks
        mock_whisper.return_value = Mock()
        mock_pipeline.return_value = Mock()

        pipeline = TranscriptionPipeline(mock_config)

        # Test initialization
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = pipeline.initialize_models("fake_token")

            # Optional: Verify the warning was issued
            cpu_warning_found = any(
                "Running on CPU" in str(warning.message) for warning in w
            )
            assert cpu_warning_found, "Expected CPU warning was not generated"

        # Verify the results
        assert result is True
        mock_whisper.assert_called_once()
        mock_pipeline.assert_called_once()


def test_initialize_models_failure(mock_config):
    """Test model initialization failure handling."""
    with patch("whisper.load_model", side_effect=Exception("Mock error")), patch(
        "pyannote.audio.Pipeline.from_pretrained"
    ):

        pipeline = TranscriptionPipeline(mock_config)
        result = pipeline.initialize_models("fake_token")

        assert result is False


def test_initialize_models_pyannote_failure(pipeline):
    """Test handling of Pyannote model initialization failure."""
    with patch("whisper.load_model") as mock_whisper, patch(
        "pyannote.audio.Pipeline.from_pretrained", side_effect=Exception("Auth error")
    ):

        mock_whisper.return_value = MagicMock()

        result = pipeline.initialize_models("fake_token")
        assert result is False


def test_process_file_success_with_progress(pipeline, tmp_dir):
    """Test successful file processing with progress bar."""
    # Setup test audio file
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    # Mock the diarization pipeline
    pipeline.diarization_pipeline = MagicMock()
    # Create two test segments with proper mock segment objects
    segments = [
        (MagicMock(start=0.0, end=1.0), None, "SPEAKER_1"),
        (MagicMock(start=1.0, end=2.0), None, "SPEAKER_2"),
    ]
    pipeline.diarization_pipeline.return_value.itertracks.return_value = segments

    # Mock the whisper model
    pipeline.whisper_model = MagicMock()
    pipeline.whisper_model.transcribe.return_value = {"text": "Test transcription"}

    # Mock AudioProcessor to succeed
    with patch("src.audio_scribe.models.AudioProcessor") as mock_audio_processor_class:
        # Configure the mock audio processor instance
        mock_audio_processor = MagicMock()
        mock_audio_processor.load_audio_segment.return_value = True
        mock_audio_processor_class.return_value = mock_audio_processor

        with patch("src.audio_scribe.models.HAVE_PROGRESS_SUPPORT", True), patch(
            "src.audio_scribe.models.alive_bar"
        ) as mock_bar, patch("threading.Thread") as mock_thread:

            # Configure progress bar mock
            mock_bar_instance = MagicMock()
            mock_bar.return_value.__enter__.return_value = mock_bar_instance

            # Configure thread mock
            mock_thread_instance = MagicMock()
            mock_thread.return_value = mock_thread_instance

            # Run the process
            result = pipeline.process_file(test_audio)

            # Verify results
            assert result is True
            assert pipeline.whisper_model.transcribe.call_count == 2
            assert mock_audio_processor.load_audio_segment.call_count == 2
            mock_thread.assert_called_once()
            mock_thread_instance.start.assert_called_once()
            mock_thread_instance.join.assert_called_once()

            # Verify segment processing
            for turn, _, speaker in segments:
                # Verify each segment was processed
                segment_path = (
                    tmp_dir
                    / "temp"
                    / f"segment_{speaker}_{turn.start:.2f}_{turn.end:.2f}.wav"
                )
                mock_audio_processor.load_audio_segment.assert_any_call(
                    test_audio, turn.start, turn.end, segment_path
                )


def test_process_file_no_progress_bar(pipeline, tmp_dir):
    """Test file processing without progress bar support."""
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    # Mock diarization pipeline
    pipeline.diarization_pipeline = MagicMock()
    segments = [(MagicMock(start=0.0, end=1.0), None, "SPEAKER_1")]
    pipeline.diarization_pipeline.return_value.itertracks.return_value = segments

    # Mock whisper model
    pipeline.whisper_model = MagicMock()
    pipeline.whisper_model.transcribe.return_value = {"text": "Test"}

    # Mock AudioProcessor
    with patch("src.audio_scribe.models.AudioProcessor") as mock_audio_processor_class:
        # Configure the mock audio processor instance
        mock_audio_processor = MagicMock()
        mock_audio_processor.load_audio_segment.return_value = True
        mock_audio_processor_class.return_value = mock_audio_processor

        with patch("src.audio_scribe.models.HAVE_PROGRESS_SUPPORT", False):
            result = pipeline.process_file(test_audio)

            assert result is True
            assert pipeline.whisper_model.transcribe.call_count == 1
            assert mock_audio_processor.load_audio_segment.call_count == 1

            # Verify segment processing
            turn, _, speaker = segments[0]
            segment_path = (
                tmp_dir
                / "temp"
                / f"segment_{speaker}_{turn.start:.2f}_{turn.end:.2f}.wav"
            )
            mock_audio_processor.load_audio_segment.assert_called_once_with(
                test_audio, turn.start, turn.end, segment_path
            )


def test_process_file_diarization_failure(pipeline, tmp_dir):
    """Test handling of diarization failure."""
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    pipeline.diarization_pipeline = MagicMock(
        side_effect=Exception("Diarization failed")
    )

    result = pipeline.process_file(test_audio)
    assert result is False


def test_resource_monitoring(pipeline):
    """Test resource monitoring functionality."""
    with patch("src.audio_scribe.models.psutil") as mock_psutil, patch(
        "src.audio_scribe.models.GPUtil"
    ) as mock_gputil:

        # Mock system metrics
        mock_psutil.cpu_percent.return_value = 50
        mock_psutil.virtual_memory.return_value.percent = 75

        # Mock GPU metrics
        mock_gpu = MagicMock()
        mock_gpu.memoryUsed = 2000
        mock_gpu.memoryTotal = 8000
        mock_gputil.getGPUs.return_value = [mock_gpu]

        mock_bar = MagicMock()

        # Run monitoring for one update
        def stop_after_update():
            pipeline._running = False

        threading.Timer(0.1, stop_after_update).start()
        pipeline._running = True
        pipeline._update_resources(mock_bar)

        # Verify the progress bar was updated with resource info
        mock_bar.text.assert_called_with("CPU: 50%, MEM: 75%, GPU Mem: 2000/8000 MB")


def test_resource_monitoring_no_gpu(pipeline):
    """Test resource monitoring without GPU."""
    with patch("src.audio_scribe.models.psutil") as mock_psutil, patch(
        "src.audio_scribe.models.GPUtil"
    ) as mock_gputil:

        mock_psutil.cpu_percent.return_value = 50
        mock_psutil.virtual_memory.return_value.percent = 75
        mock_gputil.getGPUs.return_value = []

        mock_bar = MagicMock()

        def stop_after_update():
            pipeline._running = False

        threading.Timer(0.1, stop_after_update).start()
        pipeline._running = True
        pipeline._update_resources(mock_bar)

        mock_bar.text.assert_called_with("CPU: 50%, MEM: 75%, GPU Mem: N/A")


def test_resource_monitoring_error(pipeline):
    """Test handling of errors in resource monitoring."""
    with patch("src.audio_scribe.models.psutil") as mock_psutil:
        mock_psutil.cpu_percent.side_effect = Exception("Resource error")

        mock_bar = MagicMock()

        def stop_after_update():
            pipeline._running = False

        threading.Timer(0.1, stop_after_update).start()
        pipeline._running = True
        pipeline._update_resources(mock_bar)

        # Monitoring should handle the error gracefully
        mock_bar.text.assert_not_called()


def test_process_file_segment_error(pipeline, tmp_dir):
    """Test handling of segment processing errors."""
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    # Mock the diarization pipeline
    pipeline.diarization_pipeline = MagicMock()
    segments = [(MagicMock(start=0.0, end=1.0), None, "SPEAKER_1")]
    pipeline.diarization_pipeline.return_value.itertracks.return_value = segments

    # Mock the whisper model to raise an exception
    pipeline.whisper_model = MagicMock()
    pipeline.whisper_model.transcribe.side_effect = Exception("Transcription error")

    with patch("src.audio_scribe.models.HAVE_PROGRESS_SUPPORT", False), patch(
        "src.audio_scribe.models.AudioProcessor"
    ) as mock_audio_processor_class:

        mock_audio_processor = MagicMock()
        mock_audio_processor.load_audio_segment.return_value = True
        mock_audio_processor_class.return_value = mock_audio_processor

        # Process should complete but log the error
        result = pipeline.process_file(test_audio)
        assert result is False


def test_process_file_with_empty_segments(pipeline, tmp_dir):
    """Test processing when diarization returns no segments."""
    test_audio = tmp_dir / "test.wav"
    test_audio.touch()

    # Mock both required components
    pipeline.diarization_pipeline = MagicMock()
    pipeline.whisper_model = MagicMock()
    pipeline.diarization_pipeline.return_value.itertracks.return_value = []

    result = pipeline.process_file(test_audio)
    assert result is True

    # Verify the whisper model was never called since there were no segments
    pipeline.whisper_model.transcribe.assert_not_called()
