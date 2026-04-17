from cli import run_demo


def test_run_demo_prints_all_sections(capsys):
    run_demo()
    out = capsys.readouterr().out
    assert "1) Десятичное число -> прямой/обратный/дополнительный коды" in out
    assert "2) Сложение в дополнительном коде" in out
    assert "3) Вычитание через отрицание и сложение" in out
    assert "4) Умножение в прямом коде" in out
    assert "5) Деление в прямом коде (5 знаков после запятой)" in out
    assert "6) Операции IEEE-754 (binary32)" in out
    assert "7) Сложение в 5421 BCD (вариант c)" in out

