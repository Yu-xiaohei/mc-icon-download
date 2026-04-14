# Agent Workflow

This document is for other agents, scripts, or automation flows that need to reuse the downloader without reverse-engineering the site again.

## Minimal Integration Path

An agent only needs three steps:

1. Enter the directory
2. Ensure the relevant index exists
3. Call `search`, `urls`, `export`, or `download`

Example:

```bash
cd /data/data/com.termux/files/home/mc-icon-download
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py search --kind icon --query diamond_sword --json
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

## Recommended Flows

### Scenario 1: download one exact item

```bash
python3 mc_icon_download.py search --kind icon --query 'Diamond_Sword.png' --exact --json
python3 mc_icon_download.py download --kind icon --query 'Diamond_Sword.png' --exact --first
```

### Scenario 2: user asks for a small themed batch

```bash
python3 mc_icon_download.py search --kind icon --query sword --json
python3 mc_icon_download.py download --kind icon --query sword --limit 10
```

### Scenario 3: user only wants the direct links

```bash
python3 mc_icon_download.py urls --kind icon --query Diamond_Sword.png --exact --first
```

### Scenario 4: downstream processing or further development

Export first:

```bash
python3 mc_icon_download.py export \
  --kind icon \
  --query sword \
  --output exports/sword.json \
  --format json
```

Then let the next tool or agent consume the exported JSON.

## Operational Notes

- Prefer this script over scraping the front-end again.
- If the user requests fresh remote data, add `--refresh`.
- If a download command reports multiple matches, refine with `--query`, `--exact`, `--first`, or `--limit`.
- Default download output is `downloads/`.

## Reusable Command Templates

Download one exact icon:

```bash
python3 mc_icon_download.py download --kind icon --query '{FILENAME}' --exact --first
```

Export links for later processing:

```bash
python3 mc_icon_download.py export --kind icon --query '{QUERY}' --output exports/result.json --format json
```

Print one exact texture URL:

```bash
python3 mc_icon_download.py urls --kind texture --query '{FILENAME}' --exact --first
```

## Extension Ideas

- Add `--regex`
- Add alias mapping for common names
- Add concurrent batch downloads
- Add output adapters for a custom asset pipeline

Primary file:

- `mc_icon_download.py`

Important runtime paths:

- `cache/icons_index.json`
- `cache/textures_index.json`
- `downloads/`
