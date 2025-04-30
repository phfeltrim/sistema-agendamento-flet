import flet as ft
from controllers.auth_controller import AuthController
from settings.featureToggle import FeatureToggle

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.page = page

        # Verifica se o recurso de banco de dados simulado está ativado
        if FeatureToggle.toggle_database.value == True:
            self.on_login_success = True
            self.auth_controller = True
        else:     
            self.on_login_success = on_login_success
            self.auth_controller = AuthController()
        
        # Inicializa os campos antes de build()
        self.login_field = ft.TextField(
            label="Login",
            hint_text="Digite seu login",
            border=ft.InputBorder.UNDERLINE,
            width=300
        )
        
        self.password_field = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            border=ft.InputBorder.UNDERLINE,
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        # Define o conteúdo após criar os campos
        self.content = self.build()
        
    def login(self, e):
        login = self.login_field.value
        password = self.password_field.value
        
        if self.auth_controller.login(login, password):
            self.on_login_success()
        else:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Email ou senha inválidos"))
            self.page.snack_bar.open = True
            self.page.update()

    def build(self):
        return ft.Container(
            bgcolor=ft.colors.GREY_200,
            expand=True,
            content=ft.Row(
                controls=[
                    # Coluna 1: Logo
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Icon(
                                    ft.icons.CALENDAR_MONTH,
                                    size=64,
                                    color=ft.colors.PRIMARY
                                ),
                                ft.Text(
                                    "Sistema de Agendamento",
                                    size=32,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.colors.PRIMARY
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        bgcolor=ft.colors.WHITE,
                        border_radius=20,
                        expand=True,
                        alignment=ft.alignment.center,
                        padding=40
                    ),
                    # Coluna 2: Formulário de login
                    ft.Container(
                        content=ft.Container(
                            bgcolor=ft.colors.GREY_100,
                            border_radius=20,
                            padding=40,
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Bem-vindo!",
                                        size=28,
                                        weight=ft.FontWeight.BOLD
                                    ),
                                    ft.Container(height=20),
                                    ft.Row([
                                        self.login_field,
                                        self.password_field
                                    ], spacing=10),
                                    ft.Container(height=20),
                                    ft.ElevatedButton(
                                        content=ft.Text(
                                            "Acessar",
                                            size=16,
                                            weight=ft.FontWeight.W_500
                                        ),
                                        style=ft.ButtonStyle(
                                            shape=ft.RoundedRectangleBorder(radius=8),
                                            padding=ft.padding.symmetric(horizontal=24, vertical=16)
                                        ),
                                        on_click=self.login,
                                        width=300
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                spacing=10,
                                width=400
                            )
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                        padding=50
                    )
                ],
                expand=True
            )
        )
