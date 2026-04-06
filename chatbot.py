from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from rich import print
from rich.console import Console
from dotenv import load_dotenv
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
    print(f"[bold cyan]IA: [/bold cyan]{output.content}")
    return output

# def chat_bot(msg: list[BaseMessage] | None) -> None:
#     print(f"[bold blue]--------{str(model).upper()}--------[/bold blue]\n")
#     tokens = 0
#     while True:
#         msg_user = console.input("[bold cyan]Você: [/bold cyan]")
#         if msg_user.lower() in ['q', 'quit']:
#             print("[bold red]--------SESSÃO FINALIZADA--------[/bold red]\n")
#             break
#         msg.append(HumanMessage(msg_user))
#         call = llm.invoke(msg)
#         tokens += call.usage_metadata["total_tokens"]
#         msg.append(call)
#         console.print("[bold cyan]IA: [/bold cyan]")
#         console.print(Markdown(f"{msg[-1].content}"))
#         console.print(f"[bold red]Token MSG:[/bold red] {msg[-1].usage_metadata['total_tokens']}")
#         console.print(f"[bold red]Token Total:[/bold red] {tokens}")
