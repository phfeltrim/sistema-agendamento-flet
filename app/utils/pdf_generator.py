from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.axes import XCategoryAxis, YValueAxis

def gerar_pdf_dashboard(caminho_arquivo: str, dados: dict):
    """
    Gera um relatório em PDF com os dados do dashboard.
    """
    doc = SimpleDocTemplate(caminho_arquivo, pagesize=landscape(letter))
    styles = getSampleStyleSheet()
    story = []

    # --- Título ---
    titulo = Paragraph("Relatório do Dashboard", styles['h1'])
    story.append(titulo)
    story.append(Spacer(1, 24))

    # --- KPIs ---
    kpi_data = [
        ['Faturamento Bruto', 'Lucro Líquido', 'Sessões Realizadas', 'Novos Pacientes'],
        [dados['faturamento_bruto'], dados['lucro_liquido'], str(dados['sessoes_realizadas']), str(dados['novos_pacientes'])]
    ]
    kpi_table = Table(kpi_data)
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#6E62E5")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, 1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 24))

    # --- Gráfico de Barras ---
    story.append(Paragraph("Faturamento Mensal", styles['h2']))
    
    drawing = Drawing(600, 250)
    chart_data = [(v,) for v in dados.get('faturamento_mensal', [])]
    
    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 50
    bc.height = 200
    bc.width = 550
    bc.data = chart_data
    bc.barSpacing = 5
    bc.groupSpacing = 10
    bc.valueAxis = YValueAxis()
    bc.categoryAxis = XCategoryAxis()
    bc.categoryAxis.categoryNames = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    drawing.add(bc)
    story.append(drawing)
    story.append(Spacer(1, 24))

    # --- Próximas Sessões ---
    story.append(Paragraph("Próximas Sessões", styles['h2']))
    sessoes_data = [['Paciente', 'Data e Hora']]
    for sessao in dados.get('proximas_sessoes', []):
        sessoes_data.append([
            Paragraph(sessao['name'], styles['Normal']),
            sessao['data_hora'].strftime('%d/%m/%Y às %H:%M')
        ])
    
    sessoes_table = Table(sessoes_data)
    sessoes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    ]))
    story.append(sessoes_table)
    
    # Constrói o PDF
    doc.build(story)
    print("Relatório PDF gerado com sucesso.")