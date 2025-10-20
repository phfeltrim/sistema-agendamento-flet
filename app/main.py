import flet as ft
from .views.login import LoginView
from .views.main_layout import MainLayout
from .settings.themes import tema_normal, tema_alto_contraste
import os

def main(page: ft.Page):
    # --- Configuração da Página (simplificada) ---
    page.title = "Sistema de Agendamento"
    page.theme_mode = "light"
    page.padding = 0

    page.tema_normal = tema_normal
    page.tema_alto_contraste = tema_alto_contraste
    page.theme = page.tema_normal

    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }

    # --- NOVA ABORDAGEM: Função para ser chamada após a conexão ---
    def expandir_janela(e):
        """
        Esta função é chamada uma única vez quando a janela está pronta.
        Aqui, enviamos o comando para maximizá-la.
        """
        print("Conexão estabelecida com a UI. Maximizando a janela...")
        page.window_maximized = True
        page.update()

    # --- Funções de Navegação e Sessão (sem alterações) ---
    def on_login_success(user: dict):
        page.session.set("user_id", user['id'])
        page.session.set("user_name", user['nome'])
        page.session.set("user_email", user['email'])
        page.go("/agenda")

    def on_logout():
        page.session.clear()
        page.go("/login")

    def route_change(route):
        page.views.clear()
        if not page.session.get("user_id"):
            page.views.append(
                ft.View(
                    route='/login',
                    controls=[LoginView(page, on_login_success)],
                    padding=0
                )
            )
        else:
            view_name = page.route.strip('/').split('/')[0]
            if not view_name:
                view_name = "agenda"
            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[MainLayout(page, view_name, on_navigate=page.go)],
                    padding=0
                )
            )
        
        if page.route == "/sair":
            on_logout()
            return

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # --- Inicialização da Aplicação ---
    page.on_connect = expandir_janela  # <--- LIGA A FUNÇÃO AO EVENTO DE CONEXÃO
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


if __name__ == "__main__":
    ft.app(target=main)