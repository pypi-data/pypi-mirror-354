# tests/test_fetch.py
"""
Unit test untuk modul fetch.py
"""

import unittest
from nutricheck.fetch import fetch_nutrition_data

class TestFetchNutritionData(unittest.TestCase):

    def test_fetch_returns_dict(self):
        data = fetch_nutrition_data("apple")
        self.assertIsInstance(data, dict)
        for key in ["calories", "protein", "fat", "carbs", "fiber"]:
            self.assertIn(key, data)

    def test_fetch_dummy_on_failure(self):
        # Uji dengan input yang kemungkinan tidak ada
        data = fetch_nutrition_data("nonexistentfooditem")
        self.assertIsInstance(data, dict)
        self.assertGreaterEqual(data.get("calories", 0), 0)

if __name__ == "__main__":
    unittest.main()
