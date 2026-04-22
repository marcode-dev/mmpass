"""
Configuração de Endpoints da API e conexão direta com o Supabase.
Gerencia credenciais, cabeçalhos de autenticação e rotas de tabelas para o banco de dados.
"""
import random
import requests

SUPABASE_URL = "https://dszzjdzferfxnbfthdmi.supabase.co"
SUPABASE_KEY = "sb_publishable_jwwZUJDs1NJ6niWj-cRhig_w1MWmgfa"

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
