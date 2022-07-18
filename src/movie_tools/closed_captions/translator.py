import os
from typing import TypeVar

import deepl
import dotenv

dotenv.load_dotenv(".env")

T = TypeVar("T", int, str)


class Translator:
    def __init__(self) -> None:

        auth_key = os.environ.get("DEEPL_API_KEY")
        self.translator = deepl.Translator(auth_key)

    def translate_text(self, text: T, target_lang: str) -> T:
        if isinstance(text, str):
            result = self.translator.translate_text(text, target_lang=target_lang)
            return result.text
        elif isinstance(text, list):
            result = self.translator.translate_text(text, target_lang=target_lang)
            return [text.text for text in result]
        else:
            raise NotImplementedError(f"Cannot translate type of {type(text)}")


if __name__ == "__main__":
    t = Translator()
    test = t.translate_text("こんにちは", "EN-US")
    print(test)
