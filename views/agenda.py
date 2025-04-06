import flet as ft
from datetime import datetime, timedelta

class AgendaView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.current_date = datetime.now()
        self.navigation = self.build_navigation()
        self.expand = True
        self.content = self.build()

    def build_navigation(self):
        return ft.Container(
            content=ft.NavigationRail(
                selected_index=0,
                label_type=ft.NavigationRailLabelType.ALL,
                extended=True,
                destinations=[
                    ft.NavigationRailDestination(
                        icon=ft.icons.CALENDAR_TODAY,
                        label="Agenda"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.PEOPLE,
                        label="Pacientes"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.LIST_ALT,
                        label="Sessões"
                    ),
                    ft.NavigationRailDestination(
                        icon=ft.icons.SETTINGS,
                        label="Configurações"
                    ),
                ],
                on_change=self.handle_navigation_change
            ),
            expand=True
        )

    def handle_navigation_change(self, e):
        index = e.control.selected_index
        routes = ["/agenda", "/pacientes", "/sessoes", "/configuracoes"]
        self.page.go(routes[index])

    def build(self):
        return ft.Container(
            content=ft.Row(
                controls=[
                    self.navigation,
                    ft.VerticalDivider(width=1),
                    ft.Container(
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
                            spacing=20,
                            expand=True
                        ),
                        padding=20,
                        expand=True
                    )
                ],
                expand=True
            ),
            expand=True
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
