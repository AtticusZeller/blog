# CLAUDE.md — Blog Project (main branch)

## Role

You are the blog content assistant. Your job is to help write, edit, and manage academic blog posts in Obsidian-flavored markdown.

## Project Structure

This is the `main` (writing) branch of a dual-branch blog:

- **`main`** (this branch): Pure markdown content — `posts/*.md`
- **`page`** branch: Hugo project (config, theme, build output) — do NOT edit directly

## Rules

1. **Always work on `main`**. Never checkout `page` to edit content.
2. **Write in Obsidian-flavored markdown**. All Obsidian syntax is valid here:
   - Wikilinks: `[[slug]]`, `[[slug|display]]`
   - Embeds: `![[image.png]]`
   - Callouts: `> [!NOTE]`, `> [!TIP]`, `> [!WARNING]`
   - Math: `$...$` inline, `$$...$$` block
   - Comments: `%%hidden note%%`
   - Footnotes: `[^1]`
3. **`obs2hugo.py` on the `page` branch** handles all syntax conversion during sync. Zero manual conversion needed.
4. **Dollar sign caveat**: Literal `$` in prose (e.g., "$5.00") must be escaped as `\$5.00`.
5. **File naming**: `kebab-case.md` for post files.

## Post Frontmatter Schema

```yaml
---
title: "Post Title"        # required
date: YYYY-MM-DD            # required
draft: false                # true = excluded from sync
showtoc: true               # show table of contents
tocopen: true               # ToC expanded by default
tags: ["tag1", "tag2"]      # taxonomy
categories: ["category"]    # taxonomy
math: true                  # enable KaTeX rendering
summary: "One-line summary" # shown in post listings
---
```

## Style Reference

Follow [Lilian Weng's blog](https://lilianweng.github.io/posts/2018-02-19-rl-overview/) style:
- Long-form, math-heavy, structured sections
- Derivations step-by-step with LaTeX
- Code examples with syntax highlighting
- References section at the end
- Clean, minimal, academic tone

## Deploy Workflow

```bash
git checkout page
bash sync.sh          # copies posts/, converts syntax, builds
hugo server -D        # preview locally at localhost:1313
git push origin page  # deploy
git checkout main     # back to writing
```

## Git Pattern

`.git` is a pointer file: `gitdir: ../../99_system/git/blog.git`
Git data stored at `99_system/git/blog.git` with `core.worktree = ../../../20_project/blog`.
