import os
from pathlib import Path
import zipfile
import shutil
import tempfile
from constants.paths import TEMP_SETTINGS_PATH, TEMP_ZIP

# デスクトップの実際のパスを取得する関数
def get_real_desktop_path():
    home = Path.home()
    
    # チェックする候補のリスト
    # Windowsの言語設定やOneDriveの使用状況に応じて変わる可能性があるパス
    candidates = [
        home / "Desktop",              # 通常のパス
        home / "OneDrive" / "Desktop",  # OneDrive同期中のパス
        home / "OneDrive" / "デスクトップ", # 日本語環境のOneDrive
    ]
    
    for path in candidates:
        # os.path.exists を使ってディレクトリが存在するかチェック
        if os.path.exists(path):
            return str(path)  # 文字列で返す
            
    # 見つからない場合のフォールバック（デフォルト値を返す）
    return ""

# 指定されたディレクトリを高速でzipファイルにする関数
def fast_zip(source_dir, source_file, output_zip):
    if not os.path.isdir(source_dir):
        raise ValueError(f"指定されたパス '{source_dir}' は有効なディレクトリではありません。")
    if not os.path.isfile(source_file):
        raise ValueError(f"指定されたパス '{source_file}' は有効なファイルではありません。")
    with tempfile.TemporaryDirectory() as dname:
            shutil.copytree(source_dir, dname, dirs_exist_ok=True)
            shutil.copy(source_file, os.path.join(dname, os.path.basename(source_file)))
            with zipfile.ZipFile(output_zip, 'w', compression=zipfile.ZIP_STORED) as z:
                for root, dirs, files in os.walk(dname):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, dname)
                        z.write(file_path, arcname)