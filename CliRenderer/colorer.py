"""
Contain functions related to coloring the text
"""

import numpy as np
import numpy.typing as npt
from PIL import Image
from rich.color import Color
from rich.style import Style
from rich.text import Text
from CliRenderer import PixelsPerChar
import numba as nb


@nb.njit(cache=True, fastmath=True)
def color_twotone(color: npt.NDArray[np.uint8], mask: npt.NDArray[np.uint8]) -> np.ndarray[np.uint8]:
    """
    Extracts the foreground and background colors from an image and a twotone mask.

    :param color:
    :param mask:
    :return:
    """

    if color.shape[:2] != mask.shape[:2]:
        raise ValueError(f"Image and mask must be the same size!. Mask shape: {mask.shape}, Image shape: {color.shape}")

    rows = mask.shape[0] // PixelsPerChar[1]
    cols = mask.shape[1] // PixelsPerChar[0]
    data = np.zeros((rows, cols, 2, 3), dtype=np.uint16)

    for y in range(rows):
        for x in range(cols):
            yCoords = y * PixelsPerChar[1]
            xCoords = x * PixelsPerChar[0]

            fore = np.zeros((3,), dtype=np.uint16)
            foreCount = 0
            back = np.zeros((3,), dtype=np.uint16)
            backCount = 0

            for px, py in np.ndindex(PixelsPerChar):
                p = mask[yCoords + py, xCoords + px]
                if p > 0:
                    np.add(fore, color[yCoords + py, xCoords + px], fore)
                    foreCount += 1
                else:
                    np.add(back, color[yCoords + py, xCoords + px], back)
                    backCount += 1

            # If there is no foreground, means in the mask the cell is all black aka only background because not enough
            # features in the pixels for there to be represented by the char set
            if foreCount > 0:
                data[y, x, 0] = np.floor_divide(fore, foreCount)

            data[y, x, 1] = np.floor_divide(back, backCount)

    return data


def color_char(image: Image.Image, chars: list[str], mask: Image.Image, bg_intensity: float = 1):
    """
    Colors a string of text using the source image.

    :param bg_intensity: Intensity of the background color
    :param image: The source image
    :param chars: The string to color
    :param mask: The twotone mask
    :return:
    """

    string = Text()

    colors = color_twotone(np.asarray(image).copy(order="C"), mask)

    for y, row in enumerate(chars):
        for x, char in enumerate(row):
            fore_ = colors[y, x][0]
            back_ = colors[y, x][1]
            fore = Color.from_rgb(fore_[0], fore_[1], fore_[2])
            back = Color.from_rgb(back_[0] * bg_intensity, back_[1] * bg_intensity, back_[2] * bg_intensity)
            style = Style(color=fore, bold=True, bgcolor=back)
            string.append(char, style=style)
        string += "\r\n"
    return string
