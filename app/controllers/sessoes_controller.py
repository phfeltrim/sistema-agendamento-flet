from ..models.database import Database
from datetime import datetime, timedelta
import requests
import os # Usado para buscar a chave da API de forma segura

class SessoesController:
    def __init__(self):
        self.db = Database()
        # Carrega a chave da API do Asaas a partir das variáveis de ambiente.
        # É uma prática de segurança essencial para não expor credenciais no código.
        self.ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")
        self.ASAAS_API_URL = "https://sandbox.asaas.com/api/v3/payments"

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

    def _gerar_boleto(self, paciente_id, sessao_id):
        """
        Função interna para gerar um boleto para a sessão agendada.
        """
        # 1. Buscar dados do paciente para o boleto
        # Esta query é um exemplo, ajuste conforme sua tabela de pacientes
        self.db.cursor.execute("SELECT name, cpf FROM pacientes WHERE id = %s", (paciente_id,))
        paciente = self.db.cursor.fetchone()
        if not paciente:
            print(f"AVISO: Paciente com ID {paciente_id} não encontrado. Boleto não gerado.")
            return None

        # 2. Montar os dados para a API do Asaas
        payload = {
            "customer": paciente['cpf'], # O Asaas usa o CPF para vincular/criar o cliente
            "billingType": "BOLETO",
            "value": 150.00,
            "dueDate": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            "description": f"Pagamento da sessão de agendamento ID: {sessao_id}",
            "externalReference": f"sessao_{sessao_id}",
        }

        if not self.ASAAS_API_KEY:
            print("ERRO: A variável de ambiente 'ASAAS_API_KEY' não está configurada. Boleto não pode ser gerado.")
            # Você pode optar por lançar uma exceção aqui para um tratamento de erro mais robusto.
            return None

        headers = {
            "Content-Type": "application/json",
            "access_token": self.ASAAS_API_KEY
        }

        # 3. Fazer a requisição para a API
        try:
            response = requests.post(self.ASAAS_API_URL, json=payload, headers=headers)
            response.raise_for_status() # Lança um erro para respostas 4xx ou 5xx
            dados_boleto = response.json()
            print(f"Boleto gerado com sucesso! URL: {dados_boleto.get('bankSlipUrl')}")
            return dados_boleto
        except requests.exceptions.RequestException as e:
            print(f"ERRO ao gerar boleto: {e}")
            return None

    def adicionar(self, paciente_id, data_hora):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = '''
            INSERT INTO sessoes (paciente_id, data_hora)
            VALUES (%s, %s)
        '''
        values = (paciente_id, data_hora.strftime('%Y-%m-%d %H:%M:%S'))
        try:
            self.db.cursor.execute(query, values)
            sessao_id = self.db.cursor.lastrowid
            self.db.conn.commit()
            
            # Após salvar a sessão, gera o boleto
            dados_boleto = self._gerar_boleto(paciente_id, sessao_id)
            # Retorna tanto o ID da sessão quanto os dados do boleto para a interface
            return sessao_id, dados_boleto
        except Exception as e:
            self.db.conn.rollback() # Desfaz a inserção em caso de erro no boleto
            print(f"Erro ao adicionar sessão ou gerar boleto: {e}")
            return None, None

    def listar_por_dia(self, data):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = '''
            SELECT s.id, s.paciente_id, s.data_hora, p.name as paciente_nome
            FROM sessoes s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE DATE(s.data_hora) = %s
            ORDER BY s.data_hora
            DESC
        '''
        values = (data.strftime('%Y-%m-%d'),)
        self.db.cursor.execute(query, values)
        return self.db.cursor.fetchall()
