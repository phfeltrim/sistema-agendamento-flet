import flet as ft
from ..controllers.dashboard_controller import DashboardController
import calendar
from datetime import datetime
import pandas as pd
import traceback

# Importa o nosso novo gerador de PDF
from ..utils import pdf_generator

class DashboardView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controller = DashboardController()
        self.expand = True
        self.padding = ft.padding.all(30)
        
        # --- FilePicker para Salvar Arquivos ---
        self.file_picker = ft.FilePicker(on_result=self.salvar_arquivo_resultado)
        self.page.overlay.append(self.file_picker)

        # --- DEFINIÇÃO DOS COMPONENTES DA UI ---
        anos_disponiveis = self.controller.get_anos_disponiveis()
        self.dd_ano = ft.Dropdown(label="Ano", width=150, on_change=self.update_dashboard_data, options=[ft.dropdown.Option(ano, str(ano)) for ano in anos_disponiveis])
        meses_opts = [ft.dropdown.Option("todos", "Ano Inteiro")] + [ft.dropdown.Option(i, calendar.month_name[i]) for i in range(1, 13)]
        self.dd_mes = ft.Dropdown(label="Mês", width=200, on_change=self.update_dashboard_data, options=meses_opts)
        self.kpi_faturamento_bruto = ft.Text("R$ 0,00", size=24, weight=ft.FontWeight.BOLD)
        self.kpi_lucro_liquido = ft.Text("R$ 0,00", size=24, weight=ft.FontWeight.BOLD)
        self.kpi_sessoes_realizadas = ft.Text("0", size=24, weight=ft.FontWeight.BOLD)
        self.kpi_novos_pacientes = ft.Text("0", size=24, weight=ft.FontWeight.BOLD)
        self.bar_chart = ft.BarChart(expand=True)
        self.bar_chart.left_axis = ft.ChartAxis(labels_size=40)
        self.bar_chart.bottom_axis = ft.ChartAxis(labels_size=40, labels_interval=1)
        self.lista_proximas_sessoes = ft.Column(scroll=ft.ScrollMode.ADAPTIVE)
        
        # O conteúdo da view é o layout construído pelo método build()
        self.content = self.build()

    # --- MÉTODOS DE EXPORTAÇÃO (com a nova lógica de PDF) ---
    
    def exportar_csv(self, e):
        self.file_picker.save_file(dialog_title="Salvar como CSV", file_name="relatorio_dashboard.csv", allowed_extensions=["csv"])

    def exportar_pdf(self, e):
        self.file_picker.save_file(dialog_title="Salvar como PDF", file_name="relatorio_dashboard.pdf", allowed_extensions=["pdf"])

    def salvar_arquivo_resultado(self, e: ft.FilePickerResultEvent):
        if not e.path:
            # Usuário cancelou
            return
        if e.path.endswith(".csv"):
            self.gerar_e_salvar_csv(e.path)
        elif e.path.endswith(".pdf"):
            self.gerar_e_salvar_pdf_programatico(e.path)

    def gerar_e_salvar_csv(self, caminho_arquivo):
        ano = self.dd_ano.value
        mes = self.dd_mes.value if self.dd_mes.value != "todos" else None
        dados_brutos = self.controller.get_dados_brutos_sessoes(ano, mes)
        if dados_brutos:
            df = pd.DataFrame(dados_brutos)
            df.to_csv(caminho_arquivo, index=False, sep=';', encoding='utf-8-sig')
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Relatório CSV salvo!"), bgcolor=ft.Colors.GREEN)
        else:
            self.page.snack_bar = ft.SnackBar(ft.Text("Nenhum dado para exportar."), bgcolor=ft.Colors.ORANGE)
        self.page.snack_bar.open = True
        self.page.update()

    def gerar_e_salvar_pdf_programatico(self, caminho_arquivo):
        print("Coletando dados para o relatório PDF...")
        try:
            ano = self.dd_ano.value
            mes = self.dd_mes.value if self.dd_mes.value != "todos" else None
            # Pega os dados mais recentes com base nos filtros
            dados = self.controller.get_dados_dashboard(ano=ano, mes=mes)

            if not dados or dados['sessoes_realizadas'] == 0:
                self.page.snack_bar = ft.SnackBar(ft.Text("Não há dados suficientes para gerar o relatório PDF."), bgcolor=ft.colors.ORANGE)
            else:
                # Chama o nosso novo gerador de PDF
                pdf_generator.gerar_pdf_dashboard(caminho_arquivo, dados)
                self.page.snack_bar = ft.SnackBar(ft.Text(f"Relatório PDF salvo com sucesso!"), bgcolor=ft.colors.GREEN)
        
        except Exception as ex:
            traceback.print_exc()
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Erro ao gerar relatório PDF: {ex}"), bgcolor=ft.colors.ERROR)

        self.page.snack_bar.open = True
        self.page.update()

    # --- MÉTODOS DE DADOS E CICLO DE VIDA ---
    
    def did_mount(self):
        if self.dd_ano.options:
            self.dd_ano.value = self.dd_ano.options[0].key
            self.dd_mes.value = "todos"
        self.update_dashboard_data()

    def update_dashboard_data(self, e=None):
        ano = self.dd_ano.value
        mes = self.dd_mes.value if self.dd_mes.value != "todos" else None
        if not ano: return
        
        dados = self.controller.get_dados_dashboard(ano=ano, mes=mes)

        if dados:
            self.kpi_faturamento_bruto.value = dados['faturamento_bruto']
            self.kpi_lucro_liquido.value = dados['lucro_liquido']
            self.kpi_sessoes_realizadas.value = str(dados['sessoes_realizadas'])
            self.kpi_novos_pacientes.value = str(dados['novos_pacientes'])
            
            self.bar_chart.bar_groups = []
            meses_nomes = [m[0:3] for m in calendar.month_abbr]
            for i, valor in enumerate(dados['faturamento_mensal']):
                self.bar_chart.bar_groups.append(
                    ft.BarChartGroup(x=i, bar_rods=[ft.BarChartRod(from_y=0, to_y=valor, width=15, color=ft.Colors.BLUE_GREY, tooltip=f"R$ {valor:,.2f}")])
                )
            self.bar_chart.bottom_axis.labels = [ft.ChartAxisLabel(value=i, label=ft.Text(meses_nomes[i+1])) for i in range(12)]
            
            self.lista_proximas_sessoes.controls = []
            if dados['proximas_sessoes']:
                for sessao in dados['proximas_sessoes']:
                    self.lista_proximas_sessoes.controls.append(
                        ft.ListTile(leading=ft.Icon(ft.Icons.EVENT_AVAILABLE), title=ft.Text(sessao['name']), subtitle=ft.Text(sessao['data_hora'].strftime('%d/%m/%Y às %H:%M')))
                    )
            else:
                self.lista_proximas_sessoes.controls.append(ft.Text("Nenhuma sessão futura encontrada."))
        
        self.update()

    def build(self):
        """Constrói o layout visual do dashboard."""
        export_button = ft.PopupMenuButton(
            icon=ft.Icons.SAVE_ALT, tooltip="Exportar dados do dashboard",
            items=[
                ft.PopupMenuItem(icon=ft.Icons.GRID_ON, text="Exportar para CSV", on_click=self.exportar_csv),
                ft.PopupMenuItem(icon=ft.Icons.PICTURE_AS_PDF, text="Exportar Relatório PDF", on_click=self.exportar_pdf),
            ]
        )
        return ft.Column(
            expand=True, scroll=ft.ScrollMode.ADAPTIVE,
            controls=[
                ft.Row(alignment=ft.MainAxisAlignment.SPACE_BETWEEN, controls=[ft.Text("Dashboard", style=ft.TextThemeStyle.HEADLINE_MEDIUM), export_button]),
                ft.Row(controls=[self.dd_ano, self.dd_mes]),
                ft.Divider(),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Card(ft.Container(ft.Column([ft.Text("Faturamento Bruto"), self.kpi_faturamento_bruto]), padding=20), expand=True),
                        ft.Card(ft.Container(ft.Column([ft.Text("Lucro Líquido"), self.kpi_lucro_liquido]), padding=20), expand=True),
                        ft.Card(ft.Container(ft.Column([ft.Text("Sessões Realizadas"), self.kpi_sessoes_realizadas]), padding=20), expand=True),
                        ft.Card(ft.Container(ft.Column([ft.Text("Novos Pacientes"), self.kpi_novos_pacientes]), padding=20), expand=True),
                    ]
                ),
                ft.Divider(),
                ft.Row(
                    expand=True, vertical_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Container(
                            content=ft.Column([ft.Text("Faturamento Mensal", style=ft.TextThemeStyle.TITLE_MEDIUM), self.bar_chart]),
                            expand=3, padding=10,
                        ),
                        ft.Container(
                            content=ft.Column([ft.Text("Próximas 5 Sessões", style=ft.TextThemeStyle.TITLE_MEDIUM), self.lista_proximas_sessoes]),
                            expand=1, padding=10,
                            border=ft.border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=ft.border_radius.all(8)
                        )
                    ]
                )
            ]
        )