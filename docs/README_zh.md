> 这个目录提供一个独立的小工具，用来从 `https://ccvaults.com/` 获取 Minecraft 图标和纹理的名称、直链，并直接下载原图。

英文文档请见 [[README]() ]

核心脚本：

- `mc_icon_download.py`

相关文档：

- [快速开始.md](./docs/QUICKSTART_zh.md)
- [命令使用.md](./docs/COMMANDS_zh.md)
- [Agent 工作流.md](./docs/AGENT_WORKFLOW_zh.md)
- [API 接口说明.md](./docs/API_NOTES_zh.md)

设计目标：

- 不依赖第三方 Python 库
- 可以先建立本地索引，再离线搜索
- 可以导出 JSON 或 CSV 给其他脚本、Agent、流水线使用
- 可以稳定生成原图直链，而不是依赖浏览器手点

最低要求：

- Python 3.9+

使用运行：

```bash
cd ./mc-icon-download
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
python3 mc_icon_download.py search --kind icon --query diamond_sword
```
