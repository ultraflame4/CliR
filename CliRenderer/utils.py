import math
from pathlib import Path

import validators


class Flags:
    DEBUG = False
    KEEP_ASPECT = True

def is_url(url: str) -> bool:
    return validators.url(url)


def ppc_resize(width: int, height: int, aspect_ratio: float, ppc: tuple[int, int]) -> tuple[int, int]:
    """
    Automatically resizes (shrinks) the given width and height to fit the aspect ratio.
    Also takes into account Pixels Per Character
    Will attempt to give back the biggest size (assuming that the given width and height is the maximum area allowed)
    :param width: Width to resize
    :param height: Height to resize
    :param aspect_ratio: Aspect ratio to resize to (width / height)
    :return: A tuples
    """
    width_ = ppc[0] * width
    height_ = ppc[1] * height
    new_width = math.floor(height_ * aspect_ratio / ppc[0])
    new_height = math.floor(width_ / aspect_ratio / ppc[1])
    if new_height < height:
        return width, new_height
    return new_width, height

def parse_pathoruri(value: str):
    if is_url(value):
        return value
    p = Path(value)
    if not p.is_file():
        raise FileNotFoundError(f"Could not find file at {value}")
    return value