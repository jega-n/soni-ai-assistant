import queue

import numpy as np
import sounddevice as sd
from openwakeword.model import Model

from assistant.config.settings import WAKE_WORD


class WakeWordDetector:
    SAMPLE_RATE = 16000
    CHUNK_SIZE = 1280          # 80 ms
    THRESHOLD = 0.5

    def __init__(self):
        print("Loading wake word model...")

        self.model = Model(
            wakeword_models=[WAKE_WORD],
            inference_framework="onnx"
        )

        self.audio_queue = queue.Queue()

        self.stream = sd.RawInputStream(
            samplerate=self.SAMPLE_RATE,
            blocksize=self.CHUNK_SIZE,
            channels=1,
            dtype="int16",
            callback=self._audio_callback,
        )

        self.stream.start()

    def _audio_callback(self, indata, frames, time, status):
        if status:
            print(status)

        self.audio_queue.put(bytes(indata))

    def listen(self):

        print("Listening for wake word...")
        count = 0
        while True:
            audio = np.frombuffer(
                self.audio_queue.get(),
                dtype=np.int16
            )

            prediction = self.model.predict(audio)

            score = float(prediction.get(WAKE_WORD, 0))

            if score > 0.05:
                print(f"Wake score: {score:.3f}")

            if score >= 0.1:
                count += 1
            else:
                count = 0

            if count >= 2:
                print("Wake word detected!")
                return True

    def close(self):
        if self.stream:
            self.stream.stop()
            self.stream.close()

    def wait(self):
        return self.listen()