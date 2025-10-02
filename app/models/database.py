import mysql.connector
import configparser
import os
from pathlib import Path

class Database:
    def __init__(self, config_file='config.ini'):
        self.config_file = config_file
        self.conn = None
        self.cursor = None

    def connect(self):
        if self.conn and self.conn.is_connected():
            return True
        try:
            # Esta lógica encontra a pasta raiz do projeto e procura o config.ini lá.
            base_dir = Path(__file__).resolve().parent.parent.parent
            config_path = os.path.join(base_dir, self.config_file)

            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Arquivo de configuração '{config_path}' não encontrado.")

            config = configparser.ConfigParser()
            config.read(config_path)

            db_config = config['database']

            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor(dictionary=True)
            print("Conexão com o banco de dados MySQL estabelecida com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False

    def disconnect(self):
        if self.conn and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()