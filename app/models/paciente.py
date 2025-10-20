from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

@dataclass
class Paciente:
    """
    Representa o modelo de dados para um paciente.
    Os nomes dos atributos correspondem às colunas da tabela 'pacientes'.
    """
    id: int
    name: str
    data_stamp: datetime 
    number: Optional[str] = None
    complement: Optional[str] = None
    user: Optional[int] = None
    user_modif: Optional[int] = None
    data_modif: Optional[datetime] = None
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    cep: Optional[str] = None
    email: Optional[str] = None
    status: int = 1