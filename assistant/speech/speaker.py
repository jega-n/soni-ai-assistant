import subprocess
import sounddevice as sd
import soundfile as sf
import os

from assistant.config.settings import (
    PIPER_PATH,
    VOICE_MODEL,
    OUTPUT_AUDIO,
)

from assistant.utils.logger import logger


class Speaker:

    def __init__(self):

        logger.info("Speaker initialized.")

    def speak(self, text):

        logger.info(f"Speaking: {text}")

        os.makedirs(os.path.dirname(OUTPUT_AUDIO), exist_ok=True)

        command = [
            PIPER_PATH,
            "--model",
            VOICE_MODEL,
            "--output_file",
            OUTPUT_AUDIO,
        ]

        result = subprocess.run(
            command,
            input=text + "\n",
            text=True,
            encoding="utf-8",
            check=True,
            capture_output=True
        )

        print(result.stdout)
        print(result.stderr)

        audio, sample_rate = sf.read(OUTPUT_AUDIO)
        sd.play(audio, sample_rate)
        sd.wait()
