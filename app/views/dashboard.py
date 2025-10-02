import flet as ft
from ..controllers.dashboard_controller import DashboardController

class DashboardView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controller = DashboardController()
        
        # Elementos da UI que serão atualizados
        self.dd_ano = ft.Dropdown(label="Ano", on_change=self.filtros_changed)
        self.dd_mes = ft.Dropdown(label="Mês", on_change=self.filtros_changed, options=[
            ft.dropdown.Option(key=i, text=t) for i, t in enumerate([
                "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
            ], 1)
        ])
        self.txt_pacientes_atendidos = ft.Text("0", size=28, weight=ft.FontWeight.BOLD)
        self.txt_pagos = ft.Text("0", size=20, color=ft.Colors.GREEN)
        self.txt_nao_pagos = ft.Text("0", size=20, color=ft.Colors.RED)
        self.txt_perc_pagos = ft.Text("0%", size=16)
        self.txt_perc_nao_pagos = ft.Text("0%", size=16)

        self.chart_pagamentos = ft.PieChart(
            sections=[], # Inicia vazio
            sections_space=0,
            center_space_radius=40,
            expand=True
        )

        # Constrói a view
        self.content = self.build()
        # Carrega os dados iniciais
        self.carregar_filtros_e_dados()

    def carregar_filtros_e_dados(self):
        """ Carrega os anos disponíveis para o filtro e atualiza o dashboard. """
        anos = self.controller.get_anos_disponiveis()
        self.dd_ano.options = [ft.dropdown.Option(key=ano, text=str(ano)) for ano in anos]
        self.update_dashboard()

    def filtros_changed(self, e):
        """ Chamado sempre que um filtro de data é alterado. """
        self.update_dashboard()

    def update_dashboard(self, e=None):
        """ Busca os dados no controller e atualiza a UI. """
        ano = self.dd_ano.value
        mes = self.dd_mes.value

        if not ano: # Se nenhum ano for selecionado, não faz nada
            return

        dados = self.controller.get_dados_agendamento(ano=ano, mes=mes)

        if dados:
            self.txt_pacientes_atendidos.value = str(dados['atendidos'])
            self.txt_pagos.value = str(dados['pagos'])
            self.txt_nao_pagos.value = str(dados['nao_pagos'])
            self.txt_perc_pagos.value = f"{dados['perc_pagos']}%"
            self.txt_perc_nao_pagos.value = f"{dados['perc_nao_pagos']}%"
            
            # Atualiza o gráfico de pizza
            self.chart_pagamentos.sections = [
                ft.PieChartSection(
                    dados['perc_pagos'],
                    title=f"{dados['perc_pagos']}%",
                    color=ft.Colors.GREEN,
                    radius=50,
                ),
                ft.PieChartSection(
                    dados['perc_nao_pagos'],
                    title=f"{dados['perc_nao_pagos']}%",
                    color=ft.Colors.RED,
                    radius=50,
                ),
            ]
        
        self.update() # Atualiza a tela

    def build(self):
        """ Constrói o layout visual do dashboard. """
        return ft.Column(
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Text("Dashboard de Análises", style=ft.TextThemeStyle.HEADLINE_MEDIUM),
                
                # Filtros
                ft.Row(controls=[self.dd_ano, self.dd_mes]),
                
                ft.Divider(),

                # KPIs
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                    controls=[
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column([
                                    ft.Text("Pacientes Atendidos", weight=ft.FontWeight.BOLD),
                                    self.txt_pacientes_atendidos,
                                ])
                            )
                        ),
                        ft.Card(
                            content=ft.Container(
                                padding=20,
                                content=ft.Column([
                                    ft.Text("Status de Pagamento"),
                                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, color=ft.Colors.GREEN), self.txt_pagos]),
                                    ft.Row([ft.Icon(ft.Icons.CANCEL, color=ft.Colors.RED), self.txt_nao_pagos]),
                                ])
                            )
                        ),
                    ]
                ),
                
                # Gráfico
                ft.Container(
                    height=300,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Column([
                                ft.Text("% Pagantes", weight=ft.FontWeight.BOLD),
                                self.txt_perc_pagos
                            ]),
                            self.chart_pagamentos,
                            ft.Column([
                                ft.Text("% Não Pagantes", weight=ft.FontWeight.BOLD),
                                self.txt_perc_nao_pagos
                            ]),
                        ]
                    )
                )
            ]
        )