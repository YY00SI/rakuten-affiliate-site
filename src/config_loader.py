from copy import deepcopy
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parent.parent
BASE_CONFIG_PATH = ROOT / "config" / "articles.yaml"
STOCK_CONFIG_PATH = ROOT / "config" / "articles_stock.yaml"


def load_config():
    with open(BASE_CONFIG_PATH, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    merged = deepcopy(config)
    stock_articles = []
    if STOCK_CONFIG_PATH.exists():
        with open(STOCK_CONFIG_PATH, "r", encoding="utf-8") as f:
            stock_config = yaml.safe_load(f) or {}
        stock_articles = stock_config.get("articles", [])

    merged["articles"] = list(config.get("articles", [])) + stock_articles
    return merged
