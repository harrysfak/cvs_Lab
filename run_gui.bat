REM ============================================================
REM   MILK DATA PROCESSOR - WINDOWS BATCH SCRIPTS
REM   Τοποθετήστε αυτά τα scripts στον φάκελο:
REM   C:\Users\mpamp\Υπολογιστής\csv_Lab
REM ============================================================

REM ============================================================
REM FILE: run_gui.bat
REM Εκτελεί την GUI εφαρμογή
REM ============================================================
@echo off
title Milk Data Processor - GUI
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     MILK DATA PROCESSOR - GUI                            ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Εκκίνηση GUI εφαρμογής...
echo.
python gui_app.py
if errorlevel 1 (
    echo.
    echo ❌ Σφάλμα εκτέλεσης!
    echo    Ελέγξτε αν η Python και τα modules είναι εγκατεστημένα.
    echo.
    pause
) else (
    echo.
    echo ✅ Η εφαρμογή τερματίστηκε κανονικά.
)
pause


REM ============================================================
REM FILE: run_cli.bat
REM Εκτελεί την CLI εφαρμογή
REM ============================================================
@echo off
title Milk Data Processor - CLI
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     MILK DATA PROCESSOR - COMMAND LINE                   ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
python main.py
if errorlevel 1 (
    echo.
    echo ❌ Σφάλμα εκτέλεσης!
    pause
)


