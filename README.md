# RFDrawing – Risk Framework Drawing Tool

RFDrawing 是一個將 Excel 定義的 **Nodes / Edges 因子鏈**
自動轉換為 **Graphviz DOT 架構圖 + PNG 圖形** 的工具。

---

# 1. Project Structure

```
RFDrawing/
├── build/
│   ├── mac_build.sh
│   └── win_bulid.bat
├── Example/
│   ├── Flood_Risk_Template.dot
│   ├── Flood_Risk_Template.png
│   └── Flood_Risk_Template.xlsx
├── Executable/
│   ├── MacOS/
│   │   └── RFDrawing.app
│   └── Windows/
│       ├── graphviz-win/
│       └── RFDrawing.exe
├── requirements.txt
├── README.md
└── src/
    ├── MacOS/
    │   ├── excel_to_dot.py
    │   ├── graph_config.py
    │   └── rf_drawing_gui.py
    └── Windows/
        ├── excel_to_dot.py
        ├── graph_config.py
        └── rf_drawing_gui.py
```

---

# 2. Installation & Execution

## macOS

macOS 版需要系統已安裝 Graphviz (需先安裝Homebrew: https://docs.brew.sh/Installation )：

```bash
brew install graphviz
```

執行：

```
Executable/MacOS/RFDrawing.app
```

> macOS 版使用系統 Graphviz，不包含 portable 版本。

---

## Windows

直接執行：

```
Executable/Windows/RFDrawing.exe
```

Windows 版內含：

```
Executable/Windows/graphviz-win/
```

無須另行安裝 Graphviz。

---

# 3. Using the App

1. 開啟 RFDrawing（Mac / Windows）
2. 按 **Select Excel** 選擇資料來源
3. 按 **Generate DOT & PNG**
4. 程式將產生：
   - `{filename}.dot`
   - `{filename}.png`
5. 圖片會在 GUI 中自動預覽

---

# 4. Excel Template Format

Template 必須包含兩個 Sheets：

```
Nodes
Edges
```

範例見：

```
Example/Flood_Risk_Template.xlsx
```

---

## 4.1 Nodes Sheet（必填欄位）

| Column      | Required | Example                  | Description |
|-------------|----------|---------------------------|-------------|
| NodeID      | Yes      | H1, E3, V2                | 節點唯一識別碼 |
| Label       | Yes      | Extreme Rainfall          | 節點顯示文字（支援中文） |
| Category    | Yes      | Hazard, Exposure, Risk…   | 決定節點顏色 |


---

## 4.2 Edges Sheet（必填欄位）

| Column    | Required | Example | Description |
|-----------|----------|---------|-------------|
| FromNode  | Yes      | H1      | 起點節點 |
| ToNode    | Yes      | E1      | 終點節點 |
| Style     | Optional | dashed / bold | 虛線或粗線 |

Edges Sheet 中所有 NodeID 必須存在於 Nodes Sheet。

---

# 5. Example Outputs

Example 資料夾包含：

- Flood_Risk_Template.xlsx
- Flood_Risk_Template.dot
- Flood_Risk_Template.png
![image](https://github.com/SYLeeTW/RFDrawing/blob/main/Example/Flood_Risk_Template.png)

---

# 6. Requirements (For Development)

```
pandas
openpyxl
Pillow
pyinstaller
```

---

# 7. License

## License Notice for Graphviz
This project uses Graphviz for graph rendering.
For the Windows executable, this project distributes Graphviz binaries.
Graphviz is licensed under the **Common Public License Version 1.0 (CPL-1.0)**.
For more information, see:  
Graphviz © AT&T Research and contributors.  
https://graphviz.org/license/
