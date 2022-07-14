from pathlib import Path

from PIL import Image, ImageFont, ImageDraw


class Imaging:
    DEFAULT_FONT_SIZE = 64

    def __init__(self):
        self.img = Image.new(mode="RGBA", size=(1920, 1080), color=(0, 0, 0, 0))

        self.font_path = Path(__file__).parent.joinpath("fonts", "Roboto-Bold.ttf")

    def save(self, image_path: str = r".\test.png"):
        self.img.save(image_path, quality=95)

    def write(
        self,
        text: str,
        xy: tuple[float, float],
        size: int = DEFAULT_FONT_SIZE,
    ):
        """
        白抜き黒枠の文字を画像上に描画
        位置とテキスト内容、サイズを変更可能
        """
        font = ImageFont.truetype(font=str(self.font_path), size=size)
        draw = ImageDraw.Draw(self.img)
        draw.text(
            xy,
            text,
            fill=(255, 255, 255),
            font=font,
            stroke_fill="black",
            stroke_width=4,
        )

    def paste(self, image_path: str, xy: tuple[int, int], width: int = None):
        pasted = Image.open(image_path)
        pasted = pasted.resize((width or pasted.width, pasted.height * width // pasted.width))
        self.img.paste(pasted, xy)
