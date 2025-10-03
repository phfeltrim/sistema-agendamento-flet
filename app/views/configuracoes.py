import flet as ft
from ..controllers.auth_controller import AuthController
from ..controllers.configuracoes_controller import ConfiguracoesController

class ConfiguracoesView(ft.Container):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        # Instancia os controllers uma única vez
        self.auth_controller = AuthController()
        self.config_controller = ConfiguracoesController()

        # Define os campos de texto como atributos da classe
        self.valor_sessao_tf = ft.TextField(
            label="Valor Padrão da Sessão (ex: 150.00)", 
            prefix_text="R$",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        self.custo_fixo_tf = ft.TextField(
            label="Custo Fixo Mensal (ex: 2500.00)", 
            prefix_text="R$",
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.content = self.build()

    def did_mount(self):
        """
        Chamado pelo Flet após a tela ser montada.
        Carrega as configurações salvas do banco de dados.
        """
        print("ConfiguracoesView montada. Carregando configurações...")
        self.valor_sessao_tf.value = self.config_controller.get_config("valor_sessao") or ""
        self.custo_fixo_tf.value = self.config_controller.get_config("custo_fixo_mensal") or ""
        self.update()

    def save_financial_settings(self, e):
        """Salva as configurações financeiras no banco de dados."""
        try:
            # Pega os valores dos campos e salva usando o controller
            self.config_controller.set_config("valor_sessao", self.valor_sessao_tf.value)
            self.config_controller.set_config("custo_fixo_mensal", self.custo_fixo_tf.value)
            
            # Mostra uma mensagem de sucesso
            self.page.snack_bar = ft.SnackBar(content=ft.Text("Configurações financeiras salvas!"), bgcolor=ft.Colors.GREEN)
            self.page.snack_bar.open = True
            self.page.update()
        except Exception as ex:
            print(f"Erro ao salvar configurações: {ex}")

    # --- Seções da Interface (UI) ---

    def build_financial_settings(self):
        """Cria a seção de configurações financeiras."""
        return ft.Column(
            controls=[
                ft.Text("Financeiro", style=ft.TextThemeStyle.TITLE_LARGE),
                self.valor_sessao_tf,
                self.custo_fixo_tf,
                ft.ElevatedButton(
                    "Salvar Configurações Financeiras", 
                    on_click=self.save_financial_settings,
                    icon=ft.Icons.SAVE
                )
            ]
        )   

    # --- MÉTODOS DE ACESSIBILIDADE ---
    
    def alternar_alto_contraste(self, e):
        tema_normal = self.page.client_storage.get("tema_normal")
        tema_alto_contraste = self.page.client_storage.get("tema_alto_contraste")

        if e.control.value:
            self.page.theme = self.page.tema_alto_contraste
        else:
            self.page.theme = self.page.tema_normal
        self.page.update()

    def aumentar_fonte(self, e):
        if self.page.theme and self.page.theme.text_theme:
            if self.page.theme.text_theme.body_medium.size < 22: # Limite de tamanho
                self.page.theme.text_theme.body_medium.size += 1
                self.page.theme.text_theme.title_large.size += 1
                self.page.update()

    def diminuir_fonte(self, e):
        if self.page.theme and self.page.theme.text_theme:
            if self.page.theme.text_theme.body_medium.size > 10: # Limite de tamanho
                self.page.theme.text_theme.body_medium.size -= 1
                self.page.theme.text_theme.title_large.size -= 1
                self.page.update()
            
    # --- MÉTODOS DE CONSTRUÇÃO DA UI ---

    def build_accessibility_settings(self):
        """Cria a seção de configurações de acessibilidade."""
        return ft.Column(
            controls=[
                # Usa o estilo de título do tema
                ft.Text("Acessibilidade", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Row(
                    controls=[
                        # Usa o estilo de corpo de texto do tema
                        ft.Text("Modo de Alto Contraste", style=ft.TextThemeStyle.BODY_MEDIUM),
                        ft.Switch(on_change=self.alternar_alto_contraste, tooltip="Ativar ou desativar o modo de alto contraste")
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Row(
                    controls=[
                        # Usa o estilo de corpo de texto do tema
                        ft.Text("Tamanho da Fonte", style=ft.TextThemeStyle.BODY_MEDIUM),
                        ft.Row([
                           ft.IconButton(ft.Icons.REMOVE, on_click=self.diminuir_fonte, tooltip="Diminuir o tamanho da fonte"),
                           ft.IconButton(ft.Icons.ADD, on_click=self.aumentar_fonte, tooltip="Aumentar o tamanho da fonte"),
                        ])
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
            ]
        )
    
    def build_user_management(self):
        """Cria a seção de gerenciamento de usuários."""
        return ft.Column(
            controls=[
                # Usa o estilo de título do tema
                ft.Text("Usuários do Sistema", style=ft.TextThemeStyle.TITLE_LARGE),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            text="Novo Usuário",
                            icon=ft.Icons.PERSON_ADD,
                            on_click=self.abrir_modal_novo_usuario,
                            tooltip="Criar um novo usuário no sistema"
                        ),
                        ft.ElevatedButton(
                            text="Listar Usuários",
                            icon=ft.Icons.LIST,
                            on_click=self.abrir_modal_lista_usuarios,
                            tooltip="Ver e gerenciar usuários existentes"
                        )
                    ],
                    spacing=10
                )
            ]
        )

    def build(self):
        """Constrói o layout principal da página de configurações."""
        return ft.Container(
            padding=ft.padding.all(30),
            content=ft.Column(
                controls=[
                    ft.Text("Configurações", style=ft.TextThemeStyle.HEADLINE_LARGE),
                    ft.Divider(height=20),
                    self.build_accessibility_settings(),
                    ft.Divider(height=20),
                    self.build_financial_settings(), # <--- Adiciona o novo formulário
                    ft.Divider(height=20),
                    self.build_user_management(),
                ],
                spacing=25,
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True
            )
        )

    # --- MÉTODOS PARA MODAIS E AÇÕES (Lógica original integrada e refatorada) ---

    def fechar_modal(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    def abrir_modal_novo_usuario(self, e):
        nome_tf = ft.TextField(label="Nome", autofocus=True)
        email_tf = ft.TextField(label="Email")
        senha_tf = ft.TextField(label="Senha", password=True, can_reveal_password=True)
        confirmar_senha_tf = ft.TextField(label="Confirmar Senha", password=True, can_reveal_password=True)
        
        def salvar(e):
            if not nome_tf.value or not email_tf.value or not senha_tf.value:
                # Lógica de validação...
                return
            if senha_tf.value != confirmar_senha_tf.value:
                # Lógica de validação...
                return
            try:
                # Usa a instância única do controller
                self.auth_controller.criar_usuario(nome_tf.value, email_tf.value, senha_tf.value)
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Usuário criado com sucesso!"), bgcolor=ft.Colors.GREEN_700)
                self.page.snack_bar.open = True
                self.fechar_modal()
            except Exception as ex:
                self.page.snack_bar = ft.SnackBar(content=ft.Text(f"Erro ao criar usuário: {ex}"), bgcolor=ft.Colors.ERROR)
                self.page.snack_bar.open = True
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Novo Usuário"),
            content=ft.Column([nome_tf, email_tf, senha_tf, confirmar_senha_tf]),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton("Salvar", on_click=salvar),
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def abrir_modal_lista_usuarios(self, e):
        try:
            # Usa a instância única do controller
            usuarios = self.auth_controller.listar_usuarios()
            
            usuarios_controls = []
            if not usuarios:
                usuarios_controls.append(ft.Text("Nenhum usuário cadastrado."))
            else:
                for u in usuarios:
                    usuarios_controls.append(
                        ft.Row([
                            ft.Text(u['nome'], width=180),
                            ft.Text(u['email'], width=220),
                            ft.IconButton(ft.Icons.DELETE, tooltip="Excluir Usuário", on_click=lambda e, user_id=u['id']: self.confirmar_exclusao(user_id)),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    )
        except Exception as ex:
            usuarios_controls = [ft.Text(f"Erro ao carregar usuários: {ex}", color=ft.Colors.ERROR)]

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Usuários Cadastrados"),
            content=ft.Column(usuarios_controls, scroll=ft.ScrollMode.ALWAYS, width=600, height=400),
            actions=[ft.TextButton("Fechar", on_click=self.fechar_modal)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def confirmar_exclusao(self, usuario_id):
        # Fecha o modal da lista primeiro
        self.fechar_modal()

        def deletar_confirmado(e):
            # Lógica de exclusão movida para o AuthController
            if self.auth_controller.excluir_usuario(usuario_id):
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Usuário excluído com sucesso!"), bgcolor=ft.Colors.GREEN_700)
            else:
                self.page.snack_bar = ft.SnackBar(content=ft.Text("Erro ao excluir usuário."), bgcolor=ft.Colors.ERROR)
            
            self.page.snack_bar.open = True
            self.fechar_modal() # Fecha o modal de confirmação
            self.page.update()

        dlg_confirm = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Exclusão"),
            content=ft.Text("Você tem certeza que deseja excluir este usuário? Esta ação não pode ser desfeita."),
            actions=[
                ft.TextButton("Cancelar", on_click=self.fechar_modal),
                ft.ElevatedButton("Excluir", on_click=deletar_confirmado, color=ft.colors.WHITE, bgcolor=ft.colors.RED),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg_confirm
        dlg_confirm.open = True
        self.page.update()