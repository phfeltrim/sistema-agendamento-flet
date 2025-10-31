import flet as ft
from ..controllers.auth_controller import AuthController
from ..settings.featureToggle import FeatureToggle

class LoginView(ft.Container):
    def __init__(self, page: ft.Page, on_login_success):
        super().__init__()
        self.page = page
        self.on_login_success = on_login_success
        self.auth_controller = AuthController()

        # Mantendo o FeatureToggle para seus testes, se necessário.
        if FeatureToggle.toggle_database.value:
            # Para simular, podemos criar um usuário falso
            self.user_simulado = {"id": 99, "nome": "Usuário Simulado", "email": "simulado@teste.com"}
        else:
            self.user_simulado = None

        # --- Componentes da UI ---
        self.login_field = ft.TextField(
            label="Email",
            hint_text="Digite seu email de acesso",
            width=300,
            autofocus=True,
            on_submit=self.login # Permite logar com Enter
        )
        
        self.password_field = ft.TextField(
            label="Senha",
            hint_text="Digite sua senha",
            password=True,
            can_reveal_password=True,
            width=300,
            on_submit=self.login # Permite logar com Enter
        )

        self.content = self.build()
        
    def login(self, e):
        # Lógica para o modo de simulação (FeatureToggle)
        if self.user_simulado:
            self.on_login_success(self.user_simulado)
            return

        # Limpa erros anteriores
        self.login_field.error_text = None
        self.password_field.error_text = None
        
        login = self.login_field.value.strip()
        password = self.password_field.value

        # Validação simples dos campos
        if not login or not password:
            self.login_field.error_text = "Email é obrigatório" if not login else None
            self.password_field.error_text = "Senha é obrigatória" if not password else None
            self.page.update()
            return
        
        # Chama o AuthController para verificar as credenciais no banco
        user = self.auth_controller.login(login, password)
        
        if user:
            # Sucesso! Passa os dados do usuário para a função de callback (em main.py)
            self.on_login_success(user)
        else:
            # Falha no login
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Email ou senha inválidos"),
                bgcolor=ft.Colors.ERROR
            )
            self.page.snack_bar.open = True
            self.page.update()

    def build(self):
        return ft.Container(
            # Um fundo mais suave para a página inteira
            bgcolor=ft.Colors.GREY_200,
            expand=True,
            alignment=ft.alignment.center,
            padding=20,
            content=ft.Card(
                elevation=8,
                width=450,  # Largura do card
                height=600, # Altura do card
                content=ft.Container( # Container para adicionar padding interno
                    padding=ft.padding.all(40),
                    content=ft.Column(
                    controls=[
                        # Unificando tudo em uma única coluna
                        ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, size=64, color=ft.Colors.PRIMARY),
                        ft.Text(
                            "Sistema de Agendamento",
                            style=ft.TextThemeStyle.HEADLINE_SMALL,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.PRIMARY
                        ),
                        ft.Container(height=20),
                        ft.Text("Acesse sua conta para continuar.", style=ft.TextThemeStyle.BODY_LARGE),
                        ft.Container(height=10),
                        self.login_field,
                        self.password_field,
                        ft.Container(height=20),
                        ft.ElevatedButton(
                            text="Acessar",
                            icon=ft.Icons.LOGIN,
                            on_click=self.login,
                            width=300,
                            height=48,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=8)
                            )
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15
                    )
                )
            )
        )