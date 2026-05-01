from boolfunc.minimization import QuineMcCluskeyMinimizer


def test_qmc_minimize_dnf():
    minimizer = QuineMcCluskeyMinimizer()
    points = [(1, 0, 0), (1, 0, 1), (1, 1, 0), (1, 1, 1)]
    result = minimizer.minimize(points, ["a", "b", "c"], dnf=True)
    assert "a" in result["result"]
    assert result["stages"]


def test_qmc_handles_empty_points():
    minimizer = QuineMcCluskeyMinimizer()
    result = minimizer.minimize([], ["a"], dnf=True)
    assert result["result"] == "0"
