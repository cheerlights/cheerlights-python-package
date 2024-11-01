[![Upload Python Package](https://github.com/cheerlights/cheerlights-python-package/actions/workflows/python-publish.yml/badge.svg)](https://github.com/cheerlights/cheerlights-python-package/actions/workflows/python-publish.yml)

[![PyPI - Version](https://img.shields.io/pypi/v/cheerlights_api)](https://pypi.org/project/cheerlights-api/)

# CheerLights API Python Package

A Python package to interact with the CheerLights API. It allows users to get the current CheerLights color, retrieve the color history, and perform various color-related utilities.

## Installation

You can install the package using pip:

```bash
pip install cheerlights_api
```

## Usage Examples

```python
import cheerlights_api

# Get the current color name and hex code
current_color = cheerlights_api.get_current_color()
print(current_color)  # Example: {'color': 'red', 'hex': '#FF0000'}

# Get the current color name
color_name = cheerlights_api.get_current_color_name()
print(color_name)  # Example: 'red'

# Get the current hex code
hex_code = cheerlights_api.get_current_hex()
print(hex_code)  # Example: '#FF0000'

# Get the history of colors
history = cheerlights_api.get_color_history(5)
for entry in history:
    print(f"{entry['timestamp']}: {entry['color']} ({entry['hex']})")

# Convert a color name to hex
hex_code = cheerlights_api.color_name_to_hex('green')
print(hex_code)  # '#00FF00'

# Convert hex code to RGB
rgb = cheerlights_api.hex_to_rgb('#00FF00')
print(rgb)  # (0, 255, 0)

# Check if a color is valid
is_valid = cheerlights_api.is_valid_color('purple')
print(is_valid)  # True
```
