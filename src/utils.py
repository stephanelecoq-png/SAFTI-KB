"""
Fonctions utilitaires.
"""

from pathlib import Path
import re


INVALID_FILENAME = r'[<>:"/\\\\|?*]'


def clean_filename(name: str) -> str:
    """
    Nettoie un nom de fichier.

    Compatible Windows / macOS / Linux.
    """

    name = re.sub(INVALID_FILENAME, "-", name)

    return name.strip()


def ensure_directory(path: Path):

    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str):

    path.write_text(content, encoding="utf-8")