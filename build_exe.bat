@echo off
setlocal

title Milk Data Processor - Build EXE
cd /d "%~dp0"

echo.
echo ============================================================
echo   MILK DATA PROCESSOR - BUILD EXE (Windows)
echo ============================================================
echo.

echo [1/3] Έλεγχος Python...
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Δεν βρέθηκε Python στο PATH.
    echo    Κατεβάστε την από: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version

echo.
echo [2/3] Δημιουργία/έλεγχος virtual environment...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Αποτυχία δημιουργίας virtual environment.
        pause
        exit /b 1
    )
)

echo.
echo [3/3] Build του EXE με PyInstaller...
"%CD%\.venv\Scripts\python.exe" -m pip install --upgrade pip
"%CD%\.venv\Scripts\python.exe" -m pip install pyinstaller
if errorlevel 1 (
    echo ❌ Αποτυχία εγκατάστασης PyInstaller.
    pause
    exit /b 1
)

REM Χρησιμοποιεί το setting_gui.py ως GUI entry point
"%CD%\.venv\Scripts\python.exe" -m PyInstaller ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --name "MilkDataProcessor" ^
  setting_gui.py
if errorlevel 1 (
    echo ❌ Αποτυχία build.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ Το EXE δημιουργήθηκε στο dist\MilkDataProcessor.exe
echo ============================================================
echo.
pause
