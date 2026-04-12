@echo off
REM Build standalone Windows executable for GP Presets Converter
REM Requires: pip install pyinstaller
REM Output:   dist\gp-convert.exe

echo ==========================================
echo GP Presets Converter - Windows Build
echo ==========================================
echo.

REM Navigate to project root
cd /d "%~dp0\.."

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Check PyInstaller
python -c "import PyInstaller" >nul 2>&1
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

echo Building standalone executable...
python -m PyInstaller ^
    --onefile ^
    --console ^
    --name gp-convert ^
    --distpath dist ^
    --workpath build\pyinstaller ^
    --specpath build ^
    --paths src ^
    src\gp_presets_converter\cli.py

if errorlevel 1 (
    echo.
    echo Build FAILED
    exit /b 1
)

echo.
echo ==========================================
echo Build successful!
echo Executable: dist\gp-convert.exe
echo ==========================================
echo.
echo Usage:
echo   dist\gp-convert.exe 55-TimPierce.prst --slot 70
echo   dist\gp-convert.exe .\GP5_PRESETS\ -o .\GP50_PRESETS\ --slot 60
