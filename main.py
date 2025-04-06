import flet as ft
from views.login import LoginView
from views.agenda import AgendaView
from views.pacientes import PacientesView
from views.sessoes import SessoesView
from views.configuracoes import ConfiguracoesView

def main(page: ft.Page):
    # Configuração da página
    page.title = "Sistema de Agendamento"
    page.theme_mode = "light"
    page.window_width = 1000
    page.window_height = 600
    page.window_resizable = False
    page.padding = 0
    
    # Callback para quando o login for bem-sucedido
    def on_login_success():
        page.clean()
        page.add(AgendaView(page))
        page.update()
    
    # Inicia com a tela de login
    page.add(LoginView(page, on_login_success))
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
