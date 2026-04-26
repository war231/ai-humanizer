@echo off
REM AI Humanizer - 推送到 GitHub
REM 用户名: war231

echo ========================================
echo 推送 AI Humanizer 到 GitHub
echo ========================================
echo.

cd /d e:\xiangmu\ai-humanizer

echo [1/3] 添加远程仓库...
git remote add origin https://github.com/war231/ai-humanizer.git
if %errorlevel% neq 0 (
    echo 远程仓库已存在，跳过添加
)

echo.
echo [2/3] 重命名分支为 main...
git branch -M main

echo.
echo [3/3] 推送到 GitHub...
git push -u origin main

echo.
echo ========================================
echo 推送完成！
echo ========================================
echo.
echo 访问您的仓库: https://github.com/war231/ai-humanizer
echo.
pause
