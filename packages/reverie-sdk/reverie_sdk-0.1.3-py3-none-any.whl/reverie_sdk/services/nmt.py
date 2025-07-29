import json
import typing
import requests
from reverie_sdk.base import BaseModel
from reverie_sdk.utils import getters


class ReverieLocalizationResult:
    class ReverieLocalizationResponseItem:
        def __init__(self, **data) -> None:
            self.inString: str = getters.dict_alt_getter(data, ["inString"])
            self.outString: str = getters.dict_alt_getter(data, ["outString"])
            self.outStrings: typing.Dict[str, str] = getters.dict_alt_getter(
                data,
                ["outStrings"],
            )
            self.apiStatus: int = getters.dict_alt_getter(
                data,
                ["apiStatus", "api_status"],
            )

        def __str__(self) -> str:
            outStrs = ""

            if self.outStrings:
                for k, v in self.outStrings.items():
                    outStrs += f"{' ' * 8}{k} : {v}\n"

            outStr = f"    outString   = {self.outString}\n" if self.outString else ""
            outStrs = f"    outStrings:\n{outStrs}\n" if len(outStrs) > 0 else ""

            return (
                f"{self.__class__.__name__}(\n"
                + f"    inString    = {self.inString}\n"
                + outStr
                + f"    apiStatus   = {self.apiStatus}\n"
                + outStrs
                + ")"
            )

        def __repr__(self) -> str:
            return str(self)

    def __init__(
        self,
        **resp,
    ) -> None:
        self._raw_response = resp
        # print(resp)
        self.responseList: typing.List[
            ReverieLocalizationResult.ReverieLocalizationResponseItem
        ] = []
        for e in resp.get("responseList", []):
            try:
                self.responseList.append(self.ReverieLocalizationResponseItem(**e))
            except Exception as err:
                print(err, e)

        self.status: int = resp.get("status", None)
        self.tokenConsumed: int = resp.get("tokenConsumed", None)
        self.message: str = getters.dict_alt_getter(
            resp,
            ["msg", "message", "error_cause", "errorCause"],
        )

    def __str__(self) -> str:
        responseList = "\n".join(str(e) for e in self.responseList).splitlines(True)
        responseList = "".join((" " * 8 + _l) for _l in responseList)

        contents = (
            (
                f"""    responseList:\n{responseList}\n"""
                f"""    tokenConsumed: {self.tokenConsumed}\n"""
            )
            if self.status is None
            else (
                f"""    status:        {self.status}\n"""
                f"""    message:       {self.message}\n"""
            )
        )

        return f"""{self.__class__.__name__}(\n""" f"{contents}" f""")"""

    def __repr__(self) -> str:
        return str(self)


