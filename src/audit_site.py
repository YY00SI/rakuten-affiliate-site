import re
import sys
from pathlib import Path

from article_contract import get_discouraged_embed_hosts, get_global_forbidden_terms


ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = ROOT / "docs"
STATIC_PAGE_DIRS = {"about", "privacy-policy", "how-we-test"}


class AuditReport:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, path, message):
        self.errors.append((path, message))

    def warn(self, path, message):
        self.warnings.append((path, message))

    def print(self):
        print("=== Generated Site Audit ===")
        if self.errors:
            print("\n[Errors]")
            for path, message in self.errors:
                print(f"- {path}: {message}")
        if self.warnings:
            print("\n[Warnings]")
            for path, message in self.warnings:
                print(f"- {path}: {message}")
        print(f"\nSummary: errors={len(self.errors)}, warnings={len(self.warnings)}")


def find_index_pages():
    return sorted(DOCS_DIR.glob("**/index.html"))


def rel_path(path):
    return str(path.relative_to(ROOT)).replace("\\", "/")


def page_kind(path):
    parts = path.relative_to(DOCS_DIR).parts[:-1]
    if not parts:
        return "home"
    if len(parts) == 1:
        return "static" if parts[0] in STATIC_PAGE_DIRS else "category"
    return "article"


def has_meta(html, marker):
    return marker in html


def extract_affiliate_anchors(html):
    pattern = re.compile(r'<a[^>]+href="([^"]*hb\.afl\.rakuten\.co\.jp[^"]*)"[^>]+rel="([^"]+)"', re.IGNORECASE)
    return pattern.findall(html)


def has_discouraged_product_terms(html):
    terms = get_global_forbidden_terms()
    item_name_matches = re.findall(r'<h3 class="item-name">(.*?)</h3>', html, re.DOTALL)
    comparison_matches = re.findall(r'<td style="font-weight: 500;">(.*?)</td>', html, re.DOTALL)
    haystacks = item_name_matches + comparison_matches
    hits = []
    for block in haystacks:
        for term in terms:
            if term in block:
                hits.append(term)
    return sorted(set(hits))


def count_rendered_items(html):
    return len(re.findall(r'<div id="rank-\d+" class="ranking-item">', html))


def main():
    report = AuditReport()
    pages = find_index_pages()
    category_article_counts = {}
    discouraged_embed_hosts = get_discouraged_embed_hosts()

    for path in pages:
        if page_kind(path) != "article":
            continue
        category_slug = path.relative_to(DOCS_DIR).parts[0]
        category_article_counts[category_slug] = category_article_counts.get(category_slug, 0) + 1

    if not pages:
        report.error("docs", "No generated index.html files found")
        report.print()
        sys.exit(1)

    for path in pages:
        html = path.read_text(encoding="utf-8")
        kind = page_kind(path)
        label = rel_path(path)

        for marker, message in [
            ('<link rel="canonical"', "canonical link is missing"),
            ('property="og:title"', "og:title is missing"),
            ('property="og:description"', "og:description is missing"),
            ('name="twitter:card"', "twitter card is missing"),
            ('application/ld+json', "structured data is missing"),
        ]:
            if not has_meta(html, marker):
                report.error(label, message)

        for host in discouraged_embed_hosts:
            if host and host in html:
                report.error(label, f"Discouraged external asset host found in rendered HTML: {host}")

        if kind == "article":
            affiliate_anchors = extract_affiliate_anchors(html)
            if not affiliate_anchors:
                report.error(label, "No Rakuten affiliate anchors found")
            for _, rel_value in affiliate_anchors:
                required_tokens = {"nofollow", "noopener", "sponsored"}
                if not required_tokens.issubset(set(rel_value.split())):
                    report.error(label, f"Affiliate link rel is incomplete: {rel_value}")

            forbidden_hits = has_discouraged_product_terms(html)
            if forbidden_hits:
                report.error(label, f"Discouraged product terms found in rendered item names: {', '.join(forbidden_hits)}")

            if 'id="comparison"' not in html:
                report.warn(label, "comparison anchor is missing")
            category_slug = path.relative_to(DOCS_DIR).parts[0]
            if category_article_counts.get(category_slug, 0) > 1 and "同じカテゴリの関連記事" not in html:
                report.warn(label, "related articles section is missing")

            if count_rendered_items(html) == 1:
                for phrase in ["主要モデルの比較", "おすすめランキング詳細", "比較表を見る", "1位の商品を楽天で確認する"]:
                    if phrase in html:
                        report.error(label, f"Single-pick article still uses ranking phrasing: {phrase}")

    sitemap = DOCS_DIR / "sitemap.xml"
    robots = DOCS_DIR / "robots.txt"
    if not sitemap.exists():
        report.error(rel_path(DOCS_DIR), "sitemap.xml is missing")
    if not robots.exists():
        report.error(rel_path(DOCS_DIR), "robots.txt is missing")
    elif "/sitemap.xml/" in robots.read_text(encoding="utf-8"):
        report.error(rel_path(robots), "robots.txt sitemap URL has an unexpected trailing slash")

    report.print()
    sys.exit(1 if report.errors else 0)


if __name__ == "__main__":
    main()
