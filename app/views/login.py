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
        self.email_field = ft.TextField(
            label="Email",
            border=ft.InputBorder.UNDERLINE,
            width=300
        )
        
        self.password_field = ft.TextField(
            label="Senha",
            border=ft.InputBorder.UNDERLINE,
            password=True,
            can_reveal_password=True,
            width=300
        )
        
        # Define o conteúdo após criar os campos
        self.content = self.build()
        
    def login(self, e):
        email = self.email_field.value
        password = self.password_field.value
        
        if self.auth_controller.login(email, password):
            self.on_login_success()
        else:
            self.page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Email ou senha inválidos"))
            )

    def build(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    # Lado esquerdo - Imagem/Logo
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
                                ),
                                ft.Text(
                                    "Gerencie seus agendamentos de forma simples e eficiente",
                                    size=16,
                                    color=ft.colors.SECONDARY
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20
                        ),
                        bgcolor=ft.colors.PRIMARY_CONTAINER,
                        expand=True,
                        alignment=ft.alignment.center
                    ),
                    # Lado direito - Formulário de login
                    ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(
                                    "Bem-vindo de volta!",
                                    size=32,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    "Entre com suas credenciais para continuar",
                                    size=16,
                                    color=ft.colors.SECONDARY
                                ),
                                ft.Container(height=20),  # Espaçamento
                                self.email_field,
                                self.password_field,
                                ft.Container(height=10),  # Espaçamento
                                ft.ElevatedButton(
                                    content=ft.Text(
                                        "Entrar",
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
                        ),
                        expand=True,
                        alignment=ft.alignment.center,
                        padding=50
                    )
                ],
                expand=True
            ),
            expand=True
        )
