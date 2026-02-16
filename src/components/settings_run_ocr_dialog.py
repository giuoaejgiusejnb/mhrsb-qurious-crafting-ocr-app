import json
from components.load_settings_dialog_base import LoadSettingsDialogBase
from constants.paths import SETTINGS_PATH
from constants.storage_keys import OCR_SETTINGS, SKILLS_SETTINGS_NAME

class SettingsRunOCRDialog(LoadSettingsDialogBase):
    def __init__(self, on_load):
        super().__init__(on_load, is_delete_button_visible=False, needs_overwrite_confirm=False)

    def show_overwrite_confirm_dlg(self):
        self.settings_name = self.settings_selection_group.value
        self.overwrite_confirm_msg = f"{self.settings_name}を読み込みます．"
        super().show_overwrite_confirm_dlg()

    def execute_load(self):
        self.on_load(self.settings_name)

        with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
            settings = json.load(f)
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            settings[OCR_SETTINGS][SKILLS_SETTINGS_NAME] = self.settings_name
            json.dump(settings, f, indent=4, ensure_ascii=False)

        self.open = False
        
        self.page.update()