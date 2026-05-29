import unittest
from src.analysis import BooleanFunctionAnalyzer

class TestAnalysis(unittest.TestCase):

    def test_analysis_generates_all_sections(self):
        analyzer = BooleanFunctionAnalyzer()
        data = analyzer.analyze("a|b")
        self.assertEqual(data["variables"], ["a", "b"])
        self.assertNotEqual(data["sdnf"], "")
        self.assertNotEqual(data["sknf"], "")
        self.assertIsInstance(data["index_form"], int)
        self.assertEqual(set(data["post"]), {"T0", "T1", "S", "M", "L"})
        self.assertIn("calc_dnf", data["minimization"])
        self.assertIn("calc_cnf", data["minimization"])
        self.assertIn("table_dnf", data["minimization"])
        self.assertIn("kmap_dnf", data["minimization"])

    def test_fictive_variable_found(self):
        analyzer = BooleanFunctionAnalyzer()
        data = analyzer.analyze("a")
        self.assertNotIn("b", data["variables"])
        self.assertEqual(data["fictive"], [])

    def test_minimization_result_for_simple_formula(self):
        analyzer = BooleanFunctionAnalyzer()
        data = analyzer.analyze("(a&b)|(a&!b)")
        self.assertIn("a", data["minimization"]["calc_dnf"]["result"])

    def test_karnaugh_fallback_for_5_variables(self):
        analyzer = BooleanFunctionAnalyzer()
        data = analyzer.analyze("a|b|c|d|e")
        self.assertFalse(data["minimization"]["kmap_dnf"]["supported"])

if __name__ == "__main__":
    unittest.main()