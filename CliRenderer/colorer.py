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


def color_char(chars: list[str], charcolors: np.ndarray, bg_intensity: float = 1):
    """
    Colors a string of text using the source image.

    :param bg_intensity: Intensity of the background color
    :param image: The source image
    :param chars: The string to color
    :param mask: The twotone mask
    :return:
    """

    string = Text()
    print(charcolors.shape, len(chars))
    for y, row in enumerate(chars):
        for x, char in enumerate(row):
            rawfore_ = charcolors[y, x, 0]
            rawback_ = charcolors[y, x, 1]


            # Blend the back and fore colors in a 80:20 ratio so that the background color is effectively the 20% th percentile of cell colors
            # TLDR: The background color is the darkest color in the cell,
            # by blending it with the foreground color it looks nicer and is more representative of the cell color
            # The same goes for the foreground color (which is the brightest), but it is blended with the background color instead
            fore_ = rawfore_*0.8 + rawback_*0.2
            back_ = rawfore_*0.2 + rawback_*0.8

            fore = Color.from_rgb(fore_[0], fore_[1], fore_[2])
            back = Color.from_rgb(back_[0] * bg_intensity, back_[1] * bg_intensity, back_[2] * bg_intensity)
            style = Style(color=fore, bold=True, bgcolor=back)
            string.append(char, style=style)
        string += "\r\n"

    return string
