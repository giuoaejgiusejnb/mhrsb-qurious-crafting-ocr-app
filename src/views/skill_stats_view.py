import flet as ft
import json
from functools import partial
from constants.paths import SETTINGS_PATH, ALL_SKILLS_DATA_PATH
from constants.skills import EXCLUDED_FROM_STATS
from constants.storage_keys import SKILL_STATS, TOTAL_IMAGE_COUNT
from components.save_settings_dialog import SaveSettingsDialog
from components.settings_edit_dialog import SettingsEditDialog

# --- 欲しいスキル設定ページのコンポーネント ---
@ft.component
def SkillStatsView(on_nav):
    # スキル統計データを読み込み
    with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
        settings_data = json.load(f)
        skill_stats = settings_data[SKILL_STATS]
        total_image_count = settings_data[TOTAL_IMAGE_COUNT]
    # コスト毎にスキルをまとめたデータ読み込み
    with open(ALL_SKILLS_DATA_PATH, "r", encoding="utf-8") as f:
        skills_data = json.load(f)["skill_data"]

    # 表示用のメインコンテナ
    view_content = [
        ft.Text(
            "今までに出現した各スキルの総数を表示します",
            size=25,
            weight="bold"
        ),
        ft.Text(
            "火事場力，災禍転福，攻めの守勢は欠けたときも画像認識されてしまうので，この統計では外しています",
            size=15
        ),
        ft.Text(f"今までに画像認識した数：{total_image_count}", color=ft.Colors.BLUE_800) 
        ]

    for cost_name, skill_list in skills_data.items():
        # スキルを並べるResponsiveRow
        skills_row = ft.ResponsiveRow()
        # コスト毎のスキルの出現数の合計
        total_score = 0
        # コスト毎の統計対象スキルの数（平均を求めるのに使う）
        stat_target_count = 0
        
        for skill_id in skill_list:
            score = skill_stats.get(skill_id, 0)

            if skill_id in EXCLUDED_FROM_STATS:
                display_value = "×"
                text_color = ft.Colors.RED
            else:
                display_value = str(score)
                text_color = ft.Colors.BLUE_600
                total_score += score
                stat_target_count += 1
            
            # 各スキルの表示カード
            skill_card = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(skill_id, weight=ft.FontWeight.W_500),
                        ft.Text(display_value, size=18, color=text_color, weight="bold"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=10,
                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                border_radius=8,
                # colの指定：スマホ(xs)なら半分、タブレット以上なら4つ並べる
                col={"xs": 6, "sm": 4, "md": 3}
            )
            skills_row.controls.append(skill_card)

        header = ft.Row(
            controls=[
                ft.Text(cost_name, size=20, weight="bold"),
                ft.Container(
                    content=ft.Text(f"合計: {total_score}", color=ft.Colors.WHITE, size=12),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=2),
                    border_radius=15,
                ),
                ft.Container(
                    content=ft.Text(f"平均: {total_score / stat_target_count}", color=ft.Colors.WHITE, size=12),
                    bgcolor=ft.Colors.BLUE_GREY_700,
                    padding=ft.Padding.symmetric(horizontal=10, vertical=2),
                    border_radius=15,
                )
            ],
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # 全体のリストに追加
        view_content.append(header)
        view_content.append(skills_row)
        view_content.append(ft.Divider(height=20, color=ft.Colors.BLUE))

    return ft.Column(view_content, scroll=ft.ScrollMode.AUTO)
