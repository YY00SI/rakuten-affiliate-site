import os
import shutil
import yaml

# 1. 画像ファイルのコピー
image_mapping = {
    'premium-rice-cooker': {
        'src': r'C:\Users\yoshi\.gemini\antigravity\brain\ada7dff4-f0b3-492d-994c-1dad73c234bf\premium_rice_cooker_eyecatch_1777076235048.png',
        'dest': 'rice-cooker.png',
        'dead_url': 'https://images.unsplash.com/photo-1591333139264-28414270160d?auto=format&fit=crop&w=800&q=80'
    },
    'robot-vacuum-ranking': {
        'src': r'C:\Users\yoshi\.gemini\antigravity\brain\ada7dff4-f0b3-492d-994c-1dad73c234bf\robot_vacuum_eyecatch_1777081382670.png',
        'dest': 'robot-vacuum.png',
        'dead_url': 'https://images.unsplash.com/photo-1589330694653-90d648283307?auto=format&fit=crop&w=800&q=80'
    },
    'office-chair-ranking': {
        'src': r'C:\Users\yoshi\.gemini\antigravity\brain\ada7dff4-f0b3-492d-994c-1dad73c234bf\office_chair_eyecatch_1777081398308.png',
        'dest': 'office-chair.png',
        'dead_url': 'https://images.unsplash.com/photo-1592074412690-dd9901507248?auto=format&fit=crop&w=800&q=80'
    },
    'toaster-ranking': {
        'src': r'C:\Users\yoshi\.gemini\antigravity\brain\ada7dff4-f0b3-492d-994c-1dad73c234bf\premium_toaster_eyecatch_1777081414369.png',
        'dest': 'toaster.png',
        'dead_url': 'https://images.unsplash.com/photo-1590130985552-32a265633633?auto=format&fit=crop&w=800&q=80'
    },
    'toothbrush-ranking': {
        'src': r'C:\Users\yoshi\.gemini\antigravity\brain\ada7dff4-f0b3-492d-994c-1dad73c234bf\electric_toothbrush_eyecatch_1777081428022.png',
        'dest': 'toothbrush.png',
        'dead_url': 'https://images.unsplash.com/photo-1559599141-383d43232115?auto=format&fit=crop&w=800&q=80'
    }
}

os.makedirs('docs/images', exist_ok=True)
base_url = "https://yy00si.github.io/rakuten-affiliate-site/images/"

for art_id, info in image_mapping.items():
    dest_path = os.path.join('docs/images', info['dest'])
    if os.path.exists(info['src']):
        shutil.copy(info['src'], dest_path)
        print(f"Copied {info['src']} to {dest_path}")
    else:
        print(f"WARNING: Source file not found: {info['src']}")

# 2. articles.yaml の書き換え
yaml_path = 'config/articles.yaml'
with open(yaml_path, 'r', encoding='utf-8') as f:
    content = f.read()

for art_id, info in image_mapping.items():
    new_url = base_url + info['dest']
    old_url = info['dead_url']
    if old_url in content:
        content = content.replace(old_url, new_url)
        print(f"Replaced dead URL for {art_id} with {new_url}")

with open(yaml_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Images fixed successfully. You can run 'python qa_check.py' again to verify.")
