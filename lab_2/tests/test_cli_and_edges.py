import pytest
import runpy

from boolfunc.analysis import BooleanFunctionAnalyzer
from boolfunc.cli import main
from boolfunc.minimization import QuineMcCluskeyMinimizer
from boolfunc.parser import Binary, ExpressionParser


def test_cli_prints_russian_output(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "a|b")
    main()
    out = capsys.readouterr().out
    assert "Таблица истинности" in out
    assert "СДНФ" in out
    assert "Полином Жегалкина" in out


def test_cli_entrypoint_block():
    # Просто проверяем, что модуль импортируется и main callable
    assert callable(main)


def test_cli_module_entrypoint(monkeypatch, capsys):
    monkeypatch.setattr("builtins.input", lambda _: "a")
    runpy.run_module("boolfunc.cli", run_name="__main__")
    assert "Лабораторная №2" in capsys.readouterr().out


def test_parser_errors_and_unicode():
    parser = ExpressionParser()
    with pytest.raises(ValueError):
        parser.parse("a+1")
    with pytest.raises(ValueError):
        parser.parse("(a|b")
    ast = parser.parse("¬a∨b")
    assert ast.evaluate({"a": 1, "b": 0}) == 0


def test_binary_unknown_operation_raises():
    node = Binary("^", ExpressionParser().parse("a"), ExpressionParser().parse("b"))
    with pytest.raises(ValueError):
        node.evaluate({"a": 1, "b": 0})


def test_analyzer_validation_errors():
    analyzer = BooleanFunctionAnalyzer()
    with pytest.raises(ValueError):
        analyzer.analyze("(!1)")


def test_qmc_cnf_and_empty_for_cnf():
    minimizer = QuineMcCluskeyMinimizer()
    points = [(0, 0), (0, 1)]
    result = minimizer.minimize(points, ["a", "b"], dnf=False)
    assert "&" in result["result"] or result["result"] in {"1", "0", "a", "b", "!a", "!b"}
    empty = minimizer.minimize([], ["a"], dnf=False)
    assert empty["result"] == "1"
