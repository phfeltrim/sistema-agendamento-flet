import flet as ft
from datetime import datetime, timedelta

class AgendaView(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.current_date = datetime.now()

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Agenda", size=30, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                tooltip="Novo Agendamento",
                                on_click=self.new_appointment
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    self.build_calendar(),
                    self.build_appointments_list()
                ],
                spacing=20
            ),
            padding=20
        )

    def build_calendar(self):
        # Implementação básica do calendário
        return ft.Container(
            content=ft.Text(f"Calendário - {self.current_date.strftime('%B %Y')}"),
            border=ft.border.all(1),
            padding=10
        )

    def build_appointments_list(self):
        # Lista de agendamentos do dia
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Agendamentos do Dia", weight=ft.FontWeight.BOLD),
                    ft.ListView(
                        controls=[
                            ft.Text("Nenhum agendamento para hoje")
                        ],
                        height=300
                    )
                ]
            )
        )

    def new_appointment(self, e):
        # Implementar lógica para novo agendamento
        pass
