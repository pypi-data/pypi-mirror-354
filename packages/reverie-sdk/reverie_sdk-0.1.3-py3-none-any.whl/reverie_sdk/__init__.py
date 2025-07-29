from reverie_sdk.base import BaseModel
from reverie_sdk.services import (
    ReverieASR,
    ReverieNLU,
    ReverieT13N,
    ReverieNMT,
    ReverieTTS,
)


class ReverieClient(BaseModel):
    """
    Wrapper class for all underlying Reverie services:
    - ASR/ STT
    - TTS
    - T13N
    - NMT
    - NLU
    - NLP
    """

    def __init__(
        self,
        api_key: str,
        app_id: str,
        verbose: bool = False,
        **extra,
    ) -> None:
        """
        Reverie Python3 SDK Client

        Wrapper class for all underlying Reverie services:
        - ASR/ STT
        - TTS
        - T13N
        - NMT
        - NLU
        - NLP

        :param api_key: A unique key/token is provided by Reverie to identify the user using the STT API.
        :param app_id: A unique account ID to identify the user and the default account settings.
        :param verbose: Noisy logging, extra details
        """

        super().__init__(api_key=api_key, app_id=app_id, verbose=verbose, extra=extra)

        creds = dict(api_key=api_key, app_id=app_id, verbose=verbose)

        self.asr: ReverieASR = ReverieASR(**creds)
        """
            ASR/ STT related services:
                - STT Streaming
                - STT File (non streaming)
                - STT Batch
        """

        self.tts: ReverieTTS = ReverieTTS(**creds)
        """
            TTS related services
                - TTS
                - TTS Streaming
        """

        self.t13n = ReverieT13N(**creds)
        """
            Transliteration related services
                - Transliteration
        """

        self.nmt = ReverieNMT(**creds)
        """
            Translation related services
                - Localization
        """

        self.nlu = ReverieNLU(**creds)
        """
            Text & Sansadhak services
        """

        self._logger.debug("All modules initialized!")

    def __mask_cred(self, val: str):
        masked_val = "X" * 8 + val[-4:]
        return masked_val

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__} (\n"
            f"    api_key = {self.__mask_cred(self._api_key)}\n"
            f"    app_id  = {self.__mask_cred(self._app_id)}\n"
            f"    verbose = {self._verbose}\n"
            f"    modules:\n"
            f"        - asr   = {self.asr}\n"
            f"        - nlu   = {self.nlu}\n"
            f"        - nmt   = {self.nmt}\n"
            f"        - t13n  = {self.t13n}\n"
            f"        - tts   = {self.tts}\n"
            f")"
        ).strip()

    def __repr__(self) -> str:
        return str(self)
