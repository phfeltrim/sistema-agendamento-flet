import flet as ft
from datetime import datetime, timedelta
from controllers.pacientes_controller import PacientesController
from controllers.sessoes_controller import SessoesController

class AgendaView(ft.Container):
    def __init__(self, page: ft.Page, on_view_change):
        super().__init__()
        self.page = page
        self.on_view_change = on_view_change
        self.current_date = datetime.now()
        self.appointments = []  # Lista de agendamentos
        # self.navigation = self.build_navigation()
        self.expand = True
        self.content = self.build()

    def formatar_mes_ano_ptbr(self, data):
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]
        return f"{meses[data.month-1]} {data.year}"

    def build_navigation(self):
        return ft.Container(
            content=ft.Column([
                # Logo/Título
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.icons.CALENDAR_MONTH, size=24, color=ft.colors.PRIMARY),
                            ft.Text("Agenda", size=20, weight=ft.FontWeight.BOLD)
                        ],
                        spacing=10
                    ),
                    padding=20,
                    margin=ft.margin.only(bottom=20)
                ),
                # Menu de Navegação
                ft.Container(
                    content=ft.NavigationRail(
                        selected_index=0,
                        label_type=ft.NavigationRailLabelType.ALL,
                        extended=True,
                        
                        destinations=[
                            ft.NavigationRailDestination(
                                icon=ft.icons.CALENDAR_TODAY_OUTLINED,
                                selected_icon=ft.icons.CALENDAR_TODAY,
                                label="Agenda"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.PEOPLE_OUTLINE,
                                selected_icon=ft.icons.PEOPLE,
                                label="Pacientes"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.LIST_ALT_OUTLINED,
                                selected_icon=ft.icons.LIST_ALT,
                                label="Sessões"
                            ),
                            ft.NavigationRailDestination(
                                icon=ft.icons.SETTINGS_OUTLINED,
                                selected_icon=ft.icons.SETTINGS,
                                label="Configurações"
                            ),
                        ],
                        on_change=self.handle_navigation_change
                    ),
                    
                )
            ], ),
            
            width=250,
            height=768  # Altura fixa igual à altura da janela
        )

    def handle_navigation_change(self, e):
        index = e.control.selected_index
        views = ["agenda", "pacientes", "sessoes", "configuracoes"]
        if self.on_view_change:
            self.on_view_change(views[index])

    def build(self):
        return ft.Container(
            expand=True,
            content=ft.Column(
                controls=[
                    ft.Text("Agenda", size=30, weight=ft.FontWeight.BOLD),
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=self.build_calendar(),
                                expand=True
                            ),
                            ft.Container(
                                content=self.build_appointments_list(),
                                expand=True
                            )
                        ],
                        spacing=30,
                        expand=True
                    )
                ],
                spacing=20,
                expand=True
            ),
            padding=20
        )
                                            
    def build_calendar(self):
        # Dias da semana em português
        weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        weekday_headers = [
            ft.Container(
                content=ft.Text(day, weight=ft.FontWeight.BOLD),
                width=40,
                height=30,
                alignment=ft.alignment.center
            ) for day in weekdays
        ]
        first_day = self.current_date.replace(day=1)
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        days = []
        week = []
        # Buscar todos os agendamentos do mês para destacar
        sessoes_ctrl = SessoesController()
        dias_com_agendamento = set()
        for dia in range(1, last_day + 1):
            data = first_day.replace(day=dia)
            sessoes_do_dia = sessoes_ctrl.listar_por_dia(data)
            if sessoes_do_dia:
                dias_com_agendamento.add(dia)
        # Calcula o índice do primeiro dia do mês (0=Domingo)
        first_weekday = (first_day.weekday() + 1) % 7
        # Preenche os dias vazios até o primeiro dia do mês
        for _ in range(first_weekday):
            week.append(ft.Container(
                content=ft.Text(""),
                width=40,
                height=40,
                alignment=ft.alignment.center
            ))
        # Preenche os dias do mês
        for day in range(1, last_day + 1):
            is_today = day == datetime.now().day and self.current_date.month == datetime.now().month and self.current_date.year == datetime.now().year
            is_selected = day == self.current_date.day
            highlight = day in dias_com_agendamento
            if is_selected:
                color = ft.colors.ON_PRIMARY
                bgcolor = ft.colors.PRIMARY
                border = ft.border.all(2, ft.colors.PRIMARY)
                weight = ft.FontWeight.BOLD
            elif is_today:
                color = ft.colors.PRIMARY
                bgcolor = ft.colors.SECONDARY_CONTAINER
                border = ft.border.all(1, ft.colors.PRIMARY)
                weight = ft.FontWeight.NORMAL
            elif highlight:
                color = ft.colors.ON_SURFACE
                bgcolor = "#C8F7C5"
                border = None
                weight = ft.FontWeight.NORMAL
            else:
                color = ft.colors.ON_SURFACE
                bgcolor = ft.colors.SURFACE
                border = None
                weight = ft.FontWeight.NORMAL
            week.append(ft.Container(
                content=ft.Text(str(day), color=color, weight=weight),
                width=40,
                height=40,
                alignment=ft.alignment.center,
                bgcolor=bgcolor,
                border_radius=8,
                on_click=lambda e, d=day: self.select_date(d),
                border=border
            ))
            if len(week) == 7:
                days.append(ft.Row(controls=week, alignment=ft.MainAxisAlignment.START))
                week = []
        if week:
            # Preenche o restante da última semana
            while len(week) < 7:
                week.append(ft.Container(
                    content=ft.Text(""),
                    width=40,
                    height=40,
                    alignment=ft.alignment.center
                ))
            days.append(ft.Row(controls=week, alignment=ft.MainAxisAlignment.START))
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row([
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=lambda _: self.change_month(-1)
                        ),
                        ft.Container(
                            content=ft.Text(
                                self.formatar_mes_ano_ptbr(self.current_date),
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),
                            alignment=ft.alignment.center,
                            expand=True
                        ),
                        ft.IconButton(
                            icon=ft.icons.ARROW_FORWARD,
                            on_click=lambda _: self.change_month(1)
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Row(
                        controls=weekday_headers,
                        alignment=ft.MainAxisAlignment.START
                    ),
                    *days
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            bgcolor=ft.colors.SURFACE,
            border_radius=8
        )

    def abrir_modal_edicao(self, sessao):
        selected_date = self.current_date
        # Data em português
        dias_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        dia_semana = dias_semana[selected_date.weekday()]
        mes = meses[selected_date.month - 1]
        data_str = f"{dia_semana}, {selected_date.day:02} de {mes} de {selected_date.year}"
        # Pacientes ativos
        pacientes_ctrl = PacientesController()
        pacientes = pacientes_ctrl.listar()
        paciente_options = [ft.dropdown.Option(str(p.id), text=f"{p.id} - {p.name}") for p in pacientes if p.status == 1]
        # Horários disponíveis
        horarios = []
        start_hour = 8
        end_hour = 18
        for h in range(start_hour, end_hour + 1):
            horarios.append(f"{h:02}:00")
        sessoes_ctrl = SessoesController()
        sessoes_do_dia = sessoes_ctrl.listar_por_dia(selected_date)
        horarios_ocupados = set()
        for s in sessoes_do_dia:
            if s['id'] == sessao['id']:
                continue  # Ignora o próprio
            h_existente = s['data_hora']
            if isinstance(h_existente, str):
                try:
                    h_existente = datetime.strptime(h_existente, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    continue
            horarios_ocupados.add(h_existente.hour)
        horarios_disponiveis = [h for h in horarios if int(h.split(':')[0]) not in horarios_ocupados or h == datetime.strptime(str(sessao['data_hora']), '%Y-%m-%d %H:%M:%S').strftime('%H:%M')]
        # Dropdowns preenchidos
        horario_atual = datetime.strptime(str(sessao['data_hora']), '%Y-%m-%d %H:%M:%S').strftime('%H:%M')
        paciente_atual = str(sessao['paciente_id'])
        horario_dd = ft.Dropdown(
            label="Horário",
            options=[ft.dropdown.Option(h) for h in horarios_disponiveis],
            value=horario_atual,
            width=200
        )
        paciente_dd = ft.Dropdown(
            label="Paciente",
            options=paciente_options,
            value=paciente_atual,
            width=400,
            autofocus=True
        )
        erro_txt = ft.Text("", color=ft.colors.ERROR, visible=False)
        def close_dlg(e):
            self.content = self.build()
            self.page.update()
        def save_edit(e):
            novo_paciente = paciente_dd.value
            novo_horario = horario_dd.value
            if not (novo_paciente and novo_horario):
                erro_txt.value = "Preencha todos os campos."
                erro_txt.visible = True
                self.page.update()
                return
            # Checa duplicidade
            for s in sessoes_do_dia:
                if s['id'] != sessao['id'] and str(s['paciente_id']) == novo_paciente and datetime.strptime(str(s['data_hora']), '%Y-%m-%d %H:%M:%S').strftime('%H:%M') == novo_horario:
                    erro_txt.value = "Já existe um agendamento para esse horário."
                    erro_txt.visible = True
                    self.page.update()
                    return
            novo_dt = selected_date.replace(hour=int(novo_horario.split(':')[0]), minute=0, second=0, microsecond=0)
            SessoesController().editar(sessao['id'], int(novo_paciente), novo_dt)
            close_dlg(e)
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Agendamento alterado!"), bgcolor=ft.colors.SECONDARY_CONTAINER)
            self.page.update()
            self.content = self.build()
            self.page.update()
        dlg_modal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Editar Agendamento", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Data selecionada: {data_str}"),
                    horario_dd,
                    paciente_dd,
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
            bgcolor=ft.colors.SURFACE,
            border_radius=10,
            alignment=ft.alignment.center,
            expand=True
        )
        self.dialog_agendamento = dlg_modal
        self.content = dlg_modal
        self.page.update()

    def build_appointments_list(self):
        # Handlers para editar e excluir agendamento
        def editar_agendamento(sessao):
            # Abre modal de edição com dados preenchidos
            self.abrir_modal_edicao(sessao)
        def excluir_agendamento(sessao):
            
            def confirmar_exclusao(e):
                
                SessoesController().excluir(sessao['id'])
                if hasattr(self.page, 'dialog') and self.page.dialog:
                    self.page.dialog.open = False
                    self.page.update()
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Agendamento excluído!"), bgcolor=ft.colors.ERROR)
                self.content = self.build()
                self.page.update()
            dlg = ft.AlertDialog(
                title=ft.Text("Excluir agendamento"),
                content=ft.Text("Tem certeza que deseja excluir este agendamento?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: self.fechar_dialogo()),
                    ft.TextButton("Excluir", on_click=confirmar_exclusao)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            self.page.dialog = dlg
            if hasattr(self.page, 'overlay') and isinstance(self.page.overlay, list):
                if dlg not in self.page.overlay:
                    self.page.overlay.append(dlg)
            
            self.page.dialog.open = True
            self.page.update()
            
        self.editar_agendamento = editar_agendamento
        def fechar_dialogo():
            if hasattr(self.page, 'dialog') and self.page.dialog:
                self.page.dialog.open = False
                self.page.update()
        self.fechar_dialogo = fechar_dialogo
        self.excluir_agendamento = excluir_agendamento
        # Buscar agendamentos reais do banco para o dia selecionado
        sessoes_ctrl = SessoesController()
        sessoes = sessoes_ctrl.listar_por_dia(self.current_date)
        appointment_cards = []
        import functools
        for s in sessoes:
            card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                datetime.strptime(str(s['data_hora']), '%H:%M' if len(str(s['data_hora'])) == 5 else '%Y-%m-%d %H:%M:%S').strftime('%H:%M'),
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            width=80
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    s['paciente_nome'],
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                            ],
                            spacing=5,
                        ),
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EDIT_OUTLINED,
                                    tooltip="Editar",
                                    icon_color=ft.colors.SECONDARY,
                                    on_click=lambda e, sessao=s: self.editar_agendamento(sessao)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE_OUTLINE,
                                    tooltip="Excluir",
                                    icon_color=ft.colors.ERROR,
                                    on_click=lambda e, sessao=s: self.excluir_agendamento(sessao)
                                )
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=15,
                bgcolor=ft.colors.SURFACE,
                margin=ft.margin.only(bottom=10)
            )
            appointment_cards.append(card)
        data_str = self.current_date.strftime('%d/%m/%Y')
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        f"Agendamentos do Dia: {data_str}",
                        size=20,
                        weight=ft.FontWeight.BOLD
                    ),
                    *appointment_cards,
                    ft.Container(expand=True),
                    ft.ElevatedButton(
                        text="Novo agendamento",
                        icon=ft.icons.ADD,
                        icon_color=ft.colors.ON_PRIMARY,
                        on_click=self.new_appointment
                    )
                ],
            ),
            bgcolor=ft.colors.SURFACE
        )

    def new_appointment(self, e):
        # 1. Data selecionada (não editável)
        selected_date = self.current_date
        # Data em português
        dias_semana = ["Domingo", "Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado"]
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        dia_semana = dias_semana[selected_date.weekday()]
        mes = meses[selected_date.month - 1]
        data_str = f"{dia_semana}, {selected_date.day:02} de {mes} de {selected_date.year}"
        
        # 2. Buscar pacientes ativos
        pacientes_ctrl = PacientesController()
        pacientes = pacientes_ctrl.listar()
        paciente_options = [ft.dropdown.Option(str(p.id), text=f"{p.id} - {p.name}") for p in pacientes if p.status == 1]
        
        # 3. Horários disponíveis (exemplo: 08:00 às 18:00, de hora em hora)
        horarios = []
        start_hour = 8
        end_hour = 18
        horarios = []
        for h in range(start_hour, end_hour + 1):
            horarios.append(f"{h:02}:00")
        # Filtrar horários já agendados do dia
        sessoes_ctrl = SessoesController()
        sessoes_do_dia = sessoes_ctrl.listar_por_dia(selected_date)
        horarios_ocupados = set()
        for s in sessoes_do_dia:
            h_existente = s['data_hora']
            if isinstance(h_existente, str):
                try:
                    h_existente = datetime.strptime(h_existente, '%Y-%m-%d %H:%M:%S')
                except Exception:
                    continue
            horarios_ocupados.add(h_existente.hour)
        horarios_disponiveis = [h for h in horarios if int(h.split(':')[0]) not in horarios_ocupados]
        horario_dd = ft.Dropdown(
            label="Horário",
            options=[ft.dropdown.Option(h) for h in horarios_disponiveis],
            width=200
        )
        
        # 4. Dropdown de pacientes
        paciente_dd = ft.Dropdown(
            label="Paciente",
            options=paciente_options,
            width=400,
            autofocus=True
        )
        
        def close_dlg(e):
            self.dialog_agendamento = None
            self.content = self.build()
            self.page.update()
        
        erro_txt = ft.Text("", color=ft.colors.RED, visible=False)
        def save_appointment(e):
            erro_txt.visible = False
            erro_txt.value = ""
            if not (paciente_dd.value and horario_dd.value):
                erro_txt.value = "Selecione paciente e horário."
                erro_txt.visible = True
                self.page.update()
                return
            # Montar datetime
            agendamento_dt = datetime(
                selected_date.year, selected_date.month, selected_date.day,
                int(horario_dd.value.split(':')[0]), 0, 0
            )
            # 1. Não permitir agendamento para horário anterior ou igual ao atual
            agora = datetime.now()
            if agendamento_dt <= agora:
                erro_txt.value = "Não é permitido agendar para horário anterior ou igual ao atual."
                erro_txt.visible = True
                self.page.update()
                return
            # 2. Não permitir agendamento duplicado para o mesmo horário
            sessoes_ctrl = SessoesController()
            sessoes_do_dia = sessoes_ctrl.listar_por_dia(selected_date)
            for s in sessoes_do_dia:
                h_existente = s['data_hora']
                if isinstance(h_existente, str):
                    try:
                        h_existente = datetime.strptime(h_existente, '%Y-%m-%d %H:%M:%S')
                    except Exception:
                        continue
                if h_existente.hour == agendamento_dt.hour and h_existente.date() == agendamento_dt.date():
                    erro_txt.value = "Já existe um agendamento para esse horário."
                    erro_txt.visible = True
                    self.page.update()
                    return
            # Salvar na tabela sessoes conforme diretrizes
            id_pac = int(paciente_dd.value)
            sessoes_ctrl.adicionar(id_pac, agendamento_dt)
            close_dlg(e)
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Agendamento criado com sucesso!"),
                bgcolor=ft.colors.GREEN_400
            )
            self.page.update()
            # Atualizar lista de agendamentos
            self.content = self.build()
            self.page.update()

        # Diálogo modal
        dlg_modal = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Novo Agendamento", size=22, weight=ft.FontWeight.BOLD),
                    ft.Text(f"Data selecionada: {data_str}"),
                    horario_dd,
                    paciente_dd,
                    erro_txt,
                    ft.Row([
                        ft.TextButton("Cancelar", on_click=close_dlg),
                        ft.TextButton("Salvar", on_click=save_appointment)
                    ], alignment=ft.MainAxisAlignment.END)
                ],
                tight=True,
                spacing=20
            ),
            padding=30,
            bgcolor=ft.colors.SURFACE,
            border_radius=10,
            alignment=ft.alignment.center,
            expand=True
        )
        self.dialog_agendamento = dlg_modal
        self.content = dlg_modal
        self.page.update()

        # Atualiza a lista de agendamentos do dia
        if hasattr(self, 'page'):
            # Procura o container principal e substitui o conteúdo
            # Ajuste conforme a estrutura real do layout
            for c in self.page.controls:
                if hasattr(c, 'content') and isinstance(c.content, ft.Column):
                    for idx, ctrl in enumerate(c.content.controls):
                        if isinstance(ctrl, ft.Container) and hasattr(ctrl, 'content') and isinstance(ctrl.content, ft.Column):
                            # Substitui o container de agendamentos
                            c.content.controls[idx] = self.build_appointments_list()
                            self.page.update()
                            return

    def update_time_slots(self, selected_date):
        # TODO: Buscar horários disponíveis no banco de dados
        # Por enquanto, mostra horários fixos das 8h às 18h com intervalo de 30min
        time_slots = []
        current_time = datetime.strptime("08:00", "%H:%M")
        end_time = datetime.strptime("18:00", "%H:%M")
        while current_time <= end_time:
            time_slots.append(ft.dropdown.Option(current_time.strftime("%H:%M")))
            current_time += timedelta(minutes=30)
        # Atualiza as opções do dropdown de horários
        if hasattr(self, "page") and self.page.dialog:
            time_dd = self.page.dialog.content.controls[0].controls[1]
            time_dd.options = time_slots
            self.page.update()

        
    def select_date(self, day):
        self.current_date = self.current_date.replace(day=day)
        self.content = self.build()
        self.update()

        
    def change_month(self, delta):
        # Calcula o novo mês
        new_date = self.current_date.replace(day=1)
        if delta > 0:
            if new_date.month == 12:
                new_date = new_date.replace(year=new_date.year + 1, month=1)
            else:
                new_date = new_date.replace(month=new_date.month + 1)
        else:
            if new_date.month == 1:
                new_date = new_date.replace(year=new_date.year - 1, month=12)
            else:
                new_date = new_date.replace(month=new_date.month - 1)
                
        self.current_date = new_date
        # Força a atualização da view
        self.content = self.build()
        self.update()
