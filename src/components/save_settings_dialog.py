import flet as ft
import json
from constants.paths import SETTINGS_PATH
from constants.storage_keys import DESIRED_SKILLS_SETTINGS

class SaveSettingsDialog(ft.AlertDialog):
    def __init__(self, checkbox_refs):
        super().__init__()

        self.title = ft.Text("欲しいスキル設定保存")

        # 設定のデフォルトの名前を設定1にする
        default_settings_id = 1
        # 設定1がすでに存在するなら，存在しなくなるまで末尾の数字を足していく
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)
        settings_name = f"設定{default_settings_id}"
        while settings_name in settings_data[DESIRED_SKILLS_SETTINGS].keys():
            default_settings_id += 1
            settings_name = f"設定{default_settings_id}"

        # テキストボックスをプロパティとして保持（後で値を取り出すため）
        self.name_input = ft.TextField(
            label="設定の名前",
            value=f"設定{str(default_settings_id)}",
            autofocus=True # ダイアログが開いた時にすぐ入力できる
        )
        
        self.content = ft.Column([
            ft.Text("設定名を入力してください"),
            self.name_input, # 配置
        ], tight=True)
        self.actions = [
            ft.TextButton("キャンセル", on_click=self.handle_close),
            ft.TextButton(
                "保存", 
                on_click=lambda _: self.save_desired_skills_settings(
                    checkbox_refs=checkbox_refs, 
                    settings_name=self.name_input.value,
                    settings_data=settings_data
                )
            )
        ]

    def handle_close(self):
        self.open = False
        #self.page.overlay.remove(self)
        self.page.update()

    def save_desired_skills_settings(self, checkbox_refs, settings_name, settings_data):
        if settings_name in settings_data:
            # 上書き確認ダイアログ (B)
            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("確認"),
                content=ft.Text("この設定名は既に存在しますが、上書きしますか？"),
                actions=[
                    # 修正：ここでのキャンセルは「dlg (B)」を閉じるだけにする
                    ft.TextButton("キャンセル", on_click=lambda _: (setattr(dlg, "open", False), self.page.update())),
                    ft.TextButton(
                        "保存",
                        on_click=lambda _: self.execute_save(
                            checkbox_refs=checkbox_refs,
                            settings_name=settings_name,
                            settings_data=settings_data,
                            dlg=dlg
                        )
                    )
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self.page.overlay.append(dlg)
            dlg.open = True
            self.page.update()
        else:
            self.execute_save(checkbox_refs=checkbox_refs, settings_name=settings_name, settings_data=settings_data)

    def execute_save(self, checkbox_refs, settings_name, settings_data, dlg=None):
        # 1. 確認ダイアログ (B) があれば閉じる
        if dlg is not None:
            dlg.open = False
        # page.overlay.remove(dlg) # オプション：完全に削除する場合

        # チェックがついている(value=True)スキルだけを抽出
        selected = [
            ref.current.label 
            for ref in checkbox_refs 
            if ref.current.value
        ]
        # 設定をsettings_dataに追加し，jsonファイルに書き込む
        settings_data[DESIRED_SKILLS_SETTINGS][settings_name] = selected
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=4, ensure_ascii=False)

        # 2. 自分自身 (A) も閉じる
        self.open = False
        
        # 3. スナックバー表示とページ更新
        snack_bar = ft.SnackBar(
            content=ft.Text("保存しました！"),
            behavior=ft.SnackBarBehavior.FLOATING,
            margin=ft.Margin.only(bottom=100, left=20, right=20),
        )
        self.page.overlay.append(snack_bar)
        snack_bar.open = True

        self.page.update()
