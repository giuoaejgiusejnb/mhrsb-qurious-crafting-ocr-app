from constants.skills import SKILL_MASTER_LIST
from services.file_service import get_real_desktop_path
# アプリ名に基づいた一意のID
APP_ID = "jp.qurious_crafting_ocr"

# 各種設定のキー
DESIRED_SKILLS_SETTINGS = "desired_skills_settings"
OCR_SETTINGS = "ocr_settings"
UI_THEME = "theme_mode"
SKILL_STATS = "skill_stats"
INPUT_DIR = "input_dir"
SKILLS_SETTINGS_NAME = "skills_settings_name"
OUTPUT_BASE_DIR = "output_base_dir"
TOTAL_IMAGE_COUNT = "total_image_count"

# 初期値
DEFAULTS = {
    DESIRED_SKILLS_SETTINGS: {},
    OCR_SETTINGS: {
        INPUT_DIR: "",
        SKILLS_SETTINGS_NAME: "",
        OUTPUT_BASE_DIR: get_real_desktop_path()
    },
    UI_THEME: "system",
    SKILL_STATS: dict.fromkeys(SKILL_MASTER_LIST, 0),
    TOTAL_IMAGE_COUNT: 0
}
