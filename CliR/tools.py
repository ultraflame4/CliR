import sys

import numpy as np
from PIL import Image

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