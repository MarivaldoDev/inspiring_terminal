from typing import Annotated, Literal

import typer

from inspire_term.config import reset_config
from inspire_term.flow import run, version_callback
from inspire_term.ui import ConsoleRenderer

app = typer.Typer(
    help="Exibe frases inspiradoras no terminal.",
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
            help="Exibe a versão da aplicação.",
        ),
    ] = False,
    no_translate: bool = typer.Option(
        False,
        "--no-translate",
        help="Não traduz a frase para o português.",
    ),
    style: Literal["default", "simple"] = typer.Option(
        "default",
        "--style",
        help="Escolhe o estilo de exibição da frase.",
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
