# Blog

Personal academic blog — write in Obsidian, deploy via Hugo + PaperMod.

## Dual-Branch Architecture

| Branch | Content | Purpose |
|:--|:--|:--|
| `main` | `posts/*.md` (pure Obsidian-flavored markdown) | Writing branch — clean, no build artifacts |
| `page` | Full Hugo project (config, theme, build output) | Deploy branch — GitHub Pages serves from here |

### Workflow

1. Write posts in `posts/` on `main` — use any Obsidian syntax freely
2. Switch to `page`: `git checkout page`
3. Run `bash sync.sh` — copies posts, converts syntax, builds
4. Push: `git push origin page`

## Obsidian vs Hugo Syntax

`obs2hugo.py` handles conversion automatically during sync. Here's what it does:

| Obsidian Syntax | What Happens | Example |
|:--|:--|:--|
| `[[page]]` | → `[page](/posts/page/)` | `[[rl-basics]]` → `[rl-basics](/posts/rl-basics/)` |
| `[[page\|text]]` | → `[text](/posts/page/)` | `[[rl\|RL intro]]` → `[RL intro](/posts/rl/)` |
| `![[image.png]]` | → `![image](/images/image.png)` | Works for .png, .jpg, .svg |
| `%%comment%%` | → `<!-- comment -->` | Hidden in published post |
| `$...$` math | Passes through unchanged | MathJax renders client-side |
| `$$...$$` math | Passes through unchanged | MathJax renders client-side |
| `> [!NOTE]` | Passes through unchanged | Hugo render hook handles callouts |
| `[^1]` footnotes | Passes through unchanged | Goldmark renders natively |

### Caveat: Dollar Signs in Prose

Hugo's math passthrough treats `$...$` as math delimiters. If you need a literal dollar sign (e.g., "$5.00"), escape it as `\$5.00`. The converter does NOT auto-escape these because distinguishing math from currency is ambiguous.

## Writing Conventions

- **File naming**: `kebab-case.md` (e.g., `reinforcement-learning-basics.md`)
- **Frontmatter** (required):

```yaml
---
title: "Post Title"
date: 2026-04-27
draft: false
showtoc: true
tocopen: true
tags: ["tag1", "tag2"]
categories: ["category"]
math: true          # enable math rendering
summary: "One-line summary"
---
```

- **Internal links**: Use `[[slug]]` wikilinks — auto-converted during sync
- **External links**: Use standard `[text](url)` markdown
- **Images**: Drop in `posts/` or reference `static/images/` on the `page` branch

## Citation & Reference Format

### Writing: `[^citekey]` as footnote marker

Use Zotero citekeys as footnote markers. Write freely in Obsidian, leave definitions empty:

```markdown
As shown by Mnih et al.[^mnih2015humanlevel] and later improved in[^silver2017mastering].

[^mnih2015humanlevel]:
[^silver2017mastering]:
```

### Resolution: agent fills in via Zotero

Before publishing, agent resolves empty `[^citekey]:` definitions to:

```markdown
[^mnih2015humanlevel]: Mnih, V. et al. [Human-level control through deep RL](https://doi.org/...). *Nature*. 2015.
[^silver2017mastering]: Silver, D. et al. [Mastering the game of Go without human knowledge](https://doi.org/...). *Nature*. 2017.
```

Format: `[^citekey]: Authors. [Title](URL). *Venue*. Year.`

### Auto-generated: "Cited as" BibTeX block

Every published post gets this block appended before footnotes:

```bibtex
@article{zeller2026slug,
  title   = "Post Title",
  author  = "Zeller, Atticus",
  journal = "atticuszeller.github.io/blog",
  year    = "2026",
  url     = "https://atticuszeller.github.io/blog/posts/slug/"
}
```

Generated from frontmatter (`title`, `date`, filename as slug). No manual work needed.

## Math Conventions

- Inline: `$V(s) = \max_a [...]$`
- Display: `$$...$$` on separate lines
- Equation numbering: `\begin{equation}` blocks get auto-numbered via MathJax `tags: "ams"`
- Avoid `$$` inside lists — Hugo may not parse correctly. Use `$` inline instead
- For `\begin{align}`, `\begin{equation}` environments, `$$` wrapper is not needed — MathJax processes them directly

## Visual Style

The blog uses an academic style inspired by [Lilian Weng's Lil'Log](https://lilianweng.github.io/):

- **Font**: Lora (serif) for body, Open Sans for navigation
- **Accent**: Crimson `#e0491f` for links and tags
- **Links**: Dotted underline in posts, solid crimson on hover
- **Code**: GitHub-style light syntax highlighting
- **Content width**: ~800px for readability
- **TOC**: Collapsible, open by default
- **Tags**: Pill-shaped badges
