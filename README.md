# Blog

Personal academic blog — write in Obsidian, auto-deploy via Hugo + PaperMod + GitHub Actions.

## Dual-Branch Architecture

| Branch | Content | Purpose |
|:--|:--|:--|
| `main` | `posts/*.md` (Obsidian-flavored markdown) | Writing branch |
| `page` | Hugo project (config, theme, layouts) + CI workflow | Build & deploy branch |

### Auto-Deploy Pipeline

```
push to main → notify.yml → repository_dispatch
  → deploy.yml (page branch) → sync posts → obs2hugo → hugo build → deploy-pages
```

Push to `main` triggers automatic build and deploy. No manual steps needed.

## Obsidian vs Hugo Syntax

`obs2hugo.py` handles conversion automatically during sync:

| Obsidian Syntax | What Happens | Example |
|:--|:--|:--|
| `[[page]]` | → `[page](/posts/page/)` | `[[rl-basics]]` → `[rl-basics](/posts/rl-basics/)` |
| `[[page\|text]]` | → `[text](/posts/page/)` | `[[rl\|RL intro]]` → `[RL intro](/posts/rl/)` |
| `![[image.png]]` | → `![image](/images/image.png)` | Works for .png, .jpg, .svg |
| `%%comment%%` | → `<!-- comment -->` | Hidden in published post |
| `$...$` / `$$...$$` | Passes through unchanged | MathJax v3 renders client-side |
| `> [!NOTE]` | Passes through unchanged | Hugo render hook handles callouts |
| `[^citekey]` | Passes through unchanged | Zotero citekey → agent resolves via MCP |

### Caveat: Dollar Signs in Prose

Literal `$` in prose (e.g., "$5.00") must be escaped as `\$5.00`.

## Writing Conventions

- **File naming**: `kebab-case.md`
- **Frontmatter**:

```yaml
---
title: "Post Title"
date: 2026-04-27
draft: false
showtoc: true
tocopen: true
tags: ["tag1", "tag2"]
categories: ["category"]
math: true
summary: "One-line summary"
---
```

- **Internal links**: `[[slug]]` wikilinks
- **External links**: `[text](url)` markdown
- **Citations**: `[^citekey]` with Zotero citekeys, agent resolves via Zotero MCP

## Citation & Reference Format

### Writing: `[^citekey]` as footnote marker

```markdown
As shown by Mnih et al.[^mnih2015humanlevel] and improved in[^silver2017mastering].

[^mnih2015humanlevel]:
[^silver2017mastering]:
```

### Resolution: agent fills in via Zotero

```markdown
[^mnih2015humanlevel]: Mnih, V. et al. [Human-level control through deep RL](https://doi.org/...). *Nature*. 2015.
```

Format: `[^citekey]: Authors. [Title](URL). *Venue*. Year.`

### Auto-generated: "Cited as" BibTeX block

Every published post gets a BibTeX block appended from frontmatter:

```bibtex
@article{zeller2026slug,
  title   = "Post Title",
  author  = "Zeller, Atticus",
  journal = "atticuszeller.github.io/blog",
  year    = "2026",
  url     = "https://atticuszeller.github.io/blog/posts/slug/"
}
```

## Math

- Inline: `$V(s) = \max_a [...]$`
- Display: `$$...$$` on separate lines
- Equation numbering: `\begin{equation}` auto-numbered via MathJax `tags: "ams"`

## Visual Style

Academic style inspired by [Lilian Weng's Lil'Log](https://lilianweng.github.io/):
Lora serif font, crimson `#e0491f` accent, dotted-underline links, ~800px content column, GitHub-style code highlighting, pill-shaped tags.
