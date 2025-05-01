import numpy as np
from numpy.typing import NDArray
from fastrtc.speech_to_text.stt_ import STTModel
from loguru import logger
import librosa

# "tiny"    → Fastest, least accurate, ~1GB RAM
# "base"    → Fast, lower accuracy, ~2GB RAM
# "small"   → Balanced, moderate speed, ~4GB RAM
# "medium"  → Slower, better accuracy, ~7GB RAM
# "large-v3" (default) → Slowest, best accuracy, needs 10GB+ VRAM
MODEL_SIZE = "medium"
DEVICE = "cuda"  # or cpu

# "float16" → Uses Half Precision (GPUs, saves VRAM)
# "float32" → Full Precision (More accurate uses more VRAM)
# "int8"    → Lowest Precision (Best for CPUs, lowest RAM usage)
COMPUTE_TYPE = "float32" if DEVICE == "cuda" else "int8"

class FasterWhisperSTT(STTModel):
    def __init__(self):
        try:
            from faster_whisper import WhisperModel
        except (ImportError, ModuleNotFoundError):
            raise ImportError(
                "Install fastrtc[stt] for speech-to-text and stopword detection support."
            )
        self.model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
        logger.debug(f"Whisper Model loaded: {MODEL_SIZE} | Device: {DEVICE} | Precision: {COMPUTE_TYPE}")
        logger.info("Warming up Whisper model with dummy input")
        warmup_audio = np.zeros((16000,), dtype=np.float32)
        self.model.transcribe(warmup_audio)
        logger.info("Model warmup complete")

    def stt(self, audio: tuple[int, NDArray[np.int16 | np.float32]]):
        sr, audio_np = audio
        if audio_np.dtype == np.int16:
            audio_np = audio_np.astype(np.float32) / 32768.0
        if sr != 16000:
            audio_np = librosa.resample(
                audio_np, orig_sr=sr, target_sr=16000
            )
        if audio_np.ndim == 1:
            audio_np = audio_np.reshape(1, -1)
        if np.max(np.abs(audio_np)) > 1.0:
            audio_np = audio_np / np.max(np.abs(audio_np))
        return self.model.transcribe(audio_np.squeeze(0))