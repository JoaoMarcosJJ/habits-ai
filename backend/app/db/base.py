from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Classe base para todos os modelos ORM do SQLAlchemy"""
    pass

# Importaremos os modelos aqui depois (ex: from app.models.habit import Habit)