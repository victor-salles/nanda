import os
import subprocess

from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import AssistantMessage, SystemMessage, UserMessage
from azure.core.credentials import AzureKeyCredential
from instructions import commit_instructions, initial_context, prompt_structure

"""
    Goal
    Build a chatbot that can write commit messages for a github repo.
    Steps:
    - Index the repository.
    - Parse the instructions on how it should write the messages.
    - Get the `git diff` for the staged changes
    - From receiving a task description and the git diff, write a commit message.
"""


token = os.getenv("GITHUB_TOKEN")
endpoint = "https://models.inference.ai.azure.com"
model_name = "meta-llama-3-70b-instruct"

client = ChatCompletionsClient(
    endpoint=endpoint,
    credential=AzureKeyCredential(token),
    temperature=0.3,
)


def parse_file(file_path: str) -> str:
    """Get the file content using `git show`."""
    try:
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)
        result = subprocess.run(
            ["git", "show", f":{filename}"],
            capture_output=True,
            text=True,
            check=True,
            cwd=directory,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error reading file {file_path}: {e}")


def parse_git_diff(repository_path: str) -> str:
    """Get the git diff for the staged changes."""
    try:
        result = subprocess.run(
            ["git", "--no-pager", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repository_path,
        )
        output = result.stdout
        if not output:
            raise Exception("No changes to commit.")
        return output
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running git diff: {e}")


def changed_files(repository_path: str) -> list[str]:
    """Get the list of changed files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--staged"],
            capture_output=True,
            text=True,
            check=True,
            cwd=repository_path,
        )
        output = result.stdout
        if not output:
            return "No changes to commit."
        output = output.splitlines()

        print("Scanning staged files:")
        for file in output:
            print(f"- {file}")

        output = [file.strip() for file in output if file.strip()]
        # Get the full path of the changed files.
        return [os.path.join(repository_path, file) for file in output]
    except subprocess.CalledProcessError as e:
        raise Exception(f"Error running git diff: {e}")


def generate_prompt_message_with_context(
    repository_path: str, task_description: str
) -> str:

    git_diff = parse_git_diff(repository_path)
    changed_files_paths = changed_files(repository_path)
    changed_files_contents = [parse_file(file) for file in changed_files_paths]
    full_changes = ""
    for file, content in zip(changed_files_paths, changed_files_contents):
        full_changes += f"{file}:\n"
        full_changes += content
        full_changes += "\n\n"

    return prompt_structure.format(
        task_description=task_description,
        full_changes=full_changes,
        git_diff=git_diff,
    )


def chat_with_ai(message: str):
    messages = [
        SystemMessage(content=initial_context),
        SystemMessage(content=commit_instructions),
        UserMessage(content=message),
    ]

    response = client.complete(messages=messages, model=model_name)
    ai_response = response.choices[0].message.content
    print(ai_response)


if __name__ == "__main__":
    TASK_DESCRIPTION = (
        "Implement a chatbot that can write commit messages for a GitHub repository."
    )
    REPOSITORY_PATH = "/Users/victorrodrigues/work/NaN/nanda"
    message = generate_prompt_message_with_context(REPOSITORY_PATH, TASK_DESCRIPTION)

    debug = 0
    if debug:
        print(message)
    else:
        print("\nGenerating commit message...")
        chat_with_ai(message)
