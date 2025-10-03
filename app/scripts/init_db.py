import mysql.connector
from mysql.connector import Error
import bcrypt
import configparser
from pathlib import Path
import os

def create_database():
    conn = None
    cursor = None
    try:
        # Encontra o config.ini na pasta raiz do projeto
        base_dir = Path(__file__).resolve().parent.parent.parent
        config_path = os.path.join(base_dir, 'config.ini')

        config = configparser.ConfigParser()
        config.read(config_path)
        db_config = config['database']

        conn = mysql.connector.connect(
            **{k: v for k, v in db_config.items() if k != 'database'} # Conecta sem especificar o DB
        )
        if conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            
            # Criar banco de dados
            cursor.execute("CREATE DATABASE IF NOT EXISTS agendamento")
            print("Banco de dados 'agendamento' criado com sucesso!")
            
            # Usar o banco de dados
            cursor.execute("USE agendamento")
            
            # Criar tabelas
            tables = [
                """
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    senha VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS pacientes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(100),
                    telefone VARCHAR(20),
                    data_nascimento DATE,
                    observacoes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS sessoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    paciente_id INT,
                    data_hora DATETIME NOT NULL,
                    status ENUM('agendada', 'concluida', 'cancelada') DEFAULT 'agendada',
                    observacoes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
                )
                """,
                """
                CREATE TABLE IF NOT EXISTS configuracoes (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    chave VARCHAR(50) UNIQUE NOT NULL,
                    valor TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            ]
            
            for table in tables:
                cursor.execute(table)
                
            print("Tabelas criadas com sucesso!")
            
            # Criar usuário admin padrão
            hashed_password = bcrypt.hashpw("admin123".encode('utf-8'), bcrypt.gensalt())
            try:
                cursor.execute("""
                    INSERT INTO usuarios (nome, email, senha)
                    VALUES (%s, %s, %s)
                """, ("Administrador", "admin@admin.com", hashed_password.decode('utf-8')))
                conn.commit()
                print("Usuário admin criado com sucesso!")
                print("Email: admin@admin.com")
                print("Senha: admin123")
            except Error as e:
                if e.errno == 1062:  # Duplicate entry error
                    print("Usuário admin já existe!")
                else:
                    print(f"Erro ao criar usuário admin: {e}")
                    
    except Error as e:
        print(f"Erro: {e}")
    finally: # Garante que a conexão seja fechada
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

if __name__ == "__main__":
    create_database()
