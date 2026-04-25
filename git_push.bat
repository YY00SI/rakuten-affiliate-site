@echo off
echo [PointOps Console] Starting LTS Content Build...
python src\fetch_products.py
python src\build_site.py
echo.
echo =======================================================
echo [QA CHECK] ビルド結果を確認してください。
echo [CRITICAL ERROR] が表示されている場合は、公開がブロックされています。
echo 問題なければ、以下のキーを押してGitHubへデプロイします。
echo （中止する場合は Ctrl+C を押してください）
echo =======================================================
pause

echo [PointOps Console] Starting robust upload process...
git add .
git commit -m "auto-update"
echo [PointOps Console] Syncing with GitHub...
git pull origin main --no-edit -X ours
echo [PointOps Console] Sending to GitHub...
git push origin main
echo.
echo [SUCCESS] Upload complete!
pause