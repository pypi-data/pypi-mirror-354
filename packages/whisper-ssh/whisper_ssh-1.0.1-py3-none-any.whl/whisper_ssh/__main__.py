"""
Main entry point for the whisper-ssh package.

This allows the package to be run as a module:
    python -m whisper_ssh
"""

from .cli import main

if __name__ == "__main__":
    main()