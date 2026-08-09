<img width="300" height="230" alt="Image" src="https://github.com/user-attachments/assets/8d1fe9b1-d6f3-4091-bf27-07d304c62165" />

# Inspiring Terminal

[![PyPI version](https://img.shields.io/pypi/v/inspiring-terminal.svg)](https://pypi.org/project/inspiring-terminal/)
[![CI](https://github.com/MarivaldoDev/inspiring_terminal/actions/workflows/pipeline.yaml/badge.svg)](https://github.com/MarivaldoDev/inspiring_terminal/actions/workflows/pipeline.yaml)
[![Python](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

Inspiring terminal é um CLI que exibe frases inspiradoras de uma forma bonita no seu terminal.

As frases são obtidas através da [ZenQuotes API](https://docs.zenquotes.io/zenquotes-documentation/), armazenadas em cache e traduzidas automaticamente para português.

## 📦 Instalação

```bash
pip install inspiring-terminal
```

## Caso você utilize UV:

```bash
uv too install inspiring-terminal
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
git clone https://github.com/MarivaldoDev/inspiring_terminal
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

## 🤝 Contribuições

O **Inspiring Terminal** é um projeto aberto e contribuições são bem-vindas.

Se você tiver uma ideia de melhoria, encontrar um problema ou quiser contribuir com código, fique à vontade para abrir uma *issue* ou enviar um *pull request* no repositório.

### 💡 Possíveis melhorias

Algumas ideias para versões futuras:

- 🎨 Novas opções de personalização da interface do terminal;
- 🌍 Suporte a outros idiomas;
- 💾 Melhorias no sistema de cache;
- 🧪 Ampliação da cobertura de testes;
- 🔌 Suporte a outras APIs de frases;
- ⚙️ Novas opções e comandos para a CLI;
- 📝 Melhorias na documentação;
- 🐛 Correção de bugs e melhorias de desempenho.

### Como contribuir

1. Faça um *fork* do projeto;
2. Crie uma branch para sua alteração;
3. Implemente e teste a melhoria;
4. Faça um *commit* descrevendo a alteração;
5. Envie um *pull request*.

Toda contribuição é bem-vinda, seja uma nova funcionalidade, correção de bugs, melhoria na documentação ou simplesmente uma sugestão.
