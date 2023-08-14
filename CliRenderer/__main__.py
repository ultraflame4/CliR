import importlib.metadata
import time
from pathlib import Path

import rich
import typer as typer
from PIL import Image
from rich.console import Console
import imageio as iio
from io import StringIO
from CliRenderer import render, Flags
from CliRenderer.utils import parse_pathoruri

isDev = False


def cli_main(source: str = typer.Argument(..., help="The path to source image.", parser = parse_pathoruri),
# def cli_main(source: Path = typer.Argument(..., help="The path to source image."),
             width: int = typer.Option(150, "--width", "-w", min=1,
                                       help="The width of the output in no. of characters."),
             height: int = typer.Option(50, "--height", "-h", min=1, help="The height of the output in no. of lines"),
             autosize: bool = typer.Option(False,
                                           help="Automatically sets the output size to fit the terminal. Overrides --width and --height. Only works on supported terminals."),

             output: Path = typer.Option(None, "--out", "-o",
                                         help="Saves the output to a file. (Written as bytes)"),
             debug: bool = typer.Option(False,
                                        help="Enables debug mode. This will save the intermediate images to the build folder."),
             keep_aspect: bool = typer.Option(True, help="Keeps aspect ratio when resizing images."),
             bg_intensity: float = typer.Option(1.0, "--bg-intensity", "-bgi", min=0.0, max=1.0,
                                                help="The intensity of the background. The closer to 0 the darker the background.")
             ):
    """
    Renders the source image into the console as unicode art.
    """
    start_time = time.time()
    Flags.DEBUG = debug
    Flags.KEEP_ASPECT = keep_aspect
    console = Console(file=StringIO(), record=True)

    if autosize:
        import shutil
        width, height = shutil.get_terminal_size()

    source_image = Image.fromarray(iio.v3.imread(source))
    result = render(source_image, (width, height), bg_intensity)

    console.print(result.data)
    string = console.export_text(styles=True)
    print(string)
    print(f"Final image resolution: Character Size ({result.char_size}) Image Size ({result.im_size})")
    if output is not None:
        typer.echo(f"Saving output to {output}...")
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "wb") as f:
            f.write(string.encode("utf-8"))
        print(f"Saved output to {output}... Read it using `cat {output}`")

    print(f"Finished in {time.time() - start_time} seconds")


def main():
    rich.print(f"[bold white]CliRenderer installed version: {importlib.metadata.version('CliRenderer')}.[/bold white] {'dev mode on' if isDev else ''}")
    rich.print("[grey37]Version shown may not be accurate! (especially you are running from source!)[/grey37]\n")
    typer.run(cli_main)


if __name__ == "__main__":
    main()
