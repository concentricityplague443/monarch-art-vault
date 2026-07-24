#!/usr/bin/env python3
"""
Monarch Art Vault — Visual Enrichment Pipeline v1.2.0

For each image:
  1. Read the file with Claude vision (claude-opus-4-6 via Anthropic API)
  2. Extract intent: scene, mood, subject, emotional core
  3. Generate a creative title + rich description
  4. Write metadata into EXIF/IPTC fields (title → ImageDescription + XPTitle, description → UserComment)
  5. Copy enriched file to 06_Enriched/ folder
  6. Append record to enrichment catalog JSONL

Usage:
  python scripts/enrich_assets.py <source_folder> [--managed-root ArtLibrary] [--limit N] [--resume]

Dependencies:
  pip install anthropic pillow piexif
"""

import argparse
import base64
import json
import shutil
import struct
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
except ImportError:
    sys.exit("Missing: pip install anthropic")

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import piexif
    HAS_PIEXIF = True
except ImportError:
    HAS_PIEXIF = False

SUPPORTED = {".jpg", ".jpeg", ".png", ".tiff", ".tif", ".heic", ".webp"}
MODEL = "claude-opus-4-6"
OLLAMA_VISION_MODELS = ["llava", "llava:13b", "llava:34b", "bakllava", "moondream", "llava-phi3"]

VISION_PROMPT = """You are an art cataloger and creative titler. Analyze this photograph using the PAL (Prompt Abstraction Layer) method:

Step 1 — INTENT EXTRACTION: What is the core subject? What scene, mood, and emotional energy does this image carry?
Step 2 — CONTEXT INJECTION: Consider genre (street, portrait, architecture, event, nature, abstract), lighting, composition, and dominant feeling.
Step 3 — ENHANCEMENT: Surface the deeper meaning — what story does this moment tell?

Output ONLY a JSON object with these exact keys:
{
  "title": "A creative, evocative title (4-8 words, no quotes inside)",
  "description": "A vivid 2-3 sentence description of the scene, mood, and visual intent. Write like a gallery caption.",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "mood": "one word: e.g. energetic / serene / melancholic / vibrant / intimate",
  "scene_type": "architecture / portrait / event / street / nature / abstract / other"
}

No markdown. No explanation. Just the JSON."""


def encode_image(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    mt_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
              ".tiff": "image/tiff", ".tif": "image/tiff", ".heic": "image/heic",
              ".webp": "image/webp"}
    media_type = mt_map.get(suffix, "image/jpeg")
    with path.open("rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return data, media_type


def analyze_image(client, path: Path) -> dict:
    data, media_type = encode_image(path)
    msg = client.messages.create(
        model=MODEL,
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}},
                {"type": "text", "text": VISION_PROMPT}
            ]
        }]
    )
    raw = msg.content[0].text.strip()
    # strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def write_exif_metadata(src: Path, dest: Path, title: str, description: str, tags: list):
    """Copy file to dest and embed title + description into EXIF."""
    shutil.copy2(src, dest)

    if not HAS_PIEXIF or dest.suffix.lower() not in {".jpg", ".jpeg"}:
        return  # skip EXIF write for non-JPEG

    try:
        exif_dict = piexif.load(str(dest))
    except Exception:
        exif_dict = {"0th": {}, "Exif": {}, "GPS": {}, "1st": {}}

    def utf16(s):
        return s.encode("utf-16-le") + b"\x00\x00"

    zeroth = exif_dict.get("0th", {})
    # ImageDescription (ASCII)
    zeroth[piexif.ImageIFD.ImageDescription] = description[:255].encode("ascii", errors="replace")
    # XPTitle (Windows UTF-16LE)
    zeroth[piexif.ImageIFD.XPTitle] = utf16(title[:128])
    # XPComment
    zeroth[piexif.ImageIFD.XPComment] = utf16(description[:512])
    # XPKeywords (semicolon-separated)
    zeroth[piexif.ImageIFD.XPKeywords] = utf16("; ".join(tags[:10]))
    exif_dict["0th"] = zeroth

    try:
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, str(dest))
    except Exception as e:
        print(f"  [warn] EXIF write failed for {dest.name}: {e}")


