from pathlib import Path

from PIL import Image, ImageFont, ImageDraw


def main():
    image_path = r".\test.png"
    text = "Hello World"
    color = (255, 255, 255)  # 文字の色
    font_path = Path(__file__).parent.joinpath("fonts", "Roboto-Bold.ttf")
    font_size = 200  # 文字の大きさ

    font = ImageFont.truetype(font=str(font_path), size=font_size)
    image = Image.new(mode="RGBA", size=(1920, 1080), color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((110, 20), text, fill=color, font=font)
    image.save(image_path, quality=95)


if __name__ == "__main__":
    main()
