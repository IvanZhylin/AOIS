"""Тест демонстрационного сценария (без падений)."""

import io
import unittest
from contextlib import redirect_stdout

from src.cli import run


class TestCli(unittest.TestCase):
    def test_run_prints_table(self) -> None:
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            run()
        output = buffer.getvalue()
        self.assertIn("хеш-таблица", output.lower())
        self.assertIn("Коэффициент заполнения", output)


if __name__ == "__main__":
    unittest.main()
