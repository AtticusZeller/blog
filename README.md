# Blog

Personal academic blog built with Hugo + PaperMod and deployed to GitHub Pages.

| Branch | Content |
|:--|:--|
| `main` | Generated posts: `posts/<slug>.md` and `posts/images/<slug>-<hash>.<ext>` |
| `page` | Hugo site: config, PaperMod theme, layouts |

Posts on `main` are generated from notes in the LifeOS vault by its `blog-publish` skill. Posts are already Hugo markdown (internal links `../<slug>/`, images `/images/<name>`). Edit the source note and publish again; do not edit `posts/` by hand.

## Deploy

A push to `main` that touches `posts/` runs `.github/workflows/deploy.yml`: it checks out `page` into `site/`, copies the posts and images in, builds with Hugo, and deploys to Pages. After changing only the `page` branch, trigger a build manually:

```bash
gh workflow run deploy.yml -R AtticusZeller/blog --ref main
```
