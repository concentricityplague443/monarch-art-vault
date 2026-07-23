#!/usr/bin/env python3
import json
from pathlib import Path
required=['SKILL.md','SOUL.md','README.md','LICENSE','manifest.json','references/metadata-schema.json']
root=Path(__file__).resolve().parents[1]
missing=[x for x in required if not (root/x).exists()]
json.loads((root/'manifest.json').read_text())
json.loads((root/'references/metadata-schema.json').read_text())
if missing: raise SystemExit('Missing: '+', '.join(missing))
print('Package validation passed.')
