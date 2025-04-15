import hashlib
from models.database import Database

class AuthController:
    def __init__(self):
        self.db = Database()

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
