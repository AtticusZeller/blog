# Blog — Page Branch (Hugo Project)

This branch contains the Hugo project that builds and deploys the blog.

## What's Here

| Path | Purpose |
|:--|:--|
| `hugo.yaml` | Hugo configuration (PaperMod theme, math, search) |
| `themes/PaperMod/` | PaperMod theme (git submodule) |
| `layouts/` | Custom render hooks (KaTeX, callouts) |
| `content/posts/` | Blog posts — **synced from `main` branch, do not edit here** |
| `content/archives.md` | Archives page |
| `content/search.md` | Search page |
| `obs2hugo.py` | Converts Obsidian syntax to Hugo markdown |
| `sync.sh` | Sync + convert + build pipeline |

## Sync & Deploy

```bash
bash sync.sh              # Pull posts from main, convert, build
hugo server -D            # Preview at localhost:1313
git push origin page      # Deploy to GitHub Pages
```

## Architecture

See `main` branch README for the full dual-branch architecture and Obsidian syntax guide.
