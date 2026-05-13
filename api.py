"""
Configuração de Endpoints da API e conexão direta com o Supabase.
Gerencia credenciais, cabeçalhos de autenticação e rotas de tabelas para o banco de dados.
"""

SUPABASE_URL = "https://dszzjdzferfxnbfthdmi.supabase.co"
SUPABASE_KEY = "sb_publishable_7pYO1wdMS0oveUoVaLqNcA_a6NONxcZ"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

# Endpoints diretos do PostgREST
API_EVENTOS = f"{SUPABASE_URL}/rest/v1/eventos"
API_USUARIOS = f"{SUPABASE_URL}/rest/v1/usuarios"
API_INGRESSOS = f"{SUPABASE_URL}/rest/v1/ingressos"
API_FAVORITOS = f"{SUPABASE_URL}/rest/v1/favoritos"
API_CUPONS = f"{SUPABASE_URL}/rest/v1/cupons"
API_CUPONS_USADOS = f"{SUPABASE_URL}/rest/v1/cupons_usados"
