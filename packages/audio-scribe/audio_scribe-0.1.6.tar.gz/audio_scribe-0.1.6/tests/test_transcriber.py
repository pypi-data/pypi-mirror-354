"""
Tests for the Audio Scribe CLI interface.

Comprehensive test suite covering all CLI functionality including
argument parsing, environment initialization, authentication,
and transcription workflow.
"""

import sys
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.audio_scribe.transcriber import (
    main,
    setup_argument_parser,
    configure_logging,
    initialize_environment,
    get_audio_file_path,
)


class TestArgumentParser:
    """Test suite for argument parsing functionality."""

    def test_setup_argument_parser_basic(self):
        """Test basic argument parser setup."""
        parser = setup_argument_parser()

        # Test default values
        args = parser.parse_args([])
        assert args.whisper_model == "base.en"
        assert args.show_warnings is False
        assert args.verbose is False
        assert args.quiet is False
        assert args.delete_token is False

    def test_setup_argument_parser_all_flags(self):
        """Test parser with all flags enabled."""
        parser = setup_argument_parser()

        args = parser.parse_args(
            [
                "--show-warnings",
                "--verbose",
                "--quiet",
                "--delete-token",
                "--whisper-model",
                "large",
                "--token",
                "test-token",
                "--audio",
                "/path/to/audio.wav",
                "--output",
                "/path/to/output",
            ]
        )

        assert args.show_warnings is True
        assert args.verbose is True
        assert args.quiet is True
        assert args.delete_token is True
        assert args.whisper_model == "large"
        assert args.token == "test-token"
        assert args.audio == Path("/path/to/audio.wav")
        assert args.output == Path("/path/to/output")

    def test_setup_argument_parser_version(self):
        """Test version argument handling."""
        parser = setup_argument_parser()

        with pytest.raises(SystemExit) as exc_info:
            parser.parse_args(["--version"])

        assert exc_info.value.code == 0

    def test_setup_argument_parser_invalid_model(self):
        """Test invalid whisper model rejection."""
        parser = setup_argument_parser()

        with pytest.raises(SystemExit):
            parser.parse_args(["--whisper-model", "invalid-model"])


class TestLoggingConfiguration:
    """Test suite for logging configuration."""

    @patch("src.audio_scribe.transcriber.logging")
    def test_configure_logging_verbose(self, mock_logging):
        """Test verbose logging configuration."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        configure_logging(verbose=True, quiet=False)

        mock_logger.setLevel.assert_called_with(mock_logging.DEBUG)

    @patch("src.audio_scribe.transcriber.logging")
    def test_configure_logging_quiet(self, mock_logging):
        """Test quiet logging configuration."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        configure_logging(verbose=False, quiet=True)

        mock_logger.setLevel.assert_called_with(mock_logging.WARNING)

    @patch("src.audio_scribe.transcriber.logging")
    def test_configure_logging_both_flags(self, mock_logging):
        """Test handling of conflicting verbose and quiet flags."""
        mock_logger = MagicMock()
        mock_logging.getLogger.return_value = mock_logger

        configure_logging(verbose=True, quiet=True)

        # Should default to verbose when both are specified
        mock_logger.setLevel.assert_called_with(mock_logging.DEBUG)


class TestEnvironmentInitialization:
    """Test suite for environment initialization."""

    @patch("src.audio_scribe.transcriber.DependencyManager")
    @patch("src.audio_scribe.transcriber.readline")
    def test_initialize_environment_success(self, mock_readline, mock_dm):
        """Test successful environment initialization."""
        mock_dm.verify_dependencies.return_value = True

        result = initialize_environment()

        assert result is True
        mock_dm.verify_dependencies.assert_called_once()
        mock_readline.set_completer_delims.assert_called_once()

    @patch("src.audio_scribe.transcriber.DependencyManager")
    def test_initialize_environment_dependency_failure(self, mock_dm):
        """Test environment initialization with dependency failure."""
        mock_dm.verify_dependencies.return_value = False

        result = initialize_environment()

        assert result is False

    @patch("src.audio_scribe.transcriber.DependencyManager")
    @patch("src.audio_scribe.transcriber.readline")
    def test_initialize_environment_readline_failure(self, mock_readline, mock_dm):
        """Test environment initialization with readline configuration failure."""
        mock_dm.verify_dependencies.return_value = True
        mock_readline.set_completer_delims.side_effect = Exception("Readline error")

        # Should still return True even if readline setup fails
        result = initialize_environment()

        assert result is True


