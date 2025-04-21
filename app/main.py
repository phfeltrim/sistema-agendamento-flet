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
    page.window_width = 1366
    page.window_height = 768
    page.window_resizable = True
    page.window_min_width = 1024
    page.window_min_height = 720
    page.padding = 0
    page.theme = ft.Theme(
        color_scheme_seed="#6E62E5",
        visual_density=ft.VisualDensity.COMFORTABLE,
        use_material3=True
    )
    
    # Configurações de fonte
    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }
    page.theme.font_family = "Poppins"
    
    # Callback para quando o login for bem-sucedido
    def on_login_success():
        page.clean()
        page.add(AgendaView(page, None))
        page.update()
    
    # Inicia com a tela de login
    page.add(LoginView(page, on_login_success))
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
