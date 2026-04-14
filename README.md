# mc-icon-download

`mc-icon-download` is a small Python CLI for searching, exporting, and downloading Minecraft icons and textures from `https://ccvaults.com/`.

For the Chinese version, see [README_zh.md](./README_zh.md).

## Highlights

- Uses only the Python standard library
- Fetches remote indexes and caches them locally
- Supports icon and texture search by file name or normalized display name
- Prints direct original asset URLs
- Exports filtered results to JSON or CSV
- Downloads one file or a bounded set of matches
- Works well in scripts, local automation, and agent workflows

## Requirements

- Python `3.9+`

## Installation

No dependency installation is required.

```bash
git clone https://github.com/Yu-xiaohei/mc-icon-download.git
cd mc-icon-download
python3 mc_icon_download.py --help
```

On Windows, replace `python3` with `python` if needed.

## Quick Start

Build local indexes:

```bash
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
```

Search for an icon:

```bash
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact --first
```

Search for a texture:

```bash
python3 mc_icon_download.py search --kind texture --query stone --first
```

Print direct download URLs:

```bash
python3 mc_icon_download.py urls --kind icon --query diamond_sword --first
```

Download a matching asset:

```bash
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

Export search results:

```bash
python3 mc_icon_download.py export --kind icon --query sword --format json --output exports/sword.json
python3 mc_icon_download.py export --kind texture --query stone --format csv --output exports/stone.csv
```

## Commands

### `categories`

List icon categories from the remote API.

```bash
python3 mc_icon_download.py categories
python3 mc_icon_download.py categories --json
```

### `index`

Fetch and cache the full icon or texture index.

```bash
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
```

### `search`

Search the cached index, or refresh it before searching.

Common flags:

- `--kind icon|texture`
- `--query <text>`
- `--exact`
- `--category <name>`
- `--subcategory <name>`
- `--refresh`
- `--first`
- `--limit <n>`
- `--json`

Example:

```bash
python3 mc_icon_download.py search --kind icon --query sword --category "10. Items" --limit 5
```

### `urls`

Print raw asset URLs only.

```bash
python3 mc_icon_download.py urls --kind texture --query stone --first
```

### `export`

Export filtered results to `json` or `csv`.

```bash
python3 mc_icon_download.py export --kind icon --query bow --format csv --output exports/bow.csv
```

### `download`

Download one or more matched files.

Important behavior:

- If multiple records match, the command stops unless you use `--first`, `--limit`, or `--all`.
- Output defaults to `downloads/`.

Example:

```bash
python3 mc_icon_download.py download --kind icon --query sword --limit 3
```

## Output Layout

Runtime-generated files are intentionally excluded from version control.

- `cache/`: remote token and local indexes
- `downloads/`: downloaded image files
- `exports/`: JSON and CSV exports
- `test-output/`: local command output samples and ad hoc verification data

## Repository Layout

- [mc_icon_download.py](./mc_icon_download.py): main CLI implementation
- [README.md](./README.md): English overview
- [README_zh.md](./README_zh.md): Chinese overview
- [docs/QUICKSTART.md](./docs/QUICKSTART.md): English quick start
- [docs/COMMANDS.md](./docs/COMMANDS.md): English command reference
- [docs/AGENT_WORKFLOW.md](./docs/AGENT_WORKFLOW.md): notes for automation and agent usage
- [docs/API_NOTES.md](./docs/API_NOTES.md): remote site and API notes
- [docs/QUICKSTART_zh.md](./docs/QUICKSTART_zh.md): Chinese quick start
- [docs/COMMANDS_zh.md](./docs/COMMANDS_zh.md): Chinese command reference
- [docs/AGENT_WORKFLOW_zh.md](./docs/AGENT_WORKFLOW_zh.md): Chinese automation notes
- [docs/API_NOTES_zh.md](./docs/API_NOTES_zh.md): Chinese API notes

## Notes

- The project currently targets `ccvaults.com` and depends on its API shape staying stable.
- Token caching is time-based and refreshed automatically when needed.
- Asset names are normalized from file names by removing extensions and replacing underscores with spaces.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
