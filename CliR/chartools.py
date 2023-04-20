import numpy as np
import numpy.typing as npt
from PIL import Image

PixelsPerChar = (2, 4)
PixelsPerCharCount = PixelsPerChar[0] * PixelsPerChar[1]

braille6= " ⠁⠂▘⠄⠅⠆⠇⠈▔⠊⠋⠌⠍⠎⠏⠐⠑⠒⠓⠔⠕⠖⠗▝⠙⠚▀⠜⠝⠞⠟⠠⠡⠢⠣⠤⠥⠦⠧⠨⠩⠪⠫⠬⠭⠮⠯⠰⠱⠲⠳⠴⠵⠶⠷⠸⠹⠺⠻⠼⠽⠾⠿"
braille8= "⡀⡁⡂⡃▖⡅⡆▌⡈⡉⡊⡋⡌⡍⡎⡏⡐⡑⡒⡓⡔⡕⡖⡗⡘⡙⡚⡛▞⡝⡞▛⡠⡡⡢⡣⡤⡥⡦⡧⡨⡩⡪⡫⡬⡭⡮⡯⡰⡱⡲⡳⡴⡵⡶⡷⡸⡹⡺⡻⡼⡽⡾⡿⢀⢁⢂⢃⢄⢅⢆⢇⢈⢉⢊⢋⢌⢍⢎⢏⢐⢑⢒" \
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


def split_to_char(image_: Image.Image) -> tuple[np.ndarray,Image.Image]:
    """
    Splits an image up into PixelsPerChar sized chunks.
    Results in shape (rows,cols,8) last axis where 8 is the pixels in the chunk flattened into a 1D array
    :param image_:
    :return: Returns the image chunks (rows,cols,8) and a mask of the image (rows,cols)
    """
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
                (y + 1) * PixelsPerChar[1],
            )
            xCoords = (
                x * PixelsPerChar[0],
                (x + 1) * PixelsPerChar[0],
            )
            cell = array[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]]

            min_ = int(np.amin(cell, axis=(0, 1)))
            max_ = int(np.amax(cell, axis=(0, 1)))

            mid = (max_ + min_) // 2
            # print(mid,cell[0,0],min_,max_)
            bw = (cell > mid)
            # print(yCoords,xCoords,list(bw))
            data[y, x] = bw.flatten('F')
            array[yCoords[0]:yCoords[1], xCoords[0]:xCoords[1]] = bw * 255

    im = Image.fromarray(array)
    im.save(f"./build/twotone.png")

    return data,im

