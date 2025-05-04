from models.paciente import Paciente
from models.database import Database

class PacientesController:
    def __init__(self):
        self.db = Database()

    def adicionar(self, name, cpf, telefone, cep, number, complement, email, status, user):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = """
            INSERT INTO pacientes (name, cpf, telefone, cep, number, complement, email, status, user)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (name, cpf, telefone, cep, number, complement, email, status, user)
        self.db.cursor.execute(query, values)
        paciente_id = self.db.cursor.lastrowid if hasattr(self.db.cursor, 'lastrowid') else None
        self.db.conn.commit()
        return Paciente(name, cpf, telefone, cep, number, complement, email, status, user, id=paciente_id)

    def listar(self):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        self.db.cursor.execute("SELECT * FROM pacientes")
        pacientes = []
        for row in self.db.cursor.fetchall():
            paciente = Paciente(
                row['name'],
                row['cpf'],
                row['telefone'],
                row['cep'],
                row['number'],
                row['complement'],
                row['email'],
                row['status'],
                row['user'],
                id=row['id'] if 'id' in row else None
            )
            pacientes.append(paciente)
        return pacientes

    def editar(self, paciente_id, name=None, cpf=None, telefone=None, cep=None, number=None, complement=None, email=None, status=None):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        campos = []
        valores = []
        if name is not None:
            campos.append("name=%s")
            valores.append(name)
        if cpf is not None:
            campos.append("cpf=%s")
            valores.append(cpf)
        if telefone is not None:
            campos.append("telefone=%s")
            valores.append(telefone)
        if cep is not None:
            campos.append("cep=%s")
            valores.append(cep)
        if number is not None:
            campos.append("number=%s")
            valores.append(number)
        if complement is not None:
            campos.append("complement=%s")
            valores.append(complement)
        if email is not None:
            campos.append("email=%s")
            valores.append(email)
        if status is not None:
            campos.append("status=%s")
            valores.append(status)
        if not campos:
            return False  # Nada para atualizar
        query = f"UPDATE pacientes SET {', '.join(campos)} WHERE id=%s"
        valores.append(paciente_id)
        self.db.cursor.execute(query, valores)
        self.db.conn.commit()
        return True

    # Não implementar/remover método de remoção!
