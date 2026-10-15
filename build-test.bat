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

REM Dependencies are installed only when pyproject.toml changed since the
REM last run (see build-test.sh); otherwise only this project is relinked.
for /f "usebackq delims=" %%H in (`python -c "import hashlib; print(hashlib.sha256(open('pyproject.toml','rb').read()).hexdigest())"`) do set "WANT=%%H"
set "HAVE="
if exist .venv\.deps-installed set /p HAVE=<.venv\.deps-installed
if not "%HAVE%"=="%WANT%" (
    python -m pip install -e ".[dev]"
    if errorlevel 1 ( echo DEPENDENCY INSTALL FAILED. & pause & exit /b 1 )
    > .venv\.deps-installed echo %WANT%
) else (
    python -m pip install --no-deps -e . >nul
    if errorlevel 1 ( echo PROJECT INSTALL FAILED. & pause & exit /b 1 )
)

python -m pytest tests -q
if errorlevel 1 ( echo TESTS FAILED. & pause & exit /b 1 )

echo BUILD_TEST_RESULT=PASS
pause
