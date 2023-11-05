"""
Contain functions related to coloring the text
"""

import numpy as np
from CliRenderer.ext import ansi_color

def ansi_rgb_fore(color: np.ndarray):
    return f"\033[38;2;{color[0]};{color[1]};{color[2]}m"

def ansi_rgb_back(color: np.ndarray):
    return f"\033[48;2;{color[0]};{color[1]};{color[2]}m"

def color_char(chars: list[str], charcolors: np.ndarray, bg_intensity: float = 1) -> str:
    """
    Colors a string of text using the source image.

    :param bg_intensity: Intensity of the background color
    :param image: The source image
    :param chars: The string to color
    :param mask: The twotone mask
    :return:
    """

    string = ""

    for y, row in enumerate(chars):
        for x, char in enumerate(row):
            rawfore_ = charcolors[y, x, 0]
            rawback_ = charcolors[y, x, 1]

            # Blend the back and fore colors in a 80:20 ratio so that the background color is effectively the 20% th percentile of cell colors
            # TLDR: The background color is the darkest color in the cell,
            # by blending it with the foreground color it looks nicer and is more representative of the cell color
            # The same goes for the foreground color (which is the brightest), but it is blended with the background color instead
            fore_ = rawfore_ * 0.8 + rawback_ * 0.2
            back_ = (rawfore_ * 0.2 + rawback_ * 0.8) * bg_intensity

            # string += ansi_rgb_fore(fore_.astype(int))+ansi_rgb_back(back_.astype(int))+char
            string += ansi_color(
                fore_.astype(int)[0],
                fore_.astype(int)[1],
                fore_.astype(int)[2],
                True
            )+ansi_rgb_back(back_.astype(int))+char

        string += "\r\n"

    return string
