from pathlib import Path

import typer as typer
from PIL import Image
from rich.console import Console
import imageio as iio
from io import StringIO
from CliRenderer import render, Flags


def cli_main(source: Path = typer.Argument(..., help="The path to source image."),
             width: int = typer.Option(150, "--width", "-w", min=1,
                                       help="The width of the output in no. of characters."),
             height: int = typer.Option(50, "--height", "-h", min=1, help="The height of the output in no. of lines"),
             autosize: bool = typer.Option(False,
                                           help="Automatically sets the output size to fit the terminal. Overrides --width and --height. Only works on supported terminals."),

             output: Path = typer.Option(None, "--out", "-o",
                                         help="Saves the output to a file. (Written as bytes)"),
             debug: bool = typer.Option(False,
                                        help="Enables debug mode. This will save the intermediate images to the build folder."),
             bg_intensity: float = typer.Option(1.0, "--bg-intensity", "-bgi", min=0.0, max=1.0,
                                                help="The intensity of the background. The closer to 0 the darker the background.")
             ):
    """
    Renders the source image into the console as unicode art.
    """

    Flags.DEBUG = debug
    console = Console(file=StringIO(), record=True)

    if autosize:
        import shutil
        width, height = shutil.get_terminal_size()



    source_image = Image.fromarray(iio.v3.imread(source))
    text = render(source_image, (width, height), bg_intensity)

    console.print(text)
    string = console.export_text(styles=True)


    if output is not None:
        typer.echo(f"Saving output to {output}...")
        output.parent.mkdir(parents=True, exist_ok=True)
        with open(output, "wb") as f:
            f.write(string.encode("utf-8"))

    print(string)
    print(f"Saved output to {output}... Read it using `cat {output}`")
def main():
    typer.run(cli_main)


if __name__ == "__main__":
    main()
