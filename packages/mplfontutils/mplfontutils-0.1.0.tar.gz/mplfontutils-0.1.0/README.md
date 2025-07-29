# mplfontutils

A utility package for testing and loading fonts in matplotlib.

## Installation

```shell
pip install git+https://github.com/xsjk/mplfontutils.git
```

## Usage

### Command Line

Test which fonts can display specific text:

```shell
python -m mplfontutils "Hello 世界"
```

### Python API

```python
from mplfontutils import find_available_fonts, load_fonts_from_directory

# Load fonts from directory
load_fonts_from_directory("/path/to/fonts")

# Find compatible fonts
fonts = find_available_fonts("中文测试")
print(f"Found {len(fonts)} compatible fonts")
```

## License

[MIT License](LICENSE)