class ReverieNMT(BaseModel):
    def __init__(
        self, api_key: str, app_id: str, verbose: bool = False, **extra
    ) -> None:
        super().__init__(api_key=api_key, app_id=app_id, verbose=verbose, extra=extra)
        self._logger.debug("NMT module initialized!")

    def localization(
        self,
        data: typing.List[str],
        # HEADERS
        src_lang: str,
        tgt_lang: typing.Union[str, typing.List[str]],
        domain: str = "1",
        appVersion: str = "2.0",
        #
        # REQUEST BODY
        enableNmt: bool = False,
        enableTransliteration: bool = True,
        enableLookup: bool = False,
        debugMode: bool = False,
        nmtMask: bool = False,
        nmtMaskTerms: typing.List[str] = [],
        #
        url: str = "https://revapi.reverieinc.com/",
    ) -> ReverieLocalizationResult:
        # fmt: off
        """
        NMT Localization

        Parameters
        ----------
        src_lang: (source language)
            The language of the input text  
            Mention the ISO Language code of the input text. Refer Language Codes for valid language code.  
            (https://docs.reverieinc.com/reference/localization-api/language-codes)  

        tgt_lang: (target language/s)
            Language to which you want to localize the input text  
            Note- To enter multiple target languages, separate the value using the comma separator(,) OR list of languages.  
            For example: “tgt_lang” : “hi, ta” OR ["hi", "ta"]  
            Mention the ISO Language code of the target language. Refer to Language Codes for valid language code.  
            (https://docs.reverieinc.com/reference/localization-api/language-codes)  

        domain:
            The Domain refers to the universe in which you use the Transliteration API. Example- Health Care, Insurance, Legal, etc.  
            Mention the domain ID. Refer to Supporting Domain in Localization API section for valid domain ID.  
            Note - The default domain = 1  
            (https://docs.reverieinc.com/reference/localization-api)  

        data:
            List of input text for localization.

        enableNmt:
            Specify whether the content localization process should use NMT technology or not.  
            i.e., When the enableNmt value is true, the system will initially refer to the Lookup database to localize content.  
            If the content is not available in the database, then the NMT is used for translation.  
            Note - By default, the enableNmt= false  

        enableTransliteration:
            Specify whether the content localization process should use transliteration technology or not.  
            i.e., When the enableTransliteration value is true, the system will initially refer to the Lookup database to localize content.  
            If the content is not available in the database, then nmt is used for translation. If nmt fails, transliteration is called.  
            Note - By default, the enableTransliteration= true  

        enableLookup:
            The parameter will specify whether the application should refer to the Lookup DB or not.  
            i.e., when the enableLookup is true, the system will initially refer to the Database to fetch contents.  
            Note - By default, the enableLookup= false.  

        debugMode:
            The Debug parameter will provide log details about localized content.  
            The details provided are the entity code, localization process type, and more.  
            This information is useful to capture the log and analyze the system performance.  
            Note By default, the debugMode= false  

        nmtMask:
            The feature to screen the non-dictionary words used in a sentence.  
            In other words, the mask will indicate the words that should not be translated into the target language.  
            Note - By default, the nmtMask = false  
            Note - To set the nmtMask = true, it is mandatory the src_lang = en (English).  

        nmtMaskTerms:
            Determines the Words that are to be masked.  
            Note - On defining values in the nmtMaskTerms, then automatically the nmtMask is set to true.  
            Example -  
            Masking a term - "nmtMaskTerms": ["Reverie Language Technologies"]  
            Here, the API will mask the term Reverie Language Technologies, if found in the source content, and will transliterate the word.  

        Returns
        -------
        ReverieLocalizationResult object
        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(data, typing.List), "Invalid value datatype!"
        for e in data:
            assert isinstance(e, str), "Invalid value datatype!"

        assert isinstance(src_lang, str), "Invalid value datatype!"
        assert isinstance(tgt_lang, (str, typing.List)), "Invalid value datatype!"
        if isinstance(tgt_lang, typing.List):
            for e in tgt_lang:
                assert isinstance(e, str), "Invalid value datatype!"

        assert isinstance(domain, str), "Invalid value datatype!"
        assert isinstance(appVersion, str), "Invalid value datatype!"
        assert isinstance(enableNmt, bool), "Invalid value datatype!"
        assert isinstance(enableTransliteration, bool), "Invalid value datatype!"
        assert isinstance(enableLookup, bool), "Invalid value datatype!"
        assert isinstance(debugMode, bool), "Invalid value datatype!"
        assert isinstance(nmtMask, bool), "Invalid value datatype!"
        assert isinstance(nmtMaskTerms, typing.List), "Invalid value datatype!"
        for e in nmtMaskTerms:
            assert isinstance(e, str), "Invalid value datatype!"

        assert isinstance(url, str), "Invalid value datatype!"

        if len(nmtMaskTerms) > 0:
            nmtMask = True

        if nmtMask and src_lang != "en":
            raise Exception(
                "To set the nmtMask = true, it is mandatory the src_lang = en (English)"
            )

        ###########################

        payload = {
            "data": data,
            "nmtMask": nmtMask,
            "enableNmt": enableNmt,
            "debugMode": debugMode,
            "enableLookup": enableLookup,
            "enableTransliteration": enableTransliteration,
        }

        if nmtMask:
            payload["nmtMaskTerms"] = nmtMaskTerms

        payload = json.dumps(payload)

        headers = {
            "Content-Type": "application/json",
            "REV-API-KEY": self._api_key,
            "REV-APP-ID": self._app_id,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang if isinstance(tgt_lang, str) else ",".join(tgt_lang),
            "domain": str(domain),
            "REV-APPNAME": "localization",
            "REV-APPVERSION": appVersion,
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        try:
            return ReverieLocalizationResult(**response.json())
        except Exception as err:
            print(err, response.text)
