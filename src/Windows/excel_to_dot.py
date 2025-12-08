"""
excel_to_dot.py
Read Excel (Nodes / Edges) and:
1. Build a Graphviz DOT string
2. Call Graphviz 'dot' to create a PNG

Works on both macOS and Windows with portable Graphviz:
- macOS: graphviz-mac/bin/dot
- Windows: graphviz-win/bin/dot.exe
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Tuple

import pandas as pd
from graph_config import GRAPH_ATTRS, NODE_ATTRS, EDGE_ATTRS, get_node_color


# ===================== find dot =====================

def find_dot_executable() -> str:
    """
    Prefer the portable Graphviz bundled with the project,
    then fall back to system 'dot' if available.

    Portable layouts supported:

    Development (running python rf_drawing_gui.py):

        RFDrawing/
          graphviz-mac/bin/dot
          graphviz-win/bin/dot.exe

        OR (if you keep copies under src/dist while testing)
        RFDrawing/src/dist/graphviz-mac/bin/dot
        RFDrawing/src/dist/graphviz-win/bin/dot.exe

    Frozen (.app / .exe via PyInstaller):

        macOS:
            RFDrawing/src/dist/
              RFDrawing.app
              graphviz-mac/bin/dot

        Windows (onefile or onedir):
            RFDrawing/src/dist/
              RFDrawing.exe
              graphviz-win/bin/dot.exe
    """
    from shutil import which

    candidates: list[Path] = []

    if getattr(sys, "frozen", False):
        exe = Path(sys.executable).resolve()
        exe_dir = exe.parent

        if sys.platform == "darwin":
            # .../RFDrawing/src/dist/RFDrawing.app/Contents/MacOS/RFDrawing
            macos_dir = exe_dir
            contents_dir = macos_dir.parent
            app_dir = contents_dir.parent
            dist_dir = app_dir.parent  # .../src/dist

            candidates.append(dist_dir / "graphviz-mac" / "bin" / "dot")
            # if you move it one level up later:
            candidates.append(dist_dir.parent / "graphviz-mac" / "bin" / "dot")
        else:
            # Windows (exe_dir is usually ...\src\dist)
            candidates.append(exe_dir / "graphviz-win" / "bin" / "dot.exe")
            candidates.append(exe_dir / "graphviz" / "bin" / "dot.exe")
            # if graphviz-win is beside dist
            candidates.append(exe_dir.parent / "graphviz-win" / "bin" / "dot.exe")
    else:
        # Development: this file is in RFDrawing/src
        here = Path(__file__).resolve().parent
        project_root = here.parent

        if sys.platform == "darwin":
            candidates.append(project_root / "graphviz-mac" / "bin" / "dot")
            candidates.append(here / "dist" / "graphviz-mac" / "bin" / "dot")
        else:
            candidates.append(project_root / "graphviz-win" / "bin" / "dot.exe")
            candidates.append(here / "dist" / "graphviz-win" / "bin" / "dot.exe")

    # fallback: system Graphviz if available
    sys_dot_name = "dot.exe" if os.name == "nt" else "dot"
    sys_dot = which(sys_dot_name)
    if sys_dot:
        candidates.append(Path(sys_dot))

    for c in candidates:
        if c and c.exists():
            return str(c)

    raise RuntimeError(
        "Could not find Graphviz 'dot' executable.\n"
        "On macOS: ensure graphviz-mac/bin/dot exists.\n"
        "On Windows: ensure graphviz-win/bin/dot.exe exists.\n"
        "Or install Graphviz system-wide so that 'dot' is on PATH."
    )


# ===================== build DOT string =====================

def build_dot_from_excel(
    excel_path: str,
    nodes_sheet: str = "Nodes",
    edges_sheet: str = "Edges",
) -> str:
    """Read Excel and return DOT language as a string."""
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

    # Nodes
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

    # Edges
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
    Build DOT from Excel and call Graphviz to produce PNG.

    Returns:
        (dot_path, png_path)
    """
    excel_path = Path(excel_path).resolve()
    if out_dir is None:
        out_dir = excel_path.parent
    out_dir = Path(out_dir)

    base_name = excel_path.stem
    dot_path = out_dir / f"{base_name}.dot"
    png_path = out_dir / f"{base_name}.png"

    # 1. build DOT and write file
    dot_text = build_dot_from_excel(str(excel_path))
    dot_path.write_text(dot_text, encoding="utf-8")

    # 2. find dot and call it
    dot_exe = find_dot_executable()
    cmd = [dot_exe, "-Tpng", str(dot_path), "-o", str(png_path)]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Graphviz 'dot' failed: {e}") from e

    return str(dot_path), str(png_path)
