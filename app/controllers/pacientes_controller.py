from ..models.paciente import Paciente
from ..models.database import Database
from datetime import datetime

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
        paciente_id = self.db.cursor.lastrowid
        self.db.conn.commit()
        
        # Após criar, busca o registro completo para ter todos os campos (como data_stamp)
        self.db.cursor.execute("SELECT * FROM pacientes WHERE id = %s", (paciente_id,))
        new_paciente_data = self.db.cursor.fetchone()

        # Retorna o objeto Paciente completo usando desempacotamento de dicionário
        if new_paciente_data:
            return Paciente(**new_paciente_data)
        return None

    def listar(self):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        
        self.db.cursor.execute("SELECT * FROM pacientes")
        pacientes_data = self.db.cursor.fetchall()
        return [Paciente(**p) for p in pacientes_data]

    def editar(self, paciente_id, name=None, cpf=None, telefone=None, cep=None, number=None, complement=None, email=None, status=None):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        
        campos = []
        valores = []
        if name is not None: campos.append("name=%s"); valores.append(name)
        if cpf is not None: campos.append("cpf=%s"); valores.append(cpf)
        if telefone is not None: campos.append("telefone=%s"); valores.append(telefone)
        if cep is not None: campos.append("cep=%s"); valores.append(cep)
        if number is not None: campos.append("number=%s"); valores.append(number)
        if complement is not None: campos.append("complement=%s"); valores.append(complement)
        if email is not None: campos.append("email=%s"); valores.append(email)
        if status is not None: campos.append("status=%s"); valores.append(status)
        
        if not campos: return False

        # Adiciona a data de modificação automaticamente
        campos.append("data_modif=%s")
        valores.append(datetime.now())

        query = f"UPDATE pacientes SET {', '.join(campos)} WHERE id=%s"
        valores.append(paciente_id)
        self.db.cursor.execute(query, valores)
        self.db.conn.commit()
        return True