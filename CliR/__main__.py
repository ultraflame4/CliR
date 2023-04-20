from pathlib import Path

import typer as typer


def main(source: Path,
         width: int = typer.Option(150, "--width", "-w", min=1, help="The width of the output in no. of characters."),
         height: int = typer.Option(50, "--height", "-h", min=1, help="The height of the output in no. of lines"),
         autosize: bool = typer.Option(False, help="Automatically sets the output size to fit the terminal. Overrides --width and --height. Only works on supported terminals."),
         debug: bool = typer.Option(False, help="Enables debug mode. This will save the intermediate images to the build folder."),
         bg_intensity: float = typer.Option(1.0,"--bg-intensity","-bgi", min=0.0, max=1.0, help="The intensity of the background. The closer to 0 the darker the background.")
         ):
    pass


if __name__ == "__main__":
    typer.run(main)
