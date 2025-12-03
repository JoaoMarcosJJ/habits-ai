from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime, date

# Schema de Logs (Datas Completas)
class HabitLogRead(BaseModel):
    id: int
    completed_date: date

    model_config = ConfigDict(from_attributes=True)

# Schema Base (campos comuns)
class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None

# Schema para Criação (O que o usuário envia)
class HabitCreate(HabitBase):
    pass

# Schema para Atualização (Opcionais)
class HabitUpdate(HabitBase):
    name: Optional[str] = None
    is_active: Optional[bool] = None

# Schema para Leitura (O que a API devolve)
class HabitRead(HabitBase):
    id: int
    created_at: datetime
    is_active: bool
    logs: List[HabitLogRead] = []

    # Configuração necessária para o Pydantic ler objetos ORM do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)