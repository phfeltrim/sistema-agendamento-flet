import flet as ft
from .agenda import AgendaView
from .pacientes import PacientesView
from .sessoes import SessoesView
from .configuracoes import ConfiguracoesView
from .dashboard import DashboardView
class MainLayout(ft.Container):
    DESKTOP_COLLAPSE_BREAKPOINT = 1000 # Largura em pixels para recolher o menu no desktop
    def __init__(self, page: ft.Page, view_name: str, on_navigate):
        super().__init__(expand=True) # Garante que o layout principal ocupe todo o espaço
        self.page = page
        self.view_name = view_name
        self.on_navigate = on_navigate
        
        self.menu_expanded = True # Estado atual do menu (expandido/recolhido)
        self._is_manual_override_active = False # Indica se o usuário clicou no botão
        self._last_auto_expanded_state = True # Último estado automático baseado na largura (assume tela larga inicialmente)
        self._current_view_instance = None  # To store the current view instance
        # Initialize controls that will be part of the layout
        self.navigation_rail_control = self._build_navigation_rail() # Store the NavigationRail instance
        self.menu_icon_button = ft.IconButton(ft.Icons.MENU, on_click=self._toggle_menu)
        self.navigation_column = ft.Column(
            [
                ft.Row(
                    [self.menu_icon_button],
                    alignment=ft.MainAxisAlignment.START if self.menu_expanded else ft.MainAxisAlignment.CENTER
                ),
                ft.Container( # This container holds the NavigationRail
                    content=self.navigation_rail_control,
                    height=700, # Altura fixa, pode precisar de ajuste ou ser dinâmica
                    expand=False
                )
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        self.navigation_container = ft.Container(
            content=self.navigation_column,
            width=250 if self.menu_expanded else 72,
            bgcolor=ft.Colors.GREY_200,
            animate=ft.Animation(300, "ease")
        )
        self.main_content_area = ft.Container(expand=True) # This will hold the actual view content

        # Define o conteúdo inicial para a área principal com base no view_name atual
        self._update_main_content_area()
        
        # Garante que o layout seja construído na inicialização
        self.content = self._build_layout_structure()
        self.page.on_resize = self._on_page_resize
        # Chama o resize para ajustar o layout se a largura da página já estiver disponível
        self._on_page_resize()

    def _on_page_resize(self, e=None):
        if self.page and self.page.width is not None: # Garante que page.width tenha um valor
            is_mobile = self.page.width <= 768 # Ponto de quebra para modo mobile (drawer)

            if is_mobile:
                # Em modo mobile, o menu lateral fixo não é exibido.
                # Conceitualmente, ele está "recolhido" e o drawer assume.
                if self.menu_expanded: # Se estava expandido antes de ir para mobile
                    self.menu_expanded = False
                self._is_manual_override_active = False # Reseta o override manual para quando voltar ao desktop
            else: # Modo desktop
                current_width_wants_expanded = self.page.width > self.DESKTOP_COLLAPSE_BREAKPOINT

                # Se o estado automático baseado na largura mudou (cruzou um breakpoint)
                if current_width_wants_expanded != self._last_auto_expanded_state:
                    self.menu_expanded = current_width_wants_expanded # Força para o estado automático
                    self._is_manual_override_active = False # Reseta o override manual
                elif not self._is_manual_override_active:
                    # Se não cruzou breakpoint e não há override manual, aplica o estado automático
                    self.menu_expanded = current_width_wants_expanded
                # Senão (não cruzou breakpoint E override manual está ativo):
                # Mantém self.menu_expanded como está (a escolha manual do usuário)

                self._last_auto_expanded_state = current_width_wants_expanded # Atualiza o último estado automático

            # Aplica o estado determinado de menu_expanded aos controles
            self.navigation_rail_control.extended = self.menu_expanded
            self.navigation_container.width = 250 if self.menu_expanded else 72
            self.navigation_column.controls[0].alignment = ft.MainAxisAlignment.START if self.menu_expanded else ft.MainAxisAlignment.CENTER

            self.content.controls = self._build_layout_structure().controls
            self.page.appbar = self.get_appbar_for_view()
            if self.page.drawer is None:
                self.page.drawer = self._build_navigation_drawer()
            self.page.update()

    def _toggle_menu(self, e):
        """Alterna entre o menu expandido e recolhido para desktop."""
        self.menu_expanded = not self.menu_expanded
        self._is_manual_override_active = True # O usuário clicou, então há um override manual
        self.navigation_rail_control.extended = self.menu_expanded
        self.navigation_container.width = 250 if self.menu_expanded else 72
        self.navigation_column.controls[0].alignment = ft.MainAxisAlignment.START if self.menu_expanded else ft.MainAxisAlignment.CENTER # Update alignment of the menu icon row
        self.update()

    def _open_drawer(self, e):
        self.page.drawer.open = True
        self.page.update() # Atualiza a página inteira para refletir o estado de abertura do drawer

    def _build_navigation_rail(self):
        nav_items = [
            (ft.Icons.DASHBOARD, "Dashboard", "dashboard"),
            (ft.Icons.CALENDAR_MONTH, "Agenda", "agenda"), 
            (ft.Icons.PEOPLE, "Pacientes", "pacientes"),
            (ft.Icons.LIST_ALT, "Sessões", "sessoes"),
            (ft.Icons.SETTINGS, "Configurações", "configuracoes"),
            (ft.Icons.LOGOUT, "Sair", "sair")
        ]
        selected_index = [i for i, (_, _, v) in enumerate(nav_items) if v == self.view_name]
        selected_index = selected_index[0] if selected_index else 0
        return ft.NavigationRail(
            selected_index=selected_index,
            label_type=ft.NavigationRailLabelType.ALL,
            extended=self.menu_expanded, # Usa o estado para definir se é expandido
            bgcolor=ft.Colors.GREY_200,
            destinations=[
                ft.NavigationRailDestination(icon=icon, label=label) for icon, label, route in nav_items
            ], # Use _handle_navigation_change
            on_change=self._handle_navigation_change # This is the correct handler for NavigationRail
        )

    def _build_navigation_drawer(self):
        """Cria o menu lateral no formato de gaveta para telas pequenas."""
        nav_items = [
            (ft.Icons.DASHBOARD, "Dashboard", "dashboard"),
            (ft.Icons.CALENDAR_MONTH, "Agenda", "agenda"),
            (ft.Icons.PEOPLE, "Pacientes", "pacientes"),
            (ft.Icons.LIST_ALT, "Sessões", "sessoes"),
            (ft.Icons.SETTINGS, "Configuracoes", "configuracoes"),
            (ft.Icons.LOGOUT, "Sair", "sair")
        ]

        # Determine o índice selecionado para o drawer com base na view_name atual
        selected_index = [i for i, (_, _, route) in enumerate(nav_items) if route == self.view_name]
        selected_index = selected_index[0] if selected_index else 0 # Padrão para o primeiro item se não encontrado

        def handle_drawer_change(e): # This is the handler for NavigationDrawer
            selected_route = nav_items[e.control.selected_index][2] # Pega a rota da tupla (ícone, label, rota)
            self.page.drawer.open = False # Close the drawer
            self.on_navigate(selected_route)
            self.page.update()

        # Return the NavigationDrawer instance
        return ft.NavigationDrawer(
            selected_index=selected_index,
            on_change=handle_drawer_change,
            controls=[ft.NavigationDrawerDestination(label=label, icon=icon) for icon, label, _ in nav_items]
        )

    def _handle_navigation_change(self, e):
        nav_items = ["dashboard", "agenda", "pacientes", "sessoes", "configuracoes", "sair"]
        idx = e.control.selected_index
        new_view_name = nav_items[idx]
        if new_view_name != self.view_name:
            self.view_name = new_view_name
            self._update_main_content_area() # Atualiza o conteúdo da área principal
            self.update()
        self.on_navigate(new_view_name)

    def _update_main_content_area(self):
        """Instantiates and sets the content of the main content area based on view_name."""
        if self.view_name == "dashboard":
            self._current_view_instance = DashboardView(self.page)
        elif self.view_name == "agenda":
            self._current_view_instance = AgendaView(self.page, self.on_navigate)
        elif self.view_name == "pacientes":
            self._current_view_instance = PacientesView(self.page)
        elif self.view_name == "sessoes":
            self._current_view_instance = SessoesView(self.page)
        elif self.view_name == "configuracoes":
            self._current_view_instance = ConfiguracoesView(self.page)
        else:
            self._current_view_instance = ft.Text("Tela não encontrada")
        self.main_content_area.content = self._current_view_instance
        # A chamada MainLayout.update() do pai já cuidará da atualização deste controle filho.

    def _build_layout_structure(self): # Renomeado de build
        # Define um ponto de quebra para o layout responsivo
        is_mobile = self.page.width is not None and self.page.width <= 768
        if is_mobile:
            return self.main_content_area
        
        # Retorna um ft.Row para desktop. Se self.content já for um ft.Row,
        # isso garante que a estrutura seja mantida.
        return ft.Row(
            controls=[self.navigation_container, self.main_content_area], 
            expand=True
        )

    def get_appbar_for_view(self):
        is_mobile = self.page.width is not None and self.page.width <= 768
        if is_mobile:
            return ft.AppBar(
                leading=ft.IconButton(ft.Icons.MENU, on_click=self._open_drawer),
                title=ft.Text(self.view_name.capitalize())
            )
        return None
