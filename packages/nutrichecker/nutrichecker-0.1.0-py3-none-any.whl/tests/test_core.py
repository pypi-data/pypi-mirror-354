# tests/test_core.py
"""
Unit test untuk modul core.py
"""

import unittest
from nutricheck.core import NutritionAnalyzer

class TestNutritionAnalyzer(unittest.TestCase):

    def setUp(self):
        self.profile = {"age": 25, "weight": 65, "height": 165, "activity_level": "light"}
        self.analyzer = NutritionAnalyzer(self.profile)

    def test_analyze_returns_dict(self):
        result = self.analyzer.analyze(["apple", "banana"])
        self.assertIsInstance(result, dict)
        self.assertIn("nutrition", result)
        self.assertIn("score", result)

    def test_evaluate_score_in_range(self):
        result = self.analyzer.analyze(["apple", "banana"])
        score = result.get("score", 0)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)

if __name__ == "__main__":
    unittest.main()
