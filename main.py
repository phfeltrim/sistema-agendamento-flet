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
    
    # Função para mudar de view
    def change_view(view):
        page.clean()
        page.add(view)
        
    # Navegação principal
    def show_main_navigation():
        nav_rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.CALENDAR_TODAY,
                    label="Agenda"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.PEOPLE,
                    label="Pacientes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.LIST_ALT,
                    label="Sessões"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SETTINGS,
                    label="Configurações"
                ),
            ],
            on_change=lambda e: handle_navigation_change(e.control.selected_index)
        )
        
        page.add(
            ft.Row(
                controls=[
                    nav_rail,
                    ft.VerticalDivider(width=1),
                    views[0]  # Agenda view é a view inicial
                ],
                expand=True
            )
        )
    
    # Lista de views disponíveis
    views = [
        AgendaView(page),
        PacientesView(page),
        SessoesView(page),
        ConfiguracoesView(page)
    ]
    
    def handle_navigation_change(index):
        page.clean()
        page.add(
            ft.Row(
                controls=[
                    nav_rail,
                    ft.VerticalDivider(width=1),
                    views[index]
                ],
                expand=True
            )
        )
    
    # Callback para quando o login for bem-sucedido
    def on_login_success():
        show_main_navigation()
    
    # Inicia com a tela de login
    login_view = LoginView(page, on_login_success)
    page.add(login_view)
    page.update()

if __name__ == "__main__":
    ft.app(target=main)
