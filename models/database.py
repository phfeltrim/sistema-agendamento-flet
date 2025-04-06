import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password=""
            )
            if self.conn.is_connected():
                self.cursor = self.conn.cursor(dictionary=True)
                self.cursor.execute("CREATE DATABASE IF NOT EXISTS agendamento")
                self.conn.database = "agendamento"
                self._create_tables()
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def _create_tables(self):
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
            try:
                self.cursor.execute(table)
                self.conn.commit()
            except Error as e:
                print(f"Erro ao criar tabela: {e}")

    def close(self):
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()
