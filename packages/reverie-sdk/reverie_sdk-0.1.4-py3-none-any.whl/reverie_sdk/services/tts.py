import json
import os
import warnings
import queue
import typing
import requests
import threading
from pathlib import Path
from reverie_sdk.utils import (
    threadsafe_generators as tsg,
    formatters as fmt,
    audio_utils,
)
from reverie_sdk.base import BaseModel
import xml.etree.ElementTree as ET

# from xml.etree.ElementTree import ParseError


class ReverieTtsResponse:
    def __init__(
        self,
        audio_bytes: bytes = None,
        **kwargs,
    ) -> None:
        self.audio_bytes: bytes = audio_bytes
        self.message: str = kwargs.pop("message", None)
        self.status: str = kwargs.pop("status", None)
        self.format: str = kwargs.pop("format", None)
        self.channels: int = kwargs.pop("channels", None)
        self.sample_rate: int = kwargs.pop("sample_rate", None)
        self.duration: float = None
        self.kwargs: typing.Dict = kwargs
        self._analyze_audio()

    def _analyze_audio(self):
        if self.audio_bytes:
            try:
                self.duration = audio_utils.get_audio_duration(
                    audio=self.audio_bytes,
                    base_model_obj=self,
                    format=self.format,
                    sample_rate=self.sample_rate,
                )
            except Exception:
                pass
                # print(err)

    def save_audio(
        self,
        file_path: typing.Union[str, Path, os.PathLike],
        create_parents=False,
        overwrite_existing=False,
    ):
        if self.audio_bytes is None:
            raise Exception(""" Nothing to save! """.strip())

        if not isinstance(file_path, Path):
            file_path = Path(file_path)

        if os.path.exists(file_path) and not overwrite_existing:
            raise Exception(f""" file_path="{file_path}" already exists! """.strip())

        if not os.path.exists(file_path.parent):
            if not create_parents:
                raise Exception(
                    f""" file_path.parent="{file_path.parent}" doesn't exist! """.strip()
                )
            else:
                os.makedirs(file_path.parent, exist_ok=True)

        with open(file_path, "wb") as f:
            f.write(self.audio_bytes)

    def __str__(self) -> str:
        _str = "ReverieTtsResponse(\n"

        if self.status is not None:
            _str += (
                f"    status          : {self.status}\n"
                f"    message         : {json.dumps(self.message) if self.message else self.message}\n"
            )
        else:
            _str += (
                f"    format          : {self.format}\n"
                f"    sample_rate     : {self.sample_rate}\n"
                f"    audio_bytes     : {len(self.audio_bytes) if self.audio_bytes else None}\n"
                f"    duration        : {fmt.duration_formatted(self.duration) if self.duration is not None else self.duration}\n"
            )

        if len(self.kwargs) > 0:
            _str += f"    kwargs          : {self.kwargs}\n"

        _str += ")"

        return _str.strip()


