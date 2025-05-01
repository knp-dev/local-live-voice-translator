# Local Live Voice Translator

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

*Copyright © 2025*

## Description

A local Speech to Text to Speech translation app. The goal is to convert the user speech into the desired language and provide a generated voice output, almost in real time with minor delay.

This project is built using:
- FasterWhisper
- FastRTC (for voice detection and web interface)
- Kokoro (for text to voice generation)
- Ollama to call local LLMs (e.g: gemma:4b)

## Currently supported languages (Input / Output)

- Brazilian Portuguese
- Chinese
- English
- French
- Hindi
- Japanese
- Italian

## Requirements

- [uv](https://github.com/astral-sh/uv) a Python package manager
- [Ollama](https://ollama.ai/) to load models locally

## Install

Python version: `3.1.3`

### Init a python virtual environment
```
uv venv
```

### Switch into the virtual environment

Linux:
```
source .venv/bin/activate
```
Windows:
```
.venv/Scripts/activate.bat
```

Install dependencies using uv ("cu124" for NVIDIA GPUs or "cpu"):
```
uv sync --extra cu124
```

### Download the LLM model

```bash
ollama pull gemma3:4b
```

## Usage

#### Web UI (default behaviour: translate any input language to English)
```bash
python app.py
```
Use `-p` to specify a port if needed.

#### Translate any input language to specified output language
```bash
python app.py -lang es
```
Possible `-lang` arguments are: `[en|es|fr|hi|it|ja|ptbr|zh]`