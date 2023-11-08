# import init
import statistics
from pathlib import Path
import time

from PIL import Image
from rich.console import Console

import CliRenderer


CliRenderer.Flags.DEBUG=False
Test_Count = 20

image = Image.open("./resources/pexels-pixabay-206359.jpg")
image2 = Image.open("./resources/pexels-photo-302769.jpeg")
console = Console()

timings = []

TEST_KWARGS = {
    "out_size": (170, 50),
    "bg_intensity": 1
}

print("Starting speed test with KWARGS", TEST_KWARGS)

for i in range(Test_Count):
    start_time = time.time()
    txt = CliRenderer.render(image, **TEST_KWARGS)
    resultA = (time.time()-start_time)*1000
    print(f"Test {i} A: {resultA} ms")

    start_time = time.time()
    txt2 = CliRenderer.render(image2, **TEST_KWARGS)
    resultB = (time.time() - start_time) * 1000
    print(f"Test {i} B: {resultB} ms")

    timings.append(resultA)
    timings.append(resultB)

print("--------------------\nTest KWARGS", TEST_KWARGS)
print("--Test timings--")
print(f"Avg: {sum(timings)/len(timings)} ms")
print(f"Med: {statistics.median(timings)} ms")
print(f"Max: {max(timings)} ms")
print(f"Min: {min(timings)} ms")


