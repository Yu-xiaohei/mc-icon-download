# mc-icon-download

Small utility for searching and downloading Minecraft icons and textures from `https://ccvaults.com/`.

若您需要查看中文版本说明文档，请查看
[［简体中文.md］](./README_zh.md)

## Features

- Fetches and caches icon and texture indexes
- Searches assets by name, category, or subcategory
- Prints direct original-file URLs
- Exports filtered results to JSON or CSV
- Downloads a single file or a controlled batch
- Uses only the Python standard library

## Requirements

- Python 3.9+

## Repository Layout

- `mc_icon_download.py`: main CLI entry point
- `README.md`: English project overview
- `QUICKSTART.md`: English quick start guide
- `COMMANDS.md`: English command reference
- `AGENT_WORKFLOW.md`: English automation and agent guide
- `API_NOTES.md`: English implementation notes for the remote site
- `README_zh.md`: Chinese overview
- `QUICKSTART_zh.md`: Chinese quick start guide
- `COMMANDS_zh.md`: Chinese command reference
- `AGENT_WORKFLOW_zh.md`: Chinese automation guide
- `API_NOTES_zh.md`: Chinese API notes

## Quick Start

```bash
cd ./mc-icon-download
python3 mc_icon_download.py index --kind icon
python3 mc_icon_download.py index --kind texture
python3 mc_icon_download.py search --kind icon --query Diamond_Sword.png --exact --first
python3 mc_icon_download.py download --kind icon --query Diamond_Sword.png --exact --first
```

## Documentation

- [QUICKSTART.md](./QUICKSTART.md)
- [COMMANDS.md](./COMMANDS.md)
- [AGENT_WORKFLOW.md](./AGENT_WORKFLOW.md)
- [API_NOTES.md](./API_NOTES.md)

Chinese translation:

- [README_zh.md](./README_zh.md)

## Development Notes

- Runtime outputs are intentionally kept out of version control via `.gitignore`.
- The script caches indexes and tokens under `cache/`.
- Downloaded files go to `downloads/` by default.
