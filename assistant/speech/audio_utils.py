import tempfile
from assistant.utils.logger import logger


def save_audio(audio_data):
    """
    Save AudioData as a valid WAV file.
    """

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".wav"
    )

    with open(temp_file.name, "wb") as f:
        f.write(audio_data.get_wav_data())

    logger.info(f"Temporary audio saved: {temp_file.name}")

    return temp_file.name