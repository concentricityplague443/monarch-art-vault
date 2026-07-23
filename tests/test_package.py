import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def test_core_files_exist():
    for name in ['SKILL.md','SOUL.md','README.md','LICENSE','manifest.json']:
        assert (ROOT/name).exists()
def test_manifest_identity():
    data=json.loads((ROOT/'manifest.json').read_text())
    assert data['id']=='monarch-art-vault'
    assert data['brand']=='Monarch'
def test_skill_contains_publication_gate():
    assert 'explicit approval' in (ROOT/'SKILL.md').read_text().lower()
