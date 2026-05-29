import unittest
from src.minimization import QuineMcCluskeyMinimizer

class TestMinimization(unittest.TestCase):

    def test_qmc_minimize_dnf(self):
        minimizer = QuineMcCluskeyMinimizer()
        points = [(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
        result = minimizer.minimize(points, ["a", "b", "c"], dnf=True)
        self.assertIn("a", result["result"])
        self.assertTrue(result["stages"])  # non-empty list

    def test_qmc_handles_empty_points(self):
        minimizer = QuineMcCluskeyMinimizer()
        result = minimizer.minimize([], ["a"], dnf=True)
        self.assertEqual(result["result"], "0")

if __name__ == "__main__":
    unittest.main()