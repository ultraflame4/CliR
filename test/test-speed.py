import init
from pathlib import Path
import time

from PIL import Image
from rich.console import Console

import CliRenderer


CliRenderer.Flags.DEBUG=False
Test_Count = 20

image = Image.open("../resources/pexels-pixabay-206359.jpg")
image2 = Image.open("../resources/pexels-photo-302769.jpeg")
console = Console()

timings = []

for i in range(Test_Count):
    start_time = time.time()
    txt = CliRenderer.render(image)
    resultA = (time.time()-start_time)*1000
    print(f"Test {i} A: {resultA} ms")

    start_time = time.time()
    txt2 = CliRenderer.render(image2)
    resultB = (time.time() - start_time) * 1000
    print(f"Test {i} B: {resultB} ms")

    timings.append(resultA)
    timings.append(resultB)

print(f"Average timings: {sum(timings)/len(timings)} ms")
print(f"Biggest: {max(timings)} ms")
print(f"Smallest: {min(timings)} ms")


