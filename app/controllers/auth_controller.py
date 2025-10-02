import bcrypt
from ..models.database import Database

class AuthController:
    def __init__(self):
        self.db = Database()

    def login(self, email: str, password: str):
        if not email or not password:
            return None
        if not self.db.connect():
            return None
        try:
            self.db.cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            user = self.db.cursor.fetchone()
            if user and bcrypt.checkpw(password.encode('utf-8'), user['senha'].encode('utf-8')):
                print(f"Login bem-sucedido para: {user['email']}")
                return user  # Retorna o dicionário do usuário
            print(f"Falha no login para: {email}")
            return None
        except Exception as e:
            print(f"Erro durante o login: {e}")
            return None

    # Exemplo para criar_usuario:
    def criar_usuario(self, nome, email, senha):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
        query = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
        values = (nome, email, senha_hash)
        self.db.cursor.execute(query, values)
        self.db.conn.commit()
        return self.db.cursor.lastrowid
    
    def excluir_usuario(self, usuario_id: int):
        """ Exclui um usuário do banco de dados pelo seu ID. """
        if not self.db.connect():
            raise ConnectionError("Não foi possível conectar ao banco de dados.")
        
        try:
            query = "DELETE FROM usuarios WHERE id = %s"
            self.db.cursor.execute(query, (usuario_id,))
            self.db.conn.commit()
            print(f"Usuário com ID {usuario_id} excluído com sucesso.")
            return True
        except Exception as e:
            print(f"Erro ao excluir usuário: {e}")
            self.db.conn.rollback() # Desfaz a operação em caso de erro
            return False
        finally:
            self.db.disconnect()