# CheerLights API for Python

A small Python package that reads the live CheerLights color, its recent history, and the CheerLights palette.

[![PyPI](https://img.shields.io/pypi/v/cheerlights-api)](https://pypi.org/project/cheerlights-api/) [![Python](https://img.shields.io/pypi/pyversions/cheerlights-api)](https://pypi.org/project/cheerlights-api/) [![CI](https://github.com/cheerlights/cheerlights-python-package/actions/workflows/ci.yml/badge.svg)](https://github.com/cheerlights/cheerlights-python-package/actions/workflows/ci.yml) [![License: MIT](https://img.shields.io/badge/license-MIT-yellow)](https://github.com/cheerlights/cheerlights-python-package/blob/main/LICENSE)

[CheerLights](https://cheerlights.com) is a global network of lights that all show the same color, set by anyone on the [CheerLights Discord](https://cheerlights.com/discord).
This package reads the public CheerLights feed (ThingSpeak channel 1417), so a Python script on a laptop or a Raspberry Pi can follow the color.
It needs no API key and depends only on `requests`.

## Quick start

Install it from [PyPI](https://pypi.org/project/cheerlights-api/) (Python 3.10 or later):

```bash
pip install cheerlights-api
```

Then read the current color:

```python
import cheerlights_api

print(cheerlights_api.get_current_color())
```

## Example

```python
import cheerlights_api

current = cheerlights_api.get_current_color()
print(current)
print(cheerlights_api.hex_to_rgb(current["hex"]))

for change in cheerlights_api.get_color_history(3):
    print(change)
```

Output from version 0.2.0 on 2026-10-29:

```text
{'color': 'red', 'hex': '#ff0000'}
(255, 0, 0)
{'color': 'cyan', 'hex': '#00ffff', 'timestamp': '2026-10-29T17:01:36Z'}
{'color': 'purple', 'hex': '#800080', 'timestamp': '2026-10-29T17:20:53Z'}
{'color': 'red', 'hex': '#ff0000', 'timestamp': '2026-10-29T18:00:53Z'}
```

The `(255, 0, 0)` tuple is what an RGB LED or a NeoPixel library takes.

## Features

- The current color as a name and a HEX value: `get_current_color()`, `get_current_color_name()`, `get_current_hex()`.
- The last 1 to 8000 color changes with the time each was set, oldest first: `get_color_history(count)`.
- The 11 official CheerLights colors with their HEX values, as the feed publishes them: `COLORS`.
- Name and HEX helpers: `color_name_to_hex("Old Lace")` gives `#fdf5e6`, `hex_to_rgb("#ffa500")` gives `(255, 165, 0)`, `is_valid_color("pink")` gives `True`.
- Type hints throughout, checked with mypy in strict mode.
- A 10 second timeout on every request, and clear errors: `requests` exceptions when the feed cannot be reached, `LookupError` when it returns no color, `ValueError` for bad input.

## Limits

- It reads the color; it cannot set it. Anyone sets the color with the `/cheerlights` command on the [CheerLights Discord](https://cheerlights.com/discord).
- It polls the feed. For a light that changes the moment the color does, subscribe to MQTT instead: broker `mqtt.cheerlights.com`, port 1883, topic `cheerlights` for the name or `hex` for the HEX value.
- History comes back oldest first, the order the feed returns it.

## Documentation

- [Reference](https://github.com/cheerlights/cheerlights-python-package/blob/main/docs/reference.md): every function, its return value, and its errors.
- [Changes in 0.2.0](https://github.com/cheerlights/cheerlights-python-package/blob/main/docs/reference.md#changes-in-020): what changed from 0.1.2, including the fixed green and lowercase HEX values.
- [CheerLights](https://cheerlights.com): the project, the feeds, and how to build your first light.

## Development

```bash
git clone https://github.com/cheerlights/cheerlights-python-package
cd cheerlights-python-package
uv sync
uv run pytest            # offline, against a fake feed
uv run pytest -m live    # one check against the real feed
uv run ruff check . && uv run mypy src
```

## License

MIT. See [LICENSE](https://github.com/cheerlights/cheerlights-python-package/blob/main/LICENSE).
