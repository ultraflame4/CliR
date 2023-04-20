from PIL import Image
from rich.console import Console

import CliRenderer

image = Image.open("./resources/pexels-photo-302769.jpeg")
image2 = Image.open("./resources/pexels-pixabay-206359.jpg")

console = Console()
txt = CliRenderer.render(image, (170, 60))
txt2 = CliRenderer.render(image2, (170, 60))
console.print(txt)
console.print(txt2)
