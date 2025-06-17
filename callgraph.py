import os
import runpy
import sys
from collections import defaultdict
import ast


def build_call_graph(entry: str):
    call_graph = defaultdict(set)
    call_stack = []

    project_functions = set(get_all_function_names_from_project())

    def is_project_function(func_name):
        return func_name in project_functions

    def tracefunc(frame, event, arg):
        if event == "call":
            code = frame.f_code
            func_name = code.co_name
            module = frame.f_globals.get("__name__", "")

            # Get the actual module name from the entry point file
            if module == "__main__":
                module = os.path.splitext(os.path.basename(entry))[0]

            full_name = f"{module}.{func_name}"

            if call_stack:
                caller = call_stack[-1]
                if is_project_function(caller):
                    call_graph[caller].add(full_name)

            call_stack.append(full_name)

        elif event == "return" and call_stack:
            call_stack.pop()

        return tracefunc

    sys.settrace(tracefunc)
    runpy.run_path(entry, run_name="__main__")
    sys.settrace(None)

    call_graph_str = ""
    for caller, callees in call_graph.items():
        for callee in callees:
            call_graph_str = f"{call_graph_str}\n{caller}->{callee}"

    return call_graph_str


def get_all_function_names_from_project(project_dir="."):
    defined_funcs = set()

    for dirpath, dirnames, filenames in os.walk(project_dir):
        # Skip unwanted folders
        dirnames[:] = [
            d
            for d in dirnames
            if not d.startswith(".")
            and d not in ("__pycache__", "venv", ".venv", "env")
        ]

        for filename in filenames:
            if filename.endswith(".py"):
                path = os.path.join(dirpath, filename)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=path)
                except Exception as e:
                    print(f"Skipping {path}: {e}")
                    continue

                # Get module name from file path
                rel_path = os.path.relpath(path, project_dir)
                module_name = os.path.splitext(rel_path)[0].replace(os.sep, ".")

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        defined_funcs.add(f"{module_name}.{node.name}")

    return defined_funcs
