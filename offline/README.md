# Offline DBF to Excel

For customer delivery, use the GitHub Actions ZIP package. Customers do not need to install Python.

The packaged ZIP includes:

- `轉換程式.exe`: Windows GUI converter.
- `dbf-to-excel.exe`: command-line converter.
- `convert.bat`: batch conversion helper.
- `input`: folder for batch DBF input.
- `output`: folder for batch Excel output.

## Developer Usage

Install Python 3.11 or newer, then run:

```powershell
python -m pip install -r requirements.txt
```

Single file:

```powershell
python dbf_to_excel.py C:\path\file.dbf -o C:\path\output -e cp950
```

Folder:

```powershell
python dbf_to_excel.py C:\path\dbf-folder -o C:\path\output -e cp950
```

GUI:

```powershell
python dbf_to_excel_gui.py
```

## Build EXE Locally

```powershell
build_exe.bat
```

## Encoding

Common values:

- `cp950`: common Traditional Chinese DBF encoding on Windows.
- `big5`: Big5.
- `utf-8`: UTF-8.

## Large Files

- The converter writes Excel files in streaming mode.
- Excel supports 1,048,576 rows per sheet.
- When the row limit is reached, the converter automatically creates another sheet.
