from pathlib import Path
import soundfile as sf
import typing
import io
from ..base import BaseModel


def get_audio_duration(
    audio: typing.Union[bytes, io.BytesIO, Path],
    base_model_obj: BaseModel = None,
    format: str = None,
    sample_rate: int = None,
    bit_depth: int = 16,
) -> float:
    try:
        if isinstance(audio, io.BytesIO):
            audio = audio.read()
        elif isinstance(audio, (Path, str)):
            with open(audio, "rb") as f:
                audio = f.read()

        if (format or "").lower() == "pcm":
            if not isinstance(sample_rate, (int, float)):
                return None

            if not isinstance(bit_depth, (int, float)):
                return None

            return len(audio) / (sample_rate * 1 * (bit_depth / 8))

        # default
        io_file = io.BytesIO(audio)
        with sf.SoundFile(io_file) as sf_audio:
            return len(sf_audio) / sf_audio.samplerate

    except Exception as err:
        if base_model_obj:
            base_model_obj._logger.error(err)
        else:
            print(err)

        return None
