"""
excel_to_dot.py  (macOS-only version)

1. 從 Excel (Nodes / Edges 工作表) 讀取節點與連結
2. 建立 Graphviz DOT 字串
3. 呼叫系統安裝的 Graphviz `dot` 產生 PNG

前置條件（每台 Mac 只需做一次）:
    brew install graphviz
"""

import sys
import subprocess
from pathlib import Path
from typing import Tuple

import pandas as pd
from graph_config import GRAPH_ATTRS, NODE_ATTRS, EDGE_ATTRS, get_node_color


# ===================== find dot (macOS system only) =====================

def find_dot_executable() -> str:
    """
    macOS version:
    Always use system-installed Graphviz (Homebrew or MacPorts).
    """

    from shutil import which

    # Try system PATH
    sys_dot = which("dot")
    if sys_dot:
        return sys_dot

    # Try common Homebrew path (Apple Silicon)
    hb_path = Path("/opt/homebrew/bin/dot")
    if hb_path.exists():
        return str(hb_path)

    # Try Homebrew (Intel Mac)
    hb_intel = Path("/usr/local/bin/dot")
    if hb_intel.exists():
        return str(hb_intel)

    # Try MacPorts
    mp_path = Path("/opt/local/bin/dot")
    if mp_path.exists():
        return str(mp_path)

    # Nothing found
    raise RuntimeError(
        "Could not find Graphviz 'dot' on this Mac.\n"
        "Please install it first, for example with Homebrew:\n"
        "    brew install graphviz\n"
        "Then try running RFDrawing again."
    )


# ===================== build DOT string =====================

def build_dot_from_excel(
    excel_path: str,
    nodes_sheet: str = "Nodes",
    edges_sheet: str = "Edges",
) -> str:
    """
    從 Excel 讀取節點與連結，回傳 DOT 語言字串。

    必要欄位：
        [Nodes 工作表]
            - NodeID
            - Label
            - Category (可用來決定顏色)

        [Edges 工作表]
            - FromNode
            - ToNode
            - Style (可選: 'dashed', 'bold' 等)
    """
    excel_path = str(excel_path)
    nodes = pd.read_excel(excel_path, sheet_name=nodes_sheet, engine="openpyxl")
    edges = pd.read_excel(excel_path, sheet_name=edges_sheet, engine="openpyxl")

    lines: list[str] = []
    lines.append("digraph G {")

    graph_attr_str = " ".join(f'{k}="{v}"' for k, v in GRAPH_ATTRS.items())
    if graph_attr_str:
        lines.append(f"    graph [{graph_attr_str}];")

    node_attr_str = " ".join(f'{k}="{v}"' for k, v in NODE_ATTRS.items())
    if node_attr_str:
        lines.append(f"    node [{node_attr_str}];")

    edge_attr_str = " ".join(f'{k}="{v}"' for k, v in EDGE_ATTRS.items())
    if edge_attr_str:
        lines.append(f"    edge [{edge_attr_str}];")

    # ---- Nodes ----
    for _, row in nodes.iterrows():
        nid = str(row.get("NodeID", "")).strip()
        if not nid or nid.lower() == "nan":
            continue

        label = str(row.get("Label", nid))
        category = str(row.get("Category", "")).strip()

        color = get_node_color(category)
        label_safe = label.replace('"', '\\"')

        attrs = [f'label="{label_safe}"']
        if color:
            attrs.append('style="filled"')
            attrs.append(f'fillcolor="{color}"')

        attr_str = " ".join(attrs)
        lines.append(f"    {nid} [{attr_str}];")

    # ---- Edges ----
    for _, row in edges.iterrows():
        f = str(row.get("FromNode", "")).strip()
        t = str(row.get("ToNode", "")).strip()
        if not f or not t or f.lower() == "nan" or t.lower() == "nan":
            continue

        style = str(row.get("Style", "")).strip()
        attrs = []
        if style == "dashed":
            attrs.append('style="dashed"')
        elif style == "bold":
            attrs.append('penwidth="2"')

        attr_str = ""
        if attrs:
            attr_str = " [" + " ".join(attrs) + "]"

        lines.append(f"    {f} -> {t}{attr_str};")

    lines.append("}")
    return "\n".join(lines)


# ===================== export DOT + PNG =====================

def export_graph(
    excel_path: str,
    out_dir: str | None = None,
) -> Tuple[str, str]:
    """
    從 Excel 產生 DOT 與 PNG。

    回傳:
        (dot_path, png_path)
    """
    excel_path = Path(excel_path).resolve()
    if out_dir is None:
        out_dir = excel_path.parent
    out_dir = Path(out_dir)

    base_name = excel_path.stem
    dot_path = out_dir / f"{base_name}.dot"
    png_path = out_dir / f"{base_name}.png"

    # 1. 產生 DOT 檔
    dot_text = build_dot_from_excel(str(excel_path))
    dot_path.write_text(dot_text, encoding="utf-8")

    # 2. 呼叫系統 Graphviz `dot`
    dot_exe = find_dot_executable()
    cmd = [dot_exe, "-Tpng", str(dot_path), "-o", str(png_path)]

    try:
        completed = subprocess.run(
            cmd, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        err = e.stderr or ""
        raise RuntimeError(
            f"Graphviz 'dot' failed with return code {e.returncode}.\n"
            f"Command: {' '.join(cmd)}\n"
            f"stderr:\n{err}"
        ) from e

    return str(dot_path), str(png_path)