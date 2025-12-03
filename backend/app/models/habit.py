from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Habit(Base):

    """
    Modelo de dados que representa a tabela 'habits'.
    """

    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(500), nullable=True)

    # Timestamps automáticos (Audit fields)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    is_active = Column(Boolean, default=True)
    logs = relationship("HabitLog", back_populates="habit", lazy="selectin", cascade="all, delete-orphan")

class HabitLog(Base):
    """
    Tabela que guarda os dias que o hábito foi concluído. 
    """
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    completed_date = Column(Date, nullable=False, default=func.current_date())

    habit = relationship("Habit", back_populates="logs")