import flet as ft

class ConfiguracoesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = self.build()

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Configurações", size=30, weight=ft.FontWeight.BOLD),
                    self.build_settings_form()
                ],
                spacing=20
            ),
            padding=20
        )

    def build_settings_form(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextField(
                        label="Horário de Funcionamento",
                        value="08:00 - 18:00"
                    ),
                    ft.TextField(
                        label="Duração Padrão da Sessão (minutos)",
                        value="60"
                    ),
                    ft.ElevatedButton(
                        text="Salvar Configurações",
                        on_click=self.save_settings
                    )
                ],
                spacing=10
            )
        )

    def save_settings(self, e):
        try:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Configurações salvas!"))
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            dlg = ft.AlertDialog(title=ft.Text("Aviso"), content=ft.Text("Configurações salvas!"), open=True)
            self.page.dialog = dlg
            self.page.update()
