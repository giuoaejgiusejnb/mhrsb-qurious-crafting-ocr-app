import asyncio
import flet as ft
import json
import os
from functools import partial
from components.detail_dialog import DetailDialog
from components.linked_sentence import LinkedSentence
from components.settings_run_ocr_dialog import SettingsRunOCRDialog
from constants.paths import SETTINGS_PATH, TEMP_SETTINGS_PATH, TEMP_ZIP
from constants.storage_keys import DESIRED_SKILLS_SETTINGS, OCR_SETTINGS, INPUT_DIR, SKILLS_SETTINGS_NAME, OUTPUT_BASE_DIR, TOTAL_IMAGE_COUNT, SKILL_STATS
from constants.urls import DRIVE_FOLDER_URL, COLAB_URL
from services.file_service import fast_zip

# --- 画像認識ページのコンポーネント ---
@ft.component
def OCRView(on_nav):
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings = json.load(f)

    # 画像フォルダを読み込んで，そのフォルダのパス名を表示するコントロールを定義
    input_dir, set_input_dir = ft.use_state(settings[OCR_SETTINGS][INPUT_DIR])
    async def handle_get_input_dir_path(e: ft.Event[ft.Button]):
        dir = await ft.FilePicker().get_directory_path()
        set_input_dir(dir)
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            settings[OCR_SETTINGS][INPUT_DIR] = dir
            json.dump(settings, f, indent=4, ensure_ascii=False)
    select_input_btn_row = ft.Row(
        controls=[
            ft.Button(
                content="画像フォルダを選択してください",
                icon=ft.Icons.FOLDER_OPEN,
                on_click=handle_get_input_dir_path,
            ),
            ft.Text(input_dir if os.path.isdir(input_dir) else "", size=12)
        ],
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # 設定JSONファイルに保存してある設定名を選択し，その設定名を表示するコントロールを定義
    def show_load_settings_dialog(e):
        page = e.page
        dialog = SettingsRunOCRDialog(on_load=set_settings_name)
        page.overlay.append(dialog)
        dialog.open = True
        page.update()
    def show_detail_dialog(e, settings_name):
        e.page.show_dialog(DetailDialog(settings_name=settings_name))
    settings_name, set_settings_name = ft.use_state(settings[OCR_SETTINGS][SKILLS_SETTINGS_NAME])
    settings_selection_row = ft.Row(
        controls=[
            ft.Button(
                content="欲しいスキル設定を選択してください",
                icon=ft.Icons.DOWNLOAD,
                on_click=show_load_settings_dialog
            ),
            ft.Text(settings_name if settings_name in settings[DESIRED_SKILLS_SETTINGS] else "", size=12),
            ft.Button(
                "詳細を表示",
                icon=ft.Icons.INFO_OUTLINE,
                visible=(not settings_name == ""),
                # こうしないとクロージャの仕様（遅延評価）で，settings_nameがループの最後のものに固定される
                on_click=partial(show_detail_dialog, settings_name=settings_name)
            ),
        ],
        tight=True,
        alignment=ft.MainAxisAlignment.CENTER
    )

    # zipファイルを作成するボタンを定義
    is_open_drive_sentence_visible, set_is_open_drive_sentence_visible = ft.use_state(False)
    async def handle_fast_zip(e):
        set_status_str("zipファイルを作成中...")
        desired_skills_settings = settings[DESIRED_SKILLS_SETTINGS].get(settings_name, {})
        with open(TEMP_SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(desired_skills_settings, f, ensure_ascii=False)

        try:
            await asyncio.to_thread(fast_zip, input_dir, TEMP_SETTINGS_PATH, TEMP_ZIP)
        except ValueError as ex:
            e.page.show_dialog(ft.SnackBar(ft.Text(f"zipファイル作成中にエラーが発生しました: {ex}")))

        if os.path.exists(TEMP_SETTINGS_PATH):
            os.remove(TEMP_SETTINGS_PATH)
        set_status_str("")
        set_is_open_drive_sentence_visible(True)
    fast_zip_btn = ft.Button(
        "この画像フォルダを画像認識する",
        disabled=not (os.path.isdir(input_dir) and settings_name in settings[DESIRED_SKILLS_SETTINGS]),
        on_click=handle_fast_zip
    )

    # Google Driveを開いてアップロードするよう促す文とボタンを定義

    def delete_zip_file_and_show_colab_link(e):
        if os.path.isfile(TEMP_ZIP):
            asyncio.create_task(asyncio.to_thread(os.remove, TEMP_ZIP))
        set_is_open_colab_sentence_visible(True)

    open_drive_column = ft.Column(
        controls=[
            LinkedSentence([
                "Google Driveの",
                ("このフォルダ", DRIVE_FOLDER_URL),
                "を開いて",
                (f"{TEMP_ZIP}", TEMP_ZIP),
                "をアップロードしてください"
            ]),
            ft.Button("アップロードが完全に終了したら，ここをクリックしてください（zipファイルは削除します）", on_click=delete_zip_file_and_show_colab_link)
        ]
    )
    open_drive_column.visible = is_open_drive_sentence_visible

    # Colabを開いてGPUを有効にするよう促す文とボタンを定義

    def open_how_to_enable_gpu_dialog(e):
        e.page.show_dialog(ft.AlertDialog(
            title=ft.Text("GPUを有効にする方法"),
            content=ft.Column(
                controls=[
                    ft.Text("（（スマホの場合は≡を押して，）Google Colabのメニューから，ランタイム > ランタイムのタイプを変更 を選択してください"),
                    ft.Text("ハードウェアアクセラレータのところでGPUを選択して保存をクリックしてください"),
                ],
                tight=True,
            ),
            actions=[ft.TextButton("閉じる", on_click=lambda e: e.page.pop_dialog())]
        ))

    def open_how_to_run_cells_dialog(e):
        e.page.show_dialog(ft.AlertDialog(
            title=ft.Text("すべてのセルを実行する方法"),
            content=ft.Column(
                controls=[
                    ft.Text("（（スマホの場合は≡を押して，）Google Colabのメニューから，ランタイム > すべてのセルを実行 を選択してください"),
                    ft.Text("あとはしばらく待つだけです。"),
                ],
                tight=True,
            ),
            actions=[ft.TextButton("閉じる", on_click=lambda e: e.page.pop_dialog())]
        ))

    open_colab_sentence = LinkedSentence([
        ("このサイト", COLAB_URL),
        "を開いて",
        ("GPUを有効", open_how_to_enable_gpu_dialog),
        "してから",
        ("すべてのセルを実行", open_how_to_run_cells_dialog),
        "してください．",
        "10分ほど経ったら一番下のところに結果が出ます"
    ])
    is_open_colab_sentence_visible, set_is_open_colab_sentence_visible = ft.use_state(False)
    open_colab_sentence.visible = is_open_colab_sentence_visible

    # ぐるぐる（進捗表示）用のコントロールを作成

    pr = ft.ProgressRing(
        width=50,             # 幅を大きく
        height=50,            # 高さを大きく
        stroke_width=5,       # 線の太さを強調
        color=ft.Colors.BLUE  # 色の指定
    )
    status_str, set_status_str = ft.use_state("")
    status_text = ft.Text(status_str, size=20, weight=ft.FontWeight.BOLD)
    # まとめて横に並べる
    loading_view = ft.Container(
        content=ft.Column(
            [pr, status_text],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            tight=True,
        ),
        bgcolor=ft.Colors.with_opacity(0.1, ft.Colors.BLACK_12), # ほんのり背景色
        padding=40,
        border_radius=10,
        visible=(status_str != "") # status_strが空でないときに表示
    )

    content = ft.Column(
        controls=[select_input_btn_row, settings_selection_row,fast_zip_btn, open_drive_column, open_colab_sentence, loading_view],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER, # 中身を中央へ
        tight=True, # 中身を詰め合わせる
        scroll="auto" # スクロールバーを必要に応じて表示
        )
    return ft.Container(
        content=content,
        alignment=ft.Alignment.CENTER, # これで画面の真ん中にドスンと配置される
        expand=True, # 画面全体を使う
    )
