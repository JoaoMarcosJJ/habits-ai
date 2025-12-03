from fastapi import HTTPException
from app.repositories.habit_repository import HabitRepository
from app.schemas.habit import HabitCreate, HabitRead
from typing import List
from app.models.habit import Habit, HabitLog
from datetime import date
from sqlalchemy import and_
from sqlalchemy.future import select

class HabitService:
    """
    Camada de Regra de Negócio.
    Coordena as operações e aplica validações lógicas.
    """

    def __init__(self, repository: HabitRepository):
        self.repository = repository

    async def create_new_habit(self, habit_data: HabitCreate) -> HabitRead:
        # Exemplo de regra de negócio: Não permitir hábitos duplicados (lógica futura)
        # Por enquanto, apenas delega a criação
        return await self.repository.create(habit_data)

    async def list_habits(self, skip: int = 0, limit: int = 100) -> List[HabitRead]:
        return await self.repository.get_all(skip, limit)
    
    async def get_habit(self, habit_id: int) -> HabitRead:
        habit = await self.repository.get_by_id(habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Hábito não encontrado")
        return habit
    
    async def toggle_habit(self, habit_id: int) -> Habit:
        today = date.today()
        
        query = select(HabitLog).where(and_(HabitLog.habit_id == habit_id, HabitLog.completed_date == today))

        result = await self.repository.db.execute(query)
        existing_log = result.scalar_one_or_none()

        if existing_log:
            await self.repository.db.delete(existing_log)
        else:
            new_log = HabitLog(habit_id=habit_id, completed_date=today)
            self.repository.db.add(new_log)

        await self.repository.db.commit()

        return await self.repository.get_by_id(habit_id)
    
    async def delete_habit(self, habit_id: int):
        habit = await self.repository.get_by_id(habit_id)
        if not habit:
            raise HTTPException(status_code=404, detail="Hábito não encontrado")

        await self.repository.delete(habit)