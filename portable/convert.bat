@echo off
setlocal
cd /d "%~dp0"
if not exist input mkdir input
if not exist output mkdir output
dbf-to-excel.exe input -o output -e cp950
pause
