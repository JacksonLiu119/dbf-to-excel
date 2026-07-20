# DBF 轉 Excel

這是一個純前端 DBF 轉 Excel 工具。使用者在瀏覽器選擇 `.dbf` 檔案後，程式會在本機解析 DBF 並下載 `.xlsx`，檔案不會上傳到伺服器。

## 使用方式

1. 開啟 `index.html`，或部署到 GitHub Pages。
2. 選擇中文編碼，台灣常見 DBF 通常使用 `Big5 / CP950`。
3. 選擇一個或多個 `.dbf` 檔案。
4. 按下「轉換並下載 Excel」。

## GitHub Pages 部署

1. 將這個資料夾推到 GitHub repository。
2. 到 repository 的 `Settings`。
3. 進入 `Pages`。
4. Source 選 `Deploy from a branch`。
5. Branch 選 `main`，資料夾選 `/root`。
6. 儲存後等待 GitHub 產生網站網址。

## 注意事項

- 支援常見 dBase DBF 欄位：文字、數字、日期、邏輯值。
- 若中文亂碼，請切換編碼後重新轉換。
- 若 DBF 使用外部 memo 檔，例如 `.dbt` 或 `.fpt`，memo 內容不會被轉入 Excel。

## 離線版

如果 DBF 檔案很大，建議使用 `offline` 資料夾內的 Python 離線版。它支援批次轉換整個資料夾，並且在 Excel 列數超過上限時自動分工作表。

## 給客戶使用的 Windows 版

GitHub Actions 會自動產生 `dbf-to-excel-windows.zip`。客戶不需要安裝 Python：

1. 到 GitHub repository 的 `Actions`。
2. 點選最新的 `Build Windows EXE`。
3. 下載 `dbf-to-excel-windows` artifact。
4. 解壓縮 `dbf-to-excel-windows.zip`。
5. 把 DBF 放進 `input`。
6. 雙擊 `convert.bat`。
7. Excel 會產生在 `output`。
