from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_core.tools import BaseTool
from vectorizing import db_context

load_dotenv()
base_llm = init_chat_model(model="gemini-2.5-flash", model_provider="google-genai")

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

tools: list[BaseTool] = [consultar_politicas]
llm = base_llm.bind_tools(tools)