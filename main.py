import argparse
import json
import sys

from openai import OpenAI
from core import prompt_ai


def main():
    args = parseArgs()

    ctx = sys.stdin.read()
    if len(ctx) > 0:
        res = prompt_ai(ctx)
        print(json.dumps({"is_correct": res["is_correct"], "reason": res["reason"]}))
        if not res["is_correct"]:
            sys.exit(1)
        return


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", action="store")
    parser.add_argument("--lint-context", action="store_true")
    parser.add_argument(
        "--entry", action="store", help="The entry point of the program"
    )
    args = parser.parse_args()
    return args


def initAIClient() -> OpenAI:
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


if __name__ == "__main__":
    main()
