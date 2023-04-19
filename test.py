from PIL import Image

import CliR

image = Image.open("./resources/pexels-photo-302769.jpeg")
image2 = Image.open("./resources/pexels-pixabay-206359.jpg")

CliR.render(image,(100,40))
CliR.render(image2,(170,60))