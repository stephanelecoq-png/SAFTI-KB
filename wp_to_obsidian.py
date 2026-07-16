
#!/usr/bin/env python3
import csv, os, re, sys
from pathlib import Path

if len(sys.argv) < 2:
    print("Usage: python wp_to_obsidian.py export.csv")
    sys.exit(1)

csv_file = Path(sys.argv[1])
vault = Path("SAFTI RIA ETEL KB")
articles_dir = vault / "articles"
articles_dir.mkdir(parents=True, exist_ok=True)

def slugify(text):
    text=text.lower()
    rep={"é":"e","è":"e","ê":"e","à":"a","â":"a","î":"i","ï":"i","ô":"o","ö":"o","ù":"u","û":"u","ç":"c","'":"","’":""}
    for a,b in rep.items():
        text=text.replace(a,b)
    return re.sub(r'[^a-z0-9]+','-',text).strip('-')

with open(csv_file, encoding="utf-8-sig", newline="") as f:
    rows=list(csv.DictReader(f))

fields={k.lower():k for k in rows[0].keys()}

def find(*names):
    for n in names:
        for k,v in fields.items():
            if n in k:
                return v
    return None

title_f=find("title","titre")
content_f=find("content")
slug_f=find("slug","post_name")
status_f=find("status")
date_f=find("date")
cat_f=find("categor")
tag_f=find("tag")
id_f=find("id")

index=["# Index\n"]

for row in rows:
    title=row.get(title_f,"Sans titre")
    slug=row.get(slug_f) or slugify(title)
    content=row.get(content_f,"")
    status=row.get(status_f,"")
    date=row.get(date_f,"")
    pid=row.get(id_f,"")
    cats=row.get(cat_f,"")
    tags=row.get(tag_f,"")

    tag_links=[]
    if tags:
        for t in re.split(r"[;,|]",tags):
            t=t.strip()
            if t:
                tag_links.append(f"[[{t}]]")

    md=f"""---
id: {pid}
title: "{title}"
slug: {slug}
status: {status}
date: {date}
categories: {cats}
tags: {tags}
---

# {title}

{content}

---

## Concepts

{chr(10).join(tag_links)}

## Notes

"""
    (articles_dir/f"{slug}.md").write_text(md,encoding="utf-8")
    index.append(f"- [[{slug}]]")

(vault/"index.md").write_text("\n".join(index),encoding="utf-8")
print("Export terminé :", vault)
