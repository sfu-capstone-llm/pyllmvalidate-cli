def format_result(result):
    if isinstance(result, float):
        return f"{result:.2f}"
    return str(result)
