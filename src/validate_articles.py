import sys
from pathlib import Path
import re
from urllib.parse import urlparse
from datetime import datetime

import yaml
from article_contract import is_published_article, merged_forbidden_words


ROOT = Path(__file__).resolve().parent.parent
ARTICLES_PATH = ROOT / "config" / "articles.yaml"
RULES_PATH = ROOT / "config" / "article_quality_rules.yaml"


class ValidationReport:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, article_id, message):
        self.errors.append((article_id, message))

    def warn(self, article_id, message):
        self.warnings.append((article_id, message))

    def print_report(self):
        print("=== Article Contract Validation ===")
        if self.errors:
            print("\n[Errors]")
            for article_id, message in self.errors:
                print(f"- {article_id}: {message}")
        if self.warnings:
            print("\n[Warnings]")
            for article_id, message in self.warnings:
                print(f"- {article_id}: {message}")
        print(
            f"\nSummary: errors={len(self.errors)}, warnings={len(self.warnings)}"
        )


def load_yaml(path):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def as_list(value):
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def validate_date(article_id, value, report):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except Exception:
        report.error(article_id, f"release_date must be YYYY-MM-DD: {value}")


def validate_url_host(article_id, url, discouraged_hosts, preferred_prefixes, report):
    if not url:
        report.warn(article_id, "eye_catch is missing")
        return
    host = urlparse(url).netloc
    if host in discouraged_hosts:
        return
    if preferred_prefixes and not any(url.startswith(prefix) for prefix in preferred_prefixes):
        report.warn(article_id, "eye_catch is not using a preferred local/public asset path")


def validate_site_config(config, report):
    site = config.get("site", {})
    required_fields = ["name", "description", "base_url"]
    for field in required_fields:
        if not site.get(field):
            report.error("site", f"site missing field: {field}")

    base_url = str(site.get("base_url", ""))
    parsed = urlparse(base_url)
    if base_url and (not parsed.scheme or not parsed.netloc):
        report.error("site", "site.base_url must be an absolute URL")
    if base_url and not base_url.endswith("/"):
        report.error("site", "site.base_url must end with '/'")

    verification = site.get("verification", {})
    google_verification = verification.get("google_site_verification")
    if google_verification is not None and not isinstance(google_verification, str):
        report.error("site", "site.verification.google_site_verification must be a string")

    analytics = site.get("analytics", {})
    measurement_id = analytics.get("ga4_measurement_id", "")
    if measurement_id and not re.fullmatch(r"G-[A-Z0-9]+", str(measurement_id)):
        report.error("site", "site.analytics.ga4_measurement_id must look like G-XXXXXXXXXX")


