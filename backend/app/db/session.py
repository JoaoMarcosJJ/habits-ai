from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.core.config import settings
from typing import AsyncGenerator

# Criar a Engine
engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=False, # Mude para True se quiser ver os SQLs no terminal
    future=True
)

# Criar a Session Factory
# expire_on_commit=False é padrão em async para evitar erros de I/O desnecessários
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False
)

# Dependência (Dependency Injection)
# O FastAPI vai usar isso para injetar a sessão nas rotas
async def get_db() -> AsyncGenerator[AsyncSession, None]:

    """
    Generator que cria uma sessão para cada requisição e a fecha ao terminar.
    Garante que não vai existir conexões abertas (Resource Management).
    """

    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()