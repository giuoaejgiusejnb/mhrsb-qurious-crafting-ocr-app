import flet as ft
import json
from components.load_settings_dialog_base import LoadSettingsDialogBase
from constants.paths import SETTINGS_PATH
from constants.storage_keys import DESIRED_SKILLS_SETTINGS

class SettingsEditDialog(LoadSettingsDialogBase):
    def __init__(self, on_load):
        super().__init__(on_load)

    def show_overwrite_confirm_dlg(self):
        self.settings_name = self.settings_selection_group.value
        self.overwrite_confirm_msg = f"{self.settings_name}を読み込みます．\n現在の選択は上書きされますがよろしいですか？"
        super().show_overwrite_confirm_dlg()

    def execute_load(self):
        # JSONファイルを読み込む
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)

        # チェックボックス変更
        new_skills = set(settings_data[DESIRED_SKILLS_SETTINGS][self.settings_name])
        self.on_load(new_skills)

        # 二つのダイアログを消す
        self.overwrite_confirm_dlg.open = False
        self.open = False

        # スナックバーを表示
        snack_bar = ft.SnackBar(
            content=ft.Text(f"「{self.settings_name}」を適用しました"),
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.Margin.only(bottom=100, left=20, right=20),
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True
        
        self.page.update()