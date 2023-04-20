from PIL import Image
from rich.console import Console

import CliR

image = Image.open("./resources/pexels-photo-302769.jpeg")
image2 = Image.open("./resources/pexels-pixabay-206359.jpg")

console = Console()
txt = CliR.render(image,(170,60))
txt2 = CliR.render(image2,(170,60))
console.print(txt)
console.print(txt2)
