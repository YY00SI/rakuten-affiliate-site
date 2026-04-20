@echo off
echo [PointOps Console] Starting local git push...

git add .

set /p msg="Commit message (default: update): "
if "%msg%"=="" set msg=update

git commit -m "%msg%"

echo Sending to GitHub...
git push origin main

echo.
echo Process complete!
pause
