from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.habit import HabitCreate, HabitRead
from app.repositories.habit_repository import HabitRepository
from app.services.habit_service import HabitService

router = APIRouter()

# Factory function para instanciar o Service com suas dependências
def get_habit_service(db: AsyncSession = Depends(get_db)) -> HabitService:
    repository = HabitRepository(db)
    return HabitService(repository)

@router.post("/", response_model=HabitRead, status_code=status.HTTP_201_CREATED)
async def create_habit(
    habit_in: HabitCreate,
    service: HabitService = Depends(get_habit_service)
):
    """
    Cria um novo hábito.
    """
    return await service.create_new_habit(habit_in)

@router.get("/", response_model=List[HabitRead])
async def read_habits(
    skip: int = 0,
    limit: int = 100,
    service: HabitService = Depends(get_habit_service)
):
    """
    Lista todos os hábitos ativos.
    """
    return await service.list_habits(skip, limit)

@router.post("/{habit_id}/toggle", response_model=HabitRead)
async def toggle_habit_status(
    habit_id: int,
    service: HabitService = Depends(get_habit_service)
):
    """ Marca ou desmarca hábito feito hoje. """
    return await service.toggle_habit(habit_id)

@router.delete("/{habit_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_habit(
    habit_id: int,
    service: HabitService = Depends(get_habit_service)
):
    """Apaga um hábito permanentemente."""
    await service.delete_habit(habit_id)