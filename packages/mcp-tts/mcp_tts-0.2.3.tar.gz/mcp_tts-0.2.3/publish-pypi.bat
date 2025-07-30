@echo off
echo.
echo MCP-TTS PyPI Publisher
echo =======================
echo.

echo [CHECK] Checking current git status...
git status --porcelain
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Error checking git status
    pause
    exit /b 1
)

echo.
echo [CLEAN] Cleaning previous builds...
if exist "dist\" (
    rmdir /s /q "dist"
    echo [OK] Removed old dist/ folder
)

echo.
echo [PUBLISH] Publishing to PyPI with uv...
echo [WARNING] Make sure you have your PyPI token ready!
echo.
uv publish

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Successfully published to PyPI!
    echo [INFO] Check it out: https://pypi.org/project/mcp-tts/
    echo.
    echo [TIP] Don't forget to:
    echo   1. Push your changes: git push origin main
    echo   2. Create a GitHub release if desired
) else (
    echo.
    echo [ERROR] Publishing failed!
    echo [TIP] Make sure you have a valid PyPI token configured
)

echo.
pause 