REM ============================================================
REM FILE: install.bat
REM Εγκατάσταση dependencies και έλεγχος
REM ============================================================
@echo off
title Milk Data Processor - Installation
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     MILK DATA PROCESSOR - INSTALLATION                   ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Έλεγχος Python
echo [1/5] Έλεγχος Python...
python --version
if errorlevel 1 (
    echo ❌ Python δεν βρέθηκε!
    echo    Παρακαλώ εγκαταστήστε Python από https://www.python.org
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

REM Έλεγχος pip
echo [2/5] Έλεγχος pip...
pip --version
if errorlevel 1 (
    echo ❌ pip δεν βρέθηκε!
    pause
    exit /b 1
)
echo ✅ pip OK
echo.

REM Εγκατάσταση dependencies
echo [3/5] Εγκατάσταση dependencies...
echo    Αυτό μπορεί να πάρει λίγα λεπτά...
echo.
pip install pandas numpy openpyxl xlrd
if errorlevel 1 (
    echo ❌ Αποτυχία εγκατάστασης!
    pause
    exit /b 1
)
echo ✅ Dependencies εγκαταστάθηκαν
echo.

REM Έλεγχος imports
echo [4/5] Έλεγχος imports...
python -c "import pandas; print('  ✅ pandas')"
python -c "import numpy; print('  ✅ numpy')"
python -c "import openpyxl; print('  ✅ openpyxl')"
python -c "import xlrd; print('  ✅ xlrd')"
python -c "import tkinter; print('  ✅ tkinter')"
echo.

REM Έλεγχος δομής
echo [5/5] Έλεγχος δομής φακέλων...
if not exist "modules" mkdir modules
if not exist "CSV" mkdir CSV
if not exist "CSV\parts" mkdir "CSV\parts"
if not exist "CSV\zero" mkdir "CSV\zero"
echo ✅ Δομή φακέλων OK
echo.

echo ════════════════════════════════════════════════════════════
echo    ΕΓΚΑΤΑΣΤΑΣΗ ΟΛΟΚΛΗΡΩΘΗΚΕ!
echo ════════════════════════════════════════════════════════════
echo.
echo Επόμενα βήματα:
echo 1. Τοποθετήστε το zero.xlsx στο CSV\zero\
echo 2. Τοποθετήστε τα Excel αρχεία στο CSV\
echo 3. Τρέξτε το run_gui.bat
echo.
pause


REM ============================================================
REM FILE: check_config.bat
REM Ελέγχει την configuration
REM ============================================================
@echo off
title Milk Data Processor - Check Config
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     MILK DATA PROCESSOR - CHECK CONFIG                   ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
python config.py
echo.
pause


REM ============================================================
REM FILE: open_folders.bat
REM Ανοίγει τους σημαντικούς φακέλους
REM ============================================================
@echo off
title Milk Data Processor - Open Folders
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo Άνοιγμα φακέλων...
echo.

REM Άνοιγμα CSV folder
if exist "CSV" (
    echo ✅ Άνοιξε: CSV\
    start explorer "CSV"
) else (
    echo ❌ Δεν βρέθηκε: CSV\
)

REM Άνοιγμα zero folder
if exist "CSV\zero" (
    echo ✅ Άνοιξε: CSV\zero\
    timeout /t 1 >nul
    start explorer "CSV\zero"
) else (
    echo ❌ Δεν βρέθηκε: CSV\zero\
)

REM Άνοιγμα parts folder
if exist "CSV\parts" (
    echo ✅ Άνοιξε: CSV\parts\
    timeout /t 1 >nul
    start explorer "CSV\parts"
) else (
    echo ❌ Δεν βρέθηκε: CSV\parts\
)

echo.
echo Οι φάκελοι άνοιξαν!
timeout /t 3


REM ============================================================
REM FILE: clean_output.bat
REM Καθαρίζει τα output files
REM ============================================================
@echo off
title Milk Data Processor - Clean Output
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     ΚΑΘΑΡΙΣΜΟΣ OUTPUT FILES                              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo ΠΡΟΣΟΧΗ: Θα διαγραφούν όλα τα output files!
echo.
set /p confirm="Είστε σίγουροι; (y/n): "
if /i not "%confirm%"=="y" (
    echo Ακύρωση...
    timeout /t 2
    exit /b
)

echo.
echo Διαγραφή files...

REM Διαγραφή final.csv
if exist "CSV\final.csv" (
    del "CSV\final.csv"
    echo ✅ Διαγράφηκε: final.csv
)

REM Διαγραφή parts
if exist "CSV\parts\*.csv" (
    del "CSV\parts\*.csv"
    echo ✅ Διαγράφηκε: parts\*.csv
)

REM Διαγραφή zero.csv αν υπάρχει
if exist "CSV\zero.csv" (
    del "CSV\zero.csv"
    echo ✅ Διαγράφηκε: zero.csv
)

echo.
echo ✅ Καθαρισμός ολοκληρώθηκε!
timeout /t 3


REM ============================================================
REM FILE: test_module.bat
REM Δοκιμάζει ένα συγκεκριμένο module
REM ============================================================
@echo off
title Milk Data Processor - Test Module
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║     TEST MODULE                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Επιλέξτε module για test:
echo.
echo 1. config.py
echo 2. data_loader.py
echo 3. data_processor.py
echo 4. time_handler.py
echo 5. zero_data_manager.py
echo 6. output_generator.py
echo.
set /p choice="Επιλογή (1-6): "

if "%choice%"=="1" (
    python config.py
) else if "%choice%"=="2" (
    python -m modules.data_loader
) else if "%choice%"=="3" (
    python -m modules.data_processor
) else if "%choice%"=="4" (
    python -m modules.time_handler
) else if "%choice%"=="5" (
    python -m modules.zero_data_manager
) else if "%choice%"=="6" (
    python -m modules.output_generator
) else (
    echo Μη έγκυρη επιλογή!
)

echo.
pause


REM ============================================================
REM FILE: create_desktop_shortcut.bat
REM Δημιουργεί shortcut στο Desktop
REM ============================================================
@echo off
title Create Desktop Shortcut
cd /d "C:\Users\mpamp\Υπολογιστής\csv_Lab"
echo.
echo Δημιουργία Desktop Shortcut...
echo.

set SCRIPT="%TEMP%\create_shortcut.vbs"
echo Set oWS = WScript.CreateObject("WScript.Shell") > %SCRIPT%
echo sLinkFile = "%USERPROFILE%\Desktop\Milk Data Processor.lnk" >> %SCRIPT%
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> %SCRIPT%
echo oLink.TargetPath = "%~dp0run_gui.bat" >> %SCRIPT%
echo oLink.WorkingDirectory = "%~dp0" >> %SCRIPT%
echo oLink.Description = "Milk Data Processor GUI" >> %SCRIPT%
echo oLink.Save >> %SCRIPT%

cscript /nologo %SCRIPT%
del %SCRIPT%

echo ✅ Shortcut δημιουργήθηκε στο Desktop!
echo.
timeout /t 3


REM ============================================================
REM FILE: view_help.bat
REM Εμφανίζει help information
REM ============================================================
@echo off
title Milk Data Processor - Help
cls
echo.
echo ╔══════════════════════════════════════════════════════════════════╗
echo ║               MILK DATA PROCESSOR - HELP                         ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo ΔΙΑΘΕΣΙΜΑ SCRIPTS:
echo.
echo   run_gui.bat                - Εκκίνηση GUI εφαρμογής
echo   run_cli.bat                - Εκκίνηση CLI εφαρμογής
echo   install.bat                - Εγκατάσταση dependencies
echo   check_config.bat           - Έλεγχος configuration
echo   open_folders.bat           - Άνοιγμα φακέλων
echo   clean_output.bat           - Καθαρισμός output files
echo   test_module.bat            - Test συγκεκριμένου module
echo   create_desktop_shortcut.bat - Δημιουργία Desktop shortcut
echo.
echo ΔΟΜΗ ΦΑΚΕΛΩΝ:
echo.
echo   csv_Lab\
echo   ├── modules\              (Python modules)
echo   ├── CSV\                  (Excel input files)
echo   │   ├── parts\           (Ενδιάμεσα files)
echo   │   ├── zero\            (zero.xlsx)
echo   │   └── final.csv        (Output)
echo   ├── config.py
echo   ├── main.py
echo   └── gui_app.py
echo.
echo ΧΡΗΣΙΜΕΣ ΕΝΤΟΛΕΣ:
echo.
echo   python --version         - Έλεγχος Python version
echo   pip list                 - Λίστα εγκατεστημένων packages
echo   python config.py         - Test configuration
echo   python gui_app.py        - Εκκίνηση GUI
echo   python main.py           - Εκκίνηση CLI
echo.
echo ΔΙΑΔΡΟΜΗ ΕΓΚΑΤΑΣΤΑΣΗΣ:
echo   C:\Users\mpamp\Υπολογιστής\csv_Lab
echo.
echo ══════════════════════════════════════════════════════════════════
pause
