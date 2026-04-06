from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from rich import print
from rich.console import Console
from dotenv import load_dotenv
from rich.markdown import Markdown

from state import State
from llm import llm

load_dotenv()
console = Console()

def call(msg: State | None) -> BaseMessage | str:
    msg_user = console.input("[bold cyan]Você: [/bold cyan]")
    if msg_user.lower() in ['q', 'quit']:
        print("[bold red]--------SESSÃO FINALIZADA--------[/bold red]\n")
        return "__end__"
    return HumanMessage(msg_user)

def response(msg: State) -> BaseMessage:
    output = llm.invoke(msg["messages"])

    if getattr(output, "tool_calls", None):
        return output

    content = output.content

    if isinstance(content, list):
        content = " ".join(
            part.get("text", "")
            for part in content
            if isinstance(part, dict)
        ).strip()

    if not content:
        return output

    console.print("[bold cyan]IA:[/bold cyan]", Markdown(content))

    return output
