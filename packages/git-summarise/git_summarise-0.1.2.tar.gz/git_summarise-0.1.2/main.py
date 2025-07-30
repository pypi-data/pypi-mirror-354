import transformers
from transformers import pipeline
from typing_extensions import Annotated
import subprocess
import typer

from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn, track
from rich.text import Text
from rich import print

transformers.logging.set_verbosity_error()

console = Console()

def runCommand(args):
    process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process.communicate()

def getDiff():
    stdout, stderr = runCommand(["git", "--no-pager", "diff", "--staged"])
    if len(stdout) == 0:
        print("No diff to generate summary for")
        exit(1)
    return stdout

def generateOutput(diff, additionalContext = None) -> str:
    generator = pipeline(task="text-generation", model="Qwen/Qwen2.5-1.5B-Instruct")
    chat = [{"role": "system", "content": """
            You are a CLI tool for a developer, your purpose is to read git diffs and generate a commit message for them. 
            You must make the commit message short and a overview of the diff as a whole.
            You must not list individual files and their content.
            Do not include any of the patch in your message.
            Your message must not contain any markdown formatting, it must be compatible with the `git commit -m` command.
            You must only provide the summary and nothing else with no markdown formatting so that your output can be piped directly into git commit.
            An example commit might look like: "Chore: Updated express to 1.2.3". This is just an example, do not return it.
            You must not include any markdown, such as ** ` or other markdown characters. Do NOT wrap your final message with markdown or quotes.
            """}]

    if additionalContext != None:
        chat.append({"role": "user", "content": "Additional context:" + additionalContext })

    chat.append({"role": "user", "content": diff})

    output = generator(chat)

    response = str(output[0]["generated_text"][-1]["content"])
    # Sometimes the AI misbehaves and includes these anyway. :)
    response = response.replace("```", "").replace("**", "").replace("Summary: ", "").strip()
    if(response.startswith("diff")):
        response = response.replace("diff", "", 1)
    
    return response

def getCommitMessage(amountToGenerate, summary) -> str:
    diff = getDiff()
    outputs = []
    options = []
    for i in track(range(0, amountToGenerate), description="Generating..."):
        outputs.append(generateOutput(diff, summary))
        options.append(str(i + 1))

    print(Text("The AI Generated:", style="bold"))

    if amountToGenerate == 1:
        print(outputs[0])
        print()
        approved = Confirm.ask("Do you want to use this message?", default=True)
        if approved:
            return outputs[0]
        return getCommitMessage(amountToGenerate, summary)
    
    table = Table("#", "Message", show_lines=True)
    for idx, output in enumerate(outputs):
        table.add_row(str(idx+1), output)
    table.add_row("r", "Regenerate new messages")
    console.print(table)

    options.append("r")
    opt = Prompt.ask("Pick a message:", choices=options, default="1")

    if opt == "r":
        return getCommitMessage(amountToGenerate, summary)

    return outputs[int(opt)-1]

    
def main(amountToGenerate: Annotated[int, typer.Option("--num", "-n", help="How many options to generate")] = 3, summary: Annotated[str, typer.Argument(help="Additional context for the commit generation")] = None):
    commitMessage = getCommitMessage(amountToGenerate, summary)
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        commit = progress.add_task(description="Committing...", total=1)
        push = progress.add_task(description="Pushing...", total=1)
        stdout, stderr = runCommand(["git", "commit", "-m", commitMessage])
        progress.advance(commit)
        if len(stderr) != 0:
            print(stderr)
            exit(1)
        stdout, stderr = runCommand(["git", "push"])
        if len(stderr) != 0:
            print(stderr)
            exit(1)
        progress.advance(push)

def app():
    typer.run(main)
if __name__ == "__main__":
    app()

# options = [
#     generateOutput(stdout),
#     generateOutput(stdout),
#     generateOutput(stdout)
# ]

# print(options[0])
# print(options[1])
# print(options[2])


