import os
import re

filepath = r"d:\嘉秋\Antigravity\projects\rakuten-affiliate-site\config\articles.yaml"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

sections = content.split("- id: ")
for i, sec in enumerate(sections):
    if sec.startswith("audio-glasses-ranking"):
        sections[i] = sec.replace("- keyword: MateView", "- keyword: HUAWEI")
    
    if sec.startswith("ultrawide-monitor-ranking"):
        # Make sure we search for monitors, otherwise Dell/BenQ top 30 hits will be laptops/projectors
        sec = sec.replace("Dell ウルトラワイド", "Dell モニター")
        sec = sec.replace("BenQ ウルトラワイド", "BenQ モニター")
        sec = sec.replace("MateView GT", "HUAWEI モニター")
        
        # If it was already replaced to 'Dell', 'BenQ', 'HUAWEI' in the previous failed run, fix it:
        # Wait, the previous run didn't execute this file. This file replaces the CURRENT state.
        
        sec = sec.replace("- keyword: MateView", "- keyword: HUAWEI")
        sections[i] = sec

content = "- id: ".join(sections)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Final keyword fixes applied successfully.")
