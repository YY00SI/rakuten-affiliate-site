@echo off
echo [1/5] Restoring corrupted articles.yaml...
git checkout config/articles.yaml

echo [2/5] Applying keyword fixes...
python fix_keywords.py

echo [3/5] Fetching products (Testing fixes)...
python src/fetch_products.py

echo [4/5] Building site...
python src/build_site.py

echo [5/5] Deploying to GitHub...
call .\git_push.bat "Fix future stock articles (ultrawide, projector, webcam)"

echo All done!
pause
