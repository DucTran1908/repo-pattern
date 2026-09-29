@echo off
setlocal
rem Windows launcher; leaves stdin untouched for Python and changes no system policy.
set "PYTHONDONTWRITEBYTECODE=1"
set "PYTHONIOENCODING=utf-8"
python -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>nul
if not errorlevel 1 (
  python -B "%~dp0dispatch.py"
  exit /b
)
python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>nul
if not errorlevel 1 (
  python3 -B "%~dp0dispatch.py"
  exit /b
)
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)" >nul 2>nul
if not errorlevel 1 (
  py -3 -B "%~dp0dispatch.py"
  exit /b
)
echo {"systemMessage":"Codex project hooks unavailable: Python 3.8+ not found. Workflow rules still apply; no enforcement claimed."}
exit /b 0
