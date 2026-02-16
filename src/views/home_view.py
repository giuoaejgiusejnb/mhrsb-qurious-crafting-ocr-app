import flet as ft
from constants.routes import ROUTE_OCR, ROUTE_SKILLS_SETTINGS, SKILL_STATS, SETTINGS

# --- ホームページのコンポーネント ---
@ft.component
def HomeView(on_nav):
    async def handle_ocr_view_click(e):
        await on_nav(ROUTE_OCR)
    async def handle_skill_settings_view_click(e):
        await on_nav(ROUTE_SKILLS_SETTINGS)
    async def handle_skill_stats_view_click(e):
        await on_nav(SKILL_STATS)
    async def handle_settings_view_click(e):
        await on_nav(SETTINGS)
    button1 = ft.Button(
        "画像認識ページへ",
        on_click=handle_ocr_view_click
        )
    button2 = ft.Button(
        "スキル設定ページへ",
        on_click=handle_skill_settings_view_click
        )
    button3 = ft.Button(
        "スキル統計ページへ",
        on_click=handle_skill_stats_view_click)

    return ft.Column([
        ft.Text("選択してください", size=25, weight="bold"),
        ft.Row([
            ft.Container(button1, bgcolor="blue200", padding=20, expand=True),
            ft.Container(button2, bgcolor="green200", padding=20, expand=True),
            ft.Container(button3, bgcolor="green200", padding=20, expand=True),
        ]),
        ft.FloatingActionButton(icon=ft.Icons.SETTINGS, on_click=handle_settings_view_click)
    ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)