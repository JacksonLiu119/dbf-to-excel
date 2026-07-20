@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -m pip install -r requirements.txt pyinstaller
  py -m PyInstaller --onefile --name dbf-to-excel dbf_to_excel.py
) else (
  python -m pip install -r requirements.txt pyinstaller
  python -m PyInstaller --onefile --name dbf-to-excel dbf_to_excel.py
)
pause
