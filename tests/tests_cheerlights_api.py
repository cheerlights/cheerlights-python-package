# tests/test_cheerlights_api.py

import unittest
from cheerlights_api import (
    get_current_color,
    get_current_hex,
    get_current_color_name,
    get_color_history,
    color_name_to_hex,
    hex_to_rgb,
    is_valid_color,
)

class TestCheerLights(unittest.TestCase):

    def test_get_current_color(self):
        color_info = get_current_color()
        self.assertIn('color', color_info)
        self.assertIn('hex', color_info)

    def test_get_current_hex(self):
        hex_code = get_current_hex()
        self.assertTrue(hex_code.startswith('#'))

    def test_get_current_color_name(self):
        color_name = get_current_color_name()
        self.assertIsInstance(color_name, str)

    def test_get_color_history(self):
        history = get_color_history(5)
        self.assertEqual(len(history), 5)
        for entry in history:
            self.assertIn('color', entry)
            self.assertIn('hex', entry)
            self.assertIn('timestamp', entry)

    def test_color_name_to_hex(self):
        hex_code = color_name_to_hex('red')
        self.assertEqual(hex_code, '#FF0000')

    def test_hex_to_rgb(self):
        rgb = hex_to_rgb('#FF0000')
        self.assertEqual(rgb, (255, 0, 0))

    def test_is_valid_color(self):
        self.assertTrue(is_valid_color('blue'))
        self.assertFalse(is_valid_color('black'))

if __name__ == '__main__':
    unittest.main()
