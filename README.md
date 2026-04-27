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
| `$...$` math | Passes through unchanged | Hugo configured to render natively |
| `$$...$$` math | Passes through unchanged | Hugo configured to render natively |
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
