from movie_tools.closed_captions.translator import Translator


def main():
    lines = ""
    with open("src/movie_tools/closed_captions/captions.sbv", mode="r", encoding="utf-8") as f:
        lines = f.readlines()

    result = Translator().translate_text(lines, target_lang="JA")

    with open("result.txt", mode="w", encoding="utf-8") as f:
        f.writelines(result)


if __name__ == "__main__":
    main()
