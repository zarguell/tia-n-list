# Tia Storyline

Story-centric cybersecurity news aggregator — design preview (M0).

Stories are first-class entities with timelines: original reporting → updates from
multiple sources. Hot-scored, custom static site generator (no Hugo), three RSS feeds
(daily digest / hot stories / every article).

**Note:** the current data in `engine/data/` is fictional demo content for design
inspection. Live ingestion (Miniflux + Reddit RSS → real stories) is the M1 milestone.

## Structure

- `engine/ssg.py` — static site generator (logic only; all markup in `engine/templates/`)
- `engine/templates/` — Jinja2 templates + design system (`style.css`, light default,
  dark toggle)
- `engine/data/events/<id>.md` + `<id>.json` — hybrid store: markdown content + JSON metadata
- `engine/data/stories/<id>.json` — story metadata + ordered event refs

## Regenerate

```bash
uv venv ~/.local/venvs/tia-engine && uv pip install jinja2 markdown   # once
~/.local/venvs/tia-engine/bin/python engine/ssg.py
```

Generated site lands at the repo root (GitHub Pages serves `/`).
