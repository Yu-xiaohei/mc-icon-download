# Quick Start

## 1. Enter the directory

```bash
cd /data/data/com.termux/files/home/mc-icon-download
```

## 2. Build local indexes

Icons:

```bash
python3 mc_icon_download.py index --kind icon
```

Textures:

```bash
python3 mc_icon_download.py index --kind texture
```

The script stores them in:

- `cache/icons_index.json`
- `cache/textures_index.json`

## 3. Search assets

Search icons:

```bash
python3 mc_icon_download.py search --kind icon --query diamond_sword
```

Search textures:

```bash
python3 mc_icon_download.py search --kind texture --query stone
```

Exact match:

```bash
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact
```

## 4. Print direct URLs

```bash
python3 mc_icon_download.py urls --kind icon --query Diamond_Sword.png --exact --first
```

## 5. Download one asset

```bash
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

Default output paths:

- `downloads/icon/...`
- `downloads/texture/...`

## 6. Download a batch

Download every icon in a subcategory:

```bash
python3 mc_icon_download.py download \
  --kind icon \
  --category '10. Items' \
  --subcategory '1. Swords' \
  --all
```

## 7. Export results

Export JSON:

```bash
python3 mc_icon_download.py export \
  --kind icon \
  --query sword \
  --output exports/sword-icons.json \
  --format json
```

Export CSV:

```bash
python3 mc_icon_download.py export \
  --kind texture \
  --query stone \
  --output exports/stone-textures.csv \
  --format csv
```