def main():
    config = load_yaml(ARTICLES_PATH)
    rules = load_yaml(RULES_PATH)
    report = ValidationReport()
    validate_site_config(config, report)

    hard_article = rules["hard_rules"]["article"]
    soft_article = rules["soft_rules"]["article"]
    keyword_hygiene = set(rules["soft_rules"]["keyword_hygiene"]["discouraged_terms"])

    categories = {c["id"] for c in config.get("categories", [])}
    articles = config.get("articles", [])

    seen = {field: {} for field in hard_article["unique_fields"]}

    for article in articles:
        article_id = article.get("id", "<missing-id>")
        is_live = True # audit all articles irrespective of release date

        for field in hard_article["required_fields"]:
            if field not in article or article[field] in (None, "", []):
                report.error(article_id, f"missing required field: {field}")

        article_type = article.get("type")
        if article_type and article_type not in hard_article["allowed_types"]:
            report.error(article_id, f"invalid type: {article_type}")

        category_id = article.get("category_id")
        if category_id and category_id not in categories:
            report.error(article_id, f"unknown category_id: {category_id}")

        release_date = article.get("release_date")
        if release_date:
            validate_date(article_id, release_date, report)

        for field in hard_article["unique_fields"]:
            value = article.get(field)
            if not value:
                continue
            if value in seen[field]:
                report.error(
                    article_id,
                    f"duplicate {field}: {value} (already used by {seen[field][value]})",
                )
            else:
                seen[field][value] = article_id

        test_criteria = as_list(article.get("test_criteria"))
        tc_rules = hard_article["test_criteria"]
        if not (tc_rules["min_items"] <= len(test_criteria) <= tc_rules["max_items"]):
            report.error(
                article_id,
                f"test_criteria count must be {tc_rules['min_items']}..{tc_rules['max_items']}",
            )
        criteria_ids = []
        for idx, item in enumerate(test_criteria, start=1):
            cid = item.get("id")
            cname = item.get("name")
            if not cid or not cname:
                report.error(article_id, f"test_criteria[{idx}] requires id and name")
                continue
            if cid in criteria_ids:
                report.error(article_id, f"duplicate test_criteria id: {cid}")
            criteria_ids.append(cid)

        qa_config = article.get("qa_config", {})
        qa_rules = hard_article["qa_config"]
        for field in qa_rules["required_fields"]:
            if field not in qa_config or qa_config[field] in (None, "", []):
                report.error(article_id, f"qa_config missing field: {field}")
        min_price = qa_config.get("min_price")
        if isinstance(min_price, int):
            if min_price < qa_rules["min_price_minimum"]:
                report.error(article_id, "qa_config.min_price is below minimum threshold")
        elif min_price is not None:
            report.error(article_id, "qa_config.min_price must be an integer")
        if not merged_forbidden_words(article):
            report.warn(article_id, "no forbidden product terms are active for this article")

        rakuten_params = article.get("rakuten_params", {})
        rp_rules = hard_article["rakuten_params"]
        for field in rp_rules["required_fields"]:
            if field not in rakuten_params or rakuten_params[field] in (None, "", []):
                report.error(article_id, f"rakuten_params missing field: {field}")
        hits = rakuten_params.get("hits")
        if isinstance(hits, int):
            if not (rp_rules["hits_minimum"] <= hits <= rp_rules["hits_maximum"]):
                report.error(article_id, "rakuten_params.hits is out of allowed range")
        elif hits is not None:
            report.error(article_id, "rakuten_params.hits must be an integer")

        keywords = [kw.strip() for kw in str(rakuten_params.get("keyword", "")).split(",") if kw.strip()]
        if not keywords:
            report.error(article_id, "rakuten_params.keyword must contain at least one keyword")
        elif any(kw in keyword_hygiene for kw in keywords):
            report.warn(article_id, "rakuten_params.keyword contains a generic discouraged term")

        products_extra = as_list(article.get("products_extra"))
        pe_rules = hard_article["products_extra"]
        if not (pe_rules["min_items"] <= len(products_extra) <= pe_rules["max_items"]):
            report.error(
                article_id,
                f"products_extra count must be {pe_rules['min_items']}..{pe_rules['max_items']}",
            )
        for idx, product in enumerate(products_extra, start=1):
            for field in pe_rules["required_fields"]:
                if field not in product or product[field] in (None, "", []):
                    report.error(article_id, f"products_extra[{idx}] missing field: {field}")
            pros = as_list(product.get("pros"))
            if pros and not (pe_rules["pros_min_items"] <= len(pros) <= pe_rules["pros_max_items"]):
                report.error(
                    article_id,
                    f"products_extra[{idx}].pros must contain {pe_rules['pros_min_items']}..{pe_rules['pros_max_items']} items",
                )
            scores = product.get("scores", {})
            if criteria_ids:
                missing_score_keys = [cid for cid in criteria_ids if cid not in scores]
                extra_score_keys = [key for key in scores if key not in criteria_ids]
                if missing_score_keys:
                    report.error(
                        article_id,
                        f"products_extra[{idx}].scores missing keys: {', '.join(missing_score_keys)}",
                    )
                if extra_score_keys:
                    report.error(
                        article_id,
                        f"products_extra[{idx}].scores has unknown keys: {', '.join(extra_score_keys)}",
                    )

        title = str(article.get("title", ""))
        meta_description = str(article.get("meta_description", ""))
        analysis_insight = str(article.get("analysis_insight", ""))
        intro = str(article.get("intro", ""))

        if is_live and title and not (soft_article["title"]["min_length"] <= len(title) <= soft_article["title"]["max_length"]):
            report.warn(article_id, "title length is outside the recommended range")
        if is_live and meta_description and not (
            soft_article["meta_description"]["min_length"]
            <= len(meta_description)
            <= soft_article["meta_description"]["max_length"]
        ):
            report.warn(article_id, "meta_description length is outside the recommended range")
        if is_live and analysis_insight and not (
            soft_article["analysis_insight"]["min_length"]
            <= len(analysis_insight)
            <= soft_article["analysis_insight"]["max_length"]
        ):
            report.warn(article_id, "analysis_insight length is outside the recommended range")
        if is_live and intro and not (soft_article["intro"]["min_length"] <= len(intro) <= soft_article["intro"]["max_length"]):
            report.warn(article_id, "intro length is outside the recommended range")

        preferred_fields = set(soft_article["recommended_fields"])
        for field in preferred_fields:
            if not is_live:
                continue
            current = article
            for part in field.split("."):
                if isinstance(current, dict):
                    current = current.get(part)
                else:
                    current = None
                    break
            if not current:
                report.warn(article_id, f"recommended field is missing: {field}")

        if is_live:
            validate_url_host(
                article_id,
                article.get("eye_catch", ""),
                set(soft_article["eye_catch"]["discouraged_hosts"]),
                soft_article["eye_catch"]["preferred_prefixes"],
                report,
            )

    report.print_report()
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
