from typing import TypedDict
import sys
import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class PromptAIRes(TypedDict):
    is_correct: bool
    reason: str



def prompt_ai(ctx: str) -> PromptAIRes:
    is_correct = get_ai_response(
        "Only output 'true' or 'false' on correctness of the git diff.", ctx
    )
    if is_correct is None:
        raise Exception("unable to generate reponse from llm for is_correct")

    reason = get_ai_response(
        f"You stated that this git diff is {is_correct}. Tell us the reason why right away.",
        ctx,
    )
    if reason is None:
        raise Exception("unable to generate reponse from llm for reason")

    response: PromptAIRes = {
        "is_correct": is_correct.strip().lower() == "true",
        "reason": reason.strip(),
    }

    return response


def get_ai_response(output_prompt: str, ctx: str):
    system_prompt_template = """
# Identity

You are trying to validate if a code diff fixes the bug. You will be provided a the bug description
which includes the PR and related issues from github, code diff, method trace, and full file context.
Use the bug description (PR and Issues) as the requirements for the fix.

# Instruction

* The bug is specified in the # Description section with links to the GitHub PR and Issues
* The description section should be the source of truth and provide the requirements for the fix
* Use the description, code diff, method trace, and files sections which are separated by markdown headers.
* Determine determine if the code diff correctly or incorrectly fixes the bug
* {output_format}
    """
    system_promp = system_prompt_template.format(output_format=output_prompt)
    client = initAIClient()
    try:
        completion = client.responses.create(
            model="gpt-4.1-nano-2025-04-14",
            input=[
                {"role": "developer", "content": system_promp},
                {"role": "user", "content": ctx},
            ],
            temperature=0.3,
        )
    except Exception as e:
        print(e)
        sys.exit(2)
    return completion.output_text


def initAIClient() -> OpenAI:
    return OpenAI(api_key=OPENAI_API_KEY)
