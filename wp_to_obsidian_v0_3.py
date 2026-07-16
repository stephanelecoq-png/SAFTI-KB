#!/usr/bin/env python3
import csv
import re
import sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python wp_to_obsidian.py export.csv")
    sys.exit(1)

csv_file = Path(sys.argv[1])
vault = Path("SAFTI RIA ETEL KB")
articles_dir = vault / "articles"
articles_dir.mkdir(parents=True, exist_ok=True)

def slugify(text):
    text = text.lower()
    rep = {
        "é":"e","è":"e","ê":"e","à":"a","â":"a","î":"i","ï":"i",
        "ô":"o","ö":"o","ù":"u","û":"u","ç":"c","'":"","’":""
    }
    for a, b in rep.items():
        text = text.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", text).strip("-")

with open(csv_file, encoding="utf-8-sig", newline="") as f:
    rows = list(csv.DictReader(f))

fields = {k.lower(): k for k in rows[0].keys()}

def find(*names):
    for n in names:
        for k, v in fields.items():
            if n.lower() in k:
                return v
    return None

title_f = find("title", "titre")
content_f = find("content")
slug_f = find("slug")
status_f = find("status")
date_f = find("date")
cat_f = find("catégories", "categories")
tag_f = find("étiquettes", "tags")
id_f = find("id")
url_f = find("permalink")
excerpt_f = find("excerpt")
featured_f = find("image featured")
image_url_f = find("image url")
seo_title_f = find("_aioseo_title")
seo_desc_f = find("_aioseo_description")
author_first_f = find("author first name")
author_last_f = find("author last name")

index = ["# Index\n"]

for row in rows:
    title = row.get(title_f, "Sans titre")
    slug = row.get(slug_f) or slugify(title)
    content = row.get(content_f, "")
    status = row.get(status_f, "")
    date = row.get(date_f, "")[:10]
    pid = row.get(id_f, "")
    url = row.get(url_f, "")
    excerpt = row.get(excerpt_f, "")
    featured = row.get(featured_f, "")
    image_url = row.get(image_url_f, "")
    seo_title = row.get(seo_title_f, "")
    seo_desc = row.get(seo_desc_f, "")
    author = f"{row.get(author_first_f,'').strip()} {row.get(author_last_f,'').strip()}".strip()

    cats = row.get(cat_f, "")
    tags = row.get(tag_f, "")

    cat_list = [c.strip() for c in re.split(r"[;,|]", cats) if c.strip()]
    tag_list = [t.strip() for t in re.split(r"[;,|]", tags) if t.strip()]

    tag_links = [f"[[{t}]]" for t in tag_list]

    yaml = [
        "---",
        f'title: "{title}"',
        f"slug: {slug}",
        f"date: {date}",
        f"status: {status}",
        f'author: "{author}"',
        f"wordpress_id: {pid}",
        f'source: "{url}"',
        f'excerpt: "{excerpt}"',
        f"featured: {featured}",
        f'featured_image: "{image_url}"',
        f'seo_title: "{seo_title}"',
        f'seo_description: "{seo_desc}"',
        "categories:"
    ]

    for c in cat_list:
        yaml.append(f"  - {c}")

    yaml.append("tags:")
    for t in tag_list:
        yaml.append(f"  - {t}")

    yaml.append("---")

    md = "\n".join(yaml) + f"""

# {title}

{content}

---

## Concepts

{chr(10).join(tag_links)}

## Notes

"""

    (articles_dir / f"{slug}.md").write_text(md, encoding="utf-8")
    index.append(f"- [[{slug}]]")

(vault / "index.md").write_text("\n".join(index), encoding="utf-8")
print("Export terminé :", vault)
