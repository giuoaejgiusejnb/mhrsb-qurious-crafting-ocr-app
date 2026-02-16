import flet as ft
from views.home_view import HomeView
from views.ocr_view import OCRView
from views.skill_settings_view import SkillSettingsView
from views.not_found_view import NotFoundView
from views.skill_stats_view import SkillStatsView
from views.settings_view import SettingsView
from constants.routes import HOME, ROUTE_OCR, ROUTE_SKILLS_SETTINGS, SKILL_STATS, SETTINGS

# --- メインのレンダラー ---
def App(page: ft.Page):
    # ルート定義
    router = {
        HOME: {
            "view": lambda: HomeView(on_nav=page.push_route),
            "title": "ホーム"
        },
        ROUTE_OCR: {
            "view": lambda: OCRView(on_nav=page.push_route),
            "title": "OCR画像認識"
        },
        ROUTE_SKILLS_SETTINGS: {
            "view": lambda: SkillSettingsView(on_nav=page.push_route),
            "title": "欲しいスキル設定"
        },
        SKILL_STATS: {
            "view": lambda: SkillStatsView(on_nav=page.push_route),
            "title": "スキル統計"
        },
        SETTINGS: {
            "view": lambda: SettingsView(on_nav=page.push_route),
            "title": "設定"
        }
    }

    # 辞書に page.route がなければ、404用の情報を取得する
    route_info = router.get(page.route, {
        "view": lambda: NotFoundView(on_nav=page.push_route),
        "title": "404 Not Found"
    })

    # タイトル更新
    page.title = route_info["title"]

    async def handle_back_click(e):
        await page.push_route(HOME)

    # --- 戻るボタンの制御 ---
    # ホーム以外なら「戻るアイコンボタン」を表示する
    back_button = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=handle_back_click, # ホームへ戻る
        tooltip="ホームに戻る"
    ) if page.route != HOME else None

    return ft.Column([
        # 上部にナビゲーションエリアを作成
        ft.Row([
            back_button if back_button else ft.Container(), # ボタンがなければ空
            ft.Text(page.title, size=20, weight="bold"),
        ], alignment=ft.MainAxisAlignment.START),
        
        # メインコンテンツ
        ft.Container(content=route_info["view"](), expand=True)
    ], expand=True)
