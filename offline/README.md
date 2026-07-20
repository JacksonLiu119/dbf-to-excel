# 離線版 DBF 轉 Excel

這個工具適合處理較大的 DBF 檔案，或一次批次轉換整個資料夾。檔案都在本機處理，不會上傳到網路。

## Windows 使用方式

給客戶使用時，建議下載 GitHub Actions 產生的 `dbf-to-excel-windows.zip`，不需要安裝 Python。以下方式是給開發者或需要自己打包時使用。

1. 安裝 Python 3.11 或更新版本，安裝時勾選 `Add python.exe to PATH`。
2. 第一次使用先執行 `install.bat`。
3. 把 `.dbf` 檔案放進 `input` 資料夾。
4. 執行 `convert.bat`。
5. 轉好的 `.xlsx` 會出現在 `output` 資料夾。

## 命令列使用方式

單一檔案：

```powershell
python dbf_to_excel.py C:\path\file.dbf -o C:\path\output -e cp950
```

整個資料夾：

```powershell
python dbf_to_excel.py C:\path\dbf-folder -o C:\path\output -e cp950
```

常見中文編碼：

- `cp950`：台灣 Big5 常用
- `big5`：Big5
- `utf-8`：UTF-8

## 打包成 exe

執行：

```powershell
build_exe.bat
```

完成後 exe 會在 `dist\dbf-to-excel.exe`。

## 大檔案注意事項

- 程式使用串流寫入 Excel，記憶體用量比瀏覽器版低。
- Excel 單一工作表最多 1,048,576 列；超過時會自動分成多個工作表。
- 如果 DBF 有 `.dbt` 或 `.fpt` memo 檔，請放在 DBF 同一個資料夾。
