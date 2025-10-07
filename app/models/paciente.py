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
    created_at: datetime
    cpf: Optional[str] = None
    telefone: Optional[str] = None
    cep: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    email: Optional[str] = None
    data_nascimento: Optional[date] = None
    observacoes: Optional[str] = None
    status: int = 1
    usuario_id: Optional[int] = None
    usuario_modificacao_id: Optional[int] = None
