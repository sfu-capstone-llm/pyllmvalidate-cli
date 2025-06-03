import argparse
import sys

from openai import OpenAI
from pydantic import BaseModel, ValidationError


class AIResponse(BaseModel):
    correct: bool
    reason: str


system_prompt = f"""
Description:
- You are running in a CLI tool to validate code patches.
- You should analyze the code patches for correctness

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


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--env", action="store")
    args = parser.parse_args()
    return args


def initAIClient() -> OpenAI:
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


if __name__ == "__main__":
    main()
