import io
import queue
import json
import warnings
import threading
import time
import traceback
import typing
import requests
import websockets
import asyncio  # for async feature
from websocket import WebSocket, create_connection, WebSocketBadStatusException
import websockets.exceptions
from reverie_sdk.base import BaseModel


class ReverieAsrResult:
    def __init__(
        self,
        id: str = None,
        text: str = None,
        final: bool = None,
        cause: str = None,
        success: bool = None,
        confidence: str = None,
        display_text: str = None,
        **extra,
    ) -> None:
        self.id: str = id
        self.text: str = text
        self.final: bool = final
        self.cause: str = cause
        self.success: bool = success
        self.confidence: str = confidence
        self.display_text: str = display_text
        self.extra = extra

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} (\n"
            f"    id           : {self.id}\n"
            f"    text         : {self.text}\n"
            f"    final        : {self.final}\n"
            f"    cause        : {self.cause}\n"
            f"    success      : {self.success}\n"
            f"    confidence   : {self.confidence}\n"
            f"    display_text : {self.display_text}\n"
            f"    extra args   : {self.extra}\n"
            f")"
        ).strip()


class ReverieAsrBatchResult:
    class _Word:
        def __init__(self, **data) -> None:
            self._raw_response: typing.Dict = data

            self.conf: float = data.get("conf", None)
            self.end: float = data.get("end", None)
            self.start: float = data.get("start", None)
            self.word: str = data.get("word", None)

        def __repr__(self):
            return str(self)

        def __str__(self):
            return f"""{self.__class__.__name__}(
    conf    : {self.conf}
    end     : {self.end}
    start   : {self.start}
    word    : {self.word}
)""".strip()

    class _Transcript:
        def __init__(self, **data) -> None:
            self._raw_response: typing.Dict = data

            self.transcript: str = data.get("transcript", None)
            self.original_transcript: str = data.get("original_transcript", None)
            self.channel_number: int = data.get("channel_number", None)
            self.words: typing.List = data.get("words", None)
            self.subtitles: str = data.get("subtitles", None)

            if self.words:
                words = []

                def find_words(w):
                    if isinstance(w, typing.Dict):
                        try:
                            words.append(ReverieAsrBatchResult._Word(**w))
                        except Exception as err:
                            print(err, w)
                        finally:
                            return

                    if isinstance(w, typing.List):
                        for e in w:
                            find_words(e)

                find_words(self.words)
                self.words = words

        def __repr__(self):
            return str(self)

        def __str__(self):
            return f"""{self.__class__.__name__}(
    transcript          : {self.transcript}
    original_transcript : {self.original_transcript}
    channel_number      : {self.channel_number}
    subtitles           : {json.dumps(self.subtitles)}
    words               : {len(self.words)} words
)""".strip()

    def __init__(self, **data) -> None:
        self._raw_response: typing.Dict = data

        self.job_id: str = data.get("job_id", None)
        self.code: str = data.get("code", None)
        self.message: str = data.get("message", None)
        self.result: str = data.get("result", None)
        self.status: str = data.get("status", None)

        if self.result:
            try:
                self.result = ReverieAsrBatchResult._Transcript(**self.result)
            except Exception as err:
                print(err, self.result)

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        if self.result:
            result = ("").join(
                [(" " * 4) + e for e in str(self.result).splitlines(keepends=True)]
            )
        else:
            result = None

        res = ""

        if self.code:
            res += f"    code    : {self.code}\n"

        if self.job_id:
            res += f"    job_id  : {self.job_id}\n"

        if self.status:
            res += f"    status  : {self.status}\n"

        if self.message:
            res += f"    message : {self.message}\n"

        if result:
            res += "    result  :\n" + f"{result}\n"

        return (f"{self.__class__.__name__} (\n" + res + ")").strip()


class AudioStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""

    def __init__(self):
        self.buff = queue.Queue()
        self.buff_async = asyncio.Queue()
        self.streaming: bool = True

    def add_chunk(self, in_data: bytes):
        """Continuously collect data from the audio stream, into the buffer."""
        if self.streaming:
            self.buff.put(in_data)

        return self

    async def add_chunk_async(self, in_data: bytes):
        """Continuously collect data from the audio stream, into the buffer."""
        if self.streaming:
            await self.buff_async.put(in_data)

        return self

    def generator(self):
        while self.streaming:
            data = b""
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk: bytes = self.buff.get()

            if chunk is None:
                yield data

            data += chunk

            # Now consume whatever other data's still buffered.
            while len(data) < 1024:
                try:
                    chunk = self.buff.get(block=False)
                    if chunk is None:
                        continue

                    data += chunk
                except queue.Empty:
                    break

            yield data

    async def generator_async(self, timeout_secs=5):
        try:
            while self.streaming:
                data = b""
                # Use a blocking get() to ensure there's at least one chunk of
                # data, and stop iteration if the chunk is None, indicating the
                # end of the audio stream.
                chunk: bytes = await asyncio.wait_for(
                    self.buff_async.get(),
                    timeout=timeout_secs,
                )

                if chunk is None:
                    yield data

                data += chunk

                # Now consume whatever other data's still buffered.
                while len(data) < 1024:
                    try:
                        chunk = self.buff.get(block=False)
                        if chunk is None:
                            continue

                        data += chunk
                    except queue.Empty:
                        break

                yield data
        except TimeoutError:
            pass
        except Exception as err:
            print(err)
            traceback.print_exc()


