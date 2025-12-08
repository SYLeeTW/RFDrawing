"""
graph_config.py
Common Graphviz style configuration.
"""

# Category → color mapping (you can adjust)
CATEGORY_COLORS = {
    "Hazard": "#AECBFA",
    "Exposure": "#FFE9A9",
    "Vulnerability": "#B7F0C0",
    "Impact": "#FFFFFF",
    "Risk": "#FFCDD2",
}

# Global graph attributes
GRAPH_ATTRS = {
    "rankdir": "TB",
    "fontsize": "12",
    "dpi": 280
}

# Default node attributes
NODE_ATTRS = {
    "shape": "box",
    "fontname": "Microsoft JhengHei",
}

# Default edge attributes
EDGE_ATTRS = {
    "fontname": "Microsoft JhengHei",
    "arrowhead": "open",
}


def get_node_color(category: str) -> str:
    """Return fill color for a given category substring."""
    if not category:
        return ""
    cat_lower = category.lower()
    for key, color in CATEGORY_COLORS.items():
        if key.lower() in cat_lower:
            return color
    return ""