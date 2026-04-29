from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

import yaml


ROOT = Path(__file__).resolve().parent.parent
RULES_PATH = ROOT / "config" / "article_quality_rules.yaml"
DEFAULT_DISCOURAGED_EYE_CATCH_HOSTS = {"images.unsplash.com"}


def load_quality_rules():
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_global_forbidden_terms():
    rules = load_quality_rules()
    return rules.get("soft_rules", {}).get("forbidden_product_terms", [])


def get_discouraged_embed_hosts():
    rules = load_quality_rules()
    configured = rules.get("soft_rules", {}).get("site_asset_hygiene", {}).get(
        "discouraged_embed_hosts", []
    )
    return sorted({host for host in configured if host})


def get_discouraged_eye_catch_hosts():
    rules = load_quality_rules()
    configured = rules.get("soft_rules", {}).get("article", {}).get("eye_catch", {}).get(
        "discouraged_hosts", []
    )
    return sorted(DEFAULT_DISCOURAGED_EYE_CATCH_HOSTS.union(host for host in configured if host))


def merged_forbidden_words(article):
    qa_config = article.get("qa_config", {})
    article_terms = qa_config.get("forbidden_words", []) or []
    merged = []
    for term in article_terms + get_global_forbidden_terms():
        if term and term not in merged:
            merged.append(term)
    return merged


def is_published_article(article, today_date=None):
    if not article.get("enabled", True):
        return False
    if today_date is None:
        today_date = datetime.now().strftime("%Y-%m-%d")
    return article.get("release_date", "2000-01-01") <= today_date


def is_discouraged_eye_catch(url):
    if not url:
        return True
    host = urlparse(url).netloc
    return host in set(get_discouraged_eye_catch_hosts())


def resolve_eye_catch(article, items=None):
    eye_catch = article.get("eye_catch", "")
    if eye_catch and not is_discouraged_eye_catch(eye_catch):
        return eye_catch

    for item in items or []:
        image = item.get("image")
        if image:
            return image

    return eye_catch


def build_article_intro(article):
    intro = (article.get("intro") or "").strip()
    if intro:
        return intro

    criteria = article.get("test_criteria", []) or []
    criteria_names = [item.get("name", "").strip() for item in criteria if item.get("name")]
    criteria_text = "、".join(criteria_names[:3])

    if criteria_text:
        return (
            f"{article.get('h1', '')}で失敗したくない方向けに、"
            f"{criteria_text}を中心に比較し、価格の高さに見合う価値があるモデルだけを厳選しました。"
        )

    return (
        f"{article.get('h1', '')}を検討している方向けに、"
        "後悔しやすいポイントと選ぶべき理由を整理し、買う価値のあるモデルだけをまとめています。"
    )
