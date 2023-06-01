import numpy as np
import numpy.typing as npt
from PIL import Image
import numba as nb
from CliRenderer.core import Flags

PixelsPerChar = (2, 4)
PixelsPerCharCount = PixelsPerChar[0] * PixelsPerChar[1]

braille6 = " ⠁⠂▘⠄⠅⠆⠇⠈▔⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗▝⠙⠚▀⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"
braille8 = "⡀⡁⡂⡃▖⡅⡆▌⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛▞⡝⡞▛⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒" \
           "⢓⢔⢕⢖⢗⢘⢙⢚⢛⢜⢝⢞⢟▗⢡⢢▚⢤⢥⢦⢧⢨⢩⢪⢫⢬⢭⢮⢯⢰⢱⢲⢳⢴⢵⢶⢷▐⢹⢺▜⢼⢽⢾⢿▂⣁⣂⣃⣄⣅⣆⣇⣈⣉⣊⣋⣌⣍⣎⣏⣐⣑⣒⣓⣔⣕⣖⣗⣘⣙⣚⣛⣜⣝⣞⣟⣠⣡⣢⣣▃⣥" \
           "⣦▙⣨⣩⣪⣫⣬⣭⣮⣯⣰⣱⣲⣳⣴⣵▅⣷⣸⣹⣺⣻▟⣽⣾█"
braille = braille6 + braille8


def pixels2Char(pixels: npt.NDArray):
    if len(pixels.shape) > 1 or len(pixels) != 8:
        raise Exception("Error, pixels provided must be in a 1D array of length 8!")

    # pixels = [1,1,1,1,1,1,1,1]
    converted = [pixels[7], pixels[3], pixels[6], pixels[5], pixels[4], pixels[2], pixels[1], pixels[0]]

    index = int("0b" + "".join("1" if x else "0" for x in converted), 2)

    return braille[index]

def generateColoredChars(image_: Image.Image) -> tuple[np.ndarray, np.ndarray]:
    """
    Splits an image up into PixelsPerChar sized chunks.
    Results in shape (rows,cols,8) last axis where 8 is the pixels in the chunk flattened into a 1D array
    :param image_:
    :return: Returns the image chunks (rows,cols,8) and a colors to use (rows,cols, (fore color, back color))
    """
    grayscale: npt.NDArray = np.asarray(image_.convert("L")).copy()
    sample: npt.NDArray = np.asarray(image_.convert("RGBA")).copy()

    rows = grayscale.shape[0] // PixelsPerChar[1]
    cols = grayscale.shape[1] // PixelsPerChar[0]
    # print(array.flags)
    if len(grayscale.shape) != 2:
        raise Exception("Error, image array is not grayscale!")

    data = np.zeros((rows, cols, PixelsPerCharCount), dtype=bool)
    colors = np.zeros((rows, cols, 2, sample.shape[2]), dtype=np.uint8)
    # print(sample.shape)
    # print(grayscale.shape)
    for y in range(rows):
        for x in range(cols):
            yCoords = (
                y * PixelsPerChar[1],
                (y + 1) * PixelsPerChar[1],
            )
            xCoords = (
                x * PixelsPerChar[0],
                (x + 1) * PixelsPerChar[0],
            )
            cell = grayscale[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]]

            min_index = int(np.argmin(cell))
            unraveled_min = np.unravel_index(min_index, PixelsPerChar[::-1])
            max_index = int(np.argmax(cell))
            unraveled_max = np.unravel_index(max_index, PixelsPerChar[::-1])
            # print(cell.shape)

            min_ = int(
                cell[unraveled_min[0], unraveled_min[1]])  # convert to python int to stop runtime overflow warnings
            max_ = int(cell[unraveled_max[0], unraveled_max[1]])

            mid = (min_ + max_) // 2
            bw = (cell > mid)

            data[y, x] = bw.flatten('F')

            colored_cell = sample[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]]

            colors[y, x, 0] = colored_cell[unraveled_max[0],unraveled_max[1]]
            colors[y, x, 1] = colored_cell[unraveled_min[0],unraveled_min[1]]

    if Flags.DEBUG:
        Image.fromarray(grayscale).save(f"./build/twotone.png")
        Image.fromarray(sample).save(f"./build/char-color.png")

    return data, colors
