# Rich Color Support

A Python library providing curated color palettes for rich terminal applications with descriptive color names.

## Features

- **Multiple Color Sets**: Choose from 8, 16, 32, 64, or the full palette of 200+ colors
- **Descriptive Names**: Easy-to-remember color names like `NAVY_BLUE`, `HOT_PINK`, `CHARTREUSE`
- **Color Rotation**: Built-in color rotator for cycling through colors without repetition
- **Rich Integration**: Designed to work seamlessly with the [Rich](https://github.com/Textualize/rich) library

## Installation

```bash
pip install rich-color-support
```

## Quick Start

```python
from rich_color_support import RichColors8, RichColors16, get_color_set, RichColorRotator
from rich.console import Console

console = Console()

# Use predefined color sets
console.print("Hello World!", style=f"color {RichColors8.RED}")
console.print("Colorful text!", style=f"color {RichColors16.CHARTREUSE}")

# Get a dynamic color set
colors = get_color_set(32)
for i, color in enumerate(colors):
    console.print(f"Line {i}", style=f"color {color}")

# Use color rotator for automatic cycling
rotator = RichColorRotator(8)
for i in range(20):
    color = rotator.pick()
    console.print(f"Message {i}", style=f"color {color}")
```

## Color Sets

| Class          | Colors | Description                            |
|----------------|--------|----------------------------------------|
| `RichColors8`  | 8      | Essential high-contrast colors         |
| `RichColors16` | 16     | Popular well-distinguished colors      |
| `RichColors32` | 32     | Readable colors for rich interfaces    |
| `RichColors64` | 64     | Professional colors for advanced apps  |
| `RichColors`   | 200+   | Complete palette of descriptive colors |

## Usage Examples

### Basic Color Usage

```python
from rich_color_support import RichColors16
from rich.console import Console

console = Console()

# Direct color usage
console.print("Error message", style=f"color {RichColors16.RED}")
console.print("Success message", style=f"color {RichColors16.GREEN}")
console.print("Warning message", style=f"color {RichColors16.YELLOW}")
```

### Dynamic Color Selection

```python
from rich_color_support import get_color_set

# Get exactly 10 colors
colors = get_color_set(10)

# Get colors for many items (returns full palette if > 64)
colors = get_color_set(100)
```

### Color Rotation

```python
from rich_color_support import RichColorRotator

# Create rotator with 16 colors
rotator = RichColorRotator(16)

# Colors won't repeat until all 16 are used
for item in my_items:
    color = rotator.pick()
    console.print(item, style=f"color {color}")
```

## API Reference

### Color Classes

All color classes inherit from `RichColorsBase` (which extends `StrEnum`):

- **RichColors8**: `RED`, `GREEN`, `BLUE`, `YELLOW`, `MAGENTA`, `CYAN`, `WHITE`, `ORANGE`
- **RichColors16**: Adds `BRIGHT_RED`, `DARK_GREEN`, `ROYAL_BLUE`, `GOLD`, `PURPLE`, `DARK_CYAN`, `LIGHT_CORAL`, `CHARTREUSE`
- **RichColors32**: Adds 16 more colors including `NAVY_BLUE`, `HOT_PINK`, `VIOLET`, `SALMON`
- **RichColors64**: Adds 32 more professional colors
- **RichColors**: Complete palette with 200+ descriptive color names

### Functions

#### `get_color_set(size: int) -> List[RichColorsBase]`

Returns a color set of the specified size:

- `size <= 8`: Returns subset of RichColors8
- `size <= 16`: Returns RichColors16
- `size <= 32`: Returns RichColors32
- `size <= 64`: Returns RichColors64
- `size > 64`: Returns complete RichColors palette

### Classes

#### `RichColorRotator(size: int)`

A utility class for cycling through colors without repetition.

**Methods:**

- `pick() -> RichColorsBase`: Returns next color in rotation, reshuffles when exhausted

## Requirements

- Python 3.11+
- Rich 13.0.0+

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [GitHub Repository](https://github.com/allen2c/rich-color-support)
- [Documentation](https://allen2c.github.io/rich-color-support)
- [Bug Tracker](https://github.com/allen2c/rich-color-support/issues)
