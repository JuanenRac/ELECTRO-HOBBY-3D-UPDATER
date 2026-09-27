@echo off
REM ELECTRO-HOBBY-3D-UPDATER - run.bat
REM Runs the CLI. Build first (build.bat) at least once per checkout.
REM
REM Usage:
REM   run.bat status --ecosystem all              - check every ecosystem
REM   run.bat status --ecosystem armor             - check just one
REM   run.bat install --ecosystem urtc <PROJECT>   - clone + build one project
REM   run.bat update  --ecosystem hydra-umc <PROJECT> - pull + rebuild one project
REM GPL-3.0-or-later.
cd /d "%~dp0"

REM `action` is a required subcommand (see main.py's own argparse setup) -
REM a bare double-click passes zero arguments, which used to fail with a
REM raw "the following arguments are required: action" error instead of
REM doing anything useful. Default to the tool's own first documented
REM example (a read-only status check of all three ecosystems) instead;
REM any real argument list, right or wrong, is still passed through
REM unchanged so a real CLI mistake still gets argparse's own real error.
set "ARGS=%*"
if "%ARGS%"=="" set "ARGS=status --ecosystem all"

if exist .venv\Scripts\python.exe (
    .venv\Scripts\python.exe -m electro_hobby_3d_updater.main %ARGS%
) else (
    python -m electro_hobby_3d_updater.main %ARGS%
)

pause
