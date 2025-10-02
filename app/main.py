import flet as ft
from .views.login import LoginView
from .views.main_layout import MainLayout
from .settings.themes import tema_normal, tema_alto_contraste
import os

def main(page: ft.Page):
    # --- Configuração da Página (mantida) ---
    page.title = "Sistema de Agendamento"
    page.theme_mode = "light"
    page.window_width = 1366
    page.window_height = 768
    page.window_resizable = True
    page.padding = 0

  
    page.tema_normal = tema_normal
    page.tema_alto_contraste = tema_alto_contraste
    page.theme = page.tema_normal # Define o tema inicial

    page.fonts = {
        "Poppins": "https://raw.githubusercontent.com/google/fonts/main/ofl/poppins/Poppins-Regular.ttf"
    }

    # --- Funções de Navegação e Sessão ---

    def on_login_success(user: dict):
        """
        Callback chamado pela LoginView quando o login é bem-sucedido.
        Armazena as informações do usuário na sessão da página.
        """
        page.session.set("user_id", user['id'])
        page.session.set("user_name", user['nome'])
        page.session.set("user_email", user['email'])
        page.go("/agenda") # Navega para a tela principal

    def on_logout():
        """ Limpa a sessão e redireciona para a tela de login. """
        page.session.clear()
        page.go("/login")

    def route_change(route):
        """
        Controla qual view é exibida com base na URL e no estado de login.
        Esta função é o coração do novo sistema de navegação.
        """
        page.views.clear()

        # Se o usuário não está logado, sempre mostra a tela de login
        if not page.session.get("user_id"):
            page.views.append(
                ft.View(
                    route='/login',
                    controls=[LoginView(page, on_login_success)],
                    padding=0
                )
            )
        # Se o usuário está logado, mostra o layout principal
        else:
            view_name = page.route.strip('/').split('/')[0]
            if not view_name: # Se a rota for apenas '/', vai para a agenda
                view_name = "agenda"

            page.views.append(
                ft.View(
                    route=page.route,
                    controls=[MainLayout(page, view_name, on_navigate=page.go)],
                    padding=0
                )
            )
        
        # Trata o caso de logout (a view_name é 'sair' no MainLayout)
        if page.route == "/sair":
            on_logout()
            return # A on_logout já chama page.go, então paramos aqui

        page.update()

    def view_pop(view):
        """ Lida com o botão 'voltar' do navegador/desktop. """
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # --- Inicialização da Aplicação ---
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route) # Inicia a navegação na rota atual ('/' por padrão)


if __name__ == "__main__":
    ft.app(target=main)