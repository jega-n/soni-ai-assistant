import os
import tempfile

from assistant.speech.wake_word import WakeWordDetector
from assistant.speech.recorder import Recorder
from assistant.speech.transcriber import Transcriber
from assistant.speech.speaker import Speaker


class VoiceLoop:

    def __init__(self):

        self.wake = WakeWordDetector()

        self.recorder = Recorder()
        self.transcriber = Transcriber()
        self.speaker = Speaker()

    # ------------------------------

    def wait_for_command(self):

        self.wake.wait()

        return self.listen()

    # ------------------------------

    def listen(self):

        audio_path = self.recorder.record()

        if audio_path is None:
            return None

        try:
            return self.transcriber.transcribe(audio_path)

        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)
    # ------------------------------

    def speak(self, text):

        self.speaker.speak(text)

