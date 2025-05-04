import flet as ft
from views.login import LoginView
from views.main_layout import MainLayout

def main(page: ft.Page):
    import os, time
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
    def show_view(view_name):
        page.clean()
        if view_name == "sair":
            page.add(LoginView(page, on_login_success))
        else:
            page.add(MainLayout(page, view_name, show_view))
        page.update()
    def on_login_success():
        show_view("agenda")
    # --- SEGREDO: temp.txt controla o login ---
    temp_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "temp.txt")
    if not os.path.exists(temp_path):
        page.clean()
        page.add(ft.Text("Sistema Bloqueado - Você precisa de uma licença válida para utilizar esse sistema.", color=ft.colors.ERROR, size=24))
        page.update()
        return
    with open(temp_path, "r", encoding="utf-8") as f:
        temp_content = f.read().strip()
    if temp_content == "21031979":
        show_view("agenda")
        return
    elif temp_content == "":
        page.add(LoginView(page, on_login_success))
        page.update()
        return
    else:
        # Qualquer outro conteúdo: bloqueia
        page.clean()
        page.add(ft.Text("Sistema Bloqueado - Você precisa de uma licença válida para utilizar esse sistema.", color=ft.colors.ERROR, size=24))
        page.update()
        return


if __name__ == "__main__":
    ft.app(target=main)
