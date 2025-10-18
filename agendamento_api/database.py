from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import configparser


# Lê as configurações do banco de dados
config = configparser.ConfigParser()
config.read('config.ini')
db_config = config['database']

# Monta a URL de conexão para o SQLAlchemy
DATABASE_URL = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Modelos SQLAlchemy (representação das suas tabelas) ---

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    senha = Column(String(255))

class Paciente(Base):
    __tablename__ = "pacientes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    # Adicione as outras colunas da sua tabela 'pacientes' aqui...
    email = Column(String(255))

# Adicione as outras classes para 'sessoes' e 'configuracoes' se precisar expô-las

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()