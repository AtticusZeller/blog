# CLAUDE.md — Blog Project (page branch)

## Role

You are the Hugo build & deploy assistant. Manage the Hugo project configuration, theme, and deployment pipeline on this branch.

## Branch Rules

- **This is the `page` branch** — Hugo project files only.
- **Content is synced from `main`** via `sync.sh` (locally) or CI. Never edit `content/posts/` directly.
- **Do not checkout `main`** to write content — that's the writing branch.

## Key Files

| File | Purpose |
|:--|:--|
| `hugo.yaml` | Hugo + PaperMod config (MathJax passthrough, GitHub highlight theme) |
| `layouts/_default/_markup/render-passthrough.html` | Outputs raw `$$...$$` for MathJax v3 client-side rendering |
| `layouts/_default/_markup/render-blockquote.html` | GitHub-style alerts (NOTE/TIP/WARNING/CAUTION) |
| `layouts/partials/extend_head.html` | Google Fonts + MathJax v3 config (tags: ams) |
| `static/css/academic.css` | Academic style: Lora font, crimson accent, dotted links, 800px column |
| `.github/workflows/deploy.yml` | CI: build + deploy to GitHub Pages |
| `obs2hugo.py` | Obsidian→Hugo syntax converter (wikilinks, embeds, comments) |
| `sync.sh` | Local sync: pull posts from main → convert → build |
| `themes/PaperMod/` | Git submodule — do NOT edit directly |

## Build & Deploy

```bash
bash sync.sh              # sync main content + convert + build
hugo server -D            # preview at localhost:1313
hugo --minify             # build only
```

## CI/CD Pipeline

**Auto-deploy**: push to `main` → `notify.yml` sends `repository_dispatch` → `deploy.yml` on `page` builds + deploys.

- GitHub Pages source must be set to **"GitHub Actions"** (not branch)
- Workflow installs Hugo extended 0.160.1, syncs from main, builds, deploys via `deploy-pages`
- Also triggers on push to `page` (config/theme changes) and manual `workflow_dispatch`

## Math Rendering

- **Engine**: MathJax v3 (client-side), NOT KaTeX
- **Goldmark passthrough** protects LaTeX from markdown processing
- `render-passthrough.html` outputs raw `$...$` / `$$...$$` for MathJax
- Equation auto-numbering via `tags: "ams"` in MathJax config

## Citation Resolution

When posts use `[^citekey]` with Zotero citekeys:

1. Scan for empty `[^citekey]:` definitions
2. Look up each citekey via Zotero MCP
3. Fill: `[^citekey]: Authors. [Title](URL). *Venue*. Year.`

Every published post auto-generates a "Cited as" BibTeX block from frontmatter.

## Git Pattern

`.git` → `gitdir: ../../99_system/git/blog.git`
`core.worktree = ../../../20_project/blog`
