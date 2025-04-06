import flet as ft
from controllers.auth_controller import AuthController

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.page = page
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
            content=ft.Column(
                controls=[
                    ft.Text("Login", size=30, weight=ft.FontWeight.BOLD),
                    self.email_field,
                    self.password_field,
                    ft.ElevatedButton(
                        text="Entrar",
                        on_click=self.login,
                        width=300
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            ),
            alignment=ft.alignment.center
        )
