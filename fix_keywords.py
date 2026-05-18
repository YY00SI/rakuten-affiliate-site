import os

filepath = r"d:\嘉秋\Antigravity\projects\rakuten-affiliate-site\config\articles.yaml"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = {
    "keyword: U3425WE, 34WQ75C-B, EW3880R, MateView GT 34": "keyword: Dell ウルトラワイドモニター, LG ウルトラワイドモニター, BenQ ウルトラワイドモニター, HUAWEI ウルトラワイドモニター",
    "- keyword: U3425WE": "- keyword: Dell",
    "- keyword: 34WQ75C-B": "- keyword: LG",
    "- keyword: EW3880R": "- keyword: BenQ",
    "- keyword: MateView": "- keyword: HUAWEI",
    
    "keyword: Nebula Capsule 3 Laser, MoGo 2 Pro, BenQ GV31, Aladdin Vase": "keyword: Anker プロジェクター, XGIMI プロジェクター, BenQ プロジェクター, Aladdin プロジェクター",
    "- keyword: Nebula Capsule": "- keyword: Anker",
    "- keyword: MoGo 2 Pro": "- keyword: XGIMI",
    "- keyword: BenQ GV": "- keyword: BenQ",
    "- keyword: Aladdin Vase": "- keyword: Aladdin",
    
    "keyword: Insta360 Link, OBSBOT Tiny 2, Brio 500, Elgato Facecam": "keyword: Insta360 ウェブカメラ, OBSBOT ウェブカメラ, ロジクール ウェブカメラ, Elgato ウェブカメラ",
    "- keyword: Insta360 Link": "- keyword: Insta360",
    "- keyword: OBSBOT Tiny 2": "- keyword: OBSBOT",
    "- keyword: Brio": "- keyword: ロジクール"
}

for old, new in replacements.items():
    if old in content:
        content = content.replace(old, new)
        print(f"Replaced: {old}")
    else:
        print(f"NOT FOUND: {old}")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement script finished.")
