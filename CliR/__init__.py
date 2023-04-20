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
from CliR.tools import color_twotone


def color_char(image: Image.Image, chars: list[str], mask: Image.Image,bg_intensity:float=1):
    """
    Colors a string of text using the source image.

    :param bg_intensity: Intensity of the background color
    :param image: The source image
    :param chars: The string to color
    :param mask: The twotone mask
    :return:
    """

    rows = len(chars)
    cols = len(chars[0])
    string = Text()

    colors = color_twotone(image, mask)

    for y, row in enumerate(chars):
        for x, char in enumerate(row):
            fore_ = colors[y, x][0]
            back_ = colors[y, x][1]
            fore = Color.from_rgb(fore_[0],fore_[1], fore_[2])
            back = Color.from_rgb(back_[0]*bg_intensity, back_[1]*bg_intensity , back_[2]*bg_intensity)
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
    string = color_char(image, chars,mask,1)


    console.print(string)
