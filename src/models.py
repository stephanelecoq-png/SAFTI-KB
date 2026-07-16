from dataclasses import dataclass, field


@dataclass
class Article:
    """
    Représente un article WordPress.
    """

    id: int = 0

    title: str = ""

    slug: str = ""

    status: str = ""

    date: str = ""

    categories: list[str] = field(default_factory=list)

    tags: list[str] = field(default_factory=list)

    content: str = ""

    excerpt: str = ""

    seo_title: str = ""

    meta_description: str = ""

    featured_image: str = ""

    author: str = ""

    permalink: str = ""

    def __str__(self):

        return self.title