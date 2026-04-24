import shutil
import os

agent_dir = r"d:\嘉秋\Antigravity\projects\rakuten-affiliate-site\.agent"

if os.path.exists(agent_dir):
    shutil.rmtree(agent_dir)
    print(f"[INFO] Deleted {agent_dir} completely.")
else:
    print("[INFO] Directory already deleted.")
