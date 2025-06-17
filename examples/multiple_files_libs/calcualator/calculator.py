from .math_ops import add, subtract, multiply, divide


class Calculator:
    def __init__(self):
        self.last_result = None

    def calculate(self, operation, a, b):
        if operation == "add":
            self.last_result = add(a, b)
        elif operation == "subtract":
            self.last_result = subtract(a, b)
        elif operation == "multiply":
            self.last_result = multiply(a, b)
        elif operation == "divide":
            self.last_result = divide(a, b)
        else:
            raise ValueError(f"Unknown operation: {operation}")
        return self.last_result
