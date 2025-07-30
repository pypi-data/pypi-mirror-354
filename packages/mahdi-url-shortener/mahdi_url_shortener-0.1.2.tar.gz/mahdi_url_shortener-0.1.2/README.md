# mahdi-url-shortener

[![PyPI version](https://badge.fury.io/py/mahdi-url-shortener.svg)](https://pypi.org/project/mahdi-url-shortener/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`mahdi-url-shortener` is a simple and lightweight Python package to shorten URLs using TinyURL service.  
It provides both a programmatic API and a command-line interface (CLI) for convenience.

---

## Features

- Shorten a single URL with a simple function call  
- Batch shorten URLs from one or multiple files  
- User-friendly CLI with interactive menu  
- Supports Python 3.7 and above

---

## Installation

You can install the package from PyPI:

```bash
pip install mahdi-url-shortener

```Use the CLI Run the CLI directly from the terminal
mahdi

Usage
Import and shorten URLs programmatically

from mahdi import create_short_url

long_url = "https://example.com/some/very/long/url"
short_url = create_short_url(long_url)
print(f"Shortened URL: {short_url}")

