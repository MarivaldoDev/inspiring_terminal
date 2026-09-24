import json
from pathlib import Path
from time import sleep

from inspire_term.ui import ConsoleRenderer

CONFIG_DIR = Path.home() / ".cache" / "inspiring-terminal"
CONFIG_FILE = CONFIG_DIR / "config.json"


def first_run() -> dict[str, str]:
    console = ConsoleRenderer()
    console.welcome()

    data = {
        "language": console.show_config(),
    }

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with CONFIG_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=4,
        )

    console.console.print("Configuration saved successfully!\n")
    sleep(2)
    console.console.clear()

    return data


def load_config() -> dict[str, str]:
    if not CONFIG_FILE.exists():
        return first_run()

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def reset_config() -> None:
    console = ConsoleRenderer()

    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
    else:
        console.error(
            "The configuration cannot be reset if there is no (configuration)."
        )
