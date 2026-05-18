import os
import re

filepath = r"d:\嘉秋\Antigravity\projects\rakuten-affiliate-site\config\articles.yaml"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. drum-washer-ranking
content = content.replace("日立 ビッグドラム", "日立 ドラム式洗濯機")
content = content.replace("- keyword: 日立 ドラム式洗濯機", "- keyword: 日立")

# 2. window-cleaning-robot
content = content.replace("HOBOT-388", "HOBOT")
content = content.replace("- keyword: HOBOT-388", "- keyword: HOBOT")

# 3. standing-desk-ranking
content = content.replace("KANADEMONO", "山善 昇降デスク")
content = content.replace("- keyword: 山善 昇降デスク", "- keyword: 山善")
content = content.replace("keyword: 山善", "keyword: 山善") # just in case

# 4. cordless-wet-vacuum
content = content.replace("Roborock Dyad Pro", "Roborock")
content = content.replace("- keyword: Roborock Dyad Pro", "- keyword: Roborock")

# 5. ultrawide-monitor-ranking
# Relax keywords even further
content = content.replace("Dell ウルトラワイドモニター", "Dell ウルトラワイド")
content = content.replace("LG ウルトラワイドモニター", "LG ウルトラワイド")
content = content.replace("BenQ ウルトラワイドモニター", "BenQ ウルトラワイド")
content = content.replace("HUAWEI ウルトラワイドモニター", "MateView GT")

content = content.replace("- keyword: Dell ウルトラワイド", "- keyword: Dell")
content = content.replace("- keyword: LG ウルトラワイド", "- keyword: LG")
content = content.replace("- keyword: BenQ ウルトラワイド", "- keyword: BenQ")
content = content.replace("- keyword: HUAWEI", "- keyword: MateView")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Remaining keyword fixes applied successfully.")
