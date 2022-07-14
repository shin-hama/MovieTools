import os

import dotenv

from movie_tools.exchange_rate import imaging, rate


dotenv.load_dotenv("./.env")


flags = [
    "USD",
    "EUR",
    "GBP",
    "CNY",
    "AUD",
    "CAD",
    "CHF",
    "SEK",
    "NZD",
    "THB",
    "TRY",
    "INR",
    "MXN",
    "RUB",
    "SGD",
    "AED",
    "HKD",
    "PLN",
    "ZAR",
    "PHP",
]


def get_flag(name: str) -> str:
    return f"src/movie_tools/exchange_rate/flags/{name}.png"


def main():

    rate_client = rate.Client(os.environ.get("OXRATE_APP_ID"))
    result = rate_client.get_latest()

    image = imaging.Imaging()

    width, height = image.img.size
    margin_x = 128
    space_x = 104
    space_y = 56
    unit_width = 338
    unit_height = 66

    jpy = result.rates["JPY"]
    image.paste(get_flag("JPY"), (715, 200), width=100)
    image.write(f"JPY: {jpy}", (715 + 100 + 24, 200), size=64)

    for (i, name) in enumerate(flags):
        x = i % 4 * (unit_width + space_x) + margin_x
        y = i // 4 * (unit_height + space_y) + 356
        image.paste(get_flag(name), (x, y), width=100)
        value = result.rates.get(name, 0)
        image.write(f"{name}: {value}", (x + 120, y), size=40)

    image.save("./test.png")


main()
