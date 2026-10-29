"""Read the live CheerLights color, its history, and the CheerLights palette."""

from importlib.metadata import PackageNotFoundError, version

from .cheerlights_api import (
    ALIASES,
    CHEERLIGHTS_FEED_URL,
    COLORS,
    Color,
    ColorChange,
    color_name_to_hex,
    get_color_history,
    get_current_color,
    get_current_color_name,
    get_current_hex,
    hex_to_rgb,
    is_valid_color,
)

try:
    __version__ = version("cheerlights-api")
except PackageNotFoundError:  # running from a source tree that is not installed
    __version__ = "0.0.0"

__all__ = [
    "ALIASES",
    "CHEERLIGHTS_FEED_URL",
    "COLORS",
    "Color",
    "ColorChange",
    "__version__",
    "color_name_to_hex",
    "get_color_history",
    "get_current_color",
    "get_current_color_name",
    "get_current_hex",
    "hex_to_rgb",
    "is_valid_color",
]
