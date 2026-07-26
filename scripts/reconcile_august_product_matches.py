from pathlib import Path
import json
import re
import yaml

ROOT = Path(__file__).resolve().parent.parent
STOCK = ROOT / "config" / "articles_stock.yaml"
PRODUCTS = ROOT / "data" / "products"


def dump_block(article):
    dumped = yaml.safe_dump([article], allow_unicode=True, sort_keys=False, width=1000).rstrip()
    return "\n".join("  " + line for line in dumped.splitlines()) + "\n"


def main():
    text = STOCK.read_text(encoding="utf-8")
    data = yaml.safe_load(text) or {}
    august = [a for a in data.get("articles", []) if str(a.get("release_date", "")).startswith("2026-08-")]
    expected = [f"2026-08-{day:02d}" for day in range(1, 32)]
    if sorted(str(a["release_date"]) for a in august) != expected:
        raise ValueError("August articles must cover exactly 2026-08-01 through 2026-08-31")

    counts = {}
    for article in august:
        cache_path = PRODUCTS / f"{article['id']}.json"
        if not cache_path.exists():
            raise ValueError(f"missing product cache: {article['id']}")
        cache = json.loads(cache_path.read_text(encoding="utf-8"))
        items = cache.get("items", [])
        if not items:
            raise ValueError(f"empty product cache: {article['id']}")
        matched = []
        for item in items:
            keyword = item.get("match_keyword")
            if keyword and keyword not in matched:
                matched.append(keyword)
        if not matched:
            raise ValueError(f"no matched keywords: {article['id']}")

        extras_by_keyword = {p.get("keyword"): p for p in article.get("products_extra", [])}
        missing = [keyword for keyword in matched if keyword not in extras_by_keyword]
        if missing:
            raise ValueError(f"cache/config mismatch for {article['id']}: {missing}")
        article["products_extra"] = [extras_by_keyword[keyword] for keyword in matched]
        article["rakuten_params"]["keyword"] = ", ".join(matched)
        image = items[0].get("image")
        if not image:
            raise ValueError(f"missing product image: {article['id']}")
        article["eye_catch"] = image

        names = "、".join(matched)
        article["intro"] = re.sub(r"本記事では.*?を、", f"本記事では{names}を、", article["intro"], count=1)
        topic = article["h1"].split("比較｜", 1)[0]
        axes = "・".join(c["name"] for c in article["test_criteria"])
        article["meta_description"] = (
            f"{topic}の指名買い候補を比較。{axes}を軸に、購入後の手間と使い勝手、"
            "新品本体の価格・在庫・販売元・保証を楽天市場で確認する前の判断ポイントを整理します。"
        )
        counts[len(matched)] = counts.get(len(matched), 0) + 1

        pattern = re.compile(rf"(?ms)^  - id: {re.escape(article['id'])}\r?\n.*?(?=^  - id: |\Z)")
        if not pattern.search(text):
            raise ValueError(f"article block not found: {article['id']}")
        text = pattern.sub(dump_block(article), text, count=1)

    STOCK.write_text(text.rstrip() + "\n", encoding="utf-8")
    print(f"August product matches reconciled: articles={len(august)}, product_counts={counts}")


if __name__ == "__main__":
    main()
