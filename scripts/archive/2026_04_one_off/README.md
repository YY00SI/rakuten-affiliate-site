# 2026-04 one-off maintenance scripts

This directory contains one-off migration and repair scripts from the initial article/build setup phase.

These scripts are archived because they may:

- rewrite `config/articles.yaml` directly
- contain historical absolute paths
- assume old local image locations
- no longer represent the current article quality workflow

Do not run these scripts during normal PDCA or publishing work.

Current routine operations should use:

- `src/validate_articles.py`
- `src/fetch_products.py`
- `src/build_site.py`
- `src/audit_site.py`

