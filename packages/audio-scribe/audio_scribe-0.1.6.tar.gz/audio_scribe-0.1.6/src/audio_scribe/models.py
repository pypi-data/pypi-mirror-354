"""Model handling and audio processing for Audio Scribe."""

import wave
import torch
from typing import Optional, Any, cast
import whisper  # type: ignore
import logging
import warnings
import threading
from datetime import datetime
from pathlib import Path
from pyannote.audio import Pipeline  # type: ignore

from audio_scribe.config import TranscriptionConfig
from audio_scribe.auth import TokenManager

logger = logging.getLogger(__name__)

try:
    from alive_progress import alive_bar  # type: ignore
    import psutil
    import GPUtil  # type: ignore

    HAVE_PROGRESS_SUPPORT = True
except ImportError:
    HAVE_PROGRESS_SUPPORT = False


class AudioProcessor:
    """Handles audio file processing and segmentation."""

    def __init__(self, config: TranscriptionConfig):
        self.config = config

    def load_audio_segment(
        self,
        audio_path: Path,
        start_time: float,
        end_time: float,
        output_path: Path,
    ) -> bool:
        """Extract and save the audio segment from start_time to end_time."""
        try:
            with wave.open(str(audio_path), "rb") as infile:
                params = infile.getparams()
                frame_rate = params.framerate
                start_frame = int(start_time * frame_rate)
                end_frame = min(int(end_time * frame_rate), infile.getnframes())

                infile.setpos(start_frame)
                frames = infile.readframes(end_frame - start_frame)

                with wave.open(str(output_path), "wb") as outfile:
                    outfile.setparams(params)
                    outfile.writeframes(frames)
            return True
        except Exception as e:
            logger.error(f"Failed to process audio segment: {e}")
            return False


class TranscriptionPipeline:
    """Main pipeline for audio transcription and speaker diarization."""

    def __init__(self, config: TranscriptionConfig):
        self.config = config
        self.diarization_pipeline: Optional[Pipeline] = None
        self.whisper_model: Optional[Any] = None
        self.token_manager = TokenManager()
        self._running = False
        assert config.temp_directory is not None
        self.temp_directory: Path = config.temp_directory

    def initialize_models(self, auth_token: str) -> bool:
        """Initialize the Pyannote diarization pipeline and Whisper model."""
        try:
            # Load Whisper model
            self.whisper_model = whisper.load_model(
                self.config.whisper_model,
                device=self.config.device,
                download_root=str(self.config.output_directory / "models"),
            )

            # Load Pyannote diarization pipeline
            self.diarization_pipeline = Pipeline.from_pretrained(
                self.config.diarization_model, use_auth_token=auth_token
            )

            if self.diarization_pipeline is not None:
                device = torch.device(cast(str, self.config.device))
                self.diarization_pipeline.to(device)

            if self.config.device == "cpu":
                warnings.warn(
                    "Running on CPU. GPU is recommended for better performance."
                )

            return True
        except Exception as e:
            logger.error(f"Model initialization failed: {e}")
            logger.error("Please ensure you have accepted the model conditions at:")
            logger.error("  1. https://huggingface.co/pyannote/segmentation-3.0")
            logger.error("  2. https://huggingface.co/pyannote/speaker-diarization-3.1")
            return False

    def _update_resources(self, bar: Any) -> None:
        """Update progress bar with resource usage information."""
        while self._running:
            try:
                import time

                time.sleep(0.5)

                cpu_usage = (
                    psutil.cpu_percent(interval=None) if HAVE_PROGRESS_SUPPORT else 0
                )
                memory_usage = (
                    psutil.virtual_memory().percent if HAVE_PROGRESS_SUPPORT else 0
                )

                if HAVE_PROGRESS_SUPPORT and GPUtil.getGPUs():
                    gpus = GPUtil.getGPUs()
                    gpu_mem_used = f"{gpus[0].memoryUsed:.0f}"
                    gpu_mem_total = f"{gpus[0].memoryTotal:.0f}"
                    gpu_usage_text = f"{gpu_mem_used}/{gpu_mem_total} MB"
                else:
                    gpu_usage_text = "N/A"

                resource_text = f"CPU: {cpu_usage}%, MEM: {memory_usage}%, GPU Mem: {gpu_usage_text}"
                bar.text(resource_text)
            except Exception as e:
                logger.error(f"Resource monitoring error: {e}")

    def process_file(self, audio_path: Path) -> bool:
        """Diarize, segment, and transcribe using Whisper + Pyannote with progress feedback."""
        try:
            if self.diarization_pipeline is None or self.whisper_model is None:
                logger.error("Pipeline not initialized. Call initialize_models first.")
                return False

            logger.info("Starting audio processing...")
            diarization = self.diarization_pipeline(str(audio_path))
            segments = list(diarization.itertracks(yield_label=True))
            total_segments = len(segments)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = self.config.output_directory / f"transcript_{timestamp}.txt"
            audio_processor = AudioProcessor(self.config)

            if not HAVE_PROGRESS_SUPPORT:
                # Process without progress bar
                with output_file.open("w", encoding="utf-8") as f:
                    for turn, _, speaker in segments:
                        segment_path = (
                            self.temp_directory
                            / f"segment_{speaker}_{turn.start:.2f}_{turn.end:.2f}.wav"
                        )
                        if audio_processor.load_audio_segment(
                            audio_path, turn.start, turn.end, segment_path
                        ):
                            transcription = self.whisper_model.transcribe(
                                str(segment_path)
                            )["text"]
                            segment_path.unlink(missing_ok=True)

                            line = f"[{turn.start:.2f}s - {turn.end:.2f}s] Speaker {speaker}: {transcription.strip()}\n"
                            f.write(line)
                            logger.info(line.strip())
                return True
            else:
                # Use progress bar
                with output_file.open("w", encoding="utf-8") as f, alive_bar(
                    total_segments,
                    title="Transcribing Audio",
                    spinner="pulse",
                    theme="classic",
                    stats=False,
                    elapsed=True,
                    monitor=True,
                ) as bar:
                    self._running = True
                    resource_thread = threading.Thread(
                        target=self._update_resources, args=(bar,)
                    )
                    resource_thread.start()

                    for turn, _, speaker in segments:
                        segment_path = (
                            self.temp_directory
                            / f"segment_{speaker}_{turn.start:.2f}_{turn.end:.2f}.wav"
                        )
                        if audio_processor.load_audio_segment(
                            audio_path, turn.start, turn.end, segment_path
                        ):
                            transcription = self.whisper_model.transcribe(
                                str(segment_path)
                            )["text"]
                            segment_path.unlink(missing_ok=True)

                            line = f"[{turn.start:.2f}s - {turn.end:.2f}s] Speaker {speaker}: {transcription.strip()}\n"
                            f.write(line)
                            logger.info(line.strip())

                        bar()

                    self._running = False
                    resource_thread.join()

            logger.info(f"Transcription completed. Output saved to: {output_file}")
            return True

        except Exception as e:
            logger.error(f"Processing failed: {e}")
            return False
