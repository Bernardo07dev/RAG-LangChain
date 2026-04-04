from supabase import create_client
from dotenv import load_dotenv
from data import politicas
import os

load_dotenv()
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

supabase = create_client(url, key)

for data in politicas:
    data = {
        "titulo": data['titulo'],
        "conteudo": data['conteudo'],
        "categoria": data["categoria"]
    }

    response = supabase.table("politica_empresa").insert(data).execute()
    print(response)
