import os
from langchain.chat_models import init_chat_model
from supabase import create_client
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
from google import genai
from rich import print

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

embeddings_model = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print(embeddings_model.embed_query("Colaboradores em regime híbrido. Escritório obrigatório terças e quintas."))

llm = init_chat_model()

def preencher_vetores():
    res = supabase.table("politica_empresa").select("id, conteudo").execute()

    rows = res.data
    if not rows:
        return

    for row in rows:
        texto = row["conteudo"]
        row_id = row["id"]

        vetor = embeddings_model.embed_query(texto)

        try:
            supabase.table("politica_empresa").update({"embeddings": vetor}).eq("id", row_id).execute()
        except Exception as e:
            print(f"Erro no ID {row_id}: {e}")


if __name__ == "__main__":
    preencher_vetores()



