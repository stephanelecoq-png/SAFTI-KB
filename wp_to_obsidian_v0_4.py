#!/usr/bin/env python3
import csv
import re
import sys
from pathlib import Path

try:
    from markdownify import markdownify as md
except ImportError:
    print("Installez markdownify : pip install markdownify")
    sys.exit(1)

if len(sys.argv) < 2:
    print("Usage: python wp_to_obsidian.py export.csv")
    sys.exit(1)

csv_file = Path(sys.argv[1])
vault = Path("SAFTI RIA ETEL KB")
articles_dir = vault / "articles"
articles_dir.mkdir(parents=True, exist_ok=True)

def slugify(text):
    text = text.lower()
    rep = {"é":"e","è":"e","ê":"e","à":"a","â":"a","î":"i","ï":"i","ô":"o","ö":"o","ù":"u","û":"u","ç":"c","'":"","’":""}
    for a,b in rep.items():
        text=text.replace(a,b)
    return re.sub(r"[^a-z0-9]+","-",text).strip("-")

def clean_html(html):
    if not html:
        return ""

    # Supprime les commentaires Gutenberg
    html = re.sub(r"<!--\s*/?wp:.*?-->", "", html, flags=re.DOTALL)

    # Conversion HTML -> Markdown
    text = md(html, heading_style="ATX")

    # Nettoyage
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

with open(csv_file, encoding="utf-8-sig", newline="") as f:
    rows=list(csv.DictReader(f))

fields={k.lower():k for k in rows[0].keys()}

def find(*names):
    for n in names:
        if n.lower() in fields:
            return fields[n.lower()]
    for n in names:
        for k,v in fields.items():
            if n.lower() in k:
                return v
    return None

title_f=find("title")
content_f=find("content")
slug_f=find("slug")
status_f=find("status")
created_f=find("date")
modified_f=find("post modified date")
cat_f=find("catégories","categories")
tag_f=find("étiquettes","tags")
id_f=find("id")
url_f=find("permalink")
excerpt_f=find("excerpt")
image_f=find("image url")
seo_title_f=find("_aioseo_title")
seo_desc_f=find("_aioseo_description")
author_first_f=find("author first name")
author_last_f=find("author last name")

index=["# Index\n"]

for row in rows:
    title=row.get(title_f,"Sans titre")
    slug=row.get(slug_f,"").strip() or slugify(title)

    content=clean_html(row.get(content_f,""))

    created=row.get(created_f,"")[:10]
    modified=row.get(modified_f,"")[:10]
    status=row.get(status_f,"")
    pid=row.get(id_f,"")
    url=row.get(url_f,"")
    excerpt=row.get(excerpt_f,"").replace('"','\\"')
    image=row.get(image_f,"")
    seo_title=row.get(seo_title_f,"").replace('"','\\"')
    seo_desc=row.get(seo_desc_f,"").replace('"','\\"')
    author=f"{row.get(author_first_f,'').strip()} {row.get(author_last_f,'').strip()}".strip()

    cats=[c.strip() for c in re.split(r"[;,|]",row.get(cat_f,"")) if c.strip()]
    tags=[t.strip() for t in re.split(r"[;,|]",row.get(tag_f,"")) if t.strip()]

    yaml=[
        "---",
        f'title: "{title}"',
        f"slug: {slug}",
        "type: article",
        f"created: {created}",
        f"modified: {modified}",
        f"status: {status}",
        f'author: "{author}"',
        f"wordpress_id: {pid}",
        f'source: "{url}"',
        f'excerpt: "{excerpt}"',
        f'featured_image: "{image}"',
        f'seo_title: "{seo_title}"',
        f'seo_description: "{seo_desc}"',
        "categories:"
    ]
    yaml.extend(f"  - {c}" for c in cats)
    yaml.append("tags:")
    yaml.extend(f"  - {t}" for t in tags)
    yaml.append("---")

    concepts="\n".join(f"[[{t}]]" for t in tags)

    mdfile="\n".join(yaml)+f"""

# {title}

{content}

---

## Concepts

{concepts}

## Notes

"""
    (articles_dir/f"{slug}.md").write_text(mdfile,encoding="utf-8")
    index.append(f"- [[{slug}]]")

(vault/"index.md").write_text("\n".join(index),encoding="utf-8")
print("Export terminé :",vault)
