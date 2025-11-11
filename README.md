# ✨ Rastreador de Hábitos com IA

Um simples, mas poderoso, rastreador de hábitos construído com Python (Flask) e JavaScript, que usa a API do Gemini para sugerir automaticamente novos hábitos com base numa meta maior.

---

## 🚀 Funcionalidades Principais

* **Adicionar e Remover Hábitos:** Regista e apaga hábitos diários.
* **Marcar como Concluído:** Clica para marcar um hábito como feito no dia.
* **Estatísticas Visuais:**
    * **Streak (Sequência) 🔥:** Mostra quantos dias seguidos completaste um hábito.
    * **Taxa de Sucesso 📊:** Calcula a percentagem de sucesso desde que o hábito foi criado.
    * **Gráfico de 7 Dias:** Um gráfico de barras simples mostra a tua performance na última semana.
* **Sugestão de Hábitos com IA ✨:**
    * Tens uma meta grande? (ex: "Correr uma maratona")
    * Escreve a meta no input e clica no botão "✨".
    * A aplicação usa a API do Google Gemini para quebrar essa meta em 3-5 hábitos diários mais pequenos e fáceis de gerir (ex: "Alongar 10 min", "Correr 3km", "Beber 3L de água").

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Flask, Flask-SQLAlchemy
* **Frontend:** HTML5, CSS3, JavaScript (Puro / Vanilla JS)
* **Base de Dados:** SQLite
* **API de IA:** Google Gemini

## 🏁 Como Executar o Projeto Localmente

1.  **Clona o repositório:**
    ```bash
    git clone https://github.com/JoaoMarcosJJ/habits-ai.git
    ```

2.  **Cria e ativa um ambiente virtual:**
    ```bash
    # Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    
    # macOS / Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Instala as dependências:**
    ```bash
    pip install -r requirements.txt
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

6.  Abre o teu navegador e visita: `localhost:5000/`
