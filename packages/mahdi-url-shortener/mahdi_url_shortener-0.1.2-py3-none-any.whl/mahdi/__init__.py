"""
mahdi - A simple URL shortener package.

Provides functionality to shorten URLs via TinyURL and
a command-line interface (CLI) to use it interactively.

Version: 0.1.2
Author: oxl_mahdi
"""

from .cli import create_short_url, main

__version__ = "0.1.2"
__author__ = "oxl_mahdi"

__all__ = ["create_short_url", "main"]

def run_cli():
    """
    Run the CLI interface.

    Usage:
        from mahdi import run_cli
        run_cli()
    """
    main()


if __name__ == "__main__":
    # If someone runs `python -m mahdi` this will launch CLI directly
    run_cli()
