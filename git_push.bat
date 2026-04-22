@echo off
echo [PointOps Console] Starting local git push...

git add .
git commit -m "auto-update %date% %time%"

echo Sending to GitHub...
git push origin main

echo.
echo Process complete!
pause
