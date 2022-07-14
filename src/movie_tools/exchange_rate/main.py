import os

import dotenv

from movie_tools.exchange_rate import imaging, rate


dotenv.load_dotenv("./.env")


def main():

    rate_client = rate.Client(os.environ.get("OXRATE_APP_ID"))
    result = rate_client.get_latest()

    image = imaging.Imaging()

    width, height = image.img.size
    margin = 20

    for (i, [key, value]) in enumerate(result.rates.items()):
        x = i % 18 * 100 + margin
        y = i // 18 * 100 + margin
        image.write(f"{key}: {int(value)}", (x, y), size=20)

    image.save("./test.png")


main()
