from ..models.database import Database
from ..models.paciente import Paciente


class PacientesController:
    def __init__(self):
        self.db = Database()

    def adicionar(self, name, cpf, telefone, cep, numero, complemento, email, status=1, usuario_id=None):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        
        query = """
            INSERT INTO pacientes (name, cpf, telefone, cep, numero, complemento, email, status, usuario_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            name, cpf, telefone,
            cep, numero, complemento,
            email, status, usuario_id
        )
        
        self.db.cursor.execute(query, values)
        self.db.conn.commit()
        return self.db.cursor.lastrowid

    def editar(self, paciente_id, paciente_data):
        """
        Atualiza os dados de um paciente no banco de dados.
        """
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")

        # Monta a query de atualização dinamicamente
        campos = []
        valores = []
        for chave, valor in paciente_data.items():
            campos.append(f"{chave}=%s")
            valores.append(valor)

        if not campos:
            return False # Nada para atualizar

        query = f"UPDATE pacientes SET {', '.join(campos)} WHERE id=%s"
        valores.append(paciente_id)

        self.db.cursor.execute(query, tuple(valores))
        self.db.conn.commit()
        return True

    def listar(self):
        if not self.db.connect():
            return []
        self.db.cursor.execute("SELECT * FROM pacientes")
        pacientes_data = self.db.cursor.fetchall()
        return [Paciente(**p) for p in pacientes_data]