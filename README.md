# MMPass

MMPass é uma aplicação moderna de venda e gerenciamento de inressos de eventos, desenvolvida em Python 3 utilizando a biblioteca Flet. O foco do projeto é entregar uma experiência imersiva e de altíssima qualidade visual (UI/UX premium), com layout responsivo otimizado para dispositivos móveis e desktop.

## Funcionalidades Principais

*   **Autenticação e Cadastro**: Sistema completo de login e criação de contas com integração via backend Supabase.
*   **Gerador e Catálogo de Eventos**: Busca de eventos em tempo real em alta, com filtros personalizados por categorias.
*   **Checkout Premium Multi-Método**: Fluxo moderno de pagamento com suporte a múltiplos métodos, aplicação de cupons de descontos e validação sofisticada.
*   **Assistente IA/ChatBox**: Suporte integrado dentro da aplicação (`chat.py`).
*   **Armazenamento de Sessão Persistente**: Gerenciamento de estado elegante entre telas (carrinho de compras, favoritos, login persistente).

## Stack e Arquitetura

*   **Frontend**: Flet (Python) – Abordagem modular baseada em telas (Arquitetura Screen-based).
*   **Backend / DaaS**: Supabase e chamadas de API via `requests` (`api.py`).
*   **Segurança**: Senhas formatadas usando `bcrypt`.

## Estrutura do Projeto

*   `eventos.py`: Entrypoint principal do aplicativo (onde configuramos o roteamento e inicialização das janelas).
*   `router.py`: Controlador modular de navegação entre as diferentes telas (`screens/`).
*   `screens/`: Telas individuais componentes como Login, Home, Perfil, Wallet, Checkout, etc.
*   `shared_ui.py`: Componentes de interface de usuário reutilizáveis (NavBar, AppBars, modais de notificação) para garantir consistência em toda a aplicação.
*   `api.py`: Camada de comunicação com endpoints do backend, chaves de autenticação customizadas (Supabase).
*   `chat.py`: Componente flutuante do assistente de chat para interação dos usuários.
*   `utils.py`: Funções auxiliares (como helpers locais de `client_storage`).

## Como Rodar

1.  Certifique-se de possuir Python 3.8+ instalado.
2.  Instale as dependências requeridas utilizando pip:
    ```bash
    pip install flet requests bcrypt
    ```
3.  Crie um arquivo `.env` na raiz ou atualize as variáveis da sua URL Supabase e `SUPABASE_KEY` no arquivo `api.py`.
4.  Suba a aplicação via linha de comando:
    ```bash
    flet run eventos.py
    ```
