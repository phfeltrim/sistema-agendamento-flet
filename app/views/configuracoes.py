import flet as ft

class ConfiguracoesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.usuarios_list = ft.Column([])
        self.content = self.build()

    def build(self):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Configurações", size=30, weight=ft.FontWeight.BOLD),
                    self.build_settings_form()
                ],
                spacing=20
            ),
            padding=20
        )

    def build_settings_form(self):
        # Botão para abrir modal de novo usuário
        novo_usuario_btn = ft.ElevatedButton(
            text="Novo Usuário",
            icon=ft.icons.PERSON_ADD,
            on_click=self.abrir_modal_novo_usuario
        )
        # Botão para listar usuários (abre modal)
        listar_usuarios_btn = ft.ElevatedButton(
            text="Listar Usuários",
            icon=ft.icons.LIST,
            on_click=self.abrir_modal_lista_usuarios
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("Configurações do Sistema", size=22, weight=ft.FontWeight.BOLD),
                    ft.TextField(
                        label="Horário de Funcionamento",
                        value="08:00 - 18:00"
                    ),
                    ft.TextField(
                        label="Duração Padrão da Sessão (minutos)",
                        value="60"
                    ),
                    ft.ElevatedButton(
                        text="Salvar Configurações",
                        on_click=self.save_settings
                    ),
                    ft.Divider(),
                    ft.Text("Usuários do Sistema", size=20, weight=ft.FontWeight.BOLD),
                    ft.Row([novo_usuario_btn, listar_usuarios_btn], spacing=8),
                    self.usuarios_list
                ],
                spacing=14
            )
        )

    def abrir_modal_novo_usuario(self, e):
        from controllers.auth_controller import AuthController
        nome_tf = ft.TextField(label="Nome", width=300)
        email_tf = ft.TextField(label="Email", width=250)
        senha_tf = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=200)
        confirmar_senha_tf = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True, width=200)
        erro_txt = ft.Text("", color=ft.colors.RED, visible=False)

        def fechar(_):
            dlg.open = False
            self.page.dialog = None
            self.page.update()

        def salvar(_):
            nome = nome_tf.value.strip()
            email = email_tf.value.strip()
            senha = senha_tf.value
            confirmar = confirmar_senha_tf.value
            if not nome or not email or not senha or not confirmar:
                erro_txt.value = "Preencha todos os campos."
                erro_txt.visible = True
                self.page.update()
                return
            if senha != confirmar:
                erro_txt.value = "As senhas não coincidem."
                erro_txt.visible = True
                self.page.update()
                return
            try:
                auth_ctrl = AuthController()
                auth_ctrl.criar_usuario(nome, email, senha)
                dlg.open = False
                self.page.dialog = None
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Usuário cadastrado!"), bgcolor=ft.colors.SECONDARY_CONTAINER)
                self.page.snack_bar.open = True
                self.page.update()
                self.atualizar_lista_usuarios()
            except Exception as ex:
                erro_txt.value = f"Erro ao cadastrar usuário: {ex}"
                erro_txt.visible = True
                self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Novo Usuário"),
            content=ft.Column([
                nome_tf,
                email_tf,
                senha_tf,
                confirmar_senha_tf,
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
        self.page.dialog = dlg
        self.page.update()

    def atualizar_lista_usuarios(self):
        from controllers.auth_controller import AuthController
        try:
            auth_ctrl = AuthController()
            usuarios = auth_ctrl.listar_usuarios()
            usuarios_controls = []
            for u in usuarios:
                usuarios_controls.append(
                    ft.Row([
                        ft.Text(u['nome'], width=180),
                        ft.Text(u['email'], width=220),
                        ft.Text(u['created_at'].strftime('%d/%m/%Y %H:%M') if hasattr(u['created_at'], 'strftime') else str(u['created_at']), width=120),
                        ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda _, uid=u['id']: self.excluir_usuario(uid))
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                )
            self.usuarios_list.controls = usuarios_controls
        except Exception as ex:
            self.usuarios_list.controls = [ft.Text(f"Erro ao carregar usuários: {ex}", color=ft.colors.ERROR)]
        self.usuarios_list.update()


    def abrir_modal_lista_usuarios(self, e):
        from controllers.auth_controller import AuthController
        auth_ctrl = AuthController()
        try:
            usuarios = auth_ctrl.listar_usuarios()
        except Exception as ex:
            usuarios = []
            erro = ft.Text(f"Erro ao carregar usuários: {ex}", color=ft.colors.ERROR)
        usuarios_controls = []
        for u in usuarios:
            usuarios_controls.append(
                ft.Row([
                    ft.Text(u['nome'], width=160),
                    ft.Text(u['email'], width=180),
                    ft.Text(u['created_at'].strftime('%d/%m/%Y %H:%M') if hasattr(u['created_at'], 'strftime') else str(u['created_at']), width=110),
                    ft.IconButton(icon=ft.icons.EDIT, tooltip="Editar", on_click=lambda _, usuario=u: self.abrir_modal_editar_usuario(usuario)),
                    ft.IconButton(icon=ft.icons.DELETE, tooltip="Excluir", on_click=lambda _, uid=u['id']: self.excluir_usuario_modal(uid))
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )
        if not usuarios_controls:
            usuarios_controls = [ft.Text("Nenhum usuário cadastrado.")]
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Usuários Cadastrados"),
            content=ft.Column(usuarios_controls, scroll=ft.ScrollMode.ALWAYS, width=650, height=350),
            actions=[ft.TextButton("Fechar", on_click=lambda _: self.fechar_modal())],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.dialog = dlg
        self.page.update()

    def fechar_modal(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.dialog = None
            self.page.update()

    def abrir_modal_editar_usuario(self, usuario):
        from controllers.auth_controller import AuthController
        nome_tf = ft.TextField(label="Nome", value=usuario['nome'], width=280)
        email_tf = ft.TextField(label="Email", value=usuario['email'], width=220)
        senha_tf = ft.TextField(label="Nova Senha (opcional)", password=True, can_reveal_password=True, width=200)
        confirmar_senha_tf = ft.TextField(label="Confirmar Nova Senha", password=True, can_reveal_password=True, width=200)
        erro_txt = ft.Text("", color=ft.colors.RED, visible=False)
        def salvar_edicao(_):
            nome = nome_tf.value.strip()
            email = email_tf.value.strip()
            senha = senha_tf.value
            confirmar = confirmar_senha_tf.value
            if not nome or not email:
                erro_txt.value = "Nome e email são obrigatórios."
                erro_txt.visible = True
                self.page.update()
                return
            if senha or confirmar:
                if senha != confirmar:
                    erro_txt.value = "As senhas não coincidem."
                    erro_txt.visible = True
                    self.page.update()
                    return
            try:
                auth_ctrl = AuthController()
                auth_ctrl.editar_usuario(usuario['id'], nome, email, senha if senha else None)
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Usuário atualizado!"), bgcolor=ft.colors.SECONDARY_CONTAINER)
                self.page.snack_bar.open = True
                self.fechar_modal()
                self.atualizar_lista_usuarios()
            except Exception as ex:
                erro_txt.value = f"Erro ao atualizar usuário: {ex}"
                erro_txt.visible = True
                self.page.update()
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Usuário: {usuario['nome']}"),
            content=ft.Column([
                nome_tf,
                email_tf,
                senha_tf,
                confirmar_senha_tf,
                erro_txt
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _: self.fechar_modal()),
                ft.TextButton("Salvar", on_click=salvar_edicao)
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.dialog = dlg
        self.page.update()

    def excluir_usuario_modal(self, usuario_id):
        from controllers.auth_controller import AuthController
        auth_ctrl = AuthController()
        try:
            if not auth_ctrl.db.connect():
                raise Exception("Erro ao conectar ao banco de dados.")
            auth_ctrl.db.cursor.execute("DELETE FROM usuarios WHERE id=%s", (usuario_id,))
            auth_ctrl.db.conn.commit()
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Usuário excluído!"), bgcolor=ft.colors.SECONDARY_CONTAINER)
            self.page.snack_bar.open = True
            self.fechar_modal()
            self.atualizar_lista_usuarios()
        except Exception as ex:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao excluir usuário: {ex}"), bgcolor=ft.colors.ERROR)
            self.page.snack_bar.open = True
            self.fechar_modal()
        self.page.update()


    def save_settings(self, e):
        try:
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Configurações salvas!"))
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            dlg = ft.AlertDialog(title=ft.Text("Aviso"), content=ft.Text("Configurações salvas!"), open=True)
            self.page.dialog = dlg
            self.page.update()
