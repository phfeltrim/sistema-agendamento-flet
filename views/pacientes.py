import flet as ft

class PacientesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = self.build()

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Pacientes", size=30, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Novo Paciente",
                                on_click=self.new_patient
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.build_patients_list()
                ],
                spacing=20
            ),
            padding=20
        )

    def build_patients_list(self):
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Email")),
                    ft.DataColumn(ft.Text("Telefone")),
                    ft.DataColumn(ft.Text("Ações"))
                ],
                rows=[]
            )
        )

    def new_patient(self, e):
        # Implementar lógica para novo paciente
        pass
