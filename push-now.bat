@echo off
chcp 65001 >nul
echo ========================================
echo 推送 AI Humanizer 到 GitHub
echo ========================================
echo.

cd /d e:\xiangmu\ai-humanizer

echo 正在推送...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 推送成功！
    echo ========================================
    echo.
    echo 访问您的仓库:
    echo https://github.com/war231/ai-humanizer
    echo.
) else (
    echo.
    echo ========================================
    echo 推送失败
    echo ========================================
    echo.
    echo 可能的原因:
    echo 1. 仓库未在 GitHub 创建
    echo 2. 需要登录 GitHub
    echo 3. 网络连接问题
    echo.
    echo 请检查后重试
    echo.
)

pause
