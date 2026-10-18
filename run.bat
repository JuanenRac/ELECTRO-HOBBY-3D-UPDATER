@echo off
rem Keep the window open for people, never in automation (CI / HYDRA_UMC_CI).
set "KEEP_OPEN=pause"
if defined CI set "KEEP_OPEN=ver >nul"
if "%HYDRA_UMC_CI%"=="1" set "KEEP_OPEN=ver >nul"
REM ELECTRO-HOBBY-3D-UPDATER - run.bat
REM Opens the window (no arguments) or runs the CLI. Build first (build.bat) at least once per checkout.
REM
REM Usage:
REM   run.bat status --ecosystem all              - check every ecosystem
REM   run.bat status --ecosystem armor             - check just one
REM   run.bat install --ecosystem urtc <PROJECT>   - clone + build one project
REM   run.bat update  --ecosystem hydra-umc <PROJECT> - pull + rebuild one project
REM GPL-3.0-or-later.
cd /d "%~dp0"

REM No arguments (a double click) opens the window; with arguments this is the
REM command line, exactly as before (a wrong command gets argparse's own error).
set "ARGS=%*"

if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe -m electro_hobby_3d_updater.main %ARGS%
) else (
    python -m electro_hobby_3d_updater.main %ARGS%
)

%KEEP_OPEN%
