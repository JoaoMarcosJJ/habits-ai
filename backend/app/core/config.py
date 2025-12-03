from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, computed_field
from typing import Optional

class Settings(BaseSettings):
    """
    Classe de configuração centralizada.
    Lê automaticamente as variáveis do sistema ou do arquivo .env.
    """
    PROJECT_NAME: str = "Habits GenAI"
    API_STR: str = "/api"

    SECRET_KEY: str = "chave_padrao_insegura"

    GEMINI_API_KEY: Optional[str] = None

    # Credenciais do Banco de Dados
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # Computed field gera a URL completa automaticamente
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg", # Driver assíncrono
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        ))
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "ignore" # <--- Ignora variáveis extras no .env sem dar erro

# Instância única (Singleton) para ser importada em todo o projeto
settings = Settings()