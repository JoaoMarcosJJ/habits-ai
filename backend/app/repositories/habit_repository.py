from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate

class HabitRepository:
    
    """
    Camada de Acesso a Dados (Data Access Layer).
    Responsável apenas por criar, ler, atualizar e deletar dados no banco.
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, habit_in: HabitCreate) -> Habit:
        db_habit = Habit(
            name=habit_in.name,
            description=habit_in.description
        )
        self.db.add(db_habit)
        # O commit é feito no Service ou na injeção de dependência para garantir atomicidade
        await self.db.flush() # Gera o ID sem fechar a transação
        await self.db.refresh(db_habit)
        return db_habit

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Habit]:
        query = select(Habit).where(Habit.is_active == True).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_by_id(self, habit_id: int) -> Optional[Habit]:
        query = select(Habit).where(Habit.id == habit_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def delete(self, habit: Habit) -> None:
        await self.db.delete(habit)
        await self.db.commit()