def write_sidecar(dest_dir: Path, stem: str, record: dict):
    """Write a JSON sidecar next to the enriched image."""
    sidecar = dest_dir / f"{stem}.json"
    sidecar.write_text(json.dumps(record, indent=2, ensure_ascii=False))


def main():
    p = argparse.ArgumentParser(description="Monarch Art Vault — Visual Enrichment Pipeline")
    p.add_argument("source")
    p.add_argument("--managed-root", default="ArtLibrary")
    p.add_argument("--limit", type=int, default=None, help="Process only N images (for testing)")
    p.add_argument("--resume", action="store_true", help="Skip already-enriched files")
    p.add_argument("--delay", type=float, default=0.5, help="Seconds between API calls")
    args = p.parse_args()

    source = Path(args.source).resolve()
    root = Path(args.managed_root).resolve()
    run_id = "ENRICH-" + datetime.now().strftime("%Y%m%d-%H%M%S")

    enriched_dir = root / "06_Enriched" / run_id
    catalog_dir = root / "02_Catalog"
    reports_dir = root / "99_Reports"
    enriched_dir.mkdir(parents=True, exist_ok=True)
    catalog_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    catalog_path = catalog_dir / f"{run_id}_enrichment.jsonl"
    done_path = reports_dir / f"{run_id}_enrichment_report.json"

    # collect images
    all_files = sorted([
        f for f in (source.rglob("*") if source.is_dir() else [source])
        if f.is_file() and f.suffix.lower() in SUPPORTED
    ])

    if args.limit:
        all_files = all_files[:args.limit]

    # load already-enriched stems for resume
    enriched_stems = set()
    if args.resume and catalog_path.exists():
        for line in catalog_path.read_text().splitlines():
            try:
                enriched_stems.add(json.loads(line)["filename"])
            except Exception:
                pass

    client = anthropic.Anthropic()

    total = len(all_files)
    done, skipped, failed = 0, 0, 0
    results = []

    print(f"[monarch] Run: {run_id}")
    print(f"[monarch] Source: {source}")
    print(f"[monarch] Images: {total}")
    print(f"[monarch] Output: {enriched_dir}")
    print()

    for i, path in enumerate(all_files, 1):
        if path.name in enriched_stems:
            print(f"  [{i}/{total}] SKIP (already enriched): {path.name}")
            skipped += 1
            continue

        print(f"  [{i}/{total}] Analyzing: {path.name} ...", end=" ", flush=True)

        try:
            analysis = analyze_image(client, path)
            title = analysis.get("title", path.stem)
            description = analysis.get("description", "")
            tags = analysis.get("tags", [])
            mood = analysis.get("mood", "unknown")
            scene_type = analysis.get("scene_type", "other")

            # safe filename from title
            safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in title)
            safe_title = safe_title.strip().replace(" ", "-")[:60]
            dest_name = f"{path.stem}_{safe_title}{path.suffix}"
            dest_path = enriched_dir / dest_name

            write_exif_metadata(path, dest_path, title, description, tags)
            record = {
                "run_id": run_id,
                "filename": path.name,
                "enriched_filename": dest_name,
                "enriched_path": str(dest_path),
                "source_path": str(path),
                "title": title,
                "description": description,
                "tags": tags,
                "mood": mood,
                "scene_type": scene_type,
                "title_source": "ai_suggested",
                "description_source": "ai_suggested",
                "approved": False,
                "enriched_at": datetime.now(timezone.utc).isoformat()
            }
            write_sidecar(enriched_dir, dest_path.stem, record)

            with catalog_path.open("a") as f:
                f.write(json.dumps(record) + "\n")

            results.append(record)
            done += 1
            print(f'"{title}"')

        except Exception as e:
            print(f"FAILED: {e}")
            failed += 1

        if args.delay > 0 and i < total:
            time.sleep(args.delay)

    summary = {
        "run_id": run_id,
        "total": total,
        "enriched": done,
        "skipped": skipped,
        "failed": failed,
        "enriched_dir": str(enriched_dir),
        "catalog": str(catalog_path),
        "completed_at": datetime.now(timezone.utc).isoformat()
    }
    done_path.write_text(json.dumps(summary, indent=2))

    print()
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
