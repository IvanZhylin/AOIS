import unittest
from src.parser import Binary, ExpressionParser, Not, Var

class TestParser(unittest.TestCase):

    def test_parser_builds_ast_and_evaluates(self):
        parser = ExpressionParser()
        ast = parser.parse("!(!a->!b)|c")
        self.assertEqual(ast.evaluate({"a": 0, "b": 0, "c": 0}), 0)
        self.assertEqual(ast.evaluate({"a": 0, "b": 0, "c": 1}), 1)
        self.assertEqual(ast.evaluate({"a": 1, "b": 0, "c": 0}), 0)

    def test_parser_respects_precedence(self):
        parser = ExpressionParser()
        ast = parser.parse("a|b&c")
        self.assertEqual(ast.evaluate({"a": 0, "b": 1, "c": 0}), 0)
        self.assertEqual(ast.evaluate({"a": 0, "b": 1, "c": 1}), 1)

    def test_ast_node_types(self):
        parser = ExpressionParser()
        ast = parser.parse("!(a~b)")
        self.assertIsInstance(ast, Not)
        self.assertIsInstance(ast.operand, Binary)
        self.assertIsInstance(ast.operand.left, Var)

if __name__ == "__main__":
    unittest.main()