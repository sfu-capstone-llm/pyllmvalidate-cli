import shutil
import os
import subprocess
import sys

files = ["./main.py", "./bar/baz.py"]


def copyIntoTempDir(temp_dir: str):
    os.makedirs(temp_dir, exist_ok=True)

    root_dir = os.getcwd()

    for item in os.listdir(root_dir):
        source = os.path.join(root_dir, item)
        destination = os.path.join(temp_dir, item)
        print(source, destination)
        if (
            source == temp_dir
            # or item.startswith(".git")
            or item.startswith("__pycache__")
            or item.startswith(".venv")
        ):
            continue
        print(source)
        if os.path.isdir(source):
            shutil.copytree(
                source,
                destination,
                dirs_exist_ok=True,
                copy_function=shutil.copy2,
                symlinks=True,
            )
        else:
            shutil.copy2(source, destination)


def install():
    print("Installing dependencies")
    result = subprocess.run(["uv", "sync"])
    if result.returncode != 0:
        print("Error: unable to install dependencies")
        return sys.exit(1)


def instrument():
    print("Instrumenting files")
    print("Instrumenting files with dynapyt")
    result = subprocess.run(
        [
            ".venv/bin/python",
            "-m",
            "dynapyt.instrument.instrument",
            "--files",
            *files,
            "--analysis",
            "callgraph",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error: unable to instrument files with dynapyt")
        print(result.stdout)
        print(result.stderr)
        return sys.exit(1)

    print(result.stdout)


def execute():
    print("Executing files with dynapyt")
    result = subprocess.run(
        [
            ".venv/bin/python",
            "-m",
            "dynapyt.run_analysis",
            "--entry",
            "main.py",
            "--analysis",
            "callgraph",
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("Error: unable to execute files with dynapyt")
        print("=" * 50)
        print(result.stdout)
        print("=" * 50)
        print(result.stderr)
        return sys.exit(1)

    print(result.stdout)


def get_callgraph(temp_dir: str):
    pass
