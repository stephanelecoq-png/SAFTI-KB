from src.parser import CSVParser


def exporter(csv_file: str):
    parser = CSVParser(csv_file)
    articles = parser.parse()

    print(f"{len(articles)} article(s) chargé(s).")