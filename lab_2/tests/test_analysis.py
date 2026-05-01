from boolfunc.analysis import BooleanFunctionAnalyzer


def test_analysis_generates_all_sections():
    analyzer = BooleanFunctionAnalyzer()
    data = analyzer.analyze("a|b")
    assert data["variables"] == ["a", "b"]
    assert data["sdnf"] != ""
    assert data["sknf"] != ""
    assert isinstance(data["index_form"], int)
    assert set(data["post"]) == {"T0", "T1", "S", "M", "L"}
    assert "calc_dnf" in data["minimization"]
    assert "calc_cnf" in data["minimization"]
    assert "table_dnf" in data["minimization"]
    assert "kmap_dnf" in data["minimization"]


def test_fictive_variable_found():
    analyzer = BooleanFunctionAnalyzer()
    data = analyzer.analyze("a")
    assert "b" not in data["variables"]
    assert data["fictive"] == []


def test_minimization_result_for_simple_formula():
    analyzer = BooleanFunctionAnalyzer()
    data = analyzer.analyze("(a&b)|(a&!b)")
    # После минимизации должна остаться импликанта a
    assert "a" in data["minimization"]["calc_dnf"]["result"]


def test_karnaugh_fallback_for_5_variables():
    analyzer = BooleanFunctionAnalyzer()
    data = analyzer.analyze("a|b|c|d|e")
    assert data["minimization"]["kmap_dnf"]["supported"] is False
