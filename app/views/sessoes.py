import flet as ft
from datetime import datetime
from functools import partial

class SessoesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.content = self.build()

    def build(self):
        from ..controllers.pacientes_controller import PacientesController
        # Filtro por data
        filtro_data_field = ft.TextField(label="Data", read_only=True, width=150)
        filtro_date_picker = ft.DatePicker(
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2100, 12, 31)
        )
        if not hasattr(self.page, 'overlay'):
            self.page.overlay = []
        if filtro_date_picker not in self.page.overlay:
            self.page.overlay.append(filtro_date_picker)
        def on_filtro_date_change(e):
            if filtro_date_picker.value:
                filtro_data_field.value = filtro_date_picker.value.strftime('%d/%m/%Y')
                filtro_data_field.update()
        filtro_date_picker.on_change = on_filtro_date_change
        def abrir_filtro_date_picker(e):
            filtro_date_picker.open = True
            self.page.update()
        filtro_data_field.suffix = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_filtro_date_picker)
        # Filtro por paciente
        pacientes_ctrl = PacientesController()
        pacientes = pacientes_ctrl.listar()
        paciente_options = [ft.dropdown.Option(str(p.id), text=p.name) for p in pacientes if getattr(p, 'status', 1) == 1]
        paciente_options.insert(0, ft.dropdown.Option("", text="Todos"))
        filtro_paciente_dd = ft.Dropdown(label="Paciente", options=paciente_options, value="", width=200)
        # Filtro por status
        filtro_status_dd = ft.Dropdown(label="Status", options=[
            ft.dropdown.Option("", text="Todos"),
            ft.dropdown.Option("1", text="Pago"),
            ft.dropdown.Option("0", text="Não pago")
        ], value="", width=400)
        # Botão Filtrar
        filtro_btn = ft.ElevatedButton(text="Filtrar", icon=ft.Icons.SEARCH)
        # Container de filtros
        filtro_height = 48
        def abrir_novo(ev=None):
            from ..controllers.sessoes_controller import SessoesController
            from ..controllers.pacientes_controller import PacientesController
            # Valores default
            selected_date = datetime.now()
            pacientes_ctrl = PacientesController()
            pacientes = pacientes_ctrl.listar()
            paciente_options = [ft.dropdown.Option(str(p.id), text=f"{p.id} - {p.name}") for p in pacientes if getattr(p, 'status', 1) == 1]
            horarios = [f"{h:02}:00" for h in range(8, 19)]
            horario_dd = ft.Dropdown(label="Horário", options=[ft.dropdown.Option(h) for h in horarios], value=horarios[0], width=200)
            paciente_dd = ft.Dropdown(label="Paciente", options=paciente_options, value=paciente_options[0].key if paciente_options else None, width=400, autofocus=True)
            status_switch = ft.Switch(label="Pago?", value=False)
            data_field = ft.TextField(label="Data", value=selected_date.strftime('%d/%m/%Y'), read_only=True, width=150)
            date_picker = ft.DatePicker(
                value=selected_date,
                first_date=datetime(2020, 1, 1),
                last_date=datetime(2100, 12, 31)
            )
            if not hasattr(self.page, 'overlay'):
                self.page.overlay = []
            if date_picker not in self.page.overlay:
                self.page.overlay.append(date_picker)
            def on_date_change(e):
                if date_picker.value:
                    data_field.value = date_picker.value.strftime('%d/%m/%Y')
                    data_field.update()
            date_picker.on_change = on_date_change
            def abrir_date_picker(e):
                date_picker.open = True
                self.page.update()
            data_field.suffix = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_date_picker)
            erro_txt = ft.Text("", color=ft.Colors.ERROR, visible=False)
            def close_dlg(ev):
                self.content = self.build()
                self.page.update()
            def save_new(ev):
                novo_paciente = paciente_dd.value
                novo_horario = horario_dd.value
                data_str = data_field.value
                try:
                    nova_data = datetime.strptime(data_str, '%d/%m/%Y')
                except Exception:
                    nova_data = selected_date
                novo_status = 1 if status_switch.value else 0
                if not novo_paciente or not novo_horario or not nova_data:
                    erro_txt.value = "Preencha todos os campos."
                    erro_txt.visible = True
                    self.page.update()
                    return
                # Checar duplicidade
                sessoes_ctrl = SessoesController()
                sessoes_do_dia = sessoes_ctrl.listar_por_dia(nova_data)
                for s in sessoes_do_dia:
                    if str(s['paciente_id']) == novo_paciente and datetime.strptime(str(s['data_hora']), '%Y-%m-%d %H:%M:%S').strftime('%H:%M') == novo_horario:
                        erro_txt.value = "Já existe um agendamento para esse horário."
                        erro_txt.visible = True
                        self.page.update()
                        return
                novo_dt = datetime.combine(nova_data.date(), datetime.strptime(novo_horario, '%H:%M').time())
                sessoes_ctrl.adicionar(int(novo_paciente), novo_dt, novo_status)
                close_dlg(ev)
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Sessão cadastrada!"), bgcolor=ft.Colors.SECONDARY_CONTAINER)
                self.page.update()
            dlg_modal = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Nova Sessão", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                        data_field,
                        horario_dd,
                        paciente_dd,
                        ft.Row([
                            ft.Text("Status:"),
                            status_switch
                        ]),
                        erro_txt,
                        ft.Row([
                            ft.TextButton("Cancelar", on_click=close_dlg),
                            ft.TextButton("Salvar", on_click=save_new)
                        ], alignment=ft.MainAxisAlignment.END)
                    ],
                    tight=True,
                    spacing=20
                ),
                padding=30,
                bgcolor=ft.Colors.SURFACE,
                border_radius=10,
                alignment=ft.alignment.center,
                expand=True
            )
            self.content = dlg_modal
            self.page.update()
        btn_novo = ft.ElevatedButton(text="Novo", icon=ft.Icons.ADD, on_click=abrir_novo)
        filtro_height = 48
        filtros_col = ft.Column([
            ft.Row([
                ft.Container(filtro_data_field, width=180, height=filtro_height, padding=ft.padding.only(right=0, left=0, top=0, bottom=0), alignment=ft.alignment.center),
                ft.Container(filtro_paciente_dd, width=250, height=filtro_height, padding=ft.padding.only(right=0, left=0, top=0, bottom=0), alignment=ft.alignment.center),
                ft.Container(filtro_status_dd, width=130, height=filtro_height, padding=ft.padding.only(right=0, left=0, top=0, bottom=0), alignment=ft.alignment.center),
                ft.Container(filtro_btn, width=100, height=filtro_height, alignment=ft.alignment.center),
                ft.Container(btn_novo, width=100, height=filtro_height, alignment=ft.alignment.center)
            ], spacing=10, alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ], spacing=5, alignment=ft.MainAxisAlignment.START)
        filtro_status_dd.text_size = 15
        filtro_status_dd.max_lines = 1
        filtro_status_dd.autofocus = False

        # Armazenar filtros em self
        self.filtro_data_field = filtro_data_field
        self.filtro_date_picker = filtro_date_picker
        self.filtro_paciente_dd = filtro_paciente_dd
        self.filtro_status_dd = filtro_status_dd
        self.filtro_btn = filtro_btn
        # Handler do botão filtrar
        def aplicar_filtros(e=None):
            # Exibe só o resultado filtrado e um botão voltar
            def voltar(e=None):
                self.content = self.build()
                self.page.update()
            btn_voltar = ft.ElevatedButton(text="Voltar", icon=ft.Icons.ARROW_BACK, on_click=voltar)
            tabela_filtrada = self.build_sessions_list(
                filtro_data=filtro_data_field.value,
                filtro_paciente=filtro_paciente_dd.value,
                filtro_status=filtro_status_dd.value
            )
            self.content = ft.Column([
                ft.Text("Sessões", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                btn_voltar,
                tabela_filtrada
            ], spacing=10, alignment=ft.MainAxisAlignment.START)
            self.page.update()
        filtro_btn.on_click = aplicar_filtros
        # Atualizar tabela ao trocar algum filtro (opcional: comentar se preferir só pelo botão)
        filtro_paciente_dd.on_change = aplicar_filtros
        filtro_status_dd.on_change = aplicar_filtros
        filtro_data_field.on_change = aplicar_filtros
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Sessões", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                    filtros_col,
                    self.build_sessions_list()
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.START
            ),
            padding=20
        )

    def editar_sessao(self, sessao, e=None):
        # Modal de edição próprio (independente do AgendaView)
        from ..controllers.sessoes_controller import SessoesController
        from ..controllers.pacientes_controller import PacientesController
        selected_date = sessao['data_hora'] if isinstance(sessao['data_hora'], datetime) else datetime.strptime(str(sessao['data_hora']), "%Y-%m-%d %H:%M:%S")
        pacientes_ctrl = PacientesController()
        pacientes = pacientes_ctrl.listar()
        paciente_options = [ft.dropdown.Option(str(p.id), text=f"{p.id} - {p.name}") for p in pacientes if getattr(p, 'status', 1) == 1]
        horarios = [f"{h:02}:00" for h in range(8, 19)]
        sessoes_ctrl = SessoesController()
        sessoes_do_dia = sessoes_ctrl.listar_por_dia(selected_date)
        horarios_ocupados = set()
        for s in sessoes_do_dia:
            if s['id'] == sessao['id']:
                continue
            h_existente = s['data_hora']
            if isinstance(h_existente, str):
                try:
                    h_existente = datetime.strptime(h_existente, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    continue
            horarios_ocupados.add(h_existente.hour)
        horarios_disponiveis = [h for h in horarios if int(h.split(':')[0]) not in horarios_ocupados or h == selected_date.strftime('%H')]
        horario_atual = selected_date.strftime('%H:00')
        paciente_atual = str(sessao['paciente_id'])
        status_atual = bool(sessao.get('status', 0))
        # Campo de data (TextField com botão para abrir o DatePicker)
        data_field = ft.TextField(
            label="Data",
            value=selected_date.strftime('%d/%m/%Y'),
            read_only=True,
            width=150
        )
        date_picker = ft.DatePicker(
            on_change=lambda e: data_field.update(value=e.control.value.strftime('%d/%m/%Y')),
            value=selected_date,
            first_date=datetime(2020, 1, 1),
            last_date=datetime(2100, 12, 31)
        )
        # Adiciona o date_picker ao overlay se não estiver
        if not hasattr(self.page, 'overlay'):
            self.page.overlay = []
        if date_picker not in self.page.overlay:
            self.page.overlay.append(date_picker)
        def on_date_change(e):
            if date_picker.value:
                data_field.value = date_picker.value.strftime('%d/%m/%Y')
                data_field.update()
        date_picker.on_change = on_date_change
        def abrir_date_picker(e):
            date_picker.open = True
            self.page.update()
        data_field.suffix = ft.IconButton(icon=ft.Icons.CALENDAR_MONTH, on_click=abrir_date_picker)

        horario_dd = ft.Dropdown(label="Horário", options=[ft.dropdown.Option(h) for h in horarios_disponiveis], value=horario_atual, width=200)
        paciente_dd = ft.Dropdown(label="Paciente", options=paciente_options, value=paciente_atual, width=400, autofocus=True)
        status_switch = ft.Switch(label="Pago?", value=status_atual)
        erro_txt = ft.Text("", color=ft.Colors.ERROR, visible=False)
        def close_dlg(ev):
            self.content = self.build()
            self.page.update()
        def save_edit(ev):
            novo_paciente = paciente_dd.value
            novo_horario = horario_dd.value
            data_str = data_field.value
            try:
                nova_data = datetime.strptime(data_str, '%d/%m/%Y')
            except Exception:
                nova_data = selected_date
            novo_status = 1 if status_switch.value else 0
            if not novo_paciente or not novo_horario or not nova_data:
                erro_txt.value = "Preencha todos os campos."
                erro_txt.visible = True
                self.page.update()
                return
            for s in sessoes_do_dia:
                if s['id'] != sessao['id'] and str(s['paciente_id']) == novo_paciente and datetime.strptime(str(s['data_hora']), '%Y-%m-%d %H:%M:%S').strftime('%H:%M') == novo_horario:
                    erro_txt.value = "Já existe um agendamento para esse horário."
                    erro_txt.visible = True
                    self.page.update()
                    return
            novo_dt = datetime.combine(nova_data.date(), datetime.strptime(novo_horario, '%H:%M').time())
            sessoes_ctrl.editar(sessao['id'], int(novo_paciente), novo_dt)
            # Atualizar status manualmente
            sessoes_ctrl.db.cursor.execute("UPDATE sessoes SET status=%s WHERE id=%s", (novo_status, sessao['id']))
            sessoes_ctrl.db.conn.commit()
            close_dlg(ev)
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Agendamento alterado!"), bgcolor=ft.Colors.SECONDARY_CONTAINER)
            self.page.update()
        dlg_modal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Editar Agendamento", style=ft.TextThemeStyle.TITLE_MEDIUM, weight=ft.FontWeight.BOLD),
                    data_field,
                    horario_dd,
                    paciente_dd,
                    ft.Row([
                        ft.Text("Status:"),
                        status_switch
                    ]),
                    erro_txt,
                    ft.Row([
                        ft.TextButton("Cancelar", on_click=close_dlg),
                        ft.TextButton("Salvar", on_click=save_edit)
                    ], alignment=ft.MainAxisAlignment.END)
                ],
                tight=True,
                spacing=20
            ),
            padding=30,
            bgcolor=ft.Colors.SURFACE,
            border_radius=10,
            alignment=ft.alignment.center,
            expand=True
        )
        self.content = dlg_modal
        self.page.update()

    def excluir_sessao(self, sessao, e=None):
        # Mesmo comportamento do módulo Agenda
        from ..controllers.sessoes_controller import SessoesController
        def on_confirmar(e):
            SessoesController().excluir(sessao['id'])
            if hasattr(self.page, 'dialog') and self.page.dialog:
                self.page.dialog.open = False
                self.page.update()
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Agendamento excluído!"), bgcolor=ft.Colors.ERROR)
            self.content = self.build()
            self.page.update()
        def on_cancelar(e):
            if hasattr(self.page, 'dialog') and self.page.dialog:
                self.page.dialog.open = False
                self.page.update()
        dlg = ft.AlertDialog(
            title=ft.Text("Excluir agendamento"),
            content=ft.Text(f"Deseja realmente excluir a sessão de {sessao['paciente_nome']} em {sessao['data_hora']}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancelar),
                ft.TextButton("Excluir", on_click=on_confirmar)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            open=True
        )
        self.page.dialog = dlg
        if hasattr(self.page, 'overlay') and isinstance(self.page.overlay, list):
            if dlg not in self.page.overlay:
                self.page.overlay.append(dlg)
        self.page.dialog.open = True
        self.page.update()

    def confirmar_pagamento(self, sessao, e=None):
        from ..controllers.sessoes_controller import SessoesController
        def on_confirmar(ev):
            sessoes_ctrl = SessoesController()
            if not sessoes_ctrl.db.connect():
                self.page.snack_bar = ft.SnackBar(ft.Text("Erro ao conectar ao banco."), open=True)
                self.page.dialog.open = False
                self.page.update()
                return
            query = "UPDATE sessoes SET status=1 WHERE id=%s"
            sessoes_ctrl.db.cursor.execute(query, (sessao['id'],))
            sessoes_ctrl.db.conn.commit()
            self.page.dialog.open = False
            self.page.snack_bar = ft.SnackBar(ft.Text("Sessão marcada como paga!"), open=True)
            self.page.update()
            self.content = self.build()
            self.page.update()
        def on_cancelar(ev):
            self.page.dialog.open = False
            self.page.update()
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar Pagamento"),
            content=ft.Text(f"Deseja marcar a sessão de {sessao['paciente_nome']} em {sessao['data_hora']} como PAGA?"),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancelar),
                ft.TextButton("Confirmar", on_click=on_confirmar)
            ],
            open=True
        )
        self.page.dialog = dialog
        self.page.dialog.open = True
        self.page.update()

    def build_sessions_list(self, filtro_data=None, filtro_paciente=None, filtro_status=None):
        from ..controllers.sessoes_controller import SessoesController
        sessoes_ctrl = SessoesController()
        # Buscar todas as sessões do banco
        sessoes = sessoes_ctrl.db.connect() and sessoes_ctrl.db.cursor.execute('''
            SELECT s.id, s.paciente_id, s.data_hora, s.status, p.name as paciente_nome
            FROM sessoes s
            JOIN pacientes p ON s.paciente_id = p.id
            ORDER BY s.data_hora DESC
        ''') or []
        sessoes = sessoes_ctrl.db.cursor.fetchall() if sessoes_ctrl.db.cursor else []
        # Aplicar filtros
        sessoes_filtradas = []
        for sessao in sessoes:
            try:
                data_obj = sessao['data_hora'] if isinstance(sessao['data_hora'], datetime) else datetime.strptime(str(sessao['data_hora']), "%Y-%m-%d %H:%M:%S")
            except Exception:
                data_obj = datetime.now()
            # Filtro data
            if filtro_data:
                try:
                    filtro_data_obj = datetime.strptime(filtro_data, '%d/%m/%Y')
                    if data_obj.date() != filtro_data_obj.date():
                        continue
                except Exception:
                    pass
            # Filtro paciente
            if filtro_paciente and str(sessao['paciente_id']) != str(filtro_paciente):
                continue
            # Filtro status
            if filtro_status in ["0", "1"] and str(sessao.get('status', 0)) != filtro_status:
                continue
            sessoes_filtradas.append(sessao)
        rows = []
        for sessao in sessoes_filtradas:
            # Formatar data para dd/mm/aaaa
            try:
                data_obj = sessao['data_hora'] if isinstance(sessao['data_hora'], datetime) else datetime.strptime(str(sessao['data_hora']), "%Y-%m-%d %H:%M:%S")
            except Exception:
                data_obj = datetime.now()
            data_br = data_obj.strftime("%d/%m/%Y")
            status_txt = "Sim" if sessao.get('status', 0) in [1, True, '1', 'True'] else "Não"
            pode_pagar = (data_obj.date() < datetime.now().date()) and (sessao.get('status', 0) in [0, False, '0', 'False'])
            rows.append(ft.DataRow(cells=[
                ft.DataCell(ft.Text(sessao['paciente_nome'])),
                ft.DataCell(ft.Text(data_br)),
                ft.DataCell(ft.Text(status_txt)),
                ft.DataCell(
                    ft.Row([
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            tooltip="Editar",
                            on_click=lambda e, s=sessao: self.editar_sessao(s, e)
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            tooltip="Excluir",
                            on_click=lambda e, s=sessao: self.excluir_sessao(s, e)
                        )
                    ])
                ),
            ]))
        return ft.Container(
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Paciente")),
                    ft.DataColumn(ft.Text("Data")),
                    ft.DataColumn(ft.Text("Pago?")),
                    ft.DataColumn(ft.Text("Ações"))
                ],
                rows=rows
            )
        )
