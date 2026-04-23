@echo off
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