DBF 轉 Excel 離線版

使用方式：

1. 把 DBF 檔案放到 input 資料夾。
2. 雙擊 convert.bat。
3. 轉好的 Excel 會在 output 資料夾。

如果中文亂碼：

請用記事本打開 convert.bat，把這一段：

-e cp950

改成：

-e big5

或：

-e utf-8

再重新執行 convert.bat。
