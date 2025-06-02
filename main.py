import argparse
import sys

from openai import OpenAI
from pydantic import BaseModel


def add(a: int, b: int):
    return a - b


class AIResponse(BaseModel):
    correct: bool
    reason: str


system_prompt = f"""
Description:
- You are running in a CLI tool to validate code patches.
- You should analyze the code patches for correctness based on functionality
- Code style should not be errors unless it is a big problem

Input:
- The output of git diff command
- If empty treat as correct

Output:
- Always respond with JSON in string format specified by the pydantic JSON schema that's provided below
- You MUST use this format for the output


Pydantic JSON schema:
{AIResponse.model_json_schema()}
"""


def main():
    args = parseArgs()
    code_diff = sys.stdin.read()
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

    if _res is None:
        print("no res back from ai")
        return

    # Clean Markdown formatting if present
    if _res.strip().startswith("```json"):
        _res = _res.strip().removeprefix("```json").removesuffix("```").strip()

    res = AIResponse.model_validate_json(_res)

    print(res)


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", action="store")
    args = parser.parse_args()
    return args


def initAIClient() -> OpenAI:
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


if __name__ == "__main__":
    main()
