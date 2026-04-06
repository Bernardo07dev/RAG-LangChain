from langchain_core.messages import BaseMessage, tool
from langchain_core.tools import BaseTool
from chatbot import llm, chat_bot
from dotenv import load_dotenv
from util import S_M
from rich import print
from vectorizing import db_context

@tool
def consultar_politicas(pergunta: str) -> str:
    """
    Consulta o banco de dados de políticas da empresa (RH, Financeiro, Cultura...).
    Use esta ferramenta sempre que o usuário perguntar sobre regras, benefícios,
    home office, vestimenta ou procedimentos internos.
    """
    resultados = db_context(pergunta)

    if not resultados:
        return "Nenhuma política encontrada sobre este assunto."

    contexto = f"{resultados['titulo']} - {resultados['conteudo']}"
    return contexto

messages: list[BaseMessage] = S_M
tools: list[BaseTool] = [consultar_politicas]
llm_w_tools = llm.bind_tools(tools)


chat_bot(messages)