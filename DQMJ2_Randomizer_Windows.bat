@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

:: 1. FIND PYTHON PATH IN THE PATH VARIABLE
for /f "delims=" %%I in ('where python.exe 2^>nul') do (
    set "PYTHON_EXE=%%I"
    goto :found
)

:found
if not defined PYTHON_EXE (
    echo [ERROR] Python was not found in your Windows PATH.
    echo Make sure Python is installed and added to your PATH.
    pause
    exit /b
)

:: Extract the directory only (remove "python.exe" from the end)
for %%F in ("%PYTHON_EXE%") do set "PYTHON_DIR=%%~dpF"
:: Remove the trailing backslash "\" for the cfg file
set "PYTHON_DIR=%PYTHON_DIR:~0,-1%"

:: 2. UPDATE THE PYVENV.CFG FILE
set "CFG_FILE=venv\pyvenv.cfg"

if not exist "%CFG_FILE%" (
    echo [ERROR] The file %CFG_FILE% was not found.
    pause
    exit /b
)

echo [INFO] Global Python found: %PYTHON_DIR%
echo [INFO] Updating pyvenv.cfg file...

:: Recreate the cfg file with the correct home path
set "TEMP_CFG=%CFG_FILE%.tmp"
type nul > "%TEMP_CFG%"

for /f "usebackq delims=" %%L in ("%CFG_FILE%") do (
    set "LINE=%%L"
    if "!LINE:~0,4!"=="home" (
        echo home = %PYTHON_DIR%>> "%TEMP_CFG%"
    ) else (
        echo !LINE!>> "%TEMP_CFG%"
    )
)

move /y "%TEMP_CFG%" "%CFG_FILE%" >nul

:: 3. ORIGINAL SCRIPT EXECUTION
echo [INFO] Starting main.py via the venv...
venv\Scripts\python.exe main.py
pause
endlocal