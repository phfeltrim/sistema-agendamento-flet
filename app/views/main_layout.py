import flet as ft
from views.agenda import AgendaView
from views.pacientes import PacientesView
from views.sessoes import SessoesView
from views.configuracoes import ConfiguracoesView

class MainLayout(ft.Container):
    def __init__(self, page: ft.Page, view_name: str, on_navigate):
        super().__init__()
        self.page = page
        self.view_name = view_name
        self.on_navigate = on_navigate
        self.expand = True
        self.content = self.build()

    def build_navigation(self):
        nav_items = [
            (ft.icons.CALENDAR_MONTH, "Agenda", "agenda"),
            (ft.icons.PEOPLE, "Pacientes", "pacientes"),
            (ft.icons.LIST_ALT, "Sessões", "sessoes"),
            (ft.icons.SETTINGS, "Configurações", "configuracoes"),
            (ft.icons.LOGOUT, "Sair", "sair")
        ]
        selected_index = [i for i, (_, _, v) in enumerate(nav_items) if v == self.view_name]
        selected_index = selected_index[0] if selected_index else 0
        return ft.NavigationRail(
            selected_index=selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            destinations=[
                ft.NavigationRailDestination(icon=icon, label=label) for icon, label, _ in nav_items
            ],
            on_change=self.handle_navigation_change
        )

    def handle_navigation_change(self, e):
        nav_items = ["agenda", "pacientes", "sessoes", "configuracoes", "sair"]
        idx = e.control.selected_index
        self.on_navigate(nav_items[idx])

    def build_content(self):
        if self.view_name == "agenda":
            return AgendaView(self.page, self.on_navigate)
        elif self.view_name == "pacientes":
            return PacientesView(self.page)
        elif self.view_name == "sessoes":
            return SessoesView(self.page)
        elif self.view_name == "configuracoes":
            return ConfiguracoesView(self.page)
        else:
            return ft.Text("Tela não encontrada")

    def build(self):
        return ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Icon(ft.icons.CALENDAR_MONTH, size=64, color=ft.colors.PRIMARY),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=30, bottom=10)
                    ),
                    ft.Container(
                        content=self.build_navigation(),
                        height=700,  # altura fixa para NavigationRail
                        expand=False
                    )
                ]),
                width=250,
                bgcolor=ft.colors.SURFACE_VARIANT,
                height=768
            ),
            ft.Container(
                content=self.build_content(),
                expand=True
            )
        ], expand=True)
