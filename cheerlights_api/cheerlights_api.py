# cheerlights/cheerlights_api.py

import requests

CHEERLIGHTS_FEED_URL = "https://api.thingspeak.com/channels/1417/feed.json"

def get_current_color():
    """
    Get the current CheerLights color name and hex code.

    Returns:
        dict: A dictionary with 'color' and 'hex' keys.
    """
    response = requests.get(CHEERLIGHTS_FEED_URL)
    response.raise_for_status()
    data = response.json()
    color_name = data['feeds'][0]['field1']
    hex_code = data['feeds'][0]['field2']

    return {
        'color': color_name,
        'hex': hex_code
    }

def get_current_hex():
    """
    Get the current CheerLights hex color code.

    Returns:
        str: The hex code of the current CheerLights color.
    """
    return get_current_color()['hex']

def get_current_color_name():
    """
    Get the current CheerLights color name.

    Returns:
        str: The name of the current CheerLights color.
    """
    return get_current_color()['color']

def get_color_history(count=10):
    """
    Get the history of CheerLights colors.

    Args:
        count (int): The number of recent colors to retrieve.

    Returns:
        list: A list of dictionaries with 'color', 'hex', and 'timestamp'.
    """
    url = f"{CHEERLIGHTS_FEED_URL}?results={count}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    feeds = data['feeds']
    history = []
    for entry in feeds:
        history.append({
            'color': entry['field1'],
            'hex': entry['field2'],
            'timestamp': entry['created_at']
        })
    return history

def color_name_to_hex(color_name):
    """
    Convert a CheerLights color name to its hex code.

    Args:
        color_name (str): The name of the color.

    Returns:
        str or None: The hex code of the color or None if invalid.
    """
    color_map = {
        'red': '#FF0000',
        'green': '#00FF00',
        'blue': '#0000FF',
        'cyan': '#00FFFF',
        'white': '#FFFFFF',
        'warmwhite': '#FDF5E6',
        'purple': '#800080',
        'magenta': '#FF00FF',
        'yellow': '#FFFF00',
        'orange': '#FFA500',
        'pink': '#FFC0CB',
        'oldlace': '#FDF5E6',
    }
    return color_map.get(color_name.lower())

def hex_to_rgb(hex_code):
    """
    Convert a hex color code to an RGB tuple.

    Args:
        hex_code (str): The hex color code.

    Returns:
        tuple: A tuple with (red, green, blue) values.
    """
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2 ,4))

def is_valid_color(color_name):
    """
    Check if a color name is a valid CheerLights color.

    Args:
        color_name (str): The name of the color.

    Returns:
        bool: True if valid, False otherwise.
    """
    valid_colors = [
        'red', 'green', 'blue', 'cyan', 'white', 'warmwhite',
        'purple', 'magenta', 'yellow', 'orange', 'pink', 'oldlace'
    ]
    return color_name.lower() in valid_colors
