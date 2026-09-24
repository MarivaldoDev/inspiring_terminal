<img width="300" height="230" alt="Image" src="https://github.com/user-attachments/assets/31ccc3ca-f062-484b-b9c4-9a967ab0597e"/>

# Inspiring Terminal

[![PyPI version](https://img.shields.io/pypi/v/inspiring-terminal.svg)](https://pypi.org/project/inspiring-terminal/)
[![CI](https://github.com/MarivaldoDev/inspiring_terminal/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/MarivaldoDev/inspiring_terminal/actions/workflows/pipeline.yaml)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Inspiring Terminal is a CLI that displays inspiring quotes in a beautiful way in your terminal.

The sentences are obtained through [ZenQuotes API](https://docs.zenquotes.io/zenquotes-documentation/), cached and automatically translated into Portuguese.

## 📦 Installation

```bash
pip install inspiring-terminal
```

## If you use UV:

```bash
uv too install inspiring-terminal
```

After installation, the `inspire` command will be available in the terminal.

## How do I use it?

To display a phrase:

```bash
inspire
```

Example:

```text
╭──────────────────────────────── 💡 Inspiring Terminal ─────────────────────────────────╮                        
│                                                                                        │                        
│    The less you respond to negative people, the more positive your life will become.   │                        
│                                                                                        │                        
│                                     — Paulo Coelho                                     │                        
│                                                                                        │                        
╰────────────────────────────────────────────────────────────────────────────────────────╯                        
```

### Show the original phrase

By default, phrases are translated into Portuguese.

To display the phrase in the original language:

```bash
inspire --no-translate
```

## Display styles

Inspiring Terminal allows you to choose how the phrase is displayed in the terminal.

### Standard style

```bash
inspire
```
Displays the phrase using the application's default style.

### Simple style

```bash
inspire --style simple
```
Displays the phrase more simply, without the frame used in the standard style.

You can also combine the style with other options:

```bash
inspire --style simple --no-translate
```

The translation of the sentences relies on an external service and may occasionally fail or produce a translation that is not entirely clear.


### View version

```bash
inspire --version
```

### View all options

```bash
inspire --help
```

## 💾 Cache

Inspiring Terminal stores a set of quotes locally to avoid making an API request upon every execution.

A new set of quotes is fetched when the day's cache is unavailable.

The quotes are used individually throughout the day until the set is exhausted.

## 🛠️ Development

Clone the repository:

```bash
git clone https://github.com/MarivaldoDev/inspiring_terminal
cd inspiring-terminal
```

Install the dependencies:

```bash
uv sync
```

Run the application:

```bash
uv run inspire
```

Run the tests:

```bash
uv run pytest
```

Check the code:

```bash
uv run ruff check .
```

## 📄 License

This project is available under the license defined in the file `LICENSE`.

## 🔗 Links
- **ZenQuotes API:** https://docs.zenquotes.io/zenquotes-documentation/

## 🤝 Contributions

**Inspiring Terminal** is an open project, and contributions are welcome.

If you have an idea for improvement, find a problem, or want to contribute code, feel free to open a support ticket *issue* or send a *pull request* in the repository.

### 💡 Possible improvements

Some ideas for future versions:

- 🎨 New terminal interface customization options;
- 🌍 Support for additional languages;
- 💾 Cache system improvements;
- 🧪 Expanded test coverage;
- 🔌 Support for additional quote APIs;
- ⚙️ New CLI options and commands;
- 📝 ​​Documentation improvements;
- 🐛 Bug fixes and performance improvements.

### How to contribute

1. *Fork* the project;
2. Create a *branch* for your change;
3. Implement and *test* the improvement;
4. *Commit* the change with a description;
5. Submit a *pull request*.

All contributions are welcome, whether it's a new feature, a bug fix, an improvement to the documentation, or simply a suggestion.
