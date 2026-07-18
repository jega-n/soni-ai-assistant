from faster_whisper import WhisperModel

from assistant.config.settings import (
    WHISPER_MODEL,
    DEVICE,
    COMPUTE_TYPE,
    BEAM_SIZE,
)

from assistant.utils.logger import logger


class Transcriber:

    def __init__(self):

        logger.info("Loading Whisper Model...")

        self.model = WhisperModel(
            WHISPER_MODEL,
            device=DEVICE,
            compute_type=COMPUTE_TYPE,
        )

        logger.info("Whisper Loaded.")

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(
            audio_path,
            beam_size=BEAM_SIZE,
            language="en",
            vad_filter=True
        )

        text = ""

        for segment in segments:
            text += segment.text

        logger.info(f"Recognized : {text}")

        return text.strip()