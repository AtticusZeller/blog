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
| `layouts/_default/_markup/render-passthrough.html` | KaTeX math rendering (native Hugo) |
| `layouts/_default/_markup/render-blockquotes.html` | Callout/alert rendering |
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

## Git Pattern

`.git` is a pointer file: `gitdir: ../../99_system/git/blog.git`
Git data stored at `99_system/git/blog.git` with `core.worktree = ../../../20_project/blog`.
