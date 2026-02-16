import flet as ft
import json
from functools import partial
from constants.paths import SETTINGS_PATH
from components.detail_dialog import DetailDialog
from constants.storage_keys import DESIRED_SKILLS_SETTINGS

class LoadSettingsDialogBase(ft.AlertDialog):
    def __init__(self, on_load, is_delete_button_visible=True, needs_overwrite_confirm=True):
        super().__init__()

        self.title = ft.Text("設定読み込み")
        self.overwrite_confirm_msg = "上書きしても構いませんか？"
        self.needs_overwrite_confirm = needs_overwrite_confirm
        self.apply_button_ref = ft.Ref[ft.Button]()
        self.on_load = on_load
        # JSONファイルを読み込む
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)[DESIRED_SKILLS_SETTINGS]

        # ラジオボタンの選択肢を格納するリスト
        radio_options = []

        for settings_name in settings_data.keys():
        # 設定名、詳細ボタンを横に並べるRowを作成
        # ラジオボタン本体（ft.Radio）をRowに組み込む
            row = ft.Row(
                controls=[
                    # ラジオボタン（valueには設定名を指定）
                    ft.Radio(value=settings_name, label=settings_name), 
                
                    # 右寄せにするためのスペーサー
                    ft.Container(expand=True), 
                
                    # 詳細ボタン
                    ft.Button(
                        "詳細を表示",
                        icon=ft.Icons.INFO_OUTLINE,
                        # こうしないとクロージャの仕様（遅延評価）で，settings_nameがループの最後のものに固定される
                        on_click=partial(self.show_detail_dialog, settings_name=settings_name)
                    ),

                    # 削除ボタン（is_delete_button_visibleがTrueのときのみ表示）
                    ft.Button(
                        "削除する",
                        visible=is_delete_button_visible,
                        on_click=partial(self.show_deltete_confirm_dlg, settings_name=settings_name)
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            )
            # 各行をリストに追加
            radio_options.append(ft.Container(content=row, padding=ft.Padding.symmetric(vertical=2), data=settings_name))

        # 全体をRadioGroupで包む
        self.settings_selection_group = ft.RadioGroup(
            content=ft.Column(radio_options, scroll=ft.ScrollMode.AUTO),
            on_change=lambda _: (
            setattr(self.apply_button_ref.current, "disabled", False), # 選択されたら無効化を解除
            self.update() # ダイアログを再描画)
            )
        )
        self.content = ft.Column(controls=[self.settings_selection_group], tight=True)
        self.actions = ft.Row(
            controls=[
                ft.TextButton("キャンセル", on_click=lambda _: (setattr(self, "open", False), self.page.update())),
                ft.Button(
                    "選んだ設定を読み込む", 
                    ref=self.apply_button_ref,
                    on_click=self.show_overwrite_confirm_dlg,
                    disabled=True
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )

    def show_detail_dialog(self, e, settings_name):
        e.page.show_dialog(DetailDialog(settings_name=settings_name))

    def show_overwrite_confirm_dlg(self): 
        if not self.needs_overwrite_confirm:
            self.execute_load()
            return
        self.overwrite_confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("確認"),
            content=ft.Text(self.overwrite_confirm_msg),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda _: (setattr(self.overwrite_confirm_dlg, "open", False), self.page.update())),
                ft.TextButton(
                    "読み込む",
                    on_click=self.execute_load
                )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(self.overwrite_confirm_dlg)
        self.overwrite_confirm_dlg.open = True
        self.page.update()
    
    def execute_load(self):
        pass

    def show_deltete_confirm_dlg(self, e, settings_name):
        self.settings_name = settings_name
        self.delete_confirm_dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("確認"),
            content=ft.Text(f"{settings_name}を削除しますがよろしいですか？"),
            actions=[
                ft.TextButton("キャンセル", on_click=lambda _: (setattr(self.delete_confirm_dlg, "open", False), self.page.update())),
                ft.TextButton(
                    "削除する",
                    on_click=self.execute_delete
                    )
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.overlay.append(self.delete_confirm_dlg)
        self.delete_confirm_dlg.open = True
        self.page.update()

    def execute_delete(self):
        # JSONファイルを読み込んで，指定された設定を削除したら保存する
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)

        settings_data[DESIRED_SKILLS_SETTINGS].pop(self.settings_name, None)

        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(settings_data, f, indent=4, ensure_ascii=False)

        # 読み込みダイアログに変更を反映させる
        # UIのリスト(Columnのcontrols)から削除するContainerを探す
        target_container = None
        for control in self.settings_selection_group.content.controls:
            if control.data == self.settings_name:
                target_container = control
                break

        if target_container:
            # UIから削除
            self.settings_selection_group.content.controls.remove(target_container)
            # もし削除したものが現在選択中だったら選択を解除
            if self.settings_selection_group.value == self.settings_name:
                self.settings_selection_group.value = None
                self.apply_button_ref.current.disabled = True

        # 確認ダイアログを消す
        self.delete_confirm_dlg.open = False

        self.page.update()
