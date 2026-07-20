@echo off
setlocal
cd /d "%~dp0"
if not exist input mkdir input
if not exist output mkdir output
where py >nul 2>nul
if %errorlevel%==0 (
  py dbf_to_excel.py input -o output -e cp950
) else (
  python dbf_to_excel.py input -o output -e cp950
)
pause
