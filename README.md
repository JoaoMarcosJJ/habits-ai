# 🌱 Habits GenAI

Uma aplicação Full-Stack moderna para rastreamento de hábitos, potenciada por Inteligência Artificial (Google Gemini) para gerar rotinas personalizadas e fornecer coaching interativo.

## 🚀 Funcionalidades

* **Gestão de Hábitos:** Adicionar, remover e marcar hábitos diários como concluídos.
* **Gerador de Hábitos com IA ✨:** Digite uma meta (ex: "Correr uma maratona") e a IA cria um plano de hábitos acionáveis.
* **AI Coach Chatbot 🤖:** Um assistente virtual integrado para tirar dúvidas e dar motivação sobre produtividade.
* **Análise de Dados 📊:** Gráficos interativos para visualizar o desempenho semanal de cada hábito.
* **Arquitetura:** Totalmente containerizada, com separação clara entre Frontend, Backend e Banco de Dados.

## 🛠️ Tech Stack

### Infraestrutura
* **Docker & Docker Compose:** Orquestração de containers.
* **PostgreSQL:** Banco de dados relacional robusto.

### Backend (API)
* **Python 3.11 + FastAPI:** Framework moderno e assíncrono.
* **SQLAlchemy (Async):** ORM para comunicação com o banco.
* **LangChain:** Framework para integração com LLMs.
* **Google Gemini 2.5 Flash:** Modelo de IA Generativa.
* **Alembic:** Migrações de banco de dados.

### Frontend (Client)
* **Vue.js 3 (Composition API):** Framework reativo.
* **TypeScript:** Segurança de tipagem.
* **Vite:** Build tool.
* **Pinia:** Gestão de estado global.
* **Chart.js:** Visualização de dados.

## 🏁 Como Executar o Projeto

### Pré-requisitos
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando.
* Uma API Key do [Google AI Studio](https://aistudio.google.com/).

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/JoaoMarcosJJ/habits-ai.git](https://github.com/JoaoMarcosJJ/habits-ai.git)
    cd habits-ai
    ```

2.  **Configure as Variáveis de Ambiente:**
    * Crie um arquivo `.env` dentro da pasta `backend/`.
    * Adicione a sua chave:
    ```ini
    POSTGRES_USER=admin
    POSTGRES_PASSWORD=admin
    POSTGRES_DB=habits_db
    POSTGRES_SERVER=db
    POSTGRES_PORT=5432
    
    GEMINI_API_KEY="SUA_CHAVE_AQUI"
    ```

3.  **Inicie a Aplicação (Docker):**
    Na raiz do projeto, execute:
    ```bash
    docker-compose up -d --build
    ```

4.  **Configura a tua API Key:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adiciona a tua API Key do Google Gemini dentro dele:
    ```text
    GEMINI_API_KEY="SUA_API_KEY_VAI_AQUI"
    ```

5.  **Executa a aplicação:**
    ```bash
    python app.py
    ```

6.  Abre o teu navegador e visita: `http://127.0.0.1:5000/`