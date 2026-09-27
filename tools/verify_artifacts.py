"""Verify preserved file identities and tier differences without loading DLLs."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / 'evidence/artifact-manifest.json').read_text())
assert len(manifest) == 8
for item in manifest:
    data = (root / item['path']).read_bytes()
    assert len(data) == item['bytes'], item['path']
    assert hashlib.sha256(data).hexdigest() == item['sha256'], item['path']
for edition, padding in (('Enhanced', 2334), ('Legacy', 2675)):
    for folder, form in (('', 'packed'), ('artifacts/unpacked', 'unpacked')):
        vip = (root / folder / f'VIP-{edition}.{form}.dll').read_bytes()
        mvp = (root / folder / f'MVP-{edition}.{form}.dll').read_bytes()
        assert mvp[:len(vip)] == vip, f'{edition}/{form}: prefix differs'
        assert mvp[len(vip):] == b' ' * padding, f'{edition}/{form}: padding differs'
print('PASS: all eight artifact hashes/sizes match; four VIP/MVP comparisons match the reported space padding.')
