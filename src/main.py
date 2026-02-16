import warnings
# 特定の DeprecationWarning を無視する設定
warnings.filterwarnings("ignore", category=DeprecationWarning, module="torch.utils.data._utils.pin_memory")

import flet as ft
import json
from constants.paths import SETTINGS_PATH
from constants.storage_keys import UI_THEME
from multiprocessing import freeze_support
from views.router import App
# --- main ---
async def main(page: ft.Page):
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings_data = json.load(f)
    page.theme_mode = ft.ThemeMode(settings_data[UI_THEME])
    page.on_route_change = lambda _: page.render(lambda: App(page))
    page.render(lambda: App(page))

# 実行
if __name__ == "__main__":
    freeze_support()
    ft.run(main, assets_dir="../assets")