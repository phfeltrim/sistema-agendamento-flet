import hashlib
from models.database import Database

class AuthController:
    def __init__(self):
        self.db = Database()

    def editar_usuario(self, usuario_id, nome, email, senha=None):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        if senha:
            import hashlib
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            query = "UPDATE usuarios SET nome=%s, email=%s, senha=%s WHERE id=%s"
            values = (nome, email, senha_hash, usuario_id)
        else:
            query = "UPDATE usuarios SET nome=%s, email=%s WHERE id=%s"
            values = (nome, email, usuario_id)
        self.db.cursor.execute(query, values)
        self.db.conn.commit()

    def criar_usuario(self, nome, email, senha):
        import hashlib
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()
        query = """
            INSERT INTO usuarios (nome, email, senha)
            VALUES (%s, %s, %s)
        """
        values = (nome, email, senha_hash)
        self.db.cursor.execute(query, values)
        self.db.conn.commit()
        return self.db.cursor.lastrowid if hasattr(self.db.cursor, 'lastrowid') else None

    def listar_usuarios(self):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        self.db.cursor.execute("SELECT id, nome, email, created_at FROM usuarios ORDER BY id DESC")
        return self.db.cursor.fetchall()

    def login(self, email: str, password: str) -> bool:
        if not email or not password:
            return False

        if not self.db.connect():
            return False
            
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            self.db.cursor.execute(
                "SELECT * FROM usuarios WHERE email = %s AND senha = %s",
                (email, hashed_password)
            )
            user = self.db.cursor.fetchone()
            return user is not None
        except Exception as e:
            print(f"Erro ao fazer login: {e}")
            return False
