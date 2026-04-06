from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from rich import print
from rich.console import Console
from rich.markdown import Markdown
from dotenv import load_dotenv

load_dotenv()
console = Console()

llm = init_chat_model(model="gemini-2.5-flash", model_provider="google-genai")
model = llm.model
S_M = SystemMessage("Você é uma IA")

messages: list[BaseMessage] = [S_M]

def chat_bot(msg: list[BaseMessage] | None) -> None:
    print(f"[bold blue]--------{str(model).upper()}--------[/bold blue]\n")
    tokens = 0
    while True:
        msg_user = console.input("[bold cyan]Você: [/bold cyan]")
        if msg_user.lower() in ['q', 'quit']:
            print("[bold red]--------SESSÃO FINALIZADA--------[/bold red]\n")
            break
        msg.append(HumanMessage(msg_user))
        call = llm.invoke(msg)
        tokens += call.usage_metadata["total_tokens"]
        msg.append(call)
        console.print("[bold cyan]IA: [/bold cyan]")
        console.print(Markdown(f"{msg[-1].content}"))
        console.print(f"[bold red]Token MSG:[/bold red] {msg[-1].usage_metadata['total_tokens']}")
        console.print(f"[bold red]Token Total:[/bold red] {tokens}")

if __name__ == "__main__":
    chat_bot(messages)