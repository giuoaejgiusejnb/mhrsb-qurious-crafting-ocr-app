import os

# srcフォルダのパス
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMP_SETTINGS_PATH = os.path.join(BASE_DIR, "storage", "temp_settings.json")

# 画像認識する際の一時的なzipファイルの名前
TEMP_ZIP = os.path.join(BASE_DIR, "storage", "mhrsb_temp.zip")

# すべてのスキルが書かれたJSONファイルへのパス
ALL_SKILLS_DATA_PATH  = os.path.join(BASE_DIR, "assets", "all_skills.json")

# ユーザー設定が書かれたJSONファイルへのパス
SETTINGS_PATH = os.path.join(BASE_DIR, "storage", "settings.json")
