#!/usr/bin/env python3
"""obs2hugo.py — Convert Obsidian-flavored markdown to Hugo-compatible markdown.

Handles:
  [[page]]           -> [page](/posts/page/)
  [[page|display]]   -> [display](/posts/page/)
  ![[image.png]]     -> ![image](/images/image.png)
  %%comment%%        -> <!-- comment -->
"""

import re
import sys
from pathlib import Path


def convert_wikilinks(text: str) -> str:
    """Convert [[page|display]] first (greedy), then [[page]]. Skips ![[...]] (embeds)."""

    def slugify(name: str) -> str:
        return name.strip().lower().replace(" ", "-")

    # [[page|display]] -> [display](/posts/page/)
    text = re.sub(
        r"(?<!!)\[\[([^\]|]+)\|([^\]]+)\]\]",
        lambda m: f"[{m.group(2).strip()}](/posts/{slugify(m.group(1))}/)",
        text,
    )
    # [[page]] -> [page](/posts/page/)
    text = re.sub(
        r"(?<!!)\[\[([^\]]+)\]\]",
        lambda m: f"[{m.group(1).strip()}](/posts/{slugify(m.group(1))}/)",
        text,
    )
    return text


def convert_embeds(text: str) -> str:
    """Convert ![[file.ext]] -> ![file](/images/file.ext)."""
    return re.sub(
        r"!\[\[([^\]]+)\]\]",
        lambda m: f"![{Path(m.group(1)).stem}](/images/{m.group(1).strip()})",
        text,
    )


def convert_comments(text: str) -> str:
    """Convert %%comment%% -> <!-- comment -->."""
    return re.sub(r"%%(.+?)%%", r"<!-- \1 -->", text)


def convert_file(src: Path, dst: Path) -> None:
    text = src.read_text(encoding="utf-8")
    text = convert_wikilinks(text)
    text = convert_embeds(text)
    text = convert_comments(text)
    dst.write_text(text, encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input.md> <output.md>", file=sys.stderr)
        sys.exit(1)
    convert_file(Path(sys.argv[1]), Path(sys.argv[2]))


if __name__ == "__main__":
    main()
