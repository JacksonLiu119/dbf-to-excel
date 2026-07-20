import os
import subprocess
import sys
import threading
from pathlib import Path
from tkinter import BOTH, END, LEFT, RIGHT, Button, Frame, Label, Listbox, StringVar, Tk
from tkinter import filedialog, messagebox, ttk

from dbf_to_excel import convert_dbf


class DbfToExcelApp:
    def __init__(self, root: Tk) -> None:
        self.root = root
        self.root.title("DBF 轉 Excel")
        self.root.geometry("760x520")
        self.root.minsize(680, 460)

        self.files: list[Path] = []
        self.output_dir = StringVar(value=str(Path.cwd() / "output"))
        self.encoding = StringVar(value="cp950")
        self.status = StringVar(value="請選擇 DBF 檔案。")
        self.last_outputs: list[Path] = []

        self.build_ui()

    def build_ui(self) -> None:
        container = Frame(self.root, padx=18, pady=16)
        container.pack(fill=BOTH, expand=True)

        Label(container, text="DBF 轉 Excel", font=("Microsoft JhengHei UI", 20, "bold")).pack(anchor="w")
        Label(
            container,
            text="選擇 DBF 檔案後在本機轉成 Excel，檔案不會上傳。",
            font=("Microsoft JhengHei UI", 10),
        ).pack(anchor="w", pady=(4, 14))

        toolbar = Frame(container)
        toolbar.pack(fill="x", pady=(0, 10))

        Button(toolbar, text="選擇 DBF 檔案", command=self.choose_files, width=16).pack(side=LEFT)
        Button(toolbar, text="清除", command=self.clear_files, width=10).pack(side=LEFT, padx=(8, 0))

        encoding_frame = Frame(toolbar)
        encoding_frame.pack(side=RIGHT)
        Label(encoding_frame, text="編碼").pack(side=LEFT, padx=(0, 6))
        ttk.Combobox(
            encoding_frame,
            textvariable=self.encoding,
            values=["cp950", "big5", "utf-8", "gb18030", "windows-1252"],
            width=14,
            state="readonly",
        ).pack(side=LEFT)

        self.file_list = Listbox(container, height=10)
        self.file_list.pack(fill=BOTH, expand=True)

        output_frame = Frame(container)
        output_frame.pack(fill="x", pady=(12, 8))
        Label(output_frame, text="輸出資料夾").pack(anchor="w")

        output_row = Frame(output_frame)
        output_row.pack(fill="x", pady=(4, 0))
        Label(output_row, textvariable=self.output_dir, relief="sunken", anchor="w").pack(
            side=LEFT, fill="x", expand=True, ipady=6
        )
        Button(output_row, text="選擇", command=self.choose_output, width=10).pack(
            side=RIGHT, padx=(8, 0)
        )

        action_row = Frame(container)
        action_row.pack(fill="x", pady=(8, 8))
        self.convert_button = Button(
            action_row,
            text="開始轉換",
            command=self.start_convert,
            width=16,
            state="disabled",
        )
        self.convert_button.pack(side=LEFT)
        self.open_file_button = Button(
            action_row,
            text="開啟 Excel",
            command=self.open_last_file,
            width=14,
            state="disabled",
        )
        self.open_file_button.pack(side=LEFT, padx=(8, 0))
        Button(
            action_row,
            text="開啟輸出資料夾",
            command=self.open_output_folder,
            width=18,
        ).pack(side=LEFT, padx=(8, 0))

        Label(container, textvariable=self.status, anchor="w").pack(fill="x")

    def choose_files(self) -> None:
        paths = filedialog.askopenfilenames(
            title="選擇 DBF 檔案",
            filetypes=[("DBF 檔案", "*.dbf"), ("所有檔案", "*.*")],
        )
        if not paths:
            return

        for path in paths:
            file_path = Path(path)
            if file_path not in self.files:
                self.files.append(file_path)

        self.refresh_file_list()

    def clear_files(self) -> None:
        self.files.clear()
        self.last_outputs.clear()
        self.refresh_file_list()
        self.open_file_button.config(state="disabled")
        self.status.set("請選擇 DBF 檔案。")

    def choose_output(self) -> None:
        path = filedialog.askdirectory(title="選擇輸出資料夾")
        if path:
            self.output_dir.set(path)

    def refresh_file_list(self) -> None:
        self.file_list.delete(0, END)
        for path in self.files:
            self.file_list.insert(END, str(path))

        self.convert_button.config(state="normal" if self.files else "disabled")
        self.status.set(f"已選擇 {len(self.files)} 個 DBF 檔案。" if self.files else "請選擇 DBF 檔案。")

    def start_convert(self) -> None:
        if not self.files:
            return

        self.convert_button.config(state="disabled")
        self.open_file_button.config(state="disabled")
        self.status.set("轉換中，請稍候...")
        threading.Thread(target=self.convert_files, daemon=True).start()

    def convert_files(self) -> None:
        try:
            output_dir = Path(self.output_dir.get())
            outputs = [
                convert_dbf(dbf_file, output_dir, self.encoding.get())
                for dbf_file in self.files
            ]
            self.last_outputs = outputs
            self.root.after(0, self.convert_success)
        except Exception as exc:
            self.root.after(0, lambda: self.convert_failed(exc))

    def convert_success(self) -> None:
        self.convert_button.config(state="normal")
        self.open_file_button.config(state="normal" if self.last_outputs else "disabled")
        self.status.set(f"轉換完成，共產生 {len(self.last_outputs)} 個 Excel 檔案。")
        messagebox.showinfo("轉換完成", "Excel 檔案已產生。")

    def convert_failed(self, exc: Exception) -> None:
        self.convert_button.config(state="normal" if self.files else "disabled")
        self.status.set("轉換失敗。")
        messagebox.showerror("轉換失敗", str(exc))

    def open_last_file(self) -> None:
        if self.last_outputs:
            self.open_path(self.last_outputs[-1])

    def open_output_folder(self) -> None:
        output = Path(self.output_dir.get())
        output.mkdir(parents=True, exist_ok=True)
        self.open_path(output)

    def open_path(self, path: Path) -> None:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", str(path)])
        else:
            subprocess.Popen(["xdg-open", str(path)])


def main() -> None:
    root = Tk()
    DbfToExcelApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
