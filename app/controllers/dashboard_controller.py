from ..models.database import Database
from .configuracoes_controller import ConfiguracoesController
from datetime import datetime

class DashboardController:
    def __init__(self):
        self.db = Database()
        self.config_ctrl = ConfiguracoesController()

    def get_dados_dashboard(self, ano=None, mes=None):
        """Busca e calcula todas as estatísticas para o dashboard."""
        if not self.db.connect():
            raise ConnectionError("Não foi possível conectar ao banco de dados.")

        try:
            # Pega valores de configuração como string
            valor_sessao_str = self.config_ctrl.get_config("valor_sessao") or "0"
            custo_fixo_str = self.config_ctrl.get_config("custo_fixo_mensal") or "0"

            # Substitui a vírgula pelo ponto ANTES de converter para float
            valor_sessao = float(valor_sessao_str.replace(',', '.'))
            custo_fixo = float(custo_fixo_str.replace(',', '.'))

            # --- Query para Sessões ---
            # IMPORTANTE: Assumindo que status=1 significa "Realizada/Paga"
            query_sessoes = "SELECT COUNT(id) as total, MONTH(data_hora) as mes FROM sessoes WHERE status = 1"
            params_sessoes = []
            if ano:
                query_sessoes += " AND YEAR(data_hora) = %s"
                params_sessoes.append(ano)
            if mes:
                query_sessoes += " AND MONTH(data_hora) = %s"
                params_sessoes.append(mes)
            
            self.db.cursor.execute(query_sessoes, tuple(params_sessoes))
            sessoes_realizadas = self.db.cursor.fetchone()['total'] or 0

            # --- Query para Faturamento Mensal (Gráfico) ---
            query_faturamento_mensal = """
                SELECT MONTH(data_hora) as mes, COUNT(id) as qtd 
                FROM sessoes 
                WHERE status = 1 AND YEAR(data_hora) = %s
                GROUP BY MONTH(data_hora)
            """
            self.db.cursor.execute(query_faturamento_mensal, (ano,))
            faturamento_por_mes_raw = self.db.cursor.fetchall()
            
            faturamento_mensal = [0] * 12
            for item in faturamento_por_mes_raw:
                faturamento_mensal[item['mes'] - 1] = item['qtd'] * valor_sessao

            # --- Query para Novos Pacientes ---
            query_novos_pacientes = "SELECT COUNT(id) as total FROM pacientes WHERE 1=1"
            params_pacientes = []
            if ano:
                query_novos_pacientes += " AND YEAR(data_stamp) = %s" # Assumindo data_stamp = data de criação
                params_pacientes.append(ano)
            if mes:
                query_novos_pacientes += " AND MONTH(data_stamp) = %s"
                params_pacientes.append(mes)
            
            self.db.cursor.execute(query_novos_pacientes, tuple(params_pacientes))
            novos_pacientes = self.db.cursor.fetchone()['total'] or 0

            # --- Query para Próximas Sessões ---
            hoje = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            query_proximas_sessoes = """
                SELECT s.data_hora, p.name 
                FROM sessoes s
                JOIN pacientes p ON s.paciente_id = p.id
                WHERE s.data_hora >= %s
                ORDER BY s.data_hora ASC
                LIMIT 5
            """
            self.db.cursor.execute(query_proximas_sessoes, (hoje,))
            proximas_sessoes = self.db.cursor.fetchall()
            
            # --- Cálculos Finais ---
            faturamento_bruto = sessoes_realizadas * valor_sessao
            lucro_liquido = faturamento_bruto - (custo_fixo if mes else custo_fixo * 12) # Ajusta custo para o período

            return {
                'faturamento_bruto': f"R$ {faturamento_bruto:,.2f}",
                'lucro_liquido': f"R$ {lucro_liquido:,.2f}",
                'sessoes_realizadas': sessoes_realizadas,
                'novos_pacientes': novos_pacientes,
                'faturamento_mensal': faturamento_mensal, # Array com 12 meses
                'proximas_sessoes': proximas_sessoes
            }
        finally:
            self.db.disconnect()

    def get_anos_disponiveis(self):
        """ Retorna uma lista de anos únicos que têm sessões. """
        if not self.db.connect(): return []
        try:
            self.db.cursor.execute("SELECT DISTINCT YEAR(data_hora) as ano FROM sessoes ORDER BY ano DESC")
            return [row['ano'] for row in self.db.cursor.fetchall()]
        finally:
            self.db.disconnect()

    def get_dados_brutos_sessoes(self, ano=None, mes=None):
        """
        Busca os dados detalhados das sessoes para exportação em CSV.
        """
        if not self.db.connect():
            raise ConnectionError("Não foi possível conectar ao banco de dados.")

        try:
            query = """
                SELECT 
                    s.id as id_sessao,
                    p.name as nome_paciente,
                    s.data_hora,
                    CASE s.status
                        WHEN 1 THEN 'Paga/Realizada'
                        ELSE 'Não Paga/Pendente'
                    END as status_sessao
                FROM sessoes s
                JOIN pacientes p ON s.paciente_id = p.id
                WHERE 1=1
            """
            params = []

            if ano:
                query += " AND YEAR(s.data_hora) = %s"
                params.append(ano)
            if mes:
                query += " AND MONTH(s.data_hora) = %s"
                params.append(mes)
            
            query += " ORDER BY s.data_hora DESC"
            
            self.db.cursor.execute(query, tuple(params))
            return self.db.cursor.fetchall()

        except Exception as e:
            print(f"Erro ao buscar dados brutos para CSV: {e}")
            return None
        finally:
            self.db.disconnect()