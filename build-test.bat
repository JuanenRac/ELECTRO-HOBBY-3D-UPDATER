@echo off
REM ELECTRO-HOBBY-3D-UPDATER - build-test.bat
REM Non-mutating build verification: same install as build.bat, then the
REM real pytest suite. Never bumps a version or writes CHANGELOG.md.
REM GPL-3.0-or-later.
cd /d "%~dp0"

if not exist .venv (
    python -m venv .venv
    if errorlevel 1 ( echo VENV CREATION FAILED. & pause & exit /b 1 )
)
call .venv\Scripts\activate.bat
if errorlevel 1 ( echo VENV ACTIVATION FAILED. & pause & exit /b 1 )

python -m pip install -e ".[dev]"
if errorlevel 1 ( echo DEPENDENCY INSTALL FAILED. & pause & exit /b 1 )

python -m pytest tests -q
if errorlevel 1 ( echo TESTS FAILED. & pause & exit /b 1 )

echo BUILD_TEST_RESULT=PASS
pause
