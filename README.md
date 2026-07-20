# DBF to Excel

This project provides two DBF to Excel converters:

- Web version: open the GitHub Pages site and convert smaller DBF files in the browser.
- Windows offline version: download the packaged ZIP from GitHub Actions and convert larger DBF files on the customer's PC.

## Web Version

GitHub Pages:

https://jacksonliu119.github.io/dbf-to-excel/

The browser version does not upload DBF files to a server. Conversion happens locally in the browser.

## Windows Offline Version for Customers

Customers do not need to install Python.

1. Open the GitHub repository.
2. Go to `Actions`.
3. Open the latest `Build Windows EXE` run.
4. Download the `dbf-to-excel-windows` artifact.
5. Unzip `dbf-to-excel-windows.zip`.
6. Double-click `dbf-to-excel-gui.exe`.
7. Click `選擇 DBF 檔案` and choose DBF files.
8. Choose the output folder.
9. Click `開始轉換`.
10. After conversion, click `開啟 Excel` or `開啟輸出資料夾`.

The ZIP also includes `convert.bat` for batch conversion from the `input` folder to the `output` folder.

## Notes

- Common Taiwan DBF encoding is `cp950` or `big5`.
- Excel supports 1,048,576 rows per sheet. The offline converter automatically creates additional sheets when needed.
- If a DBF uses memo files such as `.dbt` or `.fpt`, keep those files in the same folder as the DBF.
