"""
Contain functions related to coloring the text
"""

import numpy as np
from PIL import Image
from rich.color import Color
from rich.style import Style
from rich.text import Text

from CliR import PixelsPerChar


def color_twotone(image_:Image.Image, im_mask:Image.Image):
    """
    Extracts the foreground and background colors from an image and a twotone mask.

    :param image_:
    :param im_mask:
    :return:
    """
    if image_. size != im_mask.size:
        raise ValueError("Image and mask must be the same size.")

    color = np.asarray(image_)
    mask = np.asarray(im_mask)

    rows = mask.shape[0] // PixelsPerChar[1]
    cols = mask.shape[1] // PixelsPerChar[0]
    data = np.zeros((rows,cols,2,3),dtype=np.uint8)

    for y in range(rows):
        for x in range(cols):
            yCoords = y * PixelsPerChar[1]
            xCoords = x * PixelsPerChar[0]

            fore = []
            back = []

            for px,py in np.ndindex(PixelsPerChar):
                p = mask[yCoords + py, xCoords + px]
                if p > 0:
                    fore.append(color[yCoords + py, xCoords + px])
                else:
                    back.append(color[yCoords + py, xCoords + px])

            # If there is no foreground, means in the mask the cell is all black aka only background because not enough
            # features in the pixels for there to be represented by the char set
            if len(fore) != 0:
                data[y, x, 0] = np.mean(fore, axis=0)

            data[y,x,1] = np.mean(back, axis=0)

    return data


def color_char(image: Image.Image, chars: list[str], mask: Image.Image,bg_intensity:float=1):
    """
    Colors a string of text using the source image.

    :param bg_intensity: Intensity of the background color
    :param image: The source image
    :param chars: The string to color
    :param mask: The twotone mask
    :return:
    """

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
