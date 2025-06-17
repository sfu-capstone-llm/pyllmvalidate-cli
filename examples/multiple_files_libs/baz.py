from .calcualator import Calculator, format_result


def baz():
    calc = Calculator()

    result1 = calc.calculate("add", 5, 3)
    print(f"5 + 3 = {format_result(result1)}")

    result2 = calc.calculate("multiply", 4, 2.5)
    print(f"4 * 2.5 = {format_result(result2)}")

    result3 = calc.calculate("divide", 10, 2)
    print(f"10 / 2 = {format_result(result3)}")
