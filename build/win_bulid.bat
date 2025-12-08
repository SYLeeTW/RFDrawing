@echo off
REM win_build.bat
REM Build RFDrawing.exe on Windows with venv + PyInstaller

setlocal ENABLEDELAYEDEXPANSION

REM Get project root = parent folder of this script
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%\.."
set "PROJECT_ROOT=%CD%"
set "VENV_DIR=%PROJECT_ROOT%\venv"

echo Project root: %PROJECT_ROOT%
echo Using venv:   %VENV_DIR%
echo.

REM 1. Create venv if not exists
if not exist "%VENV_DIR%" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
) else (
    echo Virtual environment already exists.
)
echo.

REM 2. Install Python packages
echo Installing Python dependencies...
"%VENV_DIR%\Scripts\python.exe" -m pip install --upgrade pip
"%VENV_DIR%\Scripts\python.exe" -m pip install -r "%PROJECT_ROOT%\requirements.txt"
echo.

REM 3. Clean old build artifacts
cd /d "%PROJECT_ROOT%\src"
echo Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist RFDrawing.spec del /f /q RFDrawing.spec
echo.

REM 4. Run PyInstaller
echo Running PyInstaller...
"%VENV_DIR%\Scripts\pyinstaller.exe" --onefile --windowed --name RFDrawing rf_drawing_gui.py
echo.

echo Build finished.
echo EXE is at: %PROJECT_ROOT%\src\dist\RFDrawing.exe
echo.
pause

endlocal
