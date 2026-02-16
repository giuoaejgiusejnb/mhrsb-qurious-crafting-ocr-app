import flet as ft
import json
from functools import partial
from constants.paths import SETTINGS_PATH, ALL_SKILLS_DATA_PATH
from components.save_settings_dialog import SaveSettingsDialog
from components.settings_edit_dialog import SettingsEditDialog

# --- 欲しいスキル設定ページのコンポーネント ---
@ft.component
def SkillSettingsView(on_nav):
    selected_skills, set_selected_skills = ft.use_state(set())
    # チェックボックスの参照を保持するリスト
    checkbox_refs = []

    # 保存ボタンを押したときの処理（保存ダイアログを表示）
    def show_save_settings_dialog(e):
        page = e.page
        dialog = SaveSettingsDialog(checkbox_refs)
        # ページにオーバーレイとして追加して表示
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    # 読み込みボタンを押したときの処理（読み込みダイアログを表示）
    def show_load_settings_dialog(e):
        page = e.page
        dialog = SettingsEditDialog(on_load=set_selected_skills)
        # ページにオーバーレイとして追加して表示
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def toggle_skill(e, skill_name):
        # 現在のセットをコピー（Fletの状態更新は、新しいオブジェクトを渡す必要があるため）
        new_skills = set(selected_skills)
        is_checked = e.control.value
    
        if is_checked:
            new_skills.add(skill_name)
        else:
            new_skills.discard(skill_name)
    
        # 状態を更新（これによってCheckboxのvalueが自動で再評価される）
        set_selected_skills(new_skills)


    # 全スキルをコスト毎にまとめた辞書を作成
    with open(ALL_SKILLS_DATA_PATH, "r", encoding="utf-8") as f:
        skills_data = json.load(f)["skill_data"]    

    # データを元にUI要素を生成
    content_list = [ft.Text("スキル選択（翔と蝕はどちらも選択しないかどちらも選択するかを推奨）", size=25, weight="bold")]
    for cost, skills in skills_data.items():
        # セクションの見出し（コスト）
        content_list.append(
            ft.Text(cost, size=20, weight="bold", color=ft.Colors.BLUE_ACCENT)
        )
        # チェックボックス
        checkboxes = []
        for skill in skills:
            r = ft.Ref[ft.Checkbox]()
            checkbox_refs.append(r)
            checkboxes.append(ft.Checkbox(
                value=skill in selected_skills,
                ref=r, 
                label=skill, 
                col={"xs": 6, "sm": 4, "md": 3},
                on_change=partial(toggle_skill, skill_name=skill)
            ))
        content_list.append(ft.ResponsiveRow(
            controls=checkboxes,
            spacing=10,        # 横の間隔
            run_spacing=10,    # 縦の間隔（改行時）
            alignment=ft.MainAxisAlignment.START
            ))
        # セクション間の余白
        content_list.append(ft.Divider(height=10, color=ft.Colors.BLUE))
    skill_form_controls = (ft.Column(
    controls=content_list,
    scroll=ft.ScrollMode.ADAPTIVE,
    expand=True
    ))

    # 読み込みボタン，保存ボタンの定義
    action_buttons = []
    # 読み込みボタン
    action_buttons.append(
        ft.Row(
            controls=[
                ft.Button(
                    "設定を読み込む", 
                    icon=ft.Icons.DOWNLOAD,
                    on_click=show_load_settings_dialog
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER 
        )
    )
    # 削除ボタン
    action_buttons.append(
        ft.Row(
            controls=[
                ft.Button(
                    "保存する", 
                    icon=ft.Icons.SAVE,
                    on_click=show_save_settings_dialog
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER 
        )
    )

    # スクロール可能なカラムとして返す
    return ft.Column([ft.Row(action_buttons, alignment=ft.MainAxisAlignment.CENTER), skill_form_controls])