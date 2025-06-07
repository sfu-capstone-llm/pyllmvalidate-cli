import argparse
import sys
from pathlib import Path

from openai import OpenAI
from pydantic import BaseModel
from git import Repo, InvalidGitRepositoryError


def add(a: int, b: int):
    return a - b

def multiply(a: int, b: int):
    return a / b


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


def get_git_diff() -> str:
    try:
        repo = Repo(".")
        diff = repo.git.diff()
            
        return diff
        
    except InvalidGitRepositoryError:
        print(f"Error: current directory is not a valid git repository", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error getting git diff: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    code_diff = get_git_diff()

    print(f"Git diff output:\n{code_diff}\n" + "="*50)
    
    # If diff is empty, treat as correct
    if not code_diff.strip():
        res = AIResponse(correct=True, reason="No changes detected in git diff")
        print(res)
        return
    
    client = initAIClient()
    # completion = client.chat.completions.create(
    #     model="",
    #     messages=[
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": code_diff},
    #     ],
    # )

    # _res = completion.choices[0].message.content
    _res = """{
        "correct": "true",
        "reason": "No changes detected in git diff."
    }"""
    
    print("CODE DIFF", code_diff)
    if _res is None:
        print("no res back from ai")
        return

    # Clean Markdown formatting if present
    if _res.strip().startswith("```json"):
        _res = _res.strip().removeprefix("```json").removesuffix("```").strip()

    res = AIResponse.model_validate_json(_res)

    print(res)


def parseArgs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate code patches using AI")
    parser.add_argument("--env", action="store", help="Environment setting")
    args = parser.parse_args()
    return args


def initAIClient() -> OpenAI:
    return OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")


if __name__ == "__main__":
    main()