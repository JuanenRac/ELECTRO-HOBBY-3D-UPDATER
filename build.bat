@echo off
rem Keep the window open for people, never in automation (CI / HYDRA_UMC_CI).
set "KEEP_OPEN=pause"
if defined CI set "KEEP_OPEN=ver >nul"
if "%HYDRA_UMC_CI%"=="1" set "KEEP_OPEN=ver >nul"
REM ELECTRO-HOBBY-3D-UPDATER - build.bat
REM Creates/uses a project-local .venv, installs this project plus its three
REM real ecosystem-updater dependencies (from GitHub) in editable mode, then
REM compile-checks every module. GPL-3.0-or-later.
cd /d "%~dp0"

if not exist .venv (
    python -m venv .venv
    if errorlevel 1 ( echo VENV CREATION FAILED. & %KEEP_OPEN% & exit /b 1 )
)
call .venv\Scripts\activate.bat
if errorlevel 1 ( echo VENV ACTIVATION FAILED. & %KEEP_OPEN% & exit /b 1 )

python -m pip install -e ".[dev,gui]"
if errorlevel 1 ( echo DEPENDENCY INSTALL FAILED. & %KEEP_OPEN% & exit /b 1 )

python -m compileall -q src
if errorlevel 1 ( echo COMPILE CHECK FAILED. & %KEEP_OPEN% & exit /b 1 )

echo BUILD_RESULT=PASS
%KEEP_OPEN%
