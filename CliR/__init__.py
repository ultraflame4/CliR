import os

from PIL import Image
from rich.console import Console
from rich.text import Text

from CliR.chartools import PixelsPerChar, split_to_char, pixels2Char
from CliR.colorer import color_twotone, color_char
from CliR.core import Flags


def render(source_: Image.Image, out_size=(500, 500))->Text:
    """
    Renders a single image into unicode text.

    :param source_: The source image
    :param out_size: The size of the final text in the form of (columns, lines).
    :return: returns a rich Text object to be printed to the console with rich
    """

    FinalImageSize = (PixelsPerChar[0] * out_size[0], PixelsPerChar[1] * out_size[1])

    image = source_.resize(FinalImageSize)
    gray = source_.resize(FinalImageSize).convert("L")

    if Flags.DEBUG:
        os.makedirs("./build", exist_ok=True)
        image.save("./build/resized.png")
        gray.save("./build/gray.png")

    data, mask = split_to_char(gray)

    chars = []
    for row in data:
        char_row = ""
        for cell in row:
            char_row += pixels2Char(cell)
        chars.append(char_row)


    string = color_char(image, chars, mask, 1)
    return string
