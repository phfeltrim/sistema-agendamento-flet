from ..models.database import Database

class DashboardController:
    def __init__(self):
        self.db = Database()

    def get_dados_agendamento(self, ano=None, mes=None, dia=None):
        """
        Busca e calcula as estatísticas de agendamento com base nos filtros de data.
        """
        if not self.db.connect():
            raise ConnectionError("Não foi possível conectar ao banco de dados.")

        try:
            # A base da nossa query
            query = "SELECT status, COUNT(id) as total FROM sessoes WHERE 1=1"
            params = []

            # Adiciona os filtros de data dinamicamente
            if ano:
                query += " AND YEAR(data_hora) = %s"
                params.append(ano)
            if mes:
                query += " AND MONTH(data_hora) = %s"
                params.append(mes)
            if dia:
                query += " AND DAY(data_hora) = %s"
                params.append(dia)
            
            query += " GROUP BY status"
            
            self.db.cursor.execute(query, tuple(params))
            resultados = self.db.cursor.fetchall()

            # Processa os resultados
            stats = {
                'atendidos': 0,
                'pagos': 0,
                'nao_pagos': 0,
                'perc_pagos': 0,
                'perc_nao_pagos': 0
            }

            # ATENÇÃO: Esta lógica assume que na sua tabela 'sessoes', 
            # o status '1' significa 'pago' e '0' significa 'não pago'.
            # Se for diferente (ex: 'pago', 'pendente'), ajuste o IF abaixo.
            for res in resultados:
                total_status = res['total']
                if res['status'] == 1: # Assumindo 1 = Pago
                    stats['pagos'] = total_status
                else: # Assumindo qualquer outro status = Não Pago
                    stats['nao_pagos'] = total_status
            
            stats['atendidos'] = stats['pagos'] + stats['nao_pagos']

            # Calcula as porcentagens
            if stats['atendidos'] > 0:
                stats['perc_pagos'] = round((stats['pagos'] / stats['atendidos']) * 100, 2)
                stats['perc_nao_pagos'] = round((stats['nao_pagos'] / stats['atendidos']) * 100, 2)
            
            return stats

        except Exception as e:
            print(f"Erro ao buscar dados do dashboard: {e}")
            return None # Retorna None em caso de erro
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