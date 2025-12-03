from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import habits
from app.api import ai

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_STR}/openapi.json"
)

# Configuração de CORS (Cross-Origin Resource Sharing)
# Permite que o Frontend (em outra porta) converse com o Backend
origins = [
    "http://localhost",
    "http://localhost:3000", # Porta comum do Vue/Vite
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir Rotas
app.include_router(habits.router, prefix="/api/habits", tags=["habits"])
app.include_router(ai.router, prefix="/api/ai", tags=["ai"])

# Rota de Health Check
@app.get("/health")
def health_check():
    return {"status": "ok", "version": "0.1.0"}