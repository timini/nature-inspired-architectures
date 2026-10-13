# Diagram sources

Each `.mmd` file is an editable Mermaid flowchart with a corresponding rendered `.svg`. Pattern pages include both the SVG and a collapsible Mermaid block, so the diagrams remain available in readers without Mermaid support.

Solid edges indicate interactions within each depicted system. Dotted edges map concepts between biology and software. They are analogies, not experimentally demonstrated connections between those domains.

## Regenerate SVGs

The optional development tooling is separate from the dependency-free Python examples. Use Node.js 22 or newer and a compatible Chrome or Chromium installation.

```sh
PUPPETEER_SKIP_DOWNLOAD=true npm ci --prefix tools/diagrams
python3 scripts/render_diagrams.py --browser /absolute/path/to/chrome
```

On macOS with Google Chrome installed in Applications:

```sh
python3 scripts/render_diagrams.py \
  --browser '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
```

The CLI renders every source and fails on invalid syntax. After editing, also update the embedded Mermaid block in the pattern document and run `python3 scripts/check_docs.py`. Visually inspect labels, arrow directions and clipping; successful parsing alone is insufficient.

Tool documentation: [Mermaid syntax and usage](https://mermaid.js.org/config/usage), [Mermaid CLI](https://github.com/mermaid-js/mermaid-cli). All diagrams in this repository are original schematic illustrations; no source-paper figures are copied.
