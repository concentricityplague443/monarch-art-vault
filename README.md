<div align="center">

# 🦋 Monarch Art Vault

### The AI skill that turns your messy photo folders into a print-ready art catalog

**Preserve → Dedupe → Catalog → Organize → Prepare → Publish**

[![MIT License](https://img.shields.io/badge/License-MIT-c9a227.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776ab.svg)](https://python.org)
[![AI Agent Ready](https://img.shields.io/badge/AI%20Agent-Ready-00d4aa.svg)](#installation)
[![Google Sheets](https://img.shields.io/badge/Google%20Sheets-Sync-34a853.svg)](#spreadsheet-export)

<br />

<img src="https://raw.githubusercontent.com/diamitani/monarch-art-vault/main/assets/hero-diagram.svg" alt="Monarch Art Vault workflow" width="700" />

<br /><br />

**Stop losing your art in unnamed folders. Stop uploading duplicates. Stop guessing print sizes.**

*A Monarch skill by [Diamitani Industries](https://github.com/diamitani)*

---

[Quick Start](#-quick-start) • [Features](#-features) • [Spreadsheet Export](#-spreadsheet-export) • [Agent Integration](#-agent-integration) • [Marketplace Publishing](#-marketplace-publishing)

</div>

---

## 🎯 The Problem

Every artist has this folder:

```
Downloads/
  IMG_4521.jpg
  IMG_4521 (1).jpg
  final_final_v2_FINAL.png
  art scan maybe.tiff
  photo of painting.heic
  unnamed-23.jpg
  ...
```

No titles. No metadata. No idea which is the original. Half are duplicates. None are print-ready. You'd need hours to sort through it all.

**Monarch Art Vault fixes this in one command.**

---

## ✨ Features

| Feature | What it does |
|---------|--------------|
| **🔒 Original Preservation** | Archives originals before any changes—never lose your source files |
| **🔍 Smart Deduplication** | SHA-256 for exact dupes, perceptual hashing for near-duplicates |
| **📝 AI Metadata Generation** | Titles, descriptions, tags, alt text—clearly marked as AI suggestions |
| **📁 Auto-Organization** | Creates a clean folder structure: Archive → Catalog → Works → Publish |
| **🖨️ Print Readiness** | Calculates actual print sizes at 300 DPI—no more guessing |
| **📊 Spreadsheet Export** | CSV, Excel, or Google Sheets with all your catalog data |
| **🛒 Marketplace Drafts** | Generate Etsy/Shopify listings—publish only when you approve |
| **🔐 Privacy First** | Strips GPS/sensitive EXIF from public derivatives automatically |

---

## 🚀 Quick Start

### For AI Agents (Claude, GPT, Hermes, etc.)

1. Download or clone this repository
2. Point your agent to `SKILL.md`
3. Say: *"Organize these art photos using Monarch Art Vault"*

### For Developers

```bash
# Clone the repo
git clone https://github.com/diamitani/monarch-art-vault.git
cd monarch-art-vault

# Install optional dependencies
pip install -r scripts/requirements-optional.txt

# Run the cataloger
python scripts/catalog_assets.py ./my-photos --managed-root ./ArtLibrary
```

### One-Liner

```bash
curl -sL https://raw.githubusercontent.com/diamitani/monarch-art-vault/main/scripts/catalog_assets.py | \
  python - ~/Pictures/art-folder --managed-root ~/ArtLibrary
```

---

## 📊 Spreadsheet Export

Export your entire catalog to a spreadsheet with photos, metadata, and print-readiness info.

### CSV Export

```bash
python scripts/export_spreadsheet.py catalog.jsonl --format csv
```

### Excel Export (with formatting)

```bash
pip install openpyxl
python scripts/export_spreadsheet.py catalog.jsonl --format xlsx
```

### Google Sheets Sync

```bash
pip install gspread google-auth
python scripts/export_spreadsheet.py catalog.jsonl --format gsheets
```

<details>
<summary><strong>🔧 Google Sheets Setup</strong></summary>

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project (or select existing)
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **Credentials** → **Create Credentials** → **Service Account**
5. Download the JSON key file
6. Save it to `~/.config/monarch-art-vault/google-service-account.json`
7. Share your Google Sheet with the service account email (found in the JSON)

Or set the environment variable:
```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

</details>

### Downloadable Package

Create a full export package with CSV, Excel, and readme:

```bash
python scripts/export_spreadsheet.py catalog.jsonl --package ./export
```

Output:
```
export/
├── catalog.csv
├── catalog.xlsx
└── README.txt
```

### Spreadsheet Columns

| Column | Description |
|--------|-------------|
| `work_id` | Unique identifier (ART-2026-0001) |
| `status` | needs_review / cataloged / approved / published |
| `title` | Work title (with source: AI/embedded/user) |
| `pixel_width` / `pixel_height` | Dimensions |
| `megapixels` | Calculated size |
| `print_status` | print_ready / conditionally_ready / not_recommended |
| `print_sizes_inches` | Recommended print sizes at 300 DPI |
| `dominant_colors` | Extracted color palette |
| `style_tags` / `subject_tags` | AI-suggested categories |
| `storage_link` | Link to archived file |
| `thumbnail_url` | Preview image link |

---

## 🤖 Agent Integration

Monarch Art Vault is designed for AI agent runtimes. Load `SKILL.md` and the agent will:

1. **Never delete your originals** — archives first, asks questions later
2. **Mark AI guesses clearly** — titles show `ai_suggested` vs `user_confirmed`
3. **Ask before publishing** — marketplace uploads require explicit approval
4. **Preserve provenance** — every decision is logged with timestamp and reason

### Example Commands

```
📸 "Organize these uploaded art photos. Preserve originals, dedupe safely,
    generate metadata drafts, and create a review report."

📁 "Process my Google Drive folder as the 'Summer 2026' collection."

🖨️ "Assess works for 8x10, 11x14, and 16x20 prints. Show me which need
    higher resolution."

🛒 "Create Etsy listing drafts for works ART-2026-0001 through 0005.
    Don't publish yet."
```

### Supported Runtimes

- **Claude** (via system prompt or tools)
- **GPT-4** (via custom instructions)
- **Hermes Agent** (install as skill)
- **LangChain** / **AutoGPT** (as tool definition)
- **Any MCP-compatible agent**

---

## 📂 Folder Structure

```
ArtLibrary/
├── 00_Inbox/                    # Drop files here
├── 01_Archive_Originals/        # Untouched source files
│   └── 2026/RUN-20260723-001/
├── 02_Catalog/                  # Master database
│   ├── catalog.jsonl
│   ├── catalog.csv
│   └── duplicate-groups.json
├── 03_Works/                    # Organized art
│   └── 2026/ART-2026-0001/
│       ├── 01_Master/
│       ├── 02_Alternates/
│       ├── 05_Print_Files/
│       └── metadata.json
├── 04_Review_Required/          # Needs your decision
│   ├── Possible_Duplicates/
│   └── Low_Resolution/
├── 05_Publish_Queue/            # Marketplace staging
│   └── Etsy/Draft/
└── 99_Reports/                  # Run summaries
```

---

## 🛒 Marketplace Publishing

Monarch prepares listings but **never publishes without your approval**.

### Supported Platforms

| Platform | Drafting | Direct Upload |
|----------|----------|---------------|
| Etsy | ✅ | 🔜 Coming soon |
| Shopify | ✅ | 🔜 Coming soon |
| Printful | ✅ | 🔜 Coming soon |
| Printify | ✅ | 🔜 Coming soon |
| Fine Art America | ✅ | 🔜 Coming soon |
| Squarespace | ✅ | 🔜 Coming soon |
| WooCommerce | ✅ | 🔜 Coming soon |

### Approval Gates

Before any external action, you must approve:

- [ ] Platform connection
- [ ] Asset files to upload
- [ ] Listing copy (title, description, tags)
- [ ] Price and fulfillment settings
- [ ] Final publish action

---

## 🔐 Safety Guarantees

| Promise | Implementation |
|---------|----------------|
| **Originals are immutable** | Copied to archive before any processing |
| **No silent deletions** | AI similarity ≠ deletion; requires human review |
| **AI suggestions are labeled** | Every field has `source` and `confidence` |
| **No stealth publishing** | Every external action requires explicit approval |
| **Privacy by default** | GPS/face data stripped from public derivatives |

---

## 📖 Full Documentation

| File | Description |
|------|-------------|
| [`SKILL.md`](SKILL.md) | Complete agent instructions |
| [`SOUL.md`](SOUL.md) | Persistent identity for ROSTR runtimes |
| [`manifest.json`](manifest.json) | Capabilities and permissions |
| [`references/metadata-schema.json`](references/metadata-schema.json) | Work record JSON schema |
| [`references/folder-structure.md`](references/folder-structure.md) | Directory layout spec |
| [`references/approval-policy.md`](references/approval-policy.md) | What requires human approval |
| [`examples/commands.md`](examples/commands.md) | Sample agent prompts |

---

## 🛠️ Development

```bash
# Run tests
python -m pytest tests/

# Validate package structure
python scripts/validate_package.py

# Check catalog script
python scripts/catalog_assets.py --help
```

### Requirements

**Core (stdlib only):**
- Python 3.10+

**Optional (enhanced features):**
```bash
pip install pillow      # Image dimensions + EXIF
pip install imagehash   # Perceptual duplicate detection
pip install openpyxl    # Excel export
pip install gspread google-auth  # Google Sheets sync
```

---

## 🤝 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License — see [`LICENSE`](LICENSE)

Brand usage: "Monarch" and "Diamitani Industries" are trademarks. See [`NOTICE.md`](NOTICE.md).

---

<div align="center">

**Built with 🦋 by [Diamitani Industries](https://github.com/diamitani)**

*Stop losing art. Start selling prints.*

<br />

[⭐ Star this repo](https://github.com/diamitani/monarch-art-vault) • [🐛 Report Bug](https://github.com/diamitani/monarch-art-vault/issues) • [💡 Request Feature](https://github.com/diamitani/monarch-art-vault/issues)

</div>
