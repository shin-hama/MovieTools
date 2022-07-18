import os

import dotenv

from movie_tools.exchange_rate import imaging, oxr_client


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


def main(fee: int) -> None:
    rate_client = oxr_client.Client(os.environ.get("OXRATE_APP_ID", ""))
    result = rate_client.get_latest()

    image = imaging.Imaging()

    # Create JPY Header
    start_x = 715
    start_y = 200
    flag_width = 100
    flag_text_space = 24
    jpy = result.rates["JPY"]
    image.paste(get_flag("JPY"), (start_x, start_y), width=flag_width)
    image.write(f"JPY: {fee:,} ¥", (start_x + flag_width + flag_text_space, start_y), size=64)

    # Create exchanged fees for each countries
    margin_x = 128
    space_x = 104
    space_y = 56
    unit_width = 338
    unit_height = 66
    for (i, name) in enumerate(flags):
        x = i % 4 * (unit_width + space_x) + margin_x
        y = i // 4 * (unit_height + space_y) + start_y + flag_width + space_y
        image.paste(get_flag(name), (x, y), width=flag_width)
        rate = result.rates[name]
        image.write(f"{name}: {fee * rate / jpy:,.6g}", (x + flag_width + flag_text_space, y + 19), size=40)

    image.save("./test.png")


if __name__ == "__main__":
    main(14000)