class TestAudioFileInput:
    """Test suite for audio file path handling."""

    def test_get_audio_file_path_valid_provided(self, tmp_path):
        """Test getting audio file path when valid path is provided."""
        test_file = tmp_path / "test.wav"
        test_file.touch()

        result = get_audio_file_path(test_file)

        assert result == test_file

    @patch("builtins.input")
    def test_get_audio_file_path_interactive_success(self, mock_input, tmp_path):
        """Test interactive audio file path input."""
        test_file = tmp_path / "test.wav"
        test_file.touch()

        mock_input.return_value = str(test_file)

        result = get_audio_file_path()

        assert result == test_file
        mock_input.assert_called_once()

    @patch("builtins.input")
    def test_get_audio_file_path_interactive_retry(self, mock_input, tmp_path):
        """Test interactive input with initial invalid path."""
        test_file = tmp_path / "test.wav"
        test_file.touch()

        # First call returns invalid path, second returns valid path
        mock_input.side_effect = ["/invalid/path.wav", str(test_file)]

        result = get_audio_file_path()

        assert result == test_file
        assert mock_input.call_count == 2

    @patch("builtins.input")
    def test_get_audio_file_path_keyboard_interrupt(self, mock_input):
        """Test handling of keyboard interrupt during interactive input."""
        mock_input.side_effect = KeyboardInterrupt()

        with pytest.raises(SystemExit) as exc_info:
            get_audio_file_path()

        assert exc_info.value.code == 0


