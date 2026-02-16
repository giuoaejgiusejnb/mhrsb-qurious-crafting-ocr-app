import itertools
import json
from constants.paths import ALL_SKILLS_DATA_PATH

# 統計に表示しないスキル達
EXCLUDED_FROM_STATS = ["火事場力", "災禍転福", "攻めの守勢"]

# すべてのスキルをまとめたリストを作成
def load_master_skills(filepath=ALL_SKILLS_DATA_PATH):
    """
    JSONファイルからスキル名を読み込み、リストとして返します。
    """
    with open(filepath, "r", encoding="utf-8") as f:
        skills_data = json.load(f)["skill_data"]
    skills_list = list(itertools.chain.from_iterable(skills_data.values()))
    return skills_list

SKILL_MASTER_LIST = load_master_skills()