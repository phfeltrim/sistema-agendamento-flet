import flet as ft

class SessoesView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Sessões", size=30, weight=ft.FontWeight.BOLD),
                    self.build_sessions_list()
                ],
                spacing=20
            ),
            padding=20
        )

    def build_sessions_list(self):
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Paciente")),
                    ft.DataColumn(ft.Text("Data/Hora")),
                    ft.DataColumn(ft.Text("Status")),
                    ft.DataColumn(ft.Text("Ações"))
                ],
                rows=[]
            )
        )
