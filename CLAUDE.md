# CLAUDE.md — Blog Project (main branch)

## Role

You are the blog content assistant. Help write, edit, and manage academic blog posts in Obsidian-flavored markdown.

## Project Structure

Dual-branch blog — this is the writing branch:

- **`main`** (this branch): `posts/*.md` — pure Obsidian-flavored markdown
- **`page`** branch: Hugo project (config, theme, layouts) — do NOT edit directly

## Rules

1. **Always work on `main`**. Never checkout `page` to edit content.
2. **Write in Obsidian-flavored markdown**:
   - Wikilinks: `[[slug]]`, `[[slug|display]]`
   - Embeds: `![[image.png]]`
   - Callouts: `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`
   - Math: `$...$` inline, `$$...$$` block (MathJax v3 renders client-side)
   - Comments: `%%hidden note%%`
   - Footnotes: `[^citekey]` — use Zotero citekeys as footnote markers
3. **`obs2hugo.py` on `page` branch** handles all syntax conversion during sync.
4. **Dollar sign caveat**: Literal `$` in prose (e.g., "$5.00") must be escaped as `\$5.00`.
5. **File naming**: `kebab-case.md` for post files.

## Post Frontmatter

```yaml
---
title: "Post Title"        # required
date: YYYY-MM-DD            # required
draft: false                # true = excluded from build
showtoc: true               # table of contents
tocopen: true               # ToC expanded by default
tags: ["tag1", "tag2"]
categories: ["category"]
math: true                  # enable MathJax rendering
summary: "One-line summary"
---
```

## Citation Workflow

Write `[^citekey]` with Zotero citekeys, leave definitions empty:

```markdown
As shown by[^mnih2015humanlevel].

[^mnih2015humanlevel]:
```

Before publishing, agent resolves via Zotero MCP:

```markdown
[^mnih2015humanlevel]: Mnih, V. et al. [Title](https://doi.org/...). *Nature*. 2015.
```

Every post auto-generates a "Cited as" BibTeX block for readers to cite.

## Deploy

**Automatic**: push to `main` → CI builds + deploys to GitHub Pages. No manual steps needed.

```
push main → notify.yml → repository_dispatch → deploy.yml (page branch)
  → sync posts → obs2hugo → hugo build → deploy-pages
```

**Local preview**: `hugo server -D` on `page` branch.

## Style Reference

Follow [Lilian Weng's blog](https://lilianweng.github.io/posts/2018-02-19-rl-overview/):
- Long-form, math-heavy, structured sections
- Step-by-step derivations in LaTeX
- Clean, minimal, academic tone

## Git Pattern

`.git` is a pointer file: `gitdir: ../../99_system/git/blog.git`
Git data at `99_system/git/blog.git` with `core.worktree = ../../../20_project/blog`.
