import os

import colorama
import numpy as np
from numpy import typing as npt
from PIL import Image
from rich.color import Color
from rich.console import Console
from rich.style import Style
from rich.text import Text

from CliR.chartools import PixelsPerChar, split_to_char, pixels2Char


def color_char(image: Image.Image, chars: list[str]):
    """
    Colors a string of text using the source image.

    :param image: The source image
    :param chars: The string to color
    :return:
    """

    rows = len(chars)
    cols = len(chars[0])
    string = Text()
    data = np.asarray(image.resize((cols, rows)))

    for y, row in enumerate(chars):
        for x, char in enumerate(row):
            pixel = data[y, x]
            fore = Color.from_rgb(pixel[0], pixel[1], pixel[2])
            back = Color.from_rgb(pixel[0] / 4, pixel[1] / 4, pixel[2] / 4)
            style = Style(color=fore, bold=True, bgcolor=back)
            string.append(char, style=style)
        string += "\n"
    return string


def render(source_: Image.Image, out_size=(500, 500)):
    """
    Renders a single image into unicode text.

    :param source_: The source image
    :param out_size: The size of the final text in the form of (columns, lines).
    :return:
    """

    FinalImageSize = (PixelsPerChar[0] * out_size[0], PixelsPerChar[1] * out_size[1])

    image = source_.resize(FinalImageSize)
    gray = source_.resize(FinalImageSize).convert("L")

    os.makedirs("./build", exist_ok=True)
    image.save("./build/resized.png")
    gray.save("./build/gray.png")

    data,mask = split_to_char(gray)
    chars = []

    for row in data:
        char_row = ""
        for cell in row:
            char_row += pixels2Char(cell)
        chars.append(char_row)

    console = Console()
    string = color_char(image, chars)

    console.print(string)
