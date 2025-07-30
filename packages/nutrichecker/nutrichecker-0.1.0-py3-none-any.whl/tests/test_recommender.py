# tests/test_recommender.py
"""
Unit test untuk modul recommender.py
"""

import unittest
from nutricheck.recommender import recommend_healthier_alternatives

class TestRecommender(unittest.TestCase):

    def test_recommendation_not_empty(self):
        recommendations = recommend_healthier_alternatives(["banana", "apple"])
        self.assertTrue(len(recommendations) > 0)
        self.assertIsInstance(recommendations, list)

    def test_recommendation_type(self):
        rec = recommend_healthier_alternatives(["chicken breast"])
        self.assertTrue(all(isinstance(item, str) for item in rec))

if __name__ == "__main__":
    unittest.main()
