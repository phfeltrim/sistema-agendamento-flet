import flet as ft
from datetime import datetime, timedelta

class AgendaView(ft.Container):
    def __init__(self, page: ft.Page, on_view_change):
        super().__init__()
        self.page = page
        self.on_view_change = on_view_change
        self.current_date = datetime.now()
        self.appointments = []  # Lista de agendamentos
        self.navigation = self.build_navigation()
        self.expand = True
        self.content = self.build()

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
                        bgcolor=ft.colors.SURFACE_VARIANT,
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
                    expand=True
                )
            ], expand=True),
            bgcolor=ft.colors.SURFACE_VARIANT,
            width=250,
            height=768  # Altura fixa igual à altura da janela
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
                    ft.Container(
                        content=ft.Column([
                            # Barra superior
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Container(
                                            content=ft.Row(
                                                controls=[
                                                    ft.Icon(ft.icons.SEARCH),
                                                    ft.TextField(
                                                        border=ft.InputBorder.NONE,
                                                        hint_text="Buscar...",
                                                        expand=True
                                                    )
                                                ],
                                                spacing=10
                                            ),
                                            bgcolor=ft.colors.SURFACE_VARIANT,
                                            border_radius=8,
                                            padding=10,
                                            expand=True
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.NOTIFICATIONS_OUTLINED,
                                            tooltip="Notificações"
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.PERSON_OUTLINED,
                                            tooltip="Perfil"
                                        )
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                padding=ft.padding.only(left=32, top=20, right=32, bottom=20)
                            ),
                            # Conteúdo principal
                            ft.Container(
                                content=ft.Column([
                                    # Título e botão de novo agendamento
                                    ft.Row(
                                        controls=[
                                            ft.Text(
                                                "Agenda",
                                                size=32,
                                                weight=ft.FontWeight.BOLD
                                            ),
                                            ft.ElevatedButton(
                                                "Novo Agendamento",
                                                icon=ft.icons.ADD,
                                                on_click=self.new_appointment
                                            )
                                        ],
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                    ),
                                    # Calendário e lista de agendamentos lado a lado
                                    ft.Row(
                                        controls=[
                                            # Coluna do calendário
                                            ft.Container(
                                                content=self.build_calendar(),
                                                expand=3  # Ocupa 3/5 do espaço
                                            ),
                                            # Coluna dos agendamentos
                                            ft.Container(
                                                content=self.build_appointments_list(),
                                                expand=2  # Ocupa 2/5 do espaço
                                            )
                                        ],
                                        spacing=32,
                                        expand=True
                                    )
                                ], spacing=20),
                                padding=32,
                                expand=True
                            )
                        ]),
                        expand=True
                    )
                ],
                expand=True
            ),
            expand=True
        )

    def build_calendar(self):
        # Cria o grid de dias da semana
        weekdays = ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"]
        weekday_headers = [ft.Text(day, weight=ft.FontWeight.BOLD) for day in weekdays]
        
        # Obtém o primeiro dia do mês atual
        first_day = self.current_date.replace(day=1)
        # Obtém o último dia do mês atual
        last_day = (first_day.replace(month=first_day.month % 12 + 1, day=1) - timedelta(days=1)).day
        
        # Cria o grid de dias
        days = []
        week = []
        
        # Preenche os dias vazios até o primeiro dia do mês
        for _ in range(first_day.weekday()):
            week.append(ft.Container(
                content=ft.Text(""),
                width=40,
                height=40,
                alignment=ft.alignment.center
            ))
        
        # Preenche os dias do mês
        for day in range(1, last_day + 1):
            is_today = day == self.current_date.day
            
            day_container = ft.Container(
                content=ft.Text(
                    str(day),
                    color=ft.colors.ON_PRIMARY if is_today else None,
                    weight=ft.FontWeight.BOLD if is_today else None
                ),
                width=40,
                height=40,
                border_radius=20,
                bgcolor=ft.colors.PRIMARY if is_today else ft.colors.SURFACE_VARIANT,
                alignment=ft.alignment.center,
                on_click=lambda e, d=day: self.select_date(d)
            )
            
            week.append(day_container)
            
            if len(week) == 7:
                days.append(ft.Row(controls=week, alignment=ft.MainAxisAlignment.CENTER))
                week = []
        
        # Completa a última semana se necessário
        if week:
            while len(week) < 7:
                week.append(ft.Container(
                    content=ft.Text(""),
                    width=40,
                    height=40,
                    alignment=ft.alignment.center
                ))
            days.append(ft.Row(controls=week, alignment=ft.MainAxisAlignment.CENTER))
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    # Cabeçalho do calendário
                    ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_LEFT,
                                on_click=lambda _: self.change_month(-1)
                            ),
                            ft.Text(
                                self.current_date.strftime("%B %Y"),
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.IconButton(
                                icon=ft.icons.ARROW_RIGHT,
                                on_click=lambda _: self.change_month(1)
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Dias da semana
                    ft.Row(
                        controls=weekday_headers,
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    # Grid de dias
                    *days
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
            padding=20,
            bgcolor=ft.colors.SURFACE,
            border_radius=8
        )

    def build_appointments_list(self):
        # Exemplo de agendamentos (substituir por dados do banco)
        appointments = [
            {
                "time": "09:00",
                "patient": "João Silva",
                "type": "Consulta Regular",
                "status": "confirmed"
            },
            {
                "time": "10:30",
                "patient": "Maria Santos",
                "type": "Avaliação",
                "status": "pending"
            },
            {
                "time": "14:00",
                "patient": "Pedro Oliveira",
                "type": "Retorno",
                "status": "confirmed"
            }
        ]
        
        appointment_cards = []
        for apt in appointments:
            status_color = ft.colors.GREEN_400 if apt["status"] == "confirmed" else ft.colors.ORANGE_400
            
            card = ft.Container(
                content=ft.Row(
                    controls=[
                        # Horário
                        ft.Container(
                            content=ft.Text(
                                apt["time"],
                                size=16,
                                weight=ft.FontWeight.BOLD
                            ),
                            width=80
                        ),
                        # Linha vertical
                        ft.Container(
                            bgcolor=status_color,
                            width=4,
                            height=50,
                            border_radius=2
                        ),
                        # Informações do agendamento
                        ft.Column(
                            controls=[
                                ft.Text(
                                    apt["patient"],
                                    size=16,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Text(
                                    apt["type"],
                                    size=14,
                                    color=ft.colors.SECONDARY
                                )
                            ],
                            spacing=5,
                            expand=True
                        ),
                        # Botões de ação
                        ft.Row(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.EDIT_OUTLINED,
                                    tooltip="Editar",
                                    icon_color=ft.colors.SECONDARY
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE_OUTLINE,
                                    tooltip="Excluir",
                                    icon_color=ft.colors.ERROR
                                )
                            ]
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=15,
                bgcolor=ft.colors.SURFACE,
                border_radius=8,
                margin=ft.margin.only(bottom=10)
            )
            
            appointment_cards.append(card)
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Text(
                                    "Agendamentos do Dia",
                                    size=20,
                                    weight=ft.FontWeight.BOLD
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        self.current_date.strftime("%d/%m/%Y"),
                                        size=16,
                                        color=ft.colors.SECONDARY
                                    )
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        margin=ft.margin.only(bottom=20)
                    ),
                    ft.Container(
                        content=ft.Column(
                            controls=appointment_cards,
                            scroll=ft.ScrollMode.AUTO
                        ),
                        expand=True
                    )
                ],
                expand=True
            ),
            bgcolor=ft.colors.SURFACE,
            border_radius=8,
            padding=20,
            expand=True
        )

    def new_appointment(self, e):
        # Campos do formulário
        date_picker = ft.DatePicker(
            first_date=datetime.now(),
            last_date=datetime.now() + timedelta(days=365),
            on_change=lambda e: self.update_time_slots(e.control.value)
        )
        self.page.overlay.append(date_picker)
        
        time_dd = ft.Dropdown(
            label="Horário",
            options=[],
            autofocus=True,
            width=200
        )
        
        patient_tf = ft.TextField(
            label="Paciente",
            width=400
        )
        
        type_dd = ft.Dropdown(
            label="Tipo",
            width=200,
            options=[
                ft.dropdown.Option("Consulta Regular"),
                ft.dropdown.Option("Avaliação"),
                ft.dropdown.Option("Retorno")
            ]
        )
        
        notes_tf = ft.TextField(
            label="Observações",
            multiline=True,
            min_lines=3,
            max_lines=5,
            width=400
        )
        
        def close_dlg(e):
            dlg_modal.open = False
            self.page.update()
        
        def save_appointment(e):
            if not all([date_picker.value, time_dd.value, patient_tf.value, type_dd.value]):
                self.page.show_snack_bar(ft.SnackBar(
                    content=ft.Text("Preencha todos os campos obrigatórios"),
                    bgcolor=ft.colors.ERROR
                ))
                return
            
            # TODO: Salvar agendamento no banco de dados
            appointment_date = datetime.combine(date_picker.value, datetime.strptime(time_dd.value, "%H:%M").time())
            new_appointment = {
                "date": appointment_date,
                "patient": patient_tf.value,
                "type": type_dd.value,
                "notes": notes_tf.value,
                "status": "confirmed"
            }
            
            # Atualiza a lista de agendamentos
            self.appointments.append(new_appointment)
            self.content = self.build()
            self.update()
            
            # Fecha o diálogo
            close_dlg(e)
            
            # Mostra mensagem de sucesso
            self.page.show_snack_bar(ft.SnackBar(
                content=ft.Text("Agendamento criado com sucesso!"),
                bgcolor=ft.colors.GREEN_400
            ))
        
        # Diálogo modal
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Novo Agendamento"),
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Column([
                                    ft.Text("Data"),
                                    ft.ElevatedButton(
                                        "Selecionar Data",
                                        icon=ft.icons.CALENDAR_TODAY,
                                        on_click=lambda _: date_picker.pick_date()
                                    )
                                ])
                            ),
                            time_dd
                        ],
                        alignment=ft.MainAxisAlignment.START
                    ),
                    patient_tf,
                    type_dd,
                    notes_tf
                ],
                tight=True,
                spacing=20
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Salvar", on_click=save_appointment)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        
        # Abre o diálogo
        self.page.dialog = dlg_modal
        dlg_modal.open = True
        self.page.update()
        
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
        # TODO: Atualizar lista de agendamentos para a data selecionada
        
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
