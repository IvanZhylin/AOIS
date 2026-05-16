import unittest
import sys
from io import StringIO
from src.cli import run


class TestCLI(unittest.TestCase):
    def test_run_demo_prints_all_sections(self):
        # Перенаправляем stdout
        captured_output = StringIO()
        sys.stdout = captured_output

        try:
            # Вместо input() в run() нужно подставить значения.
            # В оригинале run() запрашивает ввод двух чисел.
            # Чтобы тест не зависал, подменим input на возврат '13' и '-5'.
            original_input = __builtins__['input']
            def mock_input(prompt):
                if "первое число" in prompt:
                    return "13"
                else:
                    return "-5"
            __builtins__['input'] = mock_input

            run()
        finally:
            # Восстанавливаем stdout и input
            sys.stdout = sys.__stdout__
            __builtins__['input'] = original_input

        output = captured_output.getvalue()
        self.assertIn("1) Десятичное число -> прямой/обратный/дополнительный коды", output)
        self.assertIn("2) Сложение в дополнительном коде", output)
        self.assertIn("3) Вычитание через отрицание и сложение", output)
        self.assertIn("4) Умножение в прямом коде", output)
        self.assertIn("5) Деление в прямом коде (5 знаков после запятой)", output)
        self.assertIn("6) Операции IEEE-754 (binary32)", output)
        self.assertIn("7) Сложение в 5421 BCD (вариант c)", output)


if __name__ == "__main__":
    unittest.main()
