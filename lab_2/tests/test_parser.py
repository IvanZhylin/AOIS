from boolfunc.parser import Binary, ExpressionParser, Not, Var


def test_parser_builds_ast_and_evaluates():
    parser = ExpressionParser()
    ast = parser.parse("!(!a->!b)|c")
    assert ast.evaluate({"a": 0, "b": 0, "c": 0}) == 0
    assert ast.evaluate({"a": 0, "b": 0, "c": 1}) == 1
    assert ast.evaluate({"a": 1, "b": 0, "c": 0}) == 0


def test_parser_respects_precedence():
    parser = ExpressionParser()
    ast = parser.parse("a|b&c")
    assert ast.evaluate({"a": 0, "b": 1, "c": 0}) == 0
    assert ast.evaluate({"a": 0, "b": 1, "c": 1}) == 1


def test_ast_node_types():
    parser = ExpressionParser()
    ast = parser.parse("!(a~b)")
    assert isinstance(ast, Not)
    assert isinstance(ast.operand, Binary)
    assert isinstance(ast.operand.left, Var)
