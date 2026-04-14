# Commands

## `categories`

List remote categories.

```bash
python3 mc_icon_download.py categories
python3 mc_icon_download.py categories --json
```

## `index`

Fetch and cache an index.

```bash
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
```

## `search`

Search the local cache. If the cache is missing, the script fetches it automatically.

```bash
python3 mc_icon_download.py search --kind icon --query sword
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact
python3 mc_icon_download.py search --kind icon --category '10. Items' --subcategory '1. Swords'
python3 mc_icon_download.py search --kind texture --query stone --limit 20
python3 mc_icon_download.py search --kind icon --query potion --json
```

Common flags:

- `--kind icon|texture`
- `--query`
- `--exact`
- `--category`
- `--subcategory`
- `--refresh`
- `--first`
- `--limit`
- `--json`

## `urls`

Print direct original-file URLs for matched records.

```bash
python3 mc_icon_download.py urls --kind icon --query Diamond_Sword.png --exact --first
python3 mc_icon_download.py urls --kind texture --query stone.png --exact --first
```

## `export`

Export matched records to `json` or `csv`.

```bash
python3 mc_icon_download.py export \
  --kind icon \
  --query sword \
  --output exports/sword-icons.json \
  --format json
```

```bash
python3 mc_icon_download.py export \
  --kind texture \
  --query stone \
  --output exports/stone-textures.csv \
  --format csv
```

## `download`

Download matched records.

Single file:

```bash
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

Limit the number of files:

```bash
python3 mc_icon_download.py download --kind texture --query stone --limit 5
```

Batch download:

```bash
python3 mc_icon_download.py download \
  --kind icon \
  --category '10. Items' \
  --subcategory '1. Swords' \
  --all
```

Custom output directory:

```bash
python3 mc_icon_download.py download \
  --kind icon \
  --query Diamond_Sword.png \
  --exact \
  --first \
  --output-dir /data/data/com.termux/files/home/my-downloads
```

Note:

- If more than one record matches and you do not pass `--first`, `--limit`, or `--all`, the script stops to avoid accidental bulk downloads.
