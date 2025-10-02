import sys
import os
import bcrypt
import getpass

# --- INÍCIO DA CORREÇÃO DE IMPORTAÇÃO ---
# Esta parte resolve o 'ModuleNotFoundError'.
# 1. Pega o caminho da pasta raiz do projeto (um nível acima de 'utility_scripts').
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# 2. Pega o caminho para a pasta 'app', onde estão os módulos.
APP_PATH = os.path.join(PROJECT_ROOT, 'app')
# 3. Adiciona a pasta 'app' ao caminho de busca do Python.
sys.path.append(APP_PATH)
# --- FIM DA CORREÇÃO ---

from models.database import Database

def update_all_user_passwords():
    """
    Este script percorre todos os usuários no banco de dados e permite
    que você defina uma nova senha para cada um, já no formato seguro bcrypt.
    """
    # Instancia o Database, passando o caminho correto para o config.ini na raiz do projeto.
    db = Database(config_file=os.path.join(PROJECT_ROOT, 'config.ini'))
    if not db.connect():
        print("ERRO: Não foi possível conectar ao banco de dados. Verifique o config.ini.")
        return

    try:
        db.cursor.execute("SELECT id, email, nome FROM usuarios")
        users = db.cursor.fetchall()

        if not users:
            print("Nenhum usuário encontrado no banco de dados.")
            return

        print("--- ATUALIZAÇÃO DE SENHAS PARA BCRYPT ---")
        for user in users:
            print(f"\n-> Atualizando senha para o usuário: {user['nome']} ({user['email']})")
            password = getpass.getpass(prompt="   Digite a NOVA senha: ")
            password_confirm = getpass.getpass(prompt="   Confirme a NOVA senha: ")

            if not password or password != password_confirm:
                print("   [AVISO] As senhas não coincidem ou estão em branco. Pulando este usuário.")
                continue

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            update_query = "UPDATE usuarios SET senha = %s WHERE id = %s"
            db.cursor.execute(update_query, (hashed_password, user['id']))
            db.conn.commit()
            print(f"   [SUCESSO] Senha para '{user['email']}' atualizada!")

    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
    finally:
        db.disconnect()

if __name__ == "__main__":
    update_all_user_passwords()