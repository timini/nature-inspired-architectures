"""Build the catalogue as a static website in _site/.

Renders README.md, the pattern pages, the docs and the references with the
`markdown` package, rewrites links between Markdown files to their HTML pages,
and copies the diagrams and data files the pages link to.

    pip install markdown
    python scripts/build_site.py
"""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
REPO = "https://github.com/timini/nature-inspired-architectures"
BLOG = "https://timini.github.io/devblog/nature-inspired-architectures/"

PAGES = {
    "README.md": "index.html",
    "references/README.md": "references/index.html",
    **{f"patterns/{p.name}": f"patterns/{p.stem}.html" for p in sorted((ROOT / "patterns").glob("*.md"))},
    **{f"docs/{p.name}": f"docs/{p.stem}.html" for p in sorted((ROOT / "docs").glob("*.md"))},
}
COPY = ["diagrams", "examples", "references/references.bib", "references/metadata.json", "catalogue.json"]

DETAILS = re.compile(r"<details>.*?</details>\s*", re.S)
LINK = re.compile(r'href="([^"#:]+)(#[^"]*)?"')

STYLE = """
:root { --ink:#1d2421; --muted:#5b6661; --paper:#fbfaf7; --line:#e3e0d8; --accent:#2f6b4f; --code:#f2efe8; }
@media (prefers-color-scheme: dark) {
  :root { --ink:#e6e8e4; --muted:#a3aba6; --paper:#161a18; --line:#2c332f; --accent:#7cc49e; --code:#232a26; }
}
* { box-sizing: border-box; }
body { margin:0; background:var(--paper); color:var(--ink);
  font: 17px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
header.site, main, footer { max-width: 860px; margin: 0 auto; padding: 0 16px; }
header.site { display:flex; flex-wrap:wrap; gap:8px 20px; align-items:baseline; padding-top:20px;
  padding-bottom:12px; border-bottom:1px solid var(--line); }
header.site a.home { font-weight:600; color:var(--ink); text-decoration:none; margin-right:auto; }
header.site nav a { color:var(--muted); margin-left:14px; font-size:15px; }
main { padding-top:8px; padding-bottom:48px; }
a { color:var(--accent); }
h1 { font-size:2rem; line-height:1.2; margin-top:1.2em; }
h2 { margin-top:1.8em; padding-top:.4em; border-top:1px solid var(--line); }
img { max-width:100%; height:auto; background:#fff; border-radius:6px; padding:8px; border:1px solid var(--line); }
table { border-collapse:collapse; width:100%; display:block; overflow-x:auto; font-size:15px; }
th, td { border:1px solid var(--line); padding:6px 10px; text-align:left; vertical-align:top; }
th { background:var(--code); }
code { background:var(--code); padding:1px 4px; border-radius:4px; font-size:.9em; }
pre { background:var(--code); padding:12px; overflow-x:auto; border-radius:6px; }
pre code { background:none; padding:0; }
footer { color:var(--muted); font-size:14px; padding-bottom:40px; border-top:1px solid var(--line); padding-top:16px; }
"""


def relative(target: str, page: str) -> str:
    """Path from the output page `page` to the output file `target`."""
    depth = page.count("/")
    return "../" * depth + target


def rewrite_links(body: str, source: str, page: str) -> str:
    source_dir = Path(source).parent

    def swap(match: re.Match[str]) -> str:
        href, anchor = match.group(1), match.group(2) or ""
        resolved = (source_dir / href).as_posix()
        parts = []
        for part in resolved.split("/"):
            if part == "..":
                parts.pop()
            elif part != ".":
                parts.append(part)
        resolved = "/".join(parts)
        if resolved in PAGES:
            return f'href="{relative(PAGES[resolved], page)}{anchor}"'
        if any(resolved == item or resolved.startswith(item + "/") for item in COPY):
            return f'href="{relative(resolved, page)}{anchor}"'
        return f'href="{REPO}/blob/main/{resolved}{anchor}"'

    return LINK.sub(swap, body)


def render(source: str, page: str) -> None:
    text = (ROOT / source).read_text(encoding="utf-8")
    text = DETAILS.sub("", text)
    body = markdown.markdown(text, extensions=["tables", "fenced_code"], output_format="html")
    body = rewrite_links(body, source, page)
    title_match = re.search(r"<h1>(.*?)</h1>", body)
    title = re.sub("<[^>]+>", "", title_match.group(1)) if title_match else "Nature-inspired architectures"
    home = relative("index.html", page)
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{STYLE}</style>
<script defer src="{relative('analytics.js', page)}" data-measurement-id="G-E7HR0ZB5K7"></script>
</head>
<body>
<header class="site">
  <a class="home" href="{home}">Nature-inspired architectures</a>
  <nav><a href="{relative('references/index.html', page)}">References</a><a href="{REPO}">Repository</a><a href="{BLOG}">Write-up</a></nav>
</header>
<main>
{body}
</main>
<footer>Built from <a href="{REPO}">{REPO.removeprefix('https://')}</a>.</footer>
</body>
</html>
"""
    out = OUT / page
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def main() -> None:
    shutil.rmtree(OUT, ignore_errors=True)
    for source, page in PAGES.items():
        render(source, page)
    for item in COPY:
        src, dst = ROOT / item, OUT / item
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    shutil.copy2(ROOT / "scripts/analytics.js", OUT / "analytics.js")
    print(f"Built {len(PAGES)} pages in {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
