# Inspiring Terminal

[![CI](https://github.com/MarivaldoDev/inspiring_terminal/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/MarivaldoDev/inspiring_terminal/actions/workflows/pipeline.yaml)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Inspiring terminal é um CLI que exibe frases inspiradoras de uma forma bonita no seu terminal.

As frases são obtidas através da [ZenQuotes API](https://docs.zenquotes.io/zenquotes-documentation/), armazenadas em cache e traduzidas automaticamente para português.

## 📦 Instalação

```bash
pip install inspiring-terminal
```

Após a instalação, o comando `inspire` estará disponível no terminal.

## Como usar?

Para exibir uma frase:

```bash
inspire
```

Exemplo:

```text
            ╭──────────────────────────────── 💡 Inspiring Terminal ─────────────────────────────────╮                        
            │                                                                                        │                        
            │  Quanto menos você responder às pessoas negativas, mais positiva sua vida se tornará.  │                        
            │                                                                                        │                        
            │                                     — Paulo Coelho                                     │                        
            │                                                                                        │                        
            ╰────────────────────────────────────────────────────────────────────────────────────────╯                        
```

### Exibir a frase original

Por padrão, as frases são traduzidas para português.

Para exibir a frase no idioma original:

```bash
inspire --no-translate
```

### Ver a versão

```bash
inspire --version
```

### Ver todas as opções

```bash
inspire --help
```

## 💾 Cache

O Inspiring Terminal armazena localmente um conjunto de frases para evitar uma requisição à API a cada execução.

Um novo conjunto de frases é obtido quando o cache do dia não está disponível.

As frases são utilizadas individualmente ao longo do dia até que o conjunto seja esgotado.

## 🛠️ Desenvolvimento

Clone o repositório:

```bash
git clone <REPOSITORY_URL>
cd inspiring-terminal
```

Instale as dependências:

```bash
uv sync
```

Execute a aplicação:

```bash
uv run inspire
```

Execute os testes:

```bash
uv run pytest
```

Verifique o código:

```bash
uv run ruff check .
```

## 📄 Licença

Este projeto está disponível sob a licença definida no arquivo `LICENSE`.

## 🔗 Links
- **ZenQuotes API:** https://docs.zenquotes.io/zenquotes-documentation/
