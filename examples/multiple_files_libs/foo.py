import random
import os
from examples.multiple_files_libs.calcualator import baz
from git import Repo


def foo():
    baz()
    print("foo")
    Repo(".")
    return random.randint(0, 100)


def bar():
    return os.getcwd()