class TestMainFunction:
    """Test suite for main function integration."""

    def test_main_delete_token_success(self, monkeypatch):
        """Test successful token deletion."""
        with patch("src.audio_scribe.transcriber.TokenManager") as mock_tm:
            mock_tm_instance = MagicMock()
            mock_tm.return_value = mock_tm_instance
            mock_tm_instance.delete_token.return_value = True

            monkeypatch.setattr(sys, "argv", ["audio-scribe", "--delete-token"])

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 0
            mock_tm_instance.delete_token.assert_called_once()

    def test_main_delete_token_failure(self, monkeypatch):
        """Test failed token deletion."""
        with patch("src.audio_scribe.transcriber.TokenManager") as mock_tm:
            mock_tm_instance = MagicMock()
            mock_tm.return_value = mock_tm_instance
            mock_tm_instance.delete_token.return_value = False

            monkeypatch.setattr(sys, "argv", ["audio-scribe", "--delete-token"])

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    @patch("src.audio_scribe.transcriber.initialize_environment")
    def test_main_environment_init_failure(self, mock_init_env, monkeypatch):
        """Test early exit on environment initialization failure."""
        mock_init_env.return_value = False

        monkeypatch.setattr(sys, "argv", ["audio-scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("src.audio_scribe.transcriber.initialize_environment")
    @patch("src.audio_scribe.transcriber.get_token")
    def test_main_no_token(self, mock_get_token, mock_init_env, monkeypatch):
        """Test early exit when no HuggingFace token is available."""
        mock_init_env.return_value = True
        mock_get_token.return_value = None

        monkeypatch.setattr(sys, "argv", ["audio-scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("src.audio_scribe.transcriber.initialize_environment")
    @patch("src.audio_scribe.transcriber.get_token")
    @patch("src.audio_scribe.transcriber.TranscriptionPipeline")
    def test_main_model_init_failure(
        self, mock_pipeline, mock_get_token, mock_init_env, monkeypatch
    ):
        """Test early exit on model initialization failure."""
        mock_init_env.return_value = True
        mock_get_token.return_value = "test-token"

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = False
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(sys, "argv", ["audio-scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1
        pipeline_instance.initialize_models.assert_called_once_with("test-token")

    @patch("src.audio_scribe.transcriber.initialize_environment")
    @patch("src.audio_scribe.transcriber.get_token")
    @patch("src.audio_scribe.transcriber.TranscriptionPipeline")
    @patch("src.audio_scribe.transcriber.get_audio_file_path")
    def test_main_successful_run(
        self,
        mock_get_audio,
        mock_pipeline,
        mock_get_token,
        mock_init_env,
        monkeypatch,
        tmp_path,
    ):
        """Test successful end-to-end transcription run."""
        test_audio = tmp_path / "test.wav"
        test_audio.touch()

        # Setup mocks for success path
        mock_init_env.return_value = True
        mock_get_token.return_value = "test-token"
        mock_get_audio.return_value = test_audio

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.return_value = True
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(sys, "argv", ["audio-scribe", "--audio", str(test_audio)])

        # Should complete without raising SystemExit
        main()

        pipeline_instance.initialize_models.assert_called_once_with("test-token")
        pipeline_instance.process_file.assert_called_once_with(test_audio)

    @patch("src.audio_scribe.transcriber.initialize_environment")
    @patch("src.audio_scribe.transcriber.get_token")
    @patch("src.audio_scribe.transcriber.TranscriptionPipeline")
    @patch("src.audio_scribe.transcriber.get_audio_file_path")
    def test_main_process_failure(
        self,
        mock_get_audio,
        mock_pipeline,
        mock_get_token,
        mock_init_env,
        monkeypatch,
        tmp_path,
    ):
        """Test handling of transcription processing failure."""
        test_audio = tmp_path / "test.wav"
        test_audio.touch()

        mock_init_env.return_value = True
        mock_get_token.return_value = "test-token"
        mock_get_audio.return_value = test_audio

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.return_value = False
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(sys, "argv", ["audio-scribe", "--audio", str(test_audio)])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    @patch("src.audio_scribe.transcriber.initialize_environment")
    @patch("src.audio_scribe.transcriber.get_token")
    @patch("src.audio_scribe.transcriber.TranscriptionPipeline")
    @patch("src.audio_scribe.transcriber.get_audio_file_path")
    def test_main_keyboard_interrupt(
        self, mock_get_audio, mock_pipeline, mock_get_token, mock_init_env, monkeypatch
    ):
        """Test handling of keyboard interrupt during processing."""
        mock_init_env.return_value = True
        mock_get_token.return_value = "test-token"
        mock_get_audio.return_value = Path("/test/audio.wav")

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.side_effect = KeyboardInterrupt()
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(sys, "argv", ["audio-scribe"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 0

    @patch("src.audio_scribe.transcriber.warnings")
    def test_main_show_warnings_flag(self, mock_warnings, monkeypatch):
        """Test --show-warnings flag behavior."""
        with patch(
            "src.audio_scribe.transcriber.initialize_environment"
        ) as mock_init_env:
            mock_init_env.return_value = False  # Force early exit

            monkeypatch.setattr(sys, "argv", ["audio-scribe", "--show-warnings"])

            with pytest.raises(SystemExit):
                main()

            mock_warnings.resetwarnings.assert_called_once()

    @patch("src.audio_scribe.transcriber.warnings")
    def test_main_suppress_warnings_default(self, mock_warnings, monkeypatch):
        """Test default warning suppression behavior."""
        with patch(
            "src.audio_scribe.transcriber.initialize_environment"
        ) as mock_init_env:
            mock_init_env.return_value = False  # Force early exit

            monkeypatch.setattr(sys, "argv", ["audio-scribe"])

            with pytest.raises(SystemExit):
                main()

            # Should call filterwarnings twice (for pyannote and whisper)
            assert mock_warnings.filterwarnings.call_count == 2

    def test_main_verbose_and_quiet_flags(self, monkeypatch):
        """Test verbose and quiet flag handling."""
        with patch(
            "src.audio_scribe.transcriber.configure_logging"
        ) as mock_config_log, patch(
            "src.audio_scribe.transcriber.initialize_environment"
        ) as mock_init_env:

            mock_init_env.return_value = False  # Force early exit

            monkeypatch.setattr(sys, "argv", ["audio-scribe", "--verbose", "--quiet"])

            with pytest.raises(SystemExit):
                main()

            mock_config_log.assert_called_once_with(True, True)


class TestIntegrationScenarios:
    """Integration tests for common usage scenarios."""

    @patch("src.audio_scribe.transcriber.initialize_environment")
    @patch("src.audio_scribe.transcriber.get_token")
    @patch("src.audio_scribe.transcriber.TranscriptionPipeline")
    def test_complete_workflow_with_token_arg(
        self, mock_pipeline, mock_get_token, mock_init_env, monkeypatch, tmp_path
    ):
        """Test complete workflow with token provided via command line."""
        test_audio = tmp_path / "interview.wav"
        test_audio.touch()

        mock_init_env.return_value = True
        # get_token should not be called when token is provided via CLI

        pipeline_instance = MagicMock()
        pipeline_instance.initialize_models.return_value = True
        pipeline_instance.process_file.return_value = True
        mock_pipeline.return_value = pipeline_instance

        monkeypatch.setattr(
            sys,
            "argv",
            [
                "audio-scribe",
                "--audio",
                str(test_audio),
                "--token",
                "cli-provided-token",
                "--whisper-model",
                "small.en",
                "--verbose",
            ],
        )

        main()

        pipeline_instance.initialize_models.assert_called_once_with(
            "cli-provided-token"
        )
        pipeline_instance.process_file.assert_called_once_with(test_audio)
        mock_get_token.assert_not_called()
