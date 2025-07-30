# Github Tracker

A Python package for tracking Github trending.

## Features

- Track github trending repositories

## Installation

```bash
pip install Github-tracker
```

## Usage

```text

```

---

## Development

- install & test

```text
pip install -e .
python -m unittest discover tests
```

- build & upload to TestPyPI

```text
python -m build
twine upload --repository testpypi dist/*  -u__token__ -p <your_token>
```