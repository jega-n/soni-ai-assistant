import speech_recognition as sr
from assistant.utils.logger import logger
from assistant.config.settings import MIC_TIMEOUT, PHRASE_TIME_LIMIT


class Recorder:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def record(self):
        with sr.Microphone() as source:
            print("🎤 Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=2)

            print("🎙️ Speak now...")

            try:
                audio = self.recognizer.listen(
                    source,
                    timeout=MIC_TIMEOUT,
                    phrase_time_limit=PHRASE_TIME_LIMIT
                )

                print("✅ Recording complete")
                logger.info("Recording completed.")

                return audio

            except sr.WaitTimeoutError:
                print("❌ No speech detected.")
                logger.warning("No speech detected.")
                return None