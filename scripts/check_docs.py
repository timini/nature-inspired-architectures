"""Check internal links, bibliography keys and catalogue completeness offline."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from natural_architectures.__main__ import PATTERNS  # noqa: E402


def main() -> None:
    errors = []
    catalogue = json.loads((ROOT / 'catalogue.json').read_text())
    references = json.loads((ROOT / 'references/metadata.json').read_text())
    keys = {r['id'] for r in references}
    bib = (ROOT / 'references/references.bib').read_text()
    bib_keys = set(re.findall(r'@\w+\{([^,]+),', bib))
    if keys != bib_keys or len(keys) != len(references):
        errors.append('Reference metadata and BibTeX keys differ or contain duplicates')
    if {p['id'] for p in catalogue} != set(PATTERNS) or len(catalogue) != len(PATTERNS):
        errors.append('Catalogue and runnable examples differ')
    for entry in catalogue:
        for field in ('document', 'implementation', 'diagram'):
            if not (ROOT / entry[field]).is_file():
                errors.append(f'Missing {entry[field]}')
        if not set(entry['references']) <= keys:
            errors.append(f'Unknown source in {entry["id"]}')
        document = (ROOT / entry['document']).read_text()
        diagram = (ROOT / entry['diagram']).read_text().strip()
        if diagram not in document:
            errors.append(f'Embedded Mermaid differs from source: {entry["id"]}')
        for ref in entry['references']:
            if f'#{ref})' not in document:
                errors.append(f'Uncited catalogue source: {entry["id"]}: {ref}')
    for file in ROOT.rglob('*.md'):
        if 'node_modules' in file.parts or '.venv' in file.parts:
            continue
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)\)', file.read_text()):
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc:
                continue
            path = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file
            if not path.exists():
                errors.append(f'{file.relative_to(ROOT)}: missing {target}')
            elif parsed.fragment and path.suffix == '.md':
                content = path.read_text()
                fragment = unquote(parsed.fragment)
                if f'id="{fragment}"' not in content:
                    errors.append(f'{file.relative_to(ROOT)}: missing explicit anchor {target}')
    output = json.loads((ROOT / 'examples/output.json').read_text())
    if set(output) != set(PATTERNS):
        errors.append('Captured output does not cover every example')
    if errors:
        raise SystemExit('\n'.join(errors))
    print(f'Checked {len(catalogue)} patterns, {len(keys)} references and all local Markdown links.')


if __name__ == '__main__':
    main()
