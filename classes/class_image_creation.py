from PIL import Image, ImageDraw, ImageFont


class ImageCreation:
    def __init__(self):
        pass

    def get_background(self, path) -> Image.Image:
        return Image.open(path).convert("RGBA")

    def get_sticker(self, path: str, size: tuple = ()) -> Image.Image:
        sticker = Image.open(path).convert("RGBA")
        if len(size) > 0:
            sticker = sticker.resize(size, Image.LANCZOS)
        return sticker

    def paste_sticker(
        self, background: Image.Image, sticker: Image.Image, position: tuple
    ) -> None:
        background.paste(sticker, position, sticker)
        return

    def create_object(self, background: Image.Image) -> ImageDraw.ImageDraw:
        return ImageDraw.Draw(background)

    def get_font(self, font_path: str, font_size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(font_path, font_size)

    def insert_title(
        self,
        background: Image.Image,
        position: tuple,
        text: str,
        font: ImageFont.FreeTypeFont,
    ) -> Image.Image:
        draw = ImageDraw.Draw(background)
        draw.text(
            position, text, font=font, fill="white"
        )  # You can adjust the fill color
        return background

    def save(
        self,
        background: Image.Image,
        name: str = "imagem_final.png",
        format: str = "PNG",
    ) -> None:
        background.save(name, format=format)
        return

    def insert_text(
        self,
        image: Image.Image,
        text: str,
        position: tuple,
        font: ImageFont.FreeTypeFont,
        color=(255, 255, 255),
    ):
        draw = ImageDraw.Draw(image)
        draw.text(position, text, font=font, fill=color)
        return image
