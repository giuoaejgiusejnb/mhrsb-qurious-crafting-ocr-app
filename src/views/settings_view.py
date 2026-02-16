import copy
import flet as ft
import json
from functools import partial
from constants.paths import SETTINGS_PATH
from constants.storage_keys import DEFAULTS, UI_THEME, SKILL_STATS, TOTAL_IMAGE_COUNT

# --- 設定ページのコンポーネント ---
@ft.component
def SettingsView(on_nav):
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings_data = json.load(f)

    def theme_changed(e):
        nonlocal settings_data
        e.page.theme_mode = ft.ThemeMode(e.control.value)
        settings_data[UI_THEME] = e.control.value
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=4, ensure_ascii=False)

    def initialize_settings(e):
        nonlocal settings_data
        new_settings = copy.deepcopy(DEFAULTS)
        for key in [SKILL_STATS, TOTAL_IMAGE_COUNT]:
            if key in settings_data:
                new_settings[key] = settings_data[key]
        settings_data = new_settings
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=4, ensure_ascii=False)
        e.page.theme_mode = ft.ThemeMode(settings_data[UI_THEME])
        e.page.pop_dialog()

    def initialize_skill_stats(e):
        nonlocal settings_data
        for key in [SKILL_STATS, TOTAL_IMAGE_COUNT]:
            if key in settings_data:
                settings_data[key] = DEFAULTS[key]
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=4, ensure_ascii=False)
        e.page.pop_dialog()

    def show_confirm_dialog(e, to_remove):
        match to_remove:
            case "settings":
                msg = "設定をすべて初期化しますか？"
                initialize = initialize_settings
            case "skill_stats":
                msg = "スキル統計を初期化しますか？"
                initialize = initialize_skill_stats

        e.page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("確認"),
            content=ft.Text(msg),
            actions=[
                ft.TextButton("キャンセル", on_click=e.page.pop_dialog),
                ft.TextButton("初期化する",on_click=initialize)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    theme_dropdown = ft.Dropdown(
        label="表示モード",
        on_select=theme_changed,
        options=[
            ft.DropdownOption("system", "システム設定に従う"),
            ft.DropdownOption("light", "ライトモード"),
            ft.DropdownOption("dark", "ダークモード"),
        ],
        value=settings_data[UI_THEME],
    )

    return ft.ListView([
        ft.Text("準備中", size=100),
        ft.ListTile(leading=ft.Icon(ft.Icons.PERSON), title=ft.Text("プロフィール設定")),
        ft.ListTile(leading=ft.Icon(ft.Icons.NOTIFICATIONS), title=ft.Text("通知設定")),
        theme_dropdown,
        ft.ListTile(
            leading=ft.Icon(ft.Icons.RESTART_ALT, color=ft.Colors.ORANGE_700),
            title=ft.Row([
                ft.Text("設定の初期化"),
                ft.Container(
                    content=ft.FilledButton("リセット", on_click=partial(show_confirm_dialog, to_remove="settings")),
                    padding=ft.Padding.only(left=20) # テキストとの距離を調整
                ),
            ])
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.RESTART_ALT, color=ft.Colors.ORANGE_700),
            title=ft.Row([
                ft.Text("スキル統計の初期化"),
                ft.Container(
                    content=ft.FilledButton("リセット", on_click=partial(show_confirm_dialog, to_remove="skill_stats")),
                    padding=ft.Padding.only(left=20) # テキストとの距離を調整
                ),
            ])
        )
    ], expand=True)