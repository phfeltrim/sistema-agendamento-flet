from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import database, schemas



# Cria as tabelas no banco de dados se elas não existirem
database.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# --- Endpoints para Pacientes ---

@app.get("/pacientes/", response_model=List[schemas.Paciente])
def listar_pacientes(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Endpoint para listar todos os pacientes.
    """
    pacientes = db.query(database.Paciente).offset(skip).limit(limit).all()
    return pacientes

@app.get("/pacientes/{paciente_id}", response_model=schemas.Paciente)
def ler_paciente(paciente_id: int, db: Session = Depends(database.get_db)):
    """
    Endpoint para obter os detalhes de um único paciente.
    """
    paciente = db.query(database.Paciente).filter(database.Paciente.id == paciente_id).first()
    if paciente is None:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return paciente