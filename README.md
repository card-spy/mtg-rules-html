<p align="center">
  <h1 align="center">MTG Rules in HTML</h1>
  <p align="center">Magic: The Gathering's Comprehensive Rules presented in HTML</p>
</p>

This repository hosts a Python script that generates an HTML page for Magic: The Gathering's Comprehensive Rules. You can find the rules on Wizard of the Coast's official page: https://magic.wizards.com/en/rules

## Usage

### Requirements

- Python 3.8+
- Pip

### Install & Run

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Linting

_This assumes you're in a venv and have the dependencies installed_

```
yapf -i main.py
```
