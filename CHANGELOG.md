# Changelog

## 1.2.0 — 2026-07-24

- Added `scripts/enrich_assets.py` — full AI vision enrichment pipeline
- Uses PAL (Prompt Abstraction Layer) method: intent extraction → context injection → prompt enhancement
- Generates creative title + gallery-style description per image via Claude vision
- Embeds title, description, and tags into EXIF fields (ImageDescription, XPTitle, XPComment, XPKeywords)
- Outputs enriched JPEG copies to `06_Enriched/{run_id}/` with descriptive filenames
- Writes JSON sidecar per enriched image
- Appends full enrichment catalog to `02_Catalog/{run_id}_enrichment.jsonl`
- All AI fields marked `ai_suggested`, `approved: false`
- Added `--resume` flag to skip already-processed files
- Added `--limit N` flag for testing on a subset
- Updated SKILL.md with step 4a (visual enrichment workflow)
- Updated manifest.json to v1.2.0 with new capabilities

## 1.0.0 — 2026-07-23

- Initial Monarch Art Vault release
- Added core `SKILL.md`, ROSTR-compatible `SOUL.md`, schemas, policy references, local inventory script, tests, and GitHub Actions validation
