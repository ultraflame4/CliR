import os

import numpy as np
from numpy import typing as npt
from PIL import Image

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
                (y+1) * PixelsPerChar[1],
            )
            xCoords = (
                x * PixelsPerChar[0],
                (x+1) * PixelsPerChar[0],
            )
            cell = array[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]]

            min_ = int(np.amin(cell, axis=(0, 1)))
            max_ = int(np.amax(cell, axis=(0, 1)))

            mid = (max_ + min_) // 2
            # print(mid,cell[0,0],min_,max_)
            bw = (cell > mid)
            # print(yCoords,xCoords,list(bw))
            data[y,x] = bw.flatten('F')
            array[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]] = bw*255

    Image.fromarray(array).save(f"./build/twotone.png")
    return data


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
    string = ""

    for row in data:
        for cell in row:
            string += pixels2Char(cell)
        string += "\n"

    print(string)