class ReverieTTS(BaseModel):
    "Text to speech"

    def __init__(
        self, api_key: str, app_id: str, verbose: bool = False, **extra
    ) -> None:
        super().__init__(api_key=api_key, app_id=app_id, verbose=verbose, extra=extra)
        self._logger.debug("TTS module initialized!")

    def tts(
        self,
        # header
        speaker: str = None,
        # body
        text: typing.Union[str, typing.List[str]] = None,
        ssml: typing.Union[str, typing.List[str]] = None,
        speed: float = 1.0,
        pitch: float = 0,
        sample_rate: int = 22050,
        format: str = "WAV",
        url: str = "https://revapi.reverieinc.com/",
    ) -> ReverieTtsResponse:
        # fmt: off
        """
        You can use the Text-to-Speech (TTS) API to convert any text to speech.

        Parameters
        ----------

        speaker:
            The desired language and voice code for synthesizing the audio file  
            Specify the speaker's code with respect to the language.   
            Refer to Supporting Speaker Code section for valid speaker code.  
            https://docs.reverieinc.com/reference/text-to-speech-api/supporting-speaker-code  
        
        text or ssml:
            The plain text or SSML input to synthesize an audio output.  
            If you want to follow W3 standards, the ssml field must be used and not the text field.  
        
        speed: (seconds)
            The speech rate of the audio file.  
            Allows values: from 0.5 (slowest speed rate) up to 1.5 (fastest speed rate).  
            Note: By default, speed = 1 (normal speed).  

        pitch: (seconds)
            Speaking pitch, in the range Allows values: from -3 up tp 3.   
            3 indicates an increase of 3 semitones from the original pitch.   
            -3 indicates a decrease of 3 semitones from the original pitch.   
            Note: By default, the pitch = 0 (zero)  

        sample_rate:
            The sampling rate (in hertz) to synthesize the audio output.   
            Refer to Supporting Sampling Rate section, to know the supporting audio sample rates.   
            Note: By default, the sample_rate = 22050 Hz (22.05kHz)  
            https://docs.reverieinc.com/reference/text-to-speech-api/supporting-sampling-rate  

        format:
            The speech audio format to generate the audio file.   
            Refer to Supporting Audio Format section, to know the supporting audio formats.   
            Note: By default, the format = WAV  
            https://docs.reverieinc.com/reference/text-to-speech-api/supporting-audio-format  

        Returns
        ------- 
        ReverieTtsResponse
        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(speaker, str), "Invalid value datatype!"
        assert isinstance(text, (type(None), str, typing.List)), (
            "Invalid value datatype!"
        )
        if isinstance(text, typing.List):
            for e in text:
                assert isinstance(e, str), "Invalid value datatype!"

        assert isinstance(ssml, (type(None), str, typing.List)), (
            "Invalid value datatype!"
        )
        if isinstance(ssml, typing.List):
            for e in ssml:
                assert isinstance(e, str), "Invalid value datatype!"

        assert isinstance(speed, (int, float)), "Invalid value datatype!"
        assert isinstance(pitch, (int, float)), "Invalid value datatype!"
        assert isinstance(sample_rate, int), "Invalid value datatype!"
        assert isinstance(format, str), "Invalid value datatype!"
        #
        assert isinstance(url, str), "Invalid value datatype!"

        if text is None and ssml is None:
            raise Exception("""Either `text` or `ssml` must be provided!""".strip())

        if text is not None and ssml is not None:
            warnings.warn(
                UserWarning(
                    """Both `text` and `ssml` are provided, using `ssml` for synthesis!""".strip()
                )
            )

        if ssml:
            try:
                ET.fromstring(ssml)
            except ET.ParseError as err:
                raise Exception(
                    f"Invalid ssml structure! "
                    f"Parsing failed! "
                    f"Raw error: {json.dumps(str(err))}"
                )

        ###########################

        payload = json.dumps(
            {
                **({"ssml": ssml} if ssml else {"text": text}),
                "speed": speed,
                "pitch": pitch,
                "sample_rate": sample_rate,
                "format": format,
            },
            # ensure_ascii=False, # TODO
        )

        headers = {
            "REV-API-KEY": self._api_key,
            "REV-APP-ID": self._app_id,
            "REV-APPNAME": "tts",
            "speaker": speaker,
            "Content-Type": "application/json",
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )

        if response.status_code == 200:
            return ReverieTtsResponse(
                audio_bytes=response.content,
                src=dict(text=text, ssml=ssml),
                sample_rate=sample_rate,
                format=format,
            )

        try:
            return ReverieTtsResponse(
                **response.json(),
                headers=headers,
                src=dict(text=text, ssml=ssml),
            )
        except Exception as e:
            print(e)
            return ReverieTtsResponse(
                message=response.text,
                status=response.status_code,
                headers=headers,
                src=dict(text=text, ssml=ssml),
            )

    def _tts_streaming_worker(self, kwargs: typing.Dict, *a, **kw):
        return self.tts(**kwargs)

    def tts_streaming(
        self,
        # reverie API related
        text: str,
        speaker: str = None,
        speed: float = 1.0,
        pitch: float = 0,
        sample_rate: int = 22050,
        format: str = "WAV",
        url: str = "https://revapi.reverieinc.com/",
        # tokenize
        fast_sentence_fragment: bool = True,
        tokenizer: str = "nltk",
        tokenizer_language: str = "en",
        sentence_fragment_delimiters: str = ".?!;:,\n…)]}。-",
        max_words_per_chunk=15,
    ) -> typing.Generator[ReverieTtsResponse, None, None]:
        try:
            import stream2sentence as s2s
        except Exception:
            print("use `pip install reverie_sdk[py3x-all]`")
            return

        done = False
        resp_queue = queue.Queue()

        sentence_queue = queue.Queue()

        # split text
        char_iterator = tsg.CharIterator()
        char_iterator.add(text)
        acc_generator = tsg.AccumulatingThreadSafeGenerator(char_iterator)

        s2s.init_tokenizer(tokenizer)
        sentences = s2s.generate_sentences(
            tokenizer=tokenizer,
            generator=acc_generator,
            cleanup_text_links=True,
            cleanup_text_emojis=True,
            language=tokenizer_language,
            sentence_fragment_delimiters=sentence_fragment_delimiters,
            quick_yield_single_sentence_fragment=fast_sentence_fragment,
            quick_yield_for_all_sentences=fast_sentence_fragment,
            quick_yield_every_fragment=fast_sentence_fragment,
            force_first_fragment_after_words=max_words_per_chunk,
        )

        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) > 0:
                sentence_queue.put(sentence)

            # if len(sentence) > 0:
            #     for chunk in chunker.chunk_sentence(sentence, max_words_per_chunk):
            #         chunk = chunk.strip()
            #         if len(chunk) > 0:
            #             sentence_queue.put(chunk)
            # else:
            #     continue  # Skip empty sentences

        sentence_queue.put(None)

        def process_text():
            # process sentence
            while True:
                try:
                    sentence = sentence_queue.get()
                    if sentence is None:  # Sentinel value to stop the worker
                        break

                    resp = self.tts(
                        text=sentence,
                        format=format,
                        pitch=pitch,
                        sample_rate=sample_rate,
                        speaker=speaker,
                        speed=speed,
                        url=url,
                    )

                    resp_queue.put(resp)
                except Exception as err:
                    self._logger.error(err)
                    break

            nonlocal done
            done = True

        worker = threading.Thread(target=process_text, daemon=True)
        worker.start()

        while not done or not resp_queue.empty():
            if not resp_queue.empty():
                yield resp_queue.get()

        worker.join()
