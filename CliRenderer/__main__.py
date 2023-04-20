import json
import sys
from pathlib import Path

import typer as typer
from PIL import Image
from rich.console import Console
import imageio as iio
from rich.progress import track
from io import StringIO
from CliRenderer import render, Flags


def cli_main(source: Path = typer.Argument(..., help="The path to source image."),
             width: int = typer.Option(150, "--width", "-w", min=1,
                                       help="The width of the output in no. of characters."),
             height: int = typer.Option(50, "--height", "-h", min=1, help="The height of the output in no. of lines"),
             autosize: bool = typer.Option(False,
                                           help="Automatically sets the output size to fit the terminal. Overrides --width and --height. Only works on supported terminals."),
             video: bool = typer.Option(False, "--video", "-v", help="Set this flag if source is a video."),
             output: Path = typer.Option(None, "--out", "-o",
                                         help="Saves the output to a file. Compulsory if --video is set."),
             playback: bool = typer.Option(False, "--playback", "-p",help="Set this flag to playback the source if it is an output (--out) from this program."),
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

    if video:

        if output is None:
            typer.echo("--out must be set if source is a video.")
            raise typer.Exit(code=1)

        texts = []
        metadata = iio.v3.immeta(source, plugin="pyav")

        total_frames = metadata["duration"] * metadata["fps"] + 10
        typer.echo("Total estimated frames count: "+str(total_frames))
        for frame in track(iio.imiter(source, plugin="pyav"), description="Processing...",total=total_frames):
            source_image = Image.fromarray(frame)
            text = render(source_image, (width, height), bg_intensity)
            console.print(text)
            texts.append(console.export_text(styles=True))


        output.parent.mkdir(parents=True, exist_ok=True)
        typer.echo(f"Saving to {output}...")
        with open(output, "w") as f:
            json.dump({"meta":{
                "fps":metadata["fps"],
            },"frames":texts}, f)

        return

    source_image = Image.fromarray(iio.v3.imread(source))
    text = render(source_image, (width, height), bg_intensity)

    console.print(text)
    string = console.export_text(styles=True)
    print(string)


def main():
    typer.run(cli_main)


if __name__ == "__main__":
    main()
