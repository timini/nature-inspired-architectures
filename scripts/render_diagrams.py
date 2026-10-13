"""Render all Mermaid sources; optionally use an existing Chrome executable."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cli', default=str(ROOT / 'tools/diagrams/node_modules/.bin/mmdc'))
    parser.add_argument('--browser', help='Absolute path to a Chrome or Chromium executable')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory() as temporary:
        config = Path(temporary) / 'puppeteer.json'
        config.write_text(json.dumps({'executablePath': args.browser} if args.browser else {}))
        for source in sorted((ROOT / 'diagrams').glob('*.mmd')):
            subprocess.run([args.cli, '-i', str(source), '-o', str(source.with_suffix('.svg')),
                            '-p', str(config), '-t', 'neutral', '-b', 'white'], check=True)


if __name__ == '__main__':
    main()
