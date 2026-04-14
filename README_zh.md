# mc-icon-download

`mc-icon-download` 是一个基于 Python 的命令行小工具，用于从 `https://ccvaults.com/` 搜索、导出并下载 Minecraft 图标和纹理资源。

英文说明请见 [README.md](./README.md)。

## 特性

- 仅使用 Python 标准库，不依赖第三方包
- 可从远端拉取索引并缓存到本地
- 支持按文件名或规范化名称搜索图标与纹理
- 可直接输出原始资源直链
- 支持将筛选结果导出为 JSON 或 CSV
- 支持下载单个资源，或受控批量下载
- 适合脚本、自动化流程和 Agent 调用

## 环境要求

- Python `3.9+`

## 安装

无需安装额外依赖。

```bash
git clone https://github.com/Yu-xiaohei/mc-icon-download.git
cd mc-icon-download
python3 mc_icon_download.py --help
```

如果你在 Windows 上使用，也可以把 `python3` 替换为 `python`。

## 快速开始

先建立本地索引：

```bash
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
```

搜索某个图标：

```bash
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact --first
```

搜索某个纹理：

```bash
python3 mc_icon_download.py search --kind texture --query stone --first
```

输出资源直链：

```bash
python3 mc_icon_download.py urls --kind icon --query diamond_sword --first
```

下载匹配资源：

```bash
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

导出查询结果：

```bash
python3 mc_icon_download.py export --kind icon --query sword --format json --output exports/sword.json
python3 mc_icon_download.py export --kind texture --query stone --format csv --output exports/stone.csv
```

## 命令说明

### `categories`

列出远端 API 返回的图标分类。

```bash
python3 mc_icon_download.py categories
python3 mc_icon_download.py categories --json
```

### `index`

抓取并缓存完整的图标或纹理索引。

```bash
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
```

### `search`

搜索本地缓存索引，或搜索前先刷新索引。

常用参数：

- `--kind icon|texture`
- `--query <文本>`
- `--exact`
- `--category <分类名>`
- `--subcategory <子分类名>`
- `--refresh`
- `--first`
- `--limit <数量>`
- `--json`

示例：

```bash
python3 mc_icon_download.py search --kind icon --query sword --category "10. Items" --limit 5
```

### `urls`

仅输出资源原始下载链接。

```bash
python3 mc_icon_download.py urls --kind texture --query stone --first
```

### `export`

将筛选结果导出为 `json` 或 `csv`。

```bash
python3 mc_icon_download.py export --kind icon --query bow --format csv --output exports/bow.csv
```

### `download`

下载一个或多个匹配文件。

需要注意：

- 如果匹配到多个结果，而你没有指定 `--first`、`--limit` 或 `--all`，命令会直接停止，避免误下载。
- 输出目录默认是 `downloads/`。

示例：

```bash
python3 mc_icon_download.py download --kind icon --query sword --limit 3
```

## 输出目录说明

运行时生成的文件默认不会加入版本控制。

- `cache/`
  远端 token 与本地索引缓存
- `downloads/`
  下载得到的图片文件
- `exports/`
  导出的 JSON / CSV 文件
- `test-output/`
  本地命令输出样例和临时验证结果

## 仓库结构

- [mc_icon_download.py](./mc_icon_download.py)
  主 CLI 实现
- [README.md](./README.md)
  英文说明
- [README_zh.md](./README_zh.md)
  中文说明
- [docs/QUICKSTART.md](./docs/QUICKSTART.md)
  英文快速开始
- [docs/COMMANDS.md](./docs/COMMANDS.md)
  英文命令参考
- [docs/AGENT_WORKFLOW.md](./docs/AGENT_WORKFLOW.md)
  自动化与 Agent 使用说明
- [docs/API_NOTES.md](./docs/API_NOTES.md)
  远端站点与 API 说明
- [docs/QUICKSTART_zh.md](./docs/QUICKSTART_zh.md)
  中文快速开始
- [docs/COMMANDS_zh.md](./docs/COMMANDS_zh.md)
  中文命令参考
- [docs/AGENT_WORKFLOW_zh.md](./docs/AGENT_WORKFLOW_zh.md)
  中文 Agent 工作流说明
- [docs/API_NOTES_zh.md](./docs/API_NOTES_zh.md)
  中文 API 说明

## 备注

- 该工具当前依赖 `ccvaults.com` 的接口结构保持稳定。
- token 采用本地缓存并按时间自动刷新。
- 资源显示名称来自文件名，会去掉扩展名并将下划线替换为空格。

## 许可证

本项目采用 MIT License，详见 [LICENSE](./LICENSE)。
