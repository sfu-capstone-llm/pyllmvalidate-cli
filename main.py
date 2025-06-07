import argparse
import shutil
import subprocess
import sys
from typing import List

from openai import OpenAI
from pydantic import BaseModel, ValidationError


def greatest_num(arr: List[int]):
    max = -1
    for num in arr:
        if num > max:
            max = num
    return max


class AIResponse(BaseModel):
    correct: bool
    reason: str


system_prompt = f"""
Description:
- You are running in a CLI tool to validate code patches.
- You should analyze the code patches for correctness
- The names of the function should have less weight to the overal decision

Input:
- The output of git diff command
- If empty treat as correct

Output:
- Always respond with JSON in STRING format specified by the pydantic JSON schema that's provided below
- Dot not include the markdown ```
- You MUST use this format for the output

Pydantic JSON schema:
{AIResponse.model_json_schema()}

Example:
{{
    "correct": false,
    "reason": "The patch modifies the 'add' function to return `a * b` instead of `a - b`, which is likely incorrect because the function name suggests addition, not multiplication."
}}
"""


def main():
    args = parseArgs()
    code_diff = sys.stdin.read()
    # print(code_diff)

    if args.lint_context:
        code_diff = add_lint_context(code_diff)
        print(code_diff)

    client = initAIClient()
    completion = client.chat.completions.create(
        model="",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": code_diff},
        ],
    )

    _res = completion.choices[0].message.content
    print(_res)

    if _res is None:
        print("no res back from ai")
        return sys.exit(1)

    # Clean Markdown formatting if present
    # if _res.strip().startswith("```json"):
    #     _res = _res.strip().removeprefix("```json").removesuffix("```").strip()

    try:
        res = AIResponse.model_validate_json(_res)
    except ValidationError as e:
        print("The LLM generated an incorrect output.")
        print(e)
        return sys.exit(1)

    print("Correct: ", res.correct)
    print("Reason: ", res.reason)


def add_lint_context(system_prompt: str) -> str:
    if not shutil.which("ruff"):
        print("Error: ruff is not installed or not in PATH")
        return sys.exit(1)

    prompt = system_prompt + "\n\n" + "Ruff linting context:\n"

    result = subprocess.run(
        ["ruff", "check"],
        capture_output=True,  # captures stdout and stderr
        text=True,  # returns output as string (instead of bytes)
    )

    if result.returncode == 0:
        prompt = prompt + result.stdout
    else:
        prompt = prompt + f"ruff check failed: {result.stdout}"
    return prompt


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", action="store")
    parser.add_argument("--lint-context", action="store_true")
    args = parser.parse_args()
    return args


def initAIClient() -> OpenAI:
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


if __name__ == "__main__":
    main()
