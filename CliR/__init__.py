import os

import colorama
import numpy as np
from numpy import typing as npt
from PIL import Image
from rich.color import Color
from rich.console import Console
from rich.style import Style
from rich.text import Text

from CliR.tools import PixelsPerChar, PixelsPerCharCount, pixels2Char


def split_to_char(image_: Image.Image) -> np.ndarray:
    array: npt.NDArray = np.asarray(image_).copy()
    rows = array.shape[0] // PixelsPerChar[1]
    cols = array.shape[1] // PixelsPerChar[0]
    # print(array.flags)
    if len(array.shape) > 2:
        raise Exception("Error, image must only be grayscale")

    data = np.zeros((rows, cols, PixelsPerCharCount), dtype=bool)
    for y in range(rows):
        for x in range(cols):
            yCoords = (
                y * PixelsPerChar[1],
                (y + 1) * PixelsPerChar[1],
            )
            xCoords = (
                x * PixelsPerChar[0],
                (x + 1) * PixelsPerChar[0],
            )
            cell = array[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]]

            min_ = int(np.amin(cell, axis=(0, 1)))
            max_ = int(np.amax(cell, axis=(0, 1)))

            mid = (max_ + min_) // 2
            # print(mid,cell[0,0],min_,max_)
            bw = (cell > mid)
            # print(yCoords,xCoords,list(bw))
            data[y, x] = bw.flatten('F')
            array[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]] = bw * 255

    Image.fromarray(array).save(f"./build/twotone.png")
    return data


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


    for y,row in enumerate(chars):
        for x,char in enumerate(row):
            pixel = data[y,x]
            fore = Color.from_rgb(pixel[0],pixel[1],pixel[2])
            back = Color.from_rgb(pixel[0]/4,pixel[1]/4,pixel[2]/4)
            style = Style(color=fore,bold=True,bgcolor=back)
            string.append(char,style=style)
        string+="\n"
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

    data = split_to_char(gray)
    chars = []

    for row in data:
        char_row = ""
        for cell in row:
            char_row += pixels2Char(cell)
        chars.append(char_row)

    console = Console()
    string = color_char(image, chars)

    console.print(string)
