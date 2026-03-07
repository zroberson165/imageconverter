# imageconverter

A command line tool to batch convert, compress, and resize images.
Supports HEIC, JPG, PNG, and RAW formats (NEF, CR2, ARW).

## Installation

Requires Python and pip.
```bash
git clone https://github.com/zroberson165/imageconverter
cd imageconverter
pip install .
```

## Usage
```bash
imgconvert --input /path/to/images --output /path/to/save --format .jpg
```

## Options

| Flag | Description | Required |
|------|-------------|----------|
| `--input` | Folder of images to convert | Yes |
| `--output` | Folder to save converted images | Yes |
| `--format` | Output format (.jpg, .png, .jpeg) | Yes |
| `--quality` | Output quality 0-100 | No |
| `--resize` | Resize by percentage e.g. 50 for 50% | No |
| `--recursive` | Process subfolders | No |
| `--recommend` | Analyze images and suggest settings | No |

Run `imgconvert --help` for a full list of options.
