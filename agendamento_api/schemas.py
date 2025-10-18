from pydantic import BaseModel, EmailStr
from typing import Optional

# Schema para exibir um paciente (não mostra dados sensíveis)
class Paciente(BaseModel):
    id: int
    name: str
    email: Optional[EmailStr] = None

    class Config:
        orm_mode = True # Permite que o Pydantic leia dados de objetos SQLAlchemy

# Schema para criar um novo paciente
class PacienteCreate(BaseModel):
    name: str
    email: EmailStr
    # Adicione outros campos necessários para criar um paciente
    