from movie_tools.closed_captions.translator import Translator
from movie_tools.closed_captions.youtube import UploadCaptionSnippet, YouTubeClient


supported = {
    "BG": "Bulgarian",
    "CS": "Czech",
    "DE": "German",
    "EL": "Greek",
    "EN-US": "English",
    "ES": "Spanish",
    "ET": "Estonian",
    "FR": "French",
    "ID": "Indonesian",
    "IT": "Italian",
    "LT": "Lithuanian",
    "LV": "Latvian",
    "NL": "Dutch",
    "PL": "Polish",
    "PT-PT": "Portuguese",
    "RU": "Russian",
    "SK": "Slovak",
    "SV": "Swedish",
    "TR": "Turkish",
    "ZH": "Chinese",
}


def main():
    client = YouTubeClient()
    video_id = "iSQCc_1CiyE"
    # captions = client.get_captions()
    # print(captions)
    data = client.get_caption("MRglHYjRG6_L71lEOICdvvyhJRApqRxZ")
    text = data.decode("utf-8")

    for key, name in supported.items():
        translated = Translator().translate_text(text, target_lang=key)

        snippet = UploadCaptionSnippet(language=key, name=name, videoId=video_id)
        client.upload_caption(translated.encode("utf-8"), snippet)
        break


if __name__ == "__main__":
    main()
