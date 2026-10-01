@echo off
REM ELECTRO-HOBBY-3D-UPDATER - build.bat
REM Creates/uses a project-local .venv, installs this project plus its three
REM real ecosystem-updater dependencies (from GitHub) in editable mode, then
REM compile-checks every module. GPL-3.0-or-later.
cd /d "%~dp0"

if not exist .venv (
    python -m venv .venv
    if errorlevel 1 ( echo VENV CREATION FAILED. & pause & exit /b 1 )
)
call .venv\Scripts\activate.bat
if errorlevel 1 ( echo VENV ACTIVATION FAILED. & pause & exit /b 1 )

python -m pip install -e ".[dev,gui]"
if errorlevel 1 ( echo DEPENDENCY INSTALL FAILED. & pause & exit /b 1 )

python -m compileall -q src
if errorlevel 1 ( echo COMPILE CHECK FAILED. & pause & exit /b 1 )

echo BUILD_RESULT=PASS
pause
