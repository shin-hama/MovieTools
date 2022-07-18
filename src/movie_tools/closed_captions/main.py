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


def main(video_id: str) -> None:
    client = YouTubeClient()
    captions = client.get_captions(video_id)
    jp_caption = list(filter(lambda cap: cap.snippet.language == "ja", captions.items))
    if len(jp_caption) == 0:
        print("ERROR: Japanese caption that is used for translating base does not found.")
        return

    data = client.get_caption(jp_caption[0].id)
    text = data.decode("utf-8")

    for key, name in supported.items():
        translated = Translator().translate_text(text, target_lang=key)

        snippet = UploadCaptionSnippet(language=key, name=name, videoId=video_id)
        client.upload_caption(translated.encode("utf-8"), snippet)
        break


if __name__ == "__main__":
    video_id = input("Input video id: ")
    print(f"Convert captions for {video_id}")
    main(video_id)
