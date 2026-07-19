import sounddevice as sd
import numpy as np
import wave
import tempfile

from assistant.utils.logger import logger
from assistant.config.settings import MIC_TIMEOUT, PHRASE_TIME_LIMIT


class Recorder:

    SAMPLE_RATE = 16000

    def __init__(self):
        pass


    def record(self):
        """
        Records microphone audio and returns wav file path.
        """

        print("🎤 Recording...")
        logger.info("Recording started.")

        duration = PHRASE_TIME_LIMIT

        try:
            audio = sd.rec(
                int(duration * self.SAMPLE_RATE),
                samplerate=self.SAMPLE_RATE,
                channels=1,
                dtype="int16"
            )

            sd.wait()

            print("✅ Recording complete")
            logger.info("Recording completed.")

            # Save temporary wav
            temp_file = tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False
            )

            with wave.open(temp_file.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.SAMPLE_RATE)
                wf.writeframes(audio.tobytes())


            return temp_file.name


        except Exception as e:
            logger.error(f"Recording failed: {e}")
            print("❌ Recording failed")
            return None