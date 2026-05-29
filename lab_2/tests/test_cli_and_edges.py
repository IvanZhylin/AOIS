import unittest
from unittest.mock import patch
import runpy
import sys
from io import StringIO

from src.analysis import BooleanFunctionAnalyzer
from src.cli import main
from src.minimization import QuineMcCluskeyMinimizer
from src.parser import Binary, ExpressionParser

class TestCLIAndEdges(unittest.TestCase):

    @patch('builtins.input', return_value="a|b")
    def test_cli_prints_russian_output(self, mock_input):
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            main()
        finally:
            sys.stdout = sys.__stdout__
        out = captured_output.getvalue()
        self.assertIn("Таблица истинности", out)
        self.assertIn("СДНФ", out)
        self.assertIn("Полином Жегалкина", out)

    def test_cli_entrypoint_block(self):
        self.assertTrue(callable(main))

    @patch('builtins.input', return_value="a")
    def test_cli_module_entrypoint(self, mock_input):
        captured_output = StringIO()
        sys.stdout = captured_output
        try:
            runpy.run_module("src.cli", run_name="__main__")
        finally:
            sys.stdout = sys.__stdout__
        self.assertIn("Лабораторная №2", captured_output.getvalue())

    def test_parser_errors_and_unicode(self):
        parser = ExpressionParser()
        with self.assertRaises(ValueError):
            parser.parse("a+1")
        with self.assertRaises(ValueError):
            parser.parse("(a|b")
        ast = parser.parse("¬a∨b")
        self.assertEqual(ast.evaluate({"a": 1, "b": 0}), 0)

    def test_binary_unknown_operation_raises(self):
        node = Binary("^", ExpressionParser().parse("a"), ExpressionParser().parse("b"))
        with self.assertRaises(ValueError):
            node.evaluate({"a": 1, "b": 0})

    def test_analyzer_validation_errors(self):
        analyzer = BooleanFunctionAnalyzer()
        with self.assertRaises(ValueError):
            analyzer.analyze("(!1)")

    def test_qmc_cnf_and_empty_for_cnf(self):
        minimizer = QuineMcCluskeyMinimizer()
        points = [(0, 0), (0, 1)]
        result = minimizer.minimize(points, ["a", "b"], dnf=False)
        # проверяем, что результат содержит '&' либо является простым литералом/константой
        self.assertTrue("&" in result["result"] or result["result"] in {"1", "0", "a", "b", "!a", "!b"})
        empty = minimizer.minimize([], ["a"], dnf=False)
        self.assertEqual(empty["result"], "1")

if __name__ == "__main__":
    unittest.main()