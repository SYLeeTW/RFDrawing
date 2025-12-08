"""
rf_drawing_gui.py
Simple GUI:
1. Select Excel (Nodes / Edges)
2. Generate DOT + PNG via Graphviz 'dot'
3. Preview PNG in the window
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path

from PIL import Image, ImageTk
from excel_to_dot import export_graph


# ================ Helpers for locating project root (for future use) ================

def get_project_root() -> Path:
    """
    Root used to locate resources (if needed).

    Development (python rf_drawing_gui.py):
        RFDrawing/ (parent of src)

    Frozen (.app via PyInstaller):
        dist/      (folder containing RFDrawing.app)
    """
    if getattr(sys, "frozen", False):
        exe = Path(sys.executable)
        macos_dir = exe.parent            # .../Contents/MacOS
        contents_dir = macos_dir.parent   # .../Contents
        app_dir = contents_dir.parent     # .../RFDrawing.app
        dist_dir = app_dir.parent         # .../dist
        return dist_dir

    here = Path(__file__).resolve().parent   # .../RFDrawing/src
    return here.parent                       # .../RFDrawing


# ========================= GUI =========================

class RFDrawingApp:
    def __init__(self, master: tk.Tk):
        self.master = master
        master.title("RFDrawing - Risk Factor Chain Drawing")

        self.excel_path: str | None = None
        self.img_tk: ImageTk.PhotoImage | None = None

        top = tk.Frame(master)
        top.pack(padx=10, pady=10, fill=tk.X)

        self.btn_select = tk.Button(top, text="Select Excel", command=self.select_excel)
        self.btn_select.pack(side=tk.LEFT)

        self.btn_generate = tk.Button(
            top, text="Generate DOT & PNG", command=self.generate_graph, state=tk.DISABLED
        )
        self.btn_generate.pack(side=tk.LEFT, padx=5)

        self.lbl_path = tk.Label(master, text="No file selected", anchor="w")
        self.lbl_path.pack(fill=tk.X, padx=10)

        self.canvas = tk.Label(master)
        self.canvas.pack(padx=10, pady=10)

    # ------------- callbacks -------------

    def select_excel(self):
        path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls")],
        )
        if not path:
            return

        self.excel_path = path
        self.lbl_path.config(text=f"Selected: {os.path.basename(path)}")
        self.btn_generate.config(state=tk.NORMAL)

    def generate_graph(self):
        if not self.excel_path:
            messagebox.showwarning("Warning", "Please select an Excel file first.")
            return

        try:
            dot_path, png_path = export_graph(self.excel_path)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate graph:\n{e}")
            return

        # display PNG
        try:
            if os.path.exists(png_path):
                img = Image.open(png_path)
                max_width = 1000
                if img.width > max_width:
                    ratio = max_width / img.width
                    img = img.resize((max_width, int(img.height * ratio)), Image.LANCZOS)

                self.img_tk = ImageTk.PhotoImage(img)
                self.canvas.config(image=self.img_tk)
            else:
                messagebox.showwarning("Warning", "PNG file not found, but DOT was created.")
        except Exception as e:
            messagebox.showwarning("Warning", f"PNG preview failed:\n{e}")

        messagebox.showinfo("Done", f"Generated:\n{dot_path}\n{png_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RFDrawingApp(root)
    root.mainloop()