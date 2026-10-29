# Reference

Everything `cheerlights_api` exports, as of version 0.2.0.
Every function that reads the feed makes one HTTPS request to `https://api.thingspeak.com/channels/1417/feed.json` with a 10 second timeout.

## Reading the feed

### `get_current_color() -> Color`

The current color as `{"color": "red", "hex": "#ff0000"}`.
The name is lowercase; the HEX value is the one the feed publishes, lowercase with a leading `#`.

Raises `requests.RequestException` (for example `requests.HTTPError` or `requests.Timeout`) when the feed cannot be reached or answers with an error, and `LookupError` when it returns no color.

### `get_current_color_name() -> str`

The name of the current color, for example `"red"`.
Same errors as `get_current_color()`.

### `get_current_hex() -> str`

The HEX value of the current color, for example `"#ff0000"`.
Same errors as `get_current_color()`.

### `get_color_history(count: int = 10) -> list[ColorChange]`

The last `count` color changes, oldest first, each as `{"color": "cyan", "hex": "#00ffff", "timestamp": "2026-10-29T17:01:36Z"}`.
The timestamp is the time the color was set, in UTC, ISO 8601.

`count` must be a whole number from 1 to 8000 (`MAX_HISTORY`, the most the feed returns at once); anything else raises `ValueError` before any request is made.
Network errors are the same as for `get_current_color()`.

Very old entries in the feed have no HEX value; for those the HEX value comes from the palette.

## The palette

### `COLORS: dict[str, str]`

The 11 official CheerLights colors and their HEX values:

| Name | HEX |
|---|---|
| red | `#ff0000` |
| green | `#008000` |
| blue | `#0000ff` |
| cyan | `#00ffff` |
| white | `#ffffff` |
| oldlace | `#fdf5e6` |
| purple | `#800080` |
| magenta | `#ff00ff` |
| yellow | `#ffff00` |
| orange | `#ffa500` |
| pink | `#ffc0cb` |

### `ALIASES: dict[str, str]`

Older names that still mean a CheerLights color: `warmwhite` is `oldlace`.

### `color_name_to_hex(color_name: str) -> str | None`

The HEX value of a color name, or `None` when the name is not a CheerLights color.
Case and spaces do not matter, and aliases count: `"Old Lace"` and `"warmwhite"` both give `"#fdf5e6"`.

### `is_valid_color(color_name: str) -> bool`

Whether a name is a CheerLights color, with the same rules as `color_name_to_hex()`.

### `hex_to_rgb(hex_code: str) -> tuple[int, int, int]`

A HEX value as a `(red, green, blue)` tuple of 0 to 255: `hex_to_rgb("#ffa500")` gives `(255, 165, 0)`.
The `#` is optional; anything other than six hexadecimal digits raises `ValueError`.

## Types and constants

- `Color`: a `TypedDict` with `color` and `hex`.
- `ColorChange`: a `TypedDict` with `color`, `hex`, and `timestamp`.
- `CHEERLIGHTS_FEED_URL`, `TIMEOUT` (10.0 seconds), `MAX_HISTORY` (8000).
- `__version__`: the installed version.

The functions can also be imported from `cheerlights_api.cheerlights_api`, the path versions before 0.2.0 used.

## Changes in 0.2.0

These change what 0.1.2 returned:

- `green` is `#008000`, the CheerLights green; 0.1.2 gave `#00ff00`.
- HEX values are lowercase everywhere, matching the feed, so `color_name_to_hex(get_current_color_name()) == get_current_hex()` holds; 0.1.2 returned uppercase from `color_name_to_hex()`.
- `get_color_history()` checks `count` and raises `ValueError` outside 1 to 8000; 0.1.2 passed any value to the feed.
- `hex_to_rgb()` raises `ValueError` for anything but six hexadecimal digits.
- An empty feed raises `LookupError` with a message; 0.1.2 raised a bare `IndexError` (also a `LookupError`).
