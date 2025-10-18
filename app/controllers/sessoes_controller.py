from ..models.database import Database
from datetime import datetime, timedelta
import requests
import os


class SessoesController:
    def __init__(self):
        self.db = Database()
        # As variáveis de ambiente agora são carregadas no main.py
        # É uma prática de segurança essencial para não expor credenciais no código.
        self.ASAAS_API_KEY = os.getenv("ASAAS_API_KEY")
        self.ASAAS_API_URL = "https://sandbox.asaas.com/api/v3/payments"
        self.ASAAS_CUSTOMER_URL = "https://sandbox.asaas.com/api/v3/customers"

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

    def _get_ou_create_asaas_customer(self, paciente):
        """Busca um cliente no Asaas pelo CPF. Se não existir, cria um novo."""
        # Garante que o CPF contenha apenas números
        cpf_limpo = ''.join(filter(str.isdigit, paciente.get('cpf', '')))
        if not cpf_limpo:
            print("ERRO: CPF do paciente está vazio ou é inválido. Não é possível criar cliente no Asaas.")
            return None

        headers = {"Content-Type": "application/json", "access_token": self.ASAAS_API_KEY}
        # 1. Tenta buscar o cliente pelo CPF
        try:
            response = requests.get(f"{self.ASAAS_CUSTOMER_URL}?cpfCnpj={cpf_limpo}", headers=headers)
            response.raise_for_status()
            data = response.json()
            if data['totalCount'] > 0:
                customer_id = data['data'][0]['id']
                print(f"Cliente Asaas encontrado: {customer_id}")
                return customer_id
        except requests.exceptions.RequestException as e:
            print(f"Erro ao buscar cliente no Asaas: {e}")
            # Continua para tentar criar, pois a busca pode ter falhado

        # 2. Se não encontrou, cria um novo cliente
        print(f"Cliente não encontrado. Criando novo cliente no Asaas para {paciente['name']}.")
        customer_payload = {
            "name": paciente['name'],
            "cpfCnpj": cpf_limpo, # Usa o CPF limpo
            "email": paciente.get('email') # Usa .get() para evitar erro se o email for nulo
        }
        try:
            response = requests.post(self.ASAAS_CUSTOMER_URL, json=customer_payload, headers=headers)
            response.raise_for_status()
            new_customer = response.json()
            customer_id = new_customer['id']
            print(f"Novo cliente Asaas criado: {customer_id}")
            return customer_id
        except requests.exceptions.HTTPError as e:
            print(f"ERRO HTTP ao criar cliente no Asaas: {e}")
            print(f"Detalhes do erro: {e.response.text}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"ERRO ao criar cliente no Asaas: {e}")
            return None

    def _gerar_boleto(self, paciente_id, sessao_id):
        """
        Função interna para gerar um boleto para a sessão agendada.
        """
        # 1. Buscar dados do paciente para o boleto
        self.db.cursor.execute("SELECT name, cpf, email FROM pacientes WHERE id = %s", (paciente_id,))
        paciente = self.db.cursor.fetchone()
        if not paciente:
            print(f"AVISO: Paciente com ID {paciente_id} não encontrado. Boleto não gerado.")
            return None

        # 2. Obter ou criar o cliente no Asaas
        customer_id = self._get_ou_create_asaas_customer(paciente)
        if not customer_id:
            return None # Falha ao obter/criar cliente, boleto não pode ser gerado.

        # 3. Montar os dados para a API do Asaas
        payload = {
            "customer": customer_id, # Agora usamos o ID do cliente Asaas
            "billingType": "BOLETO",
            "value": 150.00,
            "dueDate": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
            "description": f"Pagamento da sessão de agendamento ID: {sessao_id}",
            "externalReference": f"sessao_{sessao_id}",
        }

        if not self.ASAAS_API_KEY:
            # Lança uma exceção para um tratamento de erro mais robusto.
            raise ValueError("A variável de ambiente 'ASAAS_API_KEY' não está configurada.")

        headers = {
            "Content-Type": "application/json",
            "access_token": self.ASAAS_API_KEY
        }

        # 4. Fazer a requisição para a API de pagamentos
        try:
            response = requests.post(self.ASAAS_API_URL, json=payload, headers=headers)
            response.raise_for_status() # Lança um erro para respostas 4xx ou 5xx
            dados_boleto = response.json()
            print(f"Boleto gerado com sucesso! URL: {dados_boleto.get('bankSlipUrl')}")
            return dados_boleto
        except requests.exceptions.HTTPError as e:
            # Captura erros HTTP (como 4xx, 5xx) para inspecionar a resposta
            print(f"ERRO HTTP ao gerar boleto: {e}")
            print(f"Detalhes do erro: {e.response.text}") # Mostra a mensagem de erro da API
            return None
        except requests.exceptions.RequestException as e:
            print(f"ERRO ao gerar boleto: {e}")
            return None

    def adicionar(self, paciente_id, data_hora):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        
        try:
            # 1. Gera o boleto ANTES de inserir no banco
            dados_boleto = self._gerar_boleto(paciente_id, f"novo_agendamento_{datetime.now().timestamp()}")
            boleto_url = dados_boleto.get("bankSlipUrl") if dados_boleto else None

            # 2. Insere a sessão no banco, já com a URL do boleto
            query = '''
                INSERT INTO sessoes (paciente_id, data_hora, boleto_url)
                VALUES (%s, %s, %s)
            '''
            values = (paciente_id, data_hora.strftime('%Y-%m-%d %H:%M:%S'), boleto_url)
            
            self.db.cursor.execute(query, values)
            sessao_id = self.db.cursor.lastrowid

            # 3. Se tudo deu certo, confirma a transação
            self.db.conn.commit()

            # Retorna tanto o ID da sessão quanto os dados do boleto para a interface
            return sessao_id, dados_boleto
        except Exception as e:
            self.db.conn.rollback() # Desfaz a inserção em caso de erro no boleto
            print(f"ERRO CRÍTICO ao adicionar sessão ou gerar boleto: {e}")
            return None, None

    def listar_por_dia(self, data):
        if not self.db.connect():
            raise Exception("Erro ao conectar ao banco de dados.")
        query = '''
            SELECT s.id, s.paciente_id, s.data_hora, s.status, p.name as paciente_nome
            FROM sessoes s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE DATE(s.data_hora) = %s
            ORDER BY s.data_hora
            DESC
        '''
        values = (data.strftime('%Y-%m-%d'),)
        self.db.cursor.execute(query, values)
        return self.db.cursor.fetchall()
