import os

from PIL import Image

def render(source_:Image.Image,out_size=(500,500)):
    """
    Renders a single image into unicode text.

    :param source_: The source image
    :param out_size: The size of the final text in the form of (columns, lines).
    :return:
    """

    PixelsPerChar=(2,4)

    FinalImageSize = (PixelsPerChar[0] * out_size[0], PixelsPerChar[1] * out_size[1])

    image = source_.resize(FinalImageSize)

    os.makedirs("./build",exist_ok=True)
    image.save("./build/resized.png")