from typing import Annotated

import typer

from inspire_term.flow import run, version_callback

app = typer.Typer(
    help="Exibe frases inspiradoras no terminal.",
    add_completion=False,
)


@app.command()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Exibe a versão da aplicação.",
        ),
    ] = False,
    no_translate: bool = typer.Option(
        False,
        "--no-translate",
        help="Não traduz a frase para o português.",
    )
) -> None:
    run(no_translate=no_translate)


if __name__ == "__main__":
    app()
