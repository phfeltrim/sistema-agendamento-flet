import flet as ft

# Tema Padrão
tema_normal = ft.Theme(
    color_scheme_seed="#6E62E5", 
    use_material3=True,
    font_family="Poppins"
)
tema_normal.text_theme = ft.TextTheme(
    body_medium=ft.TextStyle(size=14, color="#6E62E5"),
    title_large=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, color="#6E62E5"),
)

# Tema de Alto Contraste (com a correção)
tema_alto_contraste = ft.Theme(
    color_scheme=ft.ColorScheme(
        background=ft.Colors.BLACK,
        surface=ft.Colors.WHITE,
        on_background=ft.Colors.WHITE,
        on_surface=ft.Colors.BLACK,
        primary=ft.Colors.BLACK,
        on_primary=ft.Colors.WHITE,
        secondary=ft.Colors.BLUE_GREY_800,
        on_secondary=ft.Colors.WHITE,
    ),
    use_material3=True,
    font_family="Poppins"
)
tema_alto_contraste.text_theme = ft.TextTheme(
    body_medium=ft.TextStyle(size=14, color=ft.Colors.BLACK),
    title_large=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
)