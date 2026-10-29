"""Read the live CheerLights color and its history from the public feed (ThingSpeak channel 1417)."""

from __future__ import annotations

from typing import Any, TypedDict

import requests

CHEERLIGHTS_FEED_URL = "https://api.thingspeak.com/channels/1417/feed.json"
TIMEOUT = 10.0
"""Seconds to wait for the feed before giving up."""
MAX_HISTORY = 8000
"""The most changes the feed returns in one request."""

COLORS: dict[str, str] = {
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "cyan": "#00ffff",
    "white": "#ffffff",
    "oldlace": "#fdf5e6",
    "purple": "#800080",
    "magenta": "#ff00ff",
    "yellow": "#ffff00",
    "orange": "#ffa500",
    "pink": "#ffc0cb",
}
"""The official CheerLights colors and their HEX values, as the feed publishes them."""

ALIASES: dict[str, str] = {"warmwhite": "oldlace"}
"""Older names that still mean a CheerLights color."""


class Color(TypedDict):
    color: str
    hex: str


class ColorChange(TypedDict):
    color: str
    hex: str
    timestamp: str


def _normalize(name: str) -> str:
    key = name.strip().lower().replace(" ", "")
    return ALIASES.get(key, key)


def _feed(results: int) -> list[dict[str, Any]]:
    response = requests.get(CHEERLIGHTS_FEED_URL, params={"results": results}, timeout=TIMEOUT)
    response.raise_for_status()
    feeds: list[dict[str, Any]] = response.json()["feeds"]
    return feeds


def _hex(entry: dict[str, Any]) -> str:
    value = entry.get("field2")
    if value:
        return str(value).strip().lower()
    return COLORS.get(_normalize(str(entry.get("field1") or "")), "")


def get_current_color() -> Color:
    """
    Get the current CheerLights color.

    Returns:
        A dict with the color name and its HEX value, for example {'color': 'red', 'hex': '#ff0000'}.

    Raises:
        requests.RequestException: The feed could not be reached or answered with an error.
        LookupError: The feed returned no color.
    """
    feeds = _feed(1)
    if not feeds:
        raise LookupError("The CheerLights feed returned no color")
    entry = feeds[-1]
    return {"color": str(entry["field1"]).strip().lower(), "hex": _hex(entry)}


def get_current_hex() -> str:
    """Get the HEX value of the current CheerLights color, for example '#ff0000'."""
    return get_current_color()["hex"]


def get_current_color_name() -> str:
    """Get the name of the current CheerLights color, for example 'red'."""
    return get_current_color()["color"]


def get_color_history(count: int = 10) -> list[ColorChange]:
    """
    Get the most recent CheerLights color changes, oldest first.

    Args:
        count: How many changes to get, 1 to 8000.

    Returns:
        A list of dicts with the color name, its HEX value, and the time it was set (UTC, ISO 8601).

    Raises:
        ValueError: count is not a whole number from 1 to 8000.
        requests.RequestException: The feed could not be reached or answered with an error.
    """
    if isinstance(count, bool) or not isinstance(count, int) or not 1 <= count <= MAX_HISTORY:
        raise ValueError(f"count must be a whole number from 1 to {MAX_HISTORY}, got {count!r}")
    return [
        {"color": str(entry["field1"]).strip().lower(), "hex": _hex(entry), "timestamp": entry["created_at"]}
        for entry in _feed(count)
    ]


def color_name_to_hex(color_name: str) -> str | None:
    """
    Get the HEX value of a CheerLights color name, for example 'green' gives '#008000'.

    Case and spaces do not matter ('Old Lace' works). Returns None for a name that is not a CheerLights color.
    """
    return COLORS.get(_normalize(color_name))


def hex_to_rgb(hex_code: str) -> tuple[int, int, int]:
    """
    Convert a HEX value such as '#ffa500' (with or without the '#') to an (red, green, blue) tuple.

    Raises:
        ValueError: The value is not six hexadecimal digits.
    """
    digits = hex_code.strip().lstrip("#")
    if len(digits) != 6 or any(c not in "0123456789abcdefABCDEF" for c in digits):
        raise ValueError(f"not a HEX color: {hex_code!r}")
    return int(digits[0:2], 16), int(digits[2:4], 16), int(digits[4:6], 16)


def is_valid_color(color_name: str) -> bool:
    """Check whether a name is a CheerLights color. Case and spaces do not matter."""
    return _normalize(color_name) in COLORS
