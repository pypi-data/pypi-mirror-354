import json
import typing
from reverie_sdk.base import BaseModel
from reverie_sdk.utils import getters
import requests


class ReverieT13nResponse:
    class Result:
        def __init__(
            self,
            apiStatus: int = None,
            inString: str = None,
            outString: typing.List[str] = None,
            **extra,
        ) -> None:
            self.apiStatus: int = apiStatus
            self.inString: str = inString
            self.outString: typing.List[str] = outString

        def __str__(self) -> str:
            outString = "\n".join([((" " * 8) + e.strip()) for e in self.outString])
            return f"""ReverieT13nResponse.Result(
    apiStatus   : {self.apiStatus}
    inString    : {self.inString}
    outString   : 
{outString}
)""".strip()

        def __repr__(self) -> str:
            return str(self)

    def __init__(self, **data) -> None:
        self._raw_response = data
        self.responseList: typing.List[ReverieT13nResponse.Result] = []

        if data.get("responseList", None) is not None:
            for e in data["responseList"]:
                try:
                    self.responseList.append(ReverieT13nResponse.Result(**e))
                except Exception as err:
                    print(err, e)

        self.status: str = getters.dict_alt_getter(data, ["status"])
        self.message: str = getters.dict_alt_getter(data, ["message"])
        self.error_cause: str = getters.dict_alt_getter(data, ["error_cause"])

    def __str__(self) -> str:
        if self.responseList:
            responseList: str = "\n".join(map(str, self.responseList or []))
            responseList = "\n" + "\n".join(
                [((" " * 8) + e) for e in responseList.splitlines()]
            )
        else:
            responseList = None

        status = f"""    status          : {self.status}\n""" if self.status else ""
        message = f"""    message         : {self.message}\n""" if self.message else ""
        err_cause = (
            f"""    error_cause     : {self.error_cause}\n"""
            if self.error_cause
            else ""
        )
        respList = (
            f"""    responseList    : {responseList}\n""" if self.responseList else ""
        )

        return (
            "ReverieT13nResponse(\n" + status + message + err_cause + respList + ")"
        ).strip()


