"""
Parser des exports WordPress (WP All Export).
"""

from __future__ import annotations

import csv
from pathlib import Path

from src.models import Article


class CSVParser:
    """
    Lit un export CSV WordPress et retourne une liste d'Article.
    """

    def __init__(self, csv_file: str | Path):

        self.csv_file = Path(csv_file)

    def parse(self) -> list[Article]:

        articles = []

        with self.csv_file.open(
            encoding="utf-8-sig",
            newline=""
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                article = Article()

                article.id = self._get(row, "id")

                article.title = self._get(row, "title")

                article.slug = self._get(row, "slug")

                article.status = self._get(row, "status")

                article.date = self._get(row, "date")

                article.content = self._get(row, "content")

                article.categories = self._split(
                    self._get(row, "categories")
                )

                article.tags = self._split(
                    self._get(row, "tags")
                )

                articles.append(article)

        return articles

    @staticmethod
    def _get(row: dict, keyword: str) -> str:
        """
        Recherche une colonne contenant keyword.
        """

        keyword = keyword.lower()

        for key, value in row.items():

            if keyword in key.lower():

                return value.strip()

        return ""

    @staticmethod
    def _split(value: str) -> list[str]:

        if not value:

            return []

        return [
            x.strip()
            for x in value.replace("|", ",").split(",")
            if x.strip()
        ]