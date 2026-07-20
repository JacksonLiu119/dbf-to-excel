DBF 轉 Excel - Windows 離線版

最簡單使用方式：

1. 雙擊 轉換程式.exe。
2. 按「選擇 DBF 檔案」。
3. 選擇輸出資料夾。
4. 按「開始轉換」。
5. 轉換完成後，可在程式中按「開啟 Excel」或「開啟輸出資料夾」。

批次資料夾使用方式：

1. 把 DBF 檔案放到 input 資料夾。
2. 雙擊 convert.bat。
3. Excel 檔案會產生在 output 資料夾。

如果中文亂碼：

請在程式右上角把編碼從 cp950 改成 big5 或 utf-8，然後重新轉換。

如果使用 convert.bat，請用記事本打開 convert.bat，把這一段：

-e cp950

改成：

-e big5

或：

-e utf-8