class ReverieT13N(BaseModel):
    def __init__(
        self, api_key: str, app_id: str, verbose: bool = False, **extra
    ) -> None:
        super().__init__(api_key=api_key, app_id=app_id, verbose=verbose, extra=extra)
        self._logger.debug("T13N module initialized!")

    def transliteration(
        self,
        data: typing.List[str],
        # headers
        src_lang: str,
        tgt_lang: str,
        cnt_lang: str,
        domain: str = "1",
        # body
        isBulk: bool = True,
        abbreviate: bool = True,
        convertOrdinal: bool = False,
        ignoreTaggedEntities: bool = False,
        abbreviationWithoutDot: bool = False,
        noOfSuggestions: int = 1,
        convertNumber: str = "local",
        #
        url="https://revapi.reverieinc.com/",
    ) -> ReverieT13nResponse:
        # fmt: off
        """
        T13N Transliterate

        Parameters
        ----------
        src_lang: (source language)
            The script used in the input text.  
            Mention the ISO language code of the input text script.  
            Refer to Language Codes for valid language code.  
            https://docs.reverieinc.com/reference/transliteration-api/language-codes  

        tgt_lang: (target language)
            The script to which you want to convert the input text.  
            Mention the ISO language code to obtain the output.  
            Refer to Language Codes for valid language code.  
            https://docs.reverieinc.com/reference/transliteration-api/language-codes  

        domain:
            The Domain refers to the universe in which you use the Transliteration API. Example: Health Care, Insurance, Legal, etc.  
            Mention the domain ID. Refer to Supporting Domain in Transliteration API section for valid domain ID. Note - The default domain 1  
            https://docs.reverieinc.com/reference/transliteration-api

        cnt_lang: (content language)
            The language of the words in the input text.  
            Example -  
            “data”: “Singh Sahab aap Kahan the.”  
            In the example above, the Hindi language words are written in the English language script (Roman Script). So cnt_lang = “hi”  
            This is an optional parameter. If no value is provided, by default the value is the same as src_lang.  
            Mention the ISO language code of the input words.  
            Refer to Language Codes for valid language code.  
            https://docs.reverieinc.com/reference/transliteration-api/language-codes  

        data:
            List of input text for transliteration.

        isBulk:
            Specify whether the API should initially search in the Exception DB to transliterate the input text.  
            Note: By default, the isBulk=True and will not search in the Exception DB.  

        noOfSuggestions:
            Mention the number of transliteration suggestions the API should return for the input text.  
            Note: By default, the noOfSuggestions = 1, means the API will return only one transliteration suggestion for the input string.  
            Example: Consider noOfSuggestions = 2  
            Source Content: Rama  
            Target Content:  
                        1.      रामा
                        2.      रमा

        abbreviate:
            The abbreviate will Validate whether any Abbreviations/ Acronyms are passed in the input text and will transliterate it accurately.  
            Note - By default, the abbreviate = true  
            Note - if the value is false, the API will consider the abbreviation as a word and transliterate it to the nearest available word.  
            Note - In the input text, pass the abbreviations in upper case.  

        convertNumber:
            Specify whether to convert the numbers in the input text to the target language script based on the value type.  
            Three types of values for this parameter:  
            i) local: this value can convert the input number to the target language script.  
                Example -  
                Consider convertNumber = "local"  
                Source String: 2020.04  
                Target String: २०२०.०४  

                
            ii) words: this value can convert numbers into words w.r.t to the target language.  
                Example -  
                Consider convertNumber = "words"  
                Source string: 505  
                Target string: पांच सौ पांच  

                
            iii) roman: this value can convert Roman numbers to English numbers.  
                Example -  
                Consider convertNumber = "roman"  
                If the user types sector V in English, - The transliteration would be - सेक्टर 5 in Hindi.  
                Block II will be transliterated as ब्लॉक 2.  

        ignoreTaggedEntities:
            Specify whether you want to retain the entities like email ID and URL in the input script.  
            Note: By default, the ignoreTaggedEntities = true and will transliterate the email ID and URL into the target language script.  
            Example: Consider ignoreTaggedEntities = False  
            Source String: Check product details in www.reverieinc.com  
            Target String: चेक प्रोडक्ट डिटेल्स इन www.reverieinc.com  

        convertOrdinal:
            This is used for transliterating ordinal values to English numbers.  
            Note - Default value = False  
            For example -  
            If the user types "15th Main" in English  
            The transliteration would be "15 मेन" in Hindi  

        abbreviationWithoutDot:
            This is used to produce the abbreviation output without a dot.  
            Note - Default value = False  
            For example- If a user wants an abbreviation output without a dot and is given SMS as an input then the result would be - एसएमएस  


        Returns
        -------
        ReverieT13nResponse object

        """
        # fmt: on

        ###########################
        #      validations        #
        ###########################

        assert isinstance(data, typing.List), "Invalid value datatype!"
        for e in data:
            assert isinstance(e, str), "Invalid value datatype!"

        assert isinstance(src_lang, str), "Invalid value datatype!"
        assert isinstance(tgt_lang, str), "Invalid value datatype!"
        assert isinstance(cnt_lang, str), "Invalid value datatype!"
        assert isinstance(domain, str), "Invalid value datatype!"
        assert isinstance(isBulk, bool), "Invalid value datatype!"
        assert isinstance(abbreviate, bool), "Invalid value datatype!"
        assert isinstance(convertOrdinal, bool), "Invalid value datatype!"
        assert isinstance(ignoreTaggedEntities, bool), "Invalid value datatype!"
        assert isinstance(abbreviationWithoutDot, bool), "Invalid value datatype!"
        assert isinstance(noOfSuggestions, int), "Invalid value datatype!"
        assert isinstance(convertNumber, str), "Invalid value datatype!"
        #
        assert isinstance(url, str), "Invalid value datatype!"

        ###########################

        headers = {
            "Content-Type": "application/json",
            "REV-API-KEY": self._api_key,
            "REV-APP-ID": self._app_id,
            "src_lang": src_lang,
            "tgt_lang": tgt_lang,
            "domain": str(domain),
            "cnt_lang": cnt_lang,
            "REV-APPNAME": "transliteration",
        }

        payload = json.dumps(
            {
                "data": data,
                "isBulk": isBulk,
                "abbreviate": abbreviate,
                "convertNumber": convertNumber,
                "convertOrdinal": convertOrdinal,
                "noOfSuggestions": noOfSuggestions,
                "ignoreTaggedEntities": ignoreTaggedEntities,
                "abbreviationWithoutDot": abbreviationWithoutDot,
            }
        )

        response = requests.request(
            "POST",
            url,
            headers=headers,
            data=payload,
        )

        try:
            return ReverieT13nResponse(**response.json())
        except Exception as err:
            print(err, response.text)
