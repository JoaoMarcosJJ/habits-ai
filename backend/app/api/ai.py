from fastapi import APIRouter, HTTPException
from app.schemas.ai import AIRequest, AIResponse, ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter()

@router.post("/suggest", response_model=AIResponse)
async def suggest_habits(request: AIRequest):
    if not request.goal:
        raise HTTPException(status_code=400, detail="A meta é obrigatória")
    
    service = AIService()
    try:
        return await service.generate_habits_from_goal(request.goal)
    except Exception as e:
        print(f"Erro na IA: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    service = AIService()
    try:
        return await service.run_chat(request)
    except Exception as e:
        return ChatResponse(response="Desculpe, estou com dificuldades de conexão no momento.")