DBF to Excel - Windows Offline Version

Easy GUI usage:

1. Double-click dbf-to-excel-gui.exe.
2. Click Select DBF Files.
3. Choose the output folder.
4. Click Start Convert.
5. After conversion, open the Excel file or output folder from the app.

Batch folder usage:

1. Put DBF files in the input folder.
2. Double-click convert.bat.
3. Excel files will be created in the output folder.

If Chinese text is garbled:

Open the app and change Encoding from cp950 to big5 or utf-8, then convert again.

For convert.bat, edit this part:

-e cp950

Change it to:

-e big5

or:

-e utf-8
