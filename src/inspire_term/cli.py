from typing import Annotated, Literal

import typer

from inspire_term.config import reset_config
from inspire_term.flow import run, version_callback
from inspire_term.ui import ConsoleRenderer

app = typer.Typer(
    help="Displays inspiring quotes in the terminal.",
    add_completion=False,
    context_settings={"help_option_names": ["--help", "-H"]},
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-V",
            callback=version_callback,
            is_eager=True,
            help="Displays the application version.",
        ),
    ] = False,
    no_translate: bool = typer.Option(
        False,
        "--no-translate",
        help="Do not translate the sentence.",
    ),
    style: Literal["default", "simple"] = typer.Option(
        "default",
        "--style",
        help="Choose the display style for the phrase.",
    ),
) -> None:
    if ctx.invoked_subcommand is None:
        run(no_translate=no_translate, style=style)


@app.command()
def reset() -> None:
    """Reset the current configuration."""
    console = ConsoleRenderer()
    choice_reset = console.screen_reset()

    if choice_reset:
        reset_config()
        typer.echo("Configuration reset successfully.")


if __name__ == "__main__":
    app()
