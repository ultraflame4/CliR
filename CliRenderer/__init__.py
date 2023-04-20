import concurrent.futures
import os

from PIL import Image
from rich.progress import track
from rich.text import Text
import numpy.typing as npt
from CliRenderer.chartools import PixelsPerChar, split_to_char, pixels2Char
from CliRenderer.colorer import color_twotone, color_char
from CliRenderer.core import Flags


def render(source_: Image.Image, out_size=(170, 50),bg_intensity=1,skip_resize=False)->Text:
    """
    Renders a single image into unicode text.

    :param source_: The source image
    :param out_size: The size of the final text in the form of (columns, lines).
    :return: returns a rich Text object to be printed to the console with rich
    :param skip_resize: If set to true, the image will not be resized. This is useful if the image is already the correct size.
    """

    FinalImageSize = (PixelsPerChar[0] * out_size[0], PixelsPerChar[1] * out_size[1])


    if not skip_resize:
        image = source_.resize(FinalImageSize).convert("RGB")
        gray = source_.resize(FinalImageSize).convert("L")
    else:
        image = source_.convert("RGB")
        gray = source_.convert("L")

    if image.size != FinalImageSize:
        raise ValueError("The image size does not match the output size. Cannot skip resize!")


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


    string = color_char(image, chars, mask, bg_intensity)
    return string
