import os
from dotenv import load_dotenv
from langchain_core.messages import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from supabase import create_client

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")

def vectorizing(msg: str) -> list:
    try:
        response = embeddings_model.embed_query(msg)
        return response
    except Exception as e:
        print(f"Erro na vetorização: {e}")
        return []

def db_context(pergunta: str):
    vetor_pergunta = vectorizing(pergunta)

    rpc_params = {
        "query_embedding": vetor_pergunta,
        "match_threshold": 0.5,
        "match_count": 1
    }

    resposta = supabase.rpc("buscar_politicas", rpc_params).execute()
    return resposta.data


if __name__ == "__main__":
    print(db_context("Me de as políticas de privacidade"))