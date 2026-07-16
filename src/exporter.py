from pathlib import Path

from src.markdown import article_to_markdown
from src.parser import CSVParser
from src.utils import write_text


def exporter(csv_file: str):
    parser = CSVParser(csv_file)
    articles = parser.parse()

    if not articles:
        print("Aucun article trouvé.")
        return

    contenu = article_to_markdown(articles[0])

    write_text(
        Path("test.md"),
        contenu
    )

    print("Fichier test.md généré.")
    print(f"{len(articles)} article(s) chargé(s).")