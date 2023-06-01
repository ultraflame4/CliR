import init
from pathlib import Path
import time
start_time = time.time()
from PIL import Image
from rich.console import Console

import CliRenderer


CliRenderer.Flags.DEBUG=False

# image = Image.open("./resources/pexels-photo-302769.jpeg")
print("test")
image2 = Image.open("../resources/pexels-pixabay-206359.jpg")
console = Console()


txt2 = CliRenderer.render(image2)

console.print(txt2)

print("--- %s seconds ---" % (time.time() - start_time))
