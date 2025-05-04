from models.database import Database
from datetime import datetime

class SessoesController:
    def __init__(self):
        self.db = Database()

    def editar(self, sessao_id, paciente_id=None, data_hora=None):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        campos = []
        valores = []
        if paciente_id is not None:
            campos.append("paciente_id=%s")
            valores.append(paciente_id)
        if data_hora is not None:
            campos.append("data_hora=%s")
            valores.append(data_hora.strftime('%Y-%m-%d %H:%M:%S'))
        if not campos:
            return False
        query = f"UPDATE sessoes SET {', '.join(campos)} WHERE id=%s"
        valores.append(sessao_id)
        self.db.cursor.execute(query, valores)
        self.db.conn.commit()
        return True

    def excluir(self, sessao_id):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = "DELETE FROM sessoes WHERE id=%s"
        self.db.cursor.execute(query, (sessao_id,))
        self.db.conn.commit()
        return True

    def adicionar(self, paciente_id, data_hora, status='agendada'):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = '''
            INSERT INTO sessoes (paciente_id, data_hora)
            VALUES (%s, %s)
        '''
        values = (paciente_id, data_hora.strftime('%Y-%m-%d %H:%M:%S'))
        self.db.cursor.execute(query, values)
        self.db.conn.commit()
        return self.db.cursor.lastrowid if hasattr(self.db.cursor, 'lastrowid') else None

    def listar_por_dia(self, data):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = '''
            SELECT s.id, s.paciente_id, s.data_hora, p.name as paciente_nome
            FROM sessoes s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE DATE(s.data_hora) = %s
            ORDER BY s.data_hora
        '''
        values = (data.strftime('%Y-%m-%d'),)
        self.db.cursor.execute(query, values)
        return self.db.cursor.fetchall()
