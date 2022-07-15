import os

import deepl
import dotenv

dotenv.load_dotenv(".env")


langs = [
    "BG",
    "CS",
    "DA",
    "DE",
    "EL",
    "EN-GB",
    "EN-US",
    "ES",
    "ET",
    "FI",
    "FR",
    "HU",
    "ID",
    "IT",
    "JA",
    "LT",
    "LV",
    "NL",
    "PL",
    "PT-PT",
    "PT-BR",
    "RO",
    "RU",
    "SK",
    "SL",
    "SV",
    "TR",
    "ZH",
]


class Translator:
    def __init__(self):

        auth_key = os.environ.get("DEEPL_API_KEY")
        self.translator = deepl.Translator(auth_key)

    def translate_text(self, text: str, target_lang: str):
        result = self.translator.translate_text("Hello world!", target_lang="JA")

        print(result.text)
        return result
