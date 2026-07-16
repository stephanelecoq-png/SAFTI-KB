from src.parser import CSVParser


def main():
    parser = CSVParser("Articles-Export.csv")
    articles = parser.parse()

    print(f"{len(articles)} article(s) chargé(s).")


if __name__ == "__main__":
    main()