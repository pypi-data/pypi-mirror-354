@echo off
echo.
echo MCP-TTS Version Bumper
echo =======================
echo.

echo DEBUG: First argument is: "%1"

if "%1"=="" (
    echo Usage: bump-version.bat [patch^|minor^|major^|version]
    echo.
    echo Examples:
    echo   bump-version.bat patch     - Bump patch version (0.2.0 -^> 0.2.1)
    echo   bump-version.bat minor     - Bump minor version (0.2.0 -^> 0.3.0)
    echo   bump-version.bat major     - Bump major version (0.2.0 -^> 1.0.0)
    echo   bump-version.bat 1.5.0     - Set specific version
    echo.
    exit /b 1
)

echo DEBUG: Argument check passed, calling Python script...
echo Running version bump script...
uv run python scripts/bump_version.py %1
echo DEBUG: Python script finished with error level: %ERRORLEVEL%

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Version bump complete!
    echo [TIP] Next step: run publish-pypi.bat to publish to PyPI
) else (
    echo.
    echo [ERROR] Version bump failed!
) 