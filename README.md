# Blog — Page Branch (Hugo Project)

This branch contains the Hugo project that builds and deploys the blog.

## What's Here

| Path | Purpose |
|:--|:--|
| `hugo.yaml` | Hugo config (PaperMod theme, MathJax passthrough, search) |
| `themes/PaperMod/` | PaperMod theme (git submodule) |
| `layouts/` | Render hooks (passthrough, blockquotes) + extend_head partial |
| `static/css/academic.css` | Academic visual style (Lora, crimson, dotted links) |
| `.github/workflows/deploy.yml` | CI: build + deploy to GitHub Pages |
| `content/posts/` | Blog posts — **synced from `main`, do not edit here** |
| `content/archives.md` | Archives page |
| `content/search.md` | Search page |
| `obs2hugo.py` | Converts Obsidian syntax to Hugo markdown |
| `sync.sh` | Local sync + convert + build pipeline |

## Deploy

**Automatic** (CI): push to `main` → auto-build → deploy to GitHub Pages.
**Local**: `bash sync.sh && hugo server -D`

### GitHub Pages Setup

GitHub Pages source must be set to **"GitHub Actions"** (Settings → Pages → Source).

### Pipeline Flow

```
push to main (posts/*.md)
  → .github/workflows/notify.yml (main branch)
  → repository_dispatch "content-update"
  → .github/workflows/deploy.yml (this branch)
  → git fetch main → sync posts → obs2hugo → hugo build → deploy-pages
```

Also triggers on push to `page` (config changes) and manual `workflow_dispatch`.

## Architecture

See `main` branch README for the full dual-branch architecture and Obsidian syntax guide.
