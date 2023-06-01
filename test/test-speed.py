import init
from pathlib import Path
import time

from PIL import Image
from rich.console import Console

import CliRenderer


CliRenderer.Flags.DEBUG=False
Test_Count = 20

image2 = Image.open("../resources/pexels-pixabay-206359.jpg")
console = Console()

timings = []

for i in range(Test_Count):
    start_time = time.time()
    txt2 = CliRenderer.render(image2)
    result = (time.time()-start_time)*1000
    print(f"Test {i}: {result} ms")
    timings.append(result)

print(f"Average timings: {sum(timings)/len(timings)} ms")
print(f"Biggest: {max(timings)} ms")
print(f"Smallest: {min(timings)} ms")


