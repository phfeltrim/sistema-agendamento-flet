from ..models.database import Database

class ConfiguracoesController:
    def __init__(self):
        self.db = Database()

    def get_config(self, chave):
        """Busca o valor de uma configuração específica no banco de dados."""
        if not self.db.connect():
            return None
        try:
            query = "SELECT valor FROM configuracoes WHERE chave = %s"
            self.db.cursor.execute(query, (chave,))
            resultado = self.db.cursor.fetchone()
            # Retorna o valor se encontrado, caso contrário, None
            return resultado['valor'] if resultado else None
        except Exception as e:
            print(f"Erro ao buscar configuração '{chave}': {e}")
            return None
        finally:
            self.db.disconnect()

    def set_config(self, chave, valor):
        """Salva ou atualiza o valor de uma configuração no banco de dados."""
        if not self.db.connect():
            return False
        try:
            # Verifica se a chave de configuração já existe na tabela
            self.db.cursor.execute("SELECT id FROM configuracoes WHERE chave = %s", (chave,))
            existe = self.db.cursor.fetchone()

            if existe:
                # Se existe, atualiza (UPDATE)
                query = "UPDATE configuracoes SET valor = %s WHERE chave = %s"
                values = (valor, chave)
            else:
                # Se não existe, insere (INSERT)
                query = "INSERT INTO configuracoes (chave, valor) VALUES (%s, %s)"
                values = (chave, valor)
            
            self.db.cursor.execute(query, values)
            self.db.conn.commit()
            return True
        except Exception as e:
            print(f"Erro ao salvar configuração '{chave}': {e}")
            self.db.conn.rollback() # Desfaz a operação em caso de erro
            return False
        finally:
            self.db.disconnect()