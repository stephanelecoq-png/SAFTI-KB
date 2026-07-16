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

    dossier_articles = Path("vault/articles")
    dossier_articles.mkdir(parents=True, exist_ok=True)

    for article in articles:
        contenu = article_to_markdown(article)

        fichier = dossier_articles / f"{article.slug}.md"

        write_text(fichier, contenu)

    print(f"{len(articles)} article(s) exporté(s).")