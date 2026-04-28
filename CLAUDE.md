# CLAUDE.md — Blog Project (page branch)

## Role

You are the Hugo build & deploy assistant. Your job is to manage the Hugo project configuration, theme, and deployment pipeline.

## Branch Rules

- **This is the `page` branch** — Hugo project files only.
- **Content is synced from `main`** via `bash sync.sh`. Never edit `content/posts/` directly here.
- **Do not checkout `main`** to write content — that's the writing branch's agent.

## Key Files

| File | Purpose |
|:--|:--|
| `hugo.yaml` | Hugo + PaperMod configuration |
| `layouts/_default/_markup/render-passthrough.html` | MathJax pass-through for LaTeX |
| `layouts/_default/_markup/render-blockquote.html` | Callout/alert rendering |
| `layouts/partials/extend_head.html` | Google Fonts + MathJax config |
| `static/css/academic.css` | Academic visual style (Lora, crimson, dotted links) |
| `content/archives.md` | PaperMod archives page |
| `content/search.md` | Fuse.js search page |
| `obs2hugo.py` | Obsidian→Hugo syntax converter |
| `sync.sh` | Main→page sync + build pipeline |
| `themes/PaperMod/` | Git submodule — do NOT edit directly |

## Build & Deploy

```bash
bash sync.sh              # sync main content + convert + build
hugo server -D            # preview at localhost:1313
hugo --minify             # build only
```

## Citation Resolution Workflow

When a post uses `[^citekey]` as footnote markers (where citekey is a Zotero citation key), resolve them before publishing:

### Input (user writes in Obsidian)

```markdown
As shown by Mnih et al.[^mnih2015humanlevel] and later improved in[^silver2017mastering].

[^mnih2015humanlevel]:
[^silver2017mastering]:
```

### Resolution steps

1. Scan post for all `[^citekey]:` footnote definitions (empty ones need resolution)
2. For each citekey, look up via Zotero MCP to get: authors, title, URL, venue, year
3. Fill the footnote definition in this exact format:

```markdown
[^citekey]: Author1, A.; Author2, B. [Title](https://doi.org/...). *Venue*. Year.
```

Format rules:
- Authors: `Last, F.` separated by `;`, last author preceded by `&`
- Title: markdown link `[Title](URL)` pointing to paper
- Venue: italicized (`*Venue*`) — journal name, conference, or "arXiv preprint"
- Year: bare number
- Example: `[^mnih2015humanlevel]: Mnih, V. et al. [Human-level control through deep RL](https://...). *Nature*. 2015.`

### Auto-generate "Cited as" BibTeX block

Every published post gets a "Cited as" block appended before the footnotes section. Generate it from the post's frontmatter:

```markdown
---

Cited as:

```bibtex
@article{zellerYYYYslug,
  title   = "Post Title",
  author  = "Zeller, Atticus",
  journal = "atticuszeller.github.io/blog",
  year    = "YYYY",
  url     = "https://atticuszeller.github.io/blog/posts/slug/"
}
```
```

Where `YYYY` = publication year, `slug` = filename without `.md`.

## Git Pattern

`.git` is a pointer file: `gitdir: ../../99_system/git/blog.git`
Git data stored at `99_system/git/blog.git` with `core.worktree = ../../../20_project/blog`.
