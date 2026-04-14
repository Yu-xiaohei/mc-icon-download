# Agent 工作流

这份文档是给后续其他 Agent、脚本代理或自动化任务用的。目标是让它们最快接入，不需要重新分析站点。

## 最短接入路径

任何 Agent 只需要执行下面三步：

1. 进入目录
2. 确保索引存在
3. 调用 `search`、`urls`、`download` 之一

示例：

```bash
cd /data/data/com.termux/files/home/mc-icon-download
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py search --kind icon --query diamond_sword --json
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

## 推荐给 Agent 的固定流程

### 场景 1：用户说“下载某个具体物品”

建议流程：

```bash
python3 mc_icon_download.py search --kind icon --query 'Diamond_Sword.png' --exact --json
python3 mc_icon_download.py download --kind icon --query 'Diamond_Sword.png' --exact --first
```

### 场景 2：用户只说“下载一些 sword 相关图标”

建议流程：

```bash
python3 mc_icon_download.py search --kind icon --query sword --json
python3 mc_icon_download.py download --kind icon --query sword --limit 10
```

### 场景 3：用户要直链，不要下载

建议流程：

```bash
python3 mc_icon_download.py urls --kind icon --query Diamond_Sword.png --exact
```

### 场景 4：用户要做二次开发

先导出 JSON：

```bash
python3 mc_icon_download.py export \
  --kind icon \
  --query sword \
  --output exports/sword.json \
  --format json
```

然后任何 Agent 都可以直接消费导出的 JSON。

## 给 Agent 的注意事项

- 先优先用本脚本，不要重复去逆向前端。
- 如果只需要搜名称和链接，优先用 `search --json` 或 `export --format json`。
- 如果要稳定工作，先执行一次 `index --kind icon` 和 `index --kind texture`。
- 如果用户说“拿最新索引”，加 `--refresh`。
- 如果下载命令返回“多个结果”，说明要补 `--first`、`--limit` 或更精确的 `--query`。

## 适合 Agent 直接复用的命令模板

精确下载一个图标：

```bash
python3 mc_icon_download.py download --kind icon --query '{FILENAME}' --exact --first
```

导出某类图标的链接：

```bash
python3 mc_icon_download.py export --kind icon --query '{QUERY}' --output exports/result.json --format json
```

打印单个纹理原图直链：

```bash
python3 mc_icon_download.py urls --kind texture --query '{FILENAME}' --exact --first
```

## 如果需要继续开发

推荐扩展方向：

- 增加 `--regex`
- 增加名称别名映射
- 增加按文件更新时间筛选
- 增加并发批量下载
- 增加把导出结果转换成你自己的资产库格式

主入口文件：

- `mc_icon_download.py`

主要缓存位置：

- `cache/icons_index.json`
- `cache/textures_index.json`

默认下载目录：

- `downloads/`
