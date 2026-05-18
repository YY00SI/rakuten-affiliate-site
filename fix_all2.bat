@echo off
echo [1/4] Applying remaining keyword fixes...
python fix_remaining.py

echo [2/4] Fetching products (Testing fixes)...
python src/fetch_products.py

echo [3/4] Building site...
python src/build_site.py

echo [4/4] Deploying to GitHub...
call .\git_push.bat "Fix remaining missing keywords (drum washer, HOBOT, FLEXISPOT, etc.)"

echo All done!
pause
