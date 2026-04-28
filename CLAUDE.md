# CLAUDE.md — Blog Project

## Role

Blog content + build assistant. Write posts on `main`, manage Hugo on `page`.

## Architecture

| Branch | Content | Purpose |
|:--|:--|:--|
| `main` | `posts/*.md` (Obsidian markdown) | Writing |
| `page` | Hugo project (config, theme, layouts) | Build & deploy via GitHub Actions |

Write on `main`, push, CI auto-deploys. Never checkout the other branch to edit its content.

## Auto-Deploy Pipeline

```
push to main → .github/workflows/notify.yml (main)
  → repository_dispatch "content-update"
  → .github/workflows/deploy.yml (page)
  → git fetch main → sync posts → obs2hugo → hugo build → deploy-pages
```

GitHub Pages source: **"GitHub Actions"** (Settings → Pages).

## Writing Rules

1. Write in Obsidian-flavored markdown: wikilinks `[[slug]]`, embeds `![[img]]`, callouts `> [!NOTE]`, math `$...$`/`$$...$$`, comments `%%..%%`
2. Footnotes use Zotero citekeys: `[^citekey]`, leave definition empty for agent resolution
3. Dollar sign caveat: literal `$` in prose → `\$5.00`
4. File naming: `kebab-case.md`
5. `obs2hugo.py` on `page` branch handles all syntax conversion during sync

## Post Frontmatter

```yaml
---
title: "Post Title"
date: YYYY-MM-DD
draft: false
showtoc: true
tocopen: true
tags: ["tag1", "tag2"]
categories: ["category"]
math: true
summary: "One-line summary"
---
```

## Citation Workflow

1. Write `[^citekey]:` (empty definition)
2. Agent resolves via Zotero MCP → `[^citekey]: Authors. [Title](URL). *Venue*. Year.`
3. Every post auto-generates "Cited as" BibTeX block from frontmatter

## Key Files (page branch)

| File | Purpose |
|:--|:--|
| `hugo.yaml` | Hugo + PaperMod config, MathJax passthrough, GitHub highlight theme |
| `layouts/_default/_markup/render-passthrough.html` | Outputs raw `$$...$$` for MathJax v3 |
| `layouts/_default/_markup/render-blockquote.html` | GitHub-style alerts |
| `layouts/partials/extend_head.html` | Google Fonts + MathJax v3 config |
| `static/css/academic.css` | Lora font, crimson accent, dotted links |
| `.github/workflows/deploy.yml` | CI build + deploy |
| `obs2hugo.py` | Obsidian→Hugo syntax converter |
| `sync.sh` | Local sync + build pipeline |

## Visual Style

Academic style (inspired by Lilian Weng): Lora serif, crimson `#e0491f`, dotted-underline links, ~800px column, GitHub code highlighting, pill tags.

## Git Pattern

`.git` → `gitdir: ../../99_system/git/blog.git`, worktree at `../../../20_project/blog`.
