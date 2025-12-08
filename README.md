# RFDrawing - Risk Factor Chain Drawing Tool

這個工具可以將團隊整理好的 Excel 因子鏈（Nodes & Edges）
自動轉換為 Graphviz 架構圖。

## 專案結構

- src/
  - rf_drawing_gui.py    主 GUI 程式
  - excel_to_dot.py      Excel → DOT 邏輯
  - graph_config.py      顏色與共用 Graphviz 設定
- resources/
  - image.png            Logo / Icon（請自行放入）
  - FloodFactorChain_Template.xlsx  範本 Excel（請自行放入）
- graphviz-win/bin/      portable Windows Graphviz (dot.exe 等)
- graphviz-mac/bin/      portable macOS Graphviz (dot 等)
- config/
  - config.ini           基本設定
- build_scripts/
  - pyinstaller_win.bat  Windows 打包腳本
  - pyinstaller_mac.sh   macOS 打包腳本
- requirements.txt       開發環境所需套件
