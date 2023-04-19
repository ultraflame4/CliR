from PIL import Image

import CliR

image = Image.open("./resources/pexels-photo-302769.jpeg")

CliR.render(image,(100,50))