import flet as ft
from ..controllers.pacientes_controller import PacientesController

class PacientesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.controller = PacientesController()
        self.content = self.build()

    def build(self):
        # Campo de busca e botões
        self.search_field = ft.TextField(label="Buscar", hint_text="Nome, CPF ou Telefone", width=300)
        self.search_btn = ft.ElevatedButton(text="Buscar", on_click=self.search_patients)
        self.new_btn = ft.ElevatedButton(text="Novo Paciente", icon=ft.Icons.ADD, on_click=self.new_patient)
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Pacientes", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.search_field,
                        self.search_btn,
                        self.new_btn
                    ], alignment=ft.MainAxisAlignment.START, spacing=10),
                    self.build_patients_list()
                ],
                spacing=20
            ),
            padding=20
        )

    def build_patients_list(self):
        pacientes = self.controller.listar()
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(p.id))),
                    ft.DataCell(ft.Text(p.name)),
                    ft.DataCell(ft.Text(p.telefone)),
                    ft.DataCell(ft.Text(p.cpf)),
                    ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda _, pid=p.id: self.edit_patient(pid)))
                ]
            ) for p in pacientes
        ]
        return ft.Container(
            padding=10,
            content=ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nome")),
                    ft.DataColumn(ft.Text("Telefone")),
                    ft.DataColumn(ft.Text("CPF")),
                    ft.DataColumn(ft.Text("Editar"))
                ],
                rows=rows
            )
        )

    def search_patients(self, e):
        # Exemplo: filtrar pacientes pelo nome, cpf ou telefone
        termo = self.search_field.value.strip().lower()
        if not termo:
            self.content = self.build()
            self.update()
            return
        pacientes = [p for p in self.controller.listar() if termo in p.name.lower() or termo in p.cpf.lower() or termo in p.telefone.lower()]
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Pacientes", style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.BOLD),
                    ft.Row([
                        self.search_field,
                        self.search_btn,
                        self.new_btn
                    ], alignment=ft.MainAxisAlignment.START, spacing=10),
                    ft.Container(
                        padding=10,
                        content=ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("ID")),
                                ft.DataColumn(ft.Text("Nome")),
                                ft.DataColumn(ft.Text("Telefone")),
                                ft.DataColumn(ft.Text("CPF")),
                                ft.DataColumn(ft.Text("Editar"))
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(str(p.id))),
                                        ft.DataCell(ft.Text(p.name)),
                                        ft.DataCell(ft.Text(p.telefone)),
                                        ft.DataCell(ft.Text(p.cpf)),
                                        ft.DataCell(ft.IconButton(icon=ft.Icons.EDIT, tooltip="Editar", on_click=lambda _, pid=p.id: self.edit_patient(pid)))
                                    ]
                                ) for p in pacientes
                            ]
                        )
                    )
                ],
                spacing=20
            ),
            padding=20
        )
        self.update()

    def edit_patient(self, paciente_id):
        # Busca paciente pelo id
        paciente = next((p for p in self.controller.listar() if p.id == paciente_id), None)
        if not paciente:
            return
        name_tf = ft.TextField(label="Nome", value=paciente.name, width=300)
        cpf_tf = ft.TextField(label="CPF", value=paciente.cpf, width=200)
        telefone_tf = ft.TextField(label="Telefone", value=paciente.telefone, width=150)
        cep_tf = ft.TextField(label="CEP", value=paciente.cep, width=150)
        number_tf = ft.TextField(label="Número", value=paciente.number, width=100)
        complement_tf = ft.TextField(label="Complemento", value=paciente.complement, width=150)
        email_tf = ft.TextField(label="Email", value=paciente.email, width=220)
        ativo_switch = ft.Switch(label="Ativo", value=getattr(paciente, 'status', True))
        erro_txt = ft.Text("", color=ft.Colors.RED, visible=False)

        def fechar(_):
            dlg.open = False
            self.page.dialog = None
            self.page.update()

        def salvar(_):
            name = name_tf.value.strip()
            cpf = cpf_tf.value.strip()
            telefone = telefone_tf.value.strip()
            cep = cep_tf.value.strip()
            number = number_tf.value.strip()
            complement = complement_tf.value.strip()
            email = email_tf.value.strip()
            status = ativo_switch.value
            if not name or not email:
                erro_txt.value = "Nome e Email são obrigatórios."
                erro_txt.visible = True
                self.page.update()
                return
            self.controller.editar(
                paciente_id,
                name=name,
                cpf=cpf,
                telefone=telefone,
                cep=cep,
                number=number,
                complement=complement,
                email=email,
                status=status
            )
            fechar(_)
            self.content = self.build()
            self.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Paciente"),
            content=ft.Column([
                name_tf,
                cpf_tf,
                telefone_tf,
                cep_tf,
                number_tf,
                complement_tf,
                email_tf,
                ativo_switch,
                erro_txt
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=fechar),
                ft.TextButton("Salvar", on_click=salvar)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()

    def new_patient(self, e):

        try:
            name_tf = ft.TextField(label="Nome", width=300)
            cpf_tf = ft.TextField(label="CPF", width=200)
            telefone_tf = ft.TextField(label="Telefone", width=150)
            cep_tf = ft.TextField(label="CEP", width=150)
            number_tf = ft.TextField(label="Número", width=100)
            complement_tf = ft.TextField(label="Complemento", width=150)
            email_tf = ft.TextField(label="Email", width=220)
            erro_txt = ft.Text("", color=ft.Colors.RED, visible=False)

            def fechar(_):
                dlg.open = False
                self.page.dialog = None
                self.page.update()

            def salvar(_):
                name = name_tf.value.strip()
                cpf = cpf_tf.value.strip()
                telefone = telefone_tf.value.strip()
                cep = cep_tf.value.strip()
                number = number_tf.value.strip()
                complement = complement_tf.value.strip()
                email = email_tf.value.strip()
                if not name or not email:
                    erro_txt.value = "Nome e Email são obrigatórios."
                    erro_txt.visible = True
                    self.page.update()
                    return
                # status=1, user=1 (admin)
                self.controller.adicionar(name, cpf, telefone, cep, number, complement, email, 1, 1)
                fechar(_)
                self.content = self.build()  # Atualiza a lista
                self.update()

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Novo Paciente"),
                content=ft.Column([
                    name_tf,
                    cpf_tf,
                    telefone_tf,
                    cep_tf,
                    number_tf,
                    complement_tf,
                    email_tf,
                    erro_txt
                ], spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=fechar),
                    ft.TextButton("Salvar", on_click=salvar)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            self.page.overlay.append(dlg)
            dlg.open = True
            self.page.update()
        except Exception as ex:
            erro_dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Erro ao abrir cadastro"),
                content=ft.Text("Erro: " + str(ex)),
                actions=[ft.TextButton("Fechar", on_click=lambda _: self.page.dialog.close())],
                open=True
            )
            self.page.dialog = erro_dlg
            self.page.update()
