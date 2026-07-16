from src.models import Article


def article_to_markdown(article: Article) -> str:
    return f"""# {article.title}

{article.content}
"""