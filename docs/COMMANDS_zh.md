# 命令说明

## `categories`

列出远程站点的分类。

```bash
python3 mc_icon_download.py categories
python3 mc_icon_download.py categories --json
```

## `index`

拉取并缓存索引。

```bash
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
```

## `search`

搜索缓存索引；如果缓存不存在，会自动拉取。

```bash
python3 mc_icon_download.py search --kind icon --query sword
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact
python3 mc_icon_download.py search --kind icon --category '10. Items' --subcategory '1. Swords'
python3 mc_icon_download.py search --kind texture --query stone --limit 20
python3 mc_icon_download.py search --kind icon --query potion --json
```

常用参数：

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

输出匹配结果的原图直链。

```bash
python3 mc_icon_download.py urls --kind icon --query Diamond_Sword.png --exact
python3 mc_icon_download.py urls --kind texture --query stone --first
```

## `export`

导出为 `json` 或 `csv`。

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

下载匹配结果。

单个下载：

```bash
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

限制数量：

```bash
python3 mc_icon_download.py download --kind texture --query stone --limit 5
```

批量：

```bash
python3 mc_icon_download.py download \
  --kind icon \
  --category '10. Items' \
  --subcategory '1. Swords' \
  --all
```

自定义输出目录：

```bash
python3 mc_icon_download.py download \
  --kind icon \
  --query Diamond_Sword.png \
  --exact \
  --first \
  --output-dir /data/data/com.termux/files/home/my-downloads
```

注意：

- 如果匹配到了多个结果，而你没有加 `--first`、`--limit` 或 `--all`，脚本会拒绝下载，防止误下。
