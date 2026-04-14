# 快速开始

## 1. 进入目录

```bash
cd /data/data/com.termux/files/home/mc-icon-download
```

## 2. 先拉取索引

图标索引：

```bash
python3 mc_icon_download.py index --kind icon
```

纹理索引：

```bash
python3 mc_icon_download.py index --kind texture
```

这会把结果缓存到：

- `cache/icons_index.json`
- `cache/textures_index.json`

## 3. 搜索素材

搜索图标：

```bash
python3 mc_icon_download.py search --kind icon --query diamond_sword
```

搜索纹理：

```bash
python3 mc_icon_download.py search --kind texture --query stone
```

按精确名称搜索：

```bash
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact
```

## 4. 只拿直链

```bash
python3 mc_icon_download.py urls --kind icon --query diamond_sword --exact
```

## 5. 下载单个素材

```bash
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

默认会下载到：

- `downloads/icon/...`
- `downloads/texture/...`

## 6. 批量下载

下载某个子分类下的全部素材：

```bash
python3 mc_icon_download.py download \
  --kind icon \
  --category '10. Items' \
  --subcategory '1. Swords' \
  --all
```

## 7. 导出结果

导出 JSON：

```bash
python3 mc_icon_download.py export \
  --kind icon \
  --query sword \
  --output exports/sword-icons.json \
  --format json
```

导出 CSV：

```bash
python3 mc_icon_download.py export \
  --kind texture \
  --query stone \
  --output exports/stone-textures.csv \
  --format csv
```
