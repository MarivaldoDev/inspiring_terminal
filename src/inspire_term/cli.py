from typing import Annotated

import typer

from inspire_term.flow import run, version_callback

app = typer.Typer()


@app.command()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the application version.",
        ),
    ] = False,
    no_translate: bool = False,
) -> None:
    run(no_translate=no_translate)


if __name__ == "__main__":
    app()