class ReverieASR(BaseModel):
    """Automatic Speech Recognition (ASR)/ Speech to Text (STT)"""

    def __init__(
        self, api_key: str, app_id: str, verbose: bool = False, **extra
    ) -> None:
        super().__init__(api_key=api_key, app_id=app_id, verbose=verbose, extra=extra)
        self._logger.debug("ASR module initialized!")

    async def __send_stream_data_async(
        self,
        ws,
        bytes_or_stream: typing.Union[AudioStream, bytes],
    ):
        if isinstance(bytes_or_stream, bytes):
            buffer = io.BytesIO(bytes_or_stream)
            try:
                while True:
                    d = buffer.read(4096)

                    if d is None or len(d) == 0:
                        break

                    await ws.send(d)
                    self._logger.debug(f"Sent {len(d)} bytes to ASR")

                await ws.send(b"--EOF--")
                self._logger.debug("Sent EOF to ASR")
            except Exception:
                self._logger.error(traceback.format_exc())

        elif isinstance(bytes_or_stream, AudioStream):
            try:
                async for chunk in bytes_or_stream.generator_async():
                    if chunk is None or len(chunk) == 0:
                        break

                    await ws.send(chunk)
                    # print(f"Sent {len(chunk)} bytes to ASR")
                    self._logger.debug(f"Sent {len(chunk)} bytes to ASR")

                await ws.send(b"--EOF--")
                # print(f"Sent EOF to ASR")
                self._logger.debug("Sent EOF to ASR")
            except websockets.exceptions.WebSocketException:
                bytes_or_stream.streaming = False
            except Exception as err:
                bytes_or_stream.streaming = False
                self._logger.error(err)
                self._logger.error(traceback.format_exc())

    def __send_stream_data_threading(
        self,
        ws: WebSocket,
        bytes_or_stream: typing.Union[AudioStream, bytes],
    ):
        if isinstance(bytes_or_stream, bytes):
            buffer = io.BytesIO(bytes_or_stream)
            try:
                while ws.connected:
                    d = buffer.read(1024)

                    if len(d) == 0:
                        break

                    if ws.connected:
                        ws.send_binary(d)
                        self._logger.debug(f"Sent {len(d)} bytes to ASR")
                        # time.sleep(0.01)

                if ws.connected:
                    ws.send_binary(b"--EOF--")
                    self._logger.debug("Sent EOF to ASR")
            except Exception:
                self._logger.error(traceback.format_exc())

        elif isinstance(bytes_or_stream, AudioStream):
            try:
                for chunk in bytes_or_stream.generator():
                    if len(chunk) == 0 or not ws.connected:
                        break

                    if ws.connected:
                        ws.send_binary(chunk)
                        self._logger.debug(f"Sent {len(chunk)} bytes to ASR")
                        # time.sleep(0.01)

                if ws.connected:
                    ws.send_binary(b"--EOF--")
                    self._logger.debug("Sent EOF to ASR")
            except Exception:
                bytes_or_stream.streaming = False
                self._logger.error(traceback.format_exc())

    def stt_stream(
        self,
        src_lang: str,
        bytes_or_stream: typing.Union[AudioStream, bytes],
        # defaults
        domain: str = "generic",
        timeout: float = 15,
        silence: float = 15,
        format: str = "16k_int16",
        logging: str = "true",
        punctuate: str = "true",
        continuous: typing.Union[str, int] = 0,
        # url formation
        secure: bool = True,
        host: str = "revapi.reverieinc.com",
        endpoint: str = "/stream",
        **extra_params,
    ) -> typing.Generator[ReverieAsrResult, None, None]:
        # fmt: off
        """
        Speech-to-Text Streaming

        Parameters
        ----------
        src_lang:
            Indicates the language in which the audio is spoken.   
            Specify the ISO language code.   
            Example: "hi"  
            Refer to section Language Codes for valid language code.  
            https://docs.reverieinc.com/reference/speech-to-text-streaming-api/language-codes  
        
        domain:
            The universe in which the Streaming STT API is used for transcribing the speech.   
            Specify the domain ID.   
            Refer to Speech to Text | Streaming APISupporting Domain section for valid domain ID.  
            https://docs.reverieinc.com/reference/speech-to-text-streaming-api  

        timeout:
            The duration to keep a connection open between the application and the STT server.   
            Note: The default timeout = 15 seconds, and the maximum time allowed = 180 seconds  
        
        silence:
            The time to determine when to end the connection automatically after detecting the silence after receiving the speech data.   
            Example:   
            Consider silence = 15 seconds   
            i.e., On passing the speech for 60 seconds, and if you remain silent, the connection will be open for the next 15 seconds and then will automatically get disconnected.   
            Note: The default silence= 1 second, and the maximum silence = 30 seconds.  

        format:
            The audio sampling rate and the data format of the speech.   
            Refer to section Supporting Audio Format section to know the supporting audio formats.   
            Note: By default, the format = 16k_int16. (WAV, Signed 16 bit, 16,000 or 16K Hz).  
            https://docs.reverieinc.com/reference/speech-to-text-streaming-api/supporting-audio-format  

        logging:
            Possible values are :  
            1. true - stores audio and keep transcripts in logs.  
            2. no_audio -  does not store audios but keep transcripts in logs.  
            3. no_transcript - does not keep transcripts in logs but stores audios.  
            4. false - does not keep neither audios nor transcripts in log.  
            Default value is true  
            
        punctuate:
            It will enable punctuation and capitalisation in the transcript. The values it can take are true and false.  
            Supported languages: en, hi  
            Default value is true  
        
        continuous:
            It will enable continuous decoding even after silence is detected.  
            Can take value true/1 or false/0.  
            Default value is false/0  



        Yields
        ------
        objects of ReverieAsrResult

        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(src_lang, str), "Invalid value datatype!"
        assert isinstance(
            bytes_or_stream,
            (AudioStream, bytes),
        ), "Invalid value datatype!"
        assert isinstance(domain, str), "Invalid value datatype!"
        assert isinstance(timeout, (int, float)), "Invalid value datatype!"
        assert isinstance(silence, (int, float)), "Invalid value datatype!"
        assert isinstance(format, str), "Invalid value datatype!"
        assert isinstance(logging, str), "Invalid value datatype!"
        assert isinstance(punctuate, str), "Invalid value datatype!"
        assert isinstance(continuous, (int, str)), "Invalid value datatype!"
        #
        assert isinstance(secure, bool), "Invalid value datatype!"
        assert isinstance(host, str), "Invalid value datatype!"
        assert isinstance(endpoint, str), "Invalid value datatype!"

        ###########################

        self._logger.debug(f"extra_params: {extra_params}")

        url = f"{'wss' if secure else 'ws'}://{host}{endpoint}?" + "&".join(
            f"{k}={v}"
            for k, v in {
                "appname": "stt_stream",
                "apikey": self._api_key,
                "appid": self._app_id,
                "domain": domain,
                "format": format,
                "logging": logging,
                "silence": silence,
                "timeout": timeout,
                "src_lang": src_lang,
                "punctuate": punctuate,
                "continuous": continuous,
                **extra_params,
            }.items()
        )

        try:
            ws = create_connection(url, enable_multithread=True)
        except WebSocketBadStatusException as e:
            err_msg = e.resp_body

            if isinstance(err_msg, bytes):
                err_msg = err_msg.decode()

            if isinstance(err_msg, str):
                try:
                    err_msg = json.loads(err_msg)
                except Exception:
                    pass

            self._logger.error(err_msg)
            # self.logger.error(traceback.format_exc())
            yield ReverieAsrResult(success=False, text=err_msg["message"])
            return

        self._logger.debug(f"Websocket connected for url: {url}")

        t = threading.Thread(
            target=self.__send_stream_data_threading,
            args=(ws, bytes_or_stream),
            daemon=True,
        )
        t.start()
        self._logger.debug("Started a thread to send audio chunks")

        while ws.connected:
            try:
                _result = ws.recv()
                self._logger.debug(f"Raw ASR response: {_result}")
                # print(result)
                result = None
                try:
                    result = ReverieAsrResult(**json.loads(_result))

                    is_final = result.final
                    if continuous not in [True, "true", 1]:
                        is_final = is_final or result.cause in [
                            "timeout",
                            "silence detected",
                            "EOF received",
                        ]

                    if is_final:
                        if isinstance(bytes_or_stream, AudioStream):
                            bytes_or_stream.streaming = False

                        ws.close()
                except Exception as err:
                    print(err, _result)

                yield result
            except Exception:
                self._logger.error(traceback.format_exc())
                break

    async def stt_stream_async(
        self,
        src_lang: str,
        bytes_or_stream: typing.Union[AudioStream, bytes],
        callback: typing.Callable,
        # defaults
        domain: str = "generic",
        timeout: float = 15,
        silence: float = 15,
        format: str = "16k_int16",
        logging: str = "true",
        punctuate: str = "true",
        continuous: typing.Union[str, int] = 0,
        # url formation
        secure: bool = True,
        host: str = "revapi.reverieinc.com",
        endpoint: str = "/stream",
        **extra_params,
    ):
        # fmt: off
        """
        Speech-to-Text Streaming (Async)

        Parameters
        ----------
        src_lang:
            Indicates the language in which the audio is spoken.   
            Specify the ISO language code.   
            Example: "hi"  
            Refer to section Language Codes for valid language code.  
            https://docs.reverieinc.com/reference/speech-to-text-streaming-api/language-codes  
        
        domain:
            The universe in which the Streaming STT API is used for transcribing the speech.   
            Specify the domain ID.   
            Refer to Speech to Text | Streaming APISupporting Domain section for valid domain ID.  
            https://docs.reverieinc.com/reference/speech-to-text-streaming-api  

        timeout:
            The duration to keep a connection open between the application and the STT server.   
            Note: The default timeout = 15 seconds, and the maximum time allowed = 180 seconds  
        
        silence:
            The time to determine when to end the connection automatically after detecting the silence after receiving the speech data.   
            Example:   
            Consider silence = 15 seconds   
            i.e., On passing the speech for 60 seconds, and if you remain silent, the connection will be open for the next 15 seconds and then will automatically get disconnected.   
            Note: The default silence= 1 second, and the maximum silence = 30 seconds.  

        format:
            The audio sampling rate and the data format of the speech.   
            Refer to section Supporting Audio Format section to know the supporting audio formats.   
            Note: By default, the format = 16k_int16. (WAV, Signed 16 bit, 16,000 or 16K Hz).  
            https://docs.reverieinc.com/reference/speech-to-text-streaming-api/supporting-audio-format  

        logging:
            Possible values are :  
            1. true - stores audio and keep transcripts in logs.  
            2. no_audio -  does not store audios but keep transcripts in logs.  
            3. no_transcript - does not keep transcripts in logs but stores audios.  
            4. false - does not keep neither audios nor transcripts in log.  
            Default value is true  
            
        punctuate:
            It will enable punctuation and capitalisation in the transcript. The values it can take are true and false.  
            Supported languages: en, hi  
            Default value is true  
        
        continuous:
            It will enable continuous decoding even after silence is detected.  
            Can take value true/1 or false/0.  
            Default value is false/0  



        Yields
        ------
        objects of ReverieAsrResult

        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(src_lang, str), "Invalid value datatype!"
        assert isinstance(
            bytes_or_stream,
            (AudioStream, bytes),
        ), "Invalid value datatype!"
        assert isinstance(callback, typing.Callable), "Invalid value datatype!"
        #
        assert isinstance(domain, str), "Invalid value datatype!"
        assert isinstance(timeout, (int, float)), "Invalid value datatype!"
        assert isinstance(silence, (int, float)), "Invalid value datatype!"
        assert isinstance(format, str), "Invalid value datatype!"
        assert isinstance(logging, str), "Invalid value datatype!"
        assert isinstance(punctuate, str), "Invalid value datatype!"
        assert isinstance(continuous, (int, str)), "Invalid value datatype!"
        #
        assert isinstance(secure, bool), "Invalid value datatype!"
        assert isinstance(host, str), "Invalid value datatype!"
        assert isinstance(endpoint, str), "Invalid value datatype!"

        ###########################
        self._logger.debug(f"extra_params: {extra_params}")

        url = f"{'wss' if secure else 'ws'}://{host}/stream?" + "&".join(
            f"{k}={v}"
            for k, v in {
                "appname": "stt_stream",
                "apikey": self._api_key,
                "appid": self._app_id,
                "domain": domain,
                "src_lang": src_lang,
                "timeout": timeout,
                "silence": silence,
                "format": format,
                "logging": logging,
                **extra_params,
            }.items()
        )

        try:
            async with websockets.connect(url) as ws:
                self._logger.debug(f"Websocket connected for url: {url}")

                sender_task = asyncio.create_task(
                    self.__send_stream_data_async(ws, bytes_or_stream)
                )

                try:
                    async for _result in ws:
                        self._logger.debug(f"Raw ASR response: {_result}")

                        try:
                            result = ReverieAsrResult(**json.loads(_result))

                            is_final = (result.final) or result.cause in [
                                "timeout",
                                "silence detected",
                                "EOF received",
                            ]

                            callback(result)

                            if is_final:
                                break
                        except Exception as err:
                            print(err, _result)
                except Exception:
                    self._logger.error(traceback.format_exc())

                finally:
                    await sender_task
                    if isinstance(bytes_or_stream, AudioStream):
                        bytes_or_stream.streaming = False

        except Exception as err:
            err_msg = str(err)

            try:
                err_msg = json.loads(err_msg)
            except Exception:
                pass

            self._logger.error(err_msg)
            self._logger.error(traceback.format_exc())
            callback(ReverieAsrResult(success=False, text=err_msg))
            return

    def stt_file(
        self,
        src_lang: str,
        data: bytes = None,
        file_url: str = None,
        # header
        domain: str = "generic",
        format: str = "16k_int16",
        logging: str = "true",
        punctuate: str = "true",
        #
        url: str = "https://revapi.reverieinc.com/",
    ) -> ReverieAsrResult:
        # fmt: off
        """
        STT File (Non-Streaming)

        Parameters
        ----------
        domain:
            Refer to the universe in which the STT API is used for transcribing the audio file  
            Example: Banking, Insurance, etc.  
            Specify the domain code.  
            Refer to Supporting Domain section for valid domain ID.  
            https://docs.reverieinc.com/speech-to-text-file-api  
            
        src_lang:
            Indicates the language in which the audio is spoken  
            Specify the language code.   
            Refer to Language Code section for valid language code.  
            https://docs.reverieinc.com/speech-to-text-file-api/language-codes  

        format:
            Indicates the supporting format of the audio file  
            Mention the audio sample rate and file format of the uploaded file.  
            Refer to the Supporting Audio Format section to know the supporting audio formats.  
            Note:  
            1. By default, the format = 16k_int16. (WAV, Signed 16 bit, 16,000 or 16K Hz).  
            2. It is an optional parameter.  
            https://docs.reverieinc.com/speech-to-text-file-api/supporting-audio-format  
        
        logging:
            Indicates the type of logging of data you can choose  
            Default value=true  
            Possible values are :  
            1. true - stores client's audio and keeps transcript in logs.  
            2. no_audio -  does not store client's audio but keeps transcript in logs.  
            3. no_transcript - does not keep transcript in logs but stores client's audio.  
            4. false - does not keep neither client's audio nor transcript in log.  
        
        punctuate:
            Indicates whether capitalisation and punctuation is needed in the transcript  
            It will enable punctuation and capitalisation in the transcript.  
            The values it can take are true and false.  
            Supported languages: en, hi  
            Default value is true  

        data:
            audio file data/ audio bytes
        
        file_url:
            The audio file's public URL to obtain the transcript.  
            Note - file_url length should be equal to or less than 300 seconds (5 minutes).  

        Returns
        -------
        ReverieAsrResult object
        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(src_lang, str), "Invalid value datatype!"
        assert isinstance(
            data,
            (type(None), bytes),
        ), "Invalid value datatype!"
        assert isinstance(
            file_url,
            (type(None), str),
        ), "Invalid value datatype!"
        assert isinstance(domain, str), "Invalid value datatype!"
        assert isinstance(format, str), "Invalid value datatype!"
        assert isinstance(logging, str), "Invalid value datatype!"
        assert isinstance(punctuate, str), "Invalid value datatype!"
        #
        assert isinstance(url, str), "Invalid value datatype!"

        if data is None and file_url is None:
            raise Exception("""Either `data` or `file_url` must be provided!""".strip())

        if data is not None and file_url is not None:
            warnings.warn(
                UserWarning(
                    """Both `data` and `file_url` are provided, using `data`!""".strip()
                )
            )

        ###########################

        headers = {
            "REV-APPNAME": "stt_file",
            "REV-API-KEY": self._api_key,
            "REV-APP-ID": self._app_id,
            "src_lang": src_lang,
            "domain": domain,
            "format": format,
            "logging": logging,
            "punctuate": punctuate,
        }

        response = requests.request(
            "POST",
            url,
            headers=headers,
            **(
                {"files": {"audio_file": data}}
                if data
                else {"data": {"file_url": file_url}}
            ),
        )

        json_resp: typing.Dict = None
        try:
            json_resp: typing.Dict = response.json()
        except Exception:
            pass

        if response.status_code != 200 or not isinstance(json_resp, dict):
            json_resp = json_resp or {}
            message = json_resp.get("message", response.text)
            self._logger.error(message)
            return ReverieAsrResult(success=False, text=message)

        try:
            return ReverieAsrResult(**json_resp)
        except Exception as err:
            print(err, json_resp)

    def stt_batch(
        self,
        src_lang: str,
        data: bytes,
        # headers
        domain: str = "generic",
        format: str = "16k_int16",
        subtitles: bool = False,
        #
        base_url: str = "https://revapi.reverieinc.com/",
    ) -> typing.Generator[ReverieAsrBatchResult, None, str]:
        # fmt: off
        """
        STT Batch

        Parameters
        ----------

        domain:
            This field identifies your use case type and set of the terminology defined for transcription.  
            e.g. for general audio is 'generic'  
            It is only required for the first API i.e Upload File API.  

        src_lang:
            Specify the language code.   
            Refer to Language Codes section for valid language code.  
            https://docs.reverieinc.com/speech-to-text-batch-api/language-codes  

        format:
            Mention the audio sample rate and file format of the uploaded file.  
            Refer to Supporting Audio Format section to know the supporting audio formats.  
            It is only required for the first API i.e Upload File API  
            Note -  
                1. By default, the format = 16k_int16. (WAV, Signed 16 bit, 16,000 or 16K Hz).  
                2. It is an optional parameter.  
            https://docs.reverieinc.com/speech-to-text-batch-api/supporting-audio-format  
        
        subtitles:
            Enables subtitling from the audio file.


                
        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(src_lang, str), "Invalid value datatype!"
        assert isinstance(data, bytes), "Invalid value datatype!"
        assert isinstance(domain, str), "Invalid value datatype!"
        assert isinstance(format, str), "Invalid value datatype!"
        assert isinstance(subtitles, bool), "Invalid value datatype!"
        #
        assert isinstance(base_url, str), "Invalid value datatype!"

        ###########################

        # initiate request
        url = f"{base_url.rstrip('/')}/upload"
        files = {"file": data}
        headers = {
            "src_lang": src_lang,
            "domain": domain,
            "format": format,
            "subtitles": json.dumps(subtitles),
            "REV-API-KEY": self._api_key,
            "REV-APPNAME": "stt_batch",
            "REV-APP-ID": self._app_id,
        }

        _response = requests.post(url, headers=headers, files=files)
        job_id = None

        try:
            resp_data = ReverieAsrBatchResult(**_response.json())
            job_id = resp_data.job_id

            yield resp_data
        except Exception as err:
            self._logger.error(err)
            raise err

        # check status
        url = f"{base_url.rstrip('/')}/status"
        headers = {
            "REV-API-KEY": self._api_key,
            "REV-APP-ID": self._app_id,
            "REV-APPNAME": "stt_batch",
        }
        params = (("job_id", job_id),)

        retries = 1
        success = False
        failed = False
        while not success and not failed:
            _resp = requests.get(url, headers=headers, params=params)
            try:
                status_resp = ReverieAsrBatchResult(**_resp.json())

                yield status_resp

                if status_resp.status is not None:
                    failed = True
                elif status_resp.code == "000":
                    success = True
                else:
                    wait = retries * 5
                    self._logger.debug(f"Sleeping for {wait} secs...")
                    time.sleep(wait)
                    retries += 1
            except Exception as err:
                print(err, _resp.text)
                break

        if not failed:
            # get transcript
            url = f"{base_url.rstrip('/')}/transcript"
            headers = {
                "REV-API-KEY": self._api_key,
                "REV-APP-ID": self._app_id,
                "REV-APPNAME": "stt_batch",
            }

            resp = requests.request(
                "GET",
                url + f"?job_id={job_id}",
                headers=headers,
            )

            try:
                yield ReverieAsrBatchResult(**resp.json())
            except Exception as err:
                print(err, resp.text)
