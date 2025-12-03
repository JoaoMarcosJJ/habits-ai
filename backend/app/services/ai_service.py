import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from app.core.config import settings
from app.schemas.ai import AIResponse
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from app.schemas.ai import AIResponse, ChatRequest, ChatResponse 

class AIService:
    def __init__(self):
        # Inicializa o Gemini com a chave da API
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash", 
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0.7
        )

    async def generate_habits_from_goal(self, goal: str) -> AIResponse:
        # Template do Prompt
        template = """
        Atue como um coach de produtividade.
        Meta do usuário: "{goal}"
        
        Crie de 3 a 5 hábitos curtos para esta meta.
        
        IMPORTANTE: Sua resposta deve ser ESTRITAMENTE um JSON válido. 
        NÃO escreva "Aqui está", NÃO use Markdown (```json), apenas o objeto JSON cru.
        
        Formato obrigatório:
        {{ "habits": ["Hábito 1", "Hábito 2", "Hábito 3", "Hábito 4", "Hábito 5"] }}
        """
        
        prompt = PromptTemplate(input_variables=["goal"], template=template)
        chain = prompt | self.llm

        try:
            # Aumentar timeout implícito aguardando a resposta
            response = await chain.ainvoke({"goal": goal})
            content = response.content

            # Limpeza para garantir uma resposta JSON
            cleaned_content = content.replace("```json", "").replace("```", "").strip()
            
            # Tenta encontrar o início e fim do JSON se houver lixo em volta
            if "{" in cleaned_content and "}" in cleaned_content:
                start = cleaned_content.find("{")
                end = cleaned_content.rfind("}") + 1
                cleaned_content = cleaned_content[start:end]

            data = json.loads(cleaned_content)
            
            # Garante que a chave habits existe
            if "habits" not in data:
                return AIResponse(habits=["A IA respondeu, mas sem hábitos válidos."])

            return AIResponse(habits=data["habits"])

        except json.JSONDecodeError as e:
            print(f"ERRO AO LER JSON: {e}")
            return AIResponse(habits=["Erro: A IA não retornou um formato válido."])
        except Exception as e:
            print(f"ERRO GERAL NA IA: {e}")
            raise e
        
    async def run_chat(self, chat_data: ChatRequest) -> ChatResponse:
        history = [
            SystemMessage(content="Você é um assistente amigável e motivador focado em produtividade e hábitos saudáveis. Responda de forma concisa e útil.")
        ]

        for msg in chat_data.messages:
            if msg.role == 'user':
                history.append(HumanMessage(content=msg.content))
            else:
                history.append(AIMessage(content=msg.content))

        response = await self.llm.ainvoke(history)
        
        return ChatResponse(response=response.content)