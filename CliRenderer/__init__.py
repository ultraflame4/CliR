import os

from PIL import Image

from rich.text import Text

from CliRenderer.chartools import PixelsPerChar, generateColoredChars, pixels2Char
from CliRenderer.colorer import color_char
from CliRenderer.core import Flags


def render(source_: Image.Image, out_size=(170, 50), bg_intensity=1, skip_resize=False) -> Text:
    """
    Renders a single image into unicode text.

    :param source_: The source image
    :param out_size: The size of the final text in the form of (columns, lines).
    :return: returns a rich Text object to be printed to the console with rich
    :param skip_resize: If set to true, the image will not be resized. This is useful if the image is already the correct size.
    """

    FinalImageSize = (PixelsPerChar[0] * out_size[0], PixelsPerChar[1] * out_size[1])

    if not skip_resize:
        image = source_.resize(FinalImageSize)
    else:
        image = source_
    if image.size != FinalImageSize:
        raise ValueError("The image size does not match the output size. Cannot skip resize!")

    if Flags.DEBUG:
        os.makedirs("./build", exist_ok=True)
        image.save("./build/resized.png")


    data, charcolors = generateColoredChars(image)

    chars = []
    for row in data:
        char_row = ""
        for cell in row:
            char_row += pixels2Char(cell)
        chars.append(char_row)

    string = color_char( chars, charcolors, bg_intensity)
    return string
    # return ""