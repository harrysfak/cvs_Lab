@echo off
setlocal

title Milk Data Processor - One Click Install
cd /d "%~dp0"

echo.
echo ============================================================
echo   MILK DATA PROCESSOR - ONE CLICK INSTALL (Windows)
echo ============================================================
echo.

echo [1/4] Έλεγχος Python...
where python >nul 2>&1
if errorlevel 1 (
    echo ❌ Δεν βρέθηκε Python στο PATH.
    echo    Κατεβάστε την από: https://www.python.org/downloads/
    pause
    exit /b 1
)
python --version

echo.
echo [2/4] Δημιουργία virtual environment...
if not exist ".venv\Scripts\python.exe" (
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Αποτυχία δημιουργίας virtual environment.
        pause
        exit /b 1
    )
)

echo.
echo [3/4] Εγκατάσταση dependencies...
"%CD%\.venv\Scripts\python.exe" -m pip install --upgrade pip
"%CD%\.venv\Scripts\python.exe" -m pip install pandas numpy openpyxl xlrd requests
if errorlevel 1 (
    echo ❌ Αποτυχία εγκατάστασης dependencies.
    pause
    exit /b 1
)

echo.
echo [4/4] Έλεγχος και δημιουργία δομής φακέλων...
"%CD%\.venv\Scripts\python.exe" config.py
if errorlevel 1 (
    echo ❌ Σφάλμα κατά τον έλεγχο ρυθμίσεων.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo ✅ Η εγκατάσταση ολοκληρώθηκε!
echo Επόμενα βήματα:
echo 1. Τοποθετήστε το zero.xlsx στο φάκελο που ορίζει το config.py.
echo 2. Τρέξτε το run_gui.bat ή το python main.py.
echo ============================================================
echo.
pause
