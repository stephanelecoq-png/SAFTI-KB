# SAFTI KB

SAFTI KB est un générateur de base de connaissances Obsidian à partir d'un export WordPress (WP All Export).

## Objectifs

- Transformer un export WordPress en coffre Obsidian
- Générer automatiquement les notes Markdown
- Préserver les métadonnées WordPress
- Générer les concepts, catégories et index
- Servir de base à une véritable base de connaissances immobilière

---

## État du projet

Version actuelle : **0.1.0**

### Roadmap

- [x] Initialisation du projet
- [ ] Lecture du CSV
- [ ] Génération des articles
- [ ] Concepts
- [ ] Catégories
- [ ] Dashboard
- [ ] Maillage automatique
- [ ] Synchronisation incrémentale

---

## Structure

```
SAFTI-KB/

src/
templates/
docs/
tests/
```

---

## Utilisation

```bash
python src/main.py export.csv
```

---

## Auteur

Stéphane LECOQ

Projet développé avec ChatGPT.