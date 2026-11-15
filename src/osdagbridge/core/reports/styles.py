"""Single source of truth for the design report's look.

Every page, table, colour, header/footer and chart setting used by the
report generator is defined here. Change a value in this file and it
applies to the whole report.
"""

# Page layout
PAPER = "a4paper"
FONT_SIZE = "12pt"
MARGIN_TOP = "1in"
MARGIN_BOTTOM = "1.25in"
MARGIN_LEFT = "1in"
MARGIN_RIGHT = "1in"
HEAD_HEIGHT = "18pt"
FOOT_SKIP = "0.55in"
LINE_SPACING = "1.15"

# Colours (LaTeX name -> HTML hex, without '#')
COLORS = {
    "osdagGreen": "91B014",   # header/footer rules and theme colour
    "passGreen": "7A9A01",    # passing checks
    "failRed": "C0392B",      # failing checks
}

# Tables
TABLE_COL_SEP = "6pt"               # space between a cell's text and its border
TABLE_COL_SEP_COMPACT = "3.5pt"     # wide tables (Bill of Materials, standards)
TABLE_COL_SEP_NARROW = "4pt"        # member property / bracing tables
TABLE_COL_SEP_TIGHT = "3pt"         # analysis summary table
TABLE_ARRAY_STRETCH = "1.12"        # row height multiplier
TABLE_ARRAY_STRETCH_LOOSE = "1.25"  # tables that need taller rows
TABLE_ROW_GAP = "6pt"               # extra space after each row (\\[\rowgap])
TABLE_RULE_WIDTH = "0.5pt"
TABLE_EXTRA_ROW_HEIGHT = "0.6pt"
LONGTABLE_PRE = "0pt"
LONGTABLE_POST = "6pt"

# Header / footer
FOOTER_LEFT_TEXT = r"Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay"
RULE_THICKNESS = "1pt"

# Figures and charts
FIGURE_WIDTH = r"\textwidth"
CHART_DPI = 200
CHART_PASS_COLOR = "#" + COLORS["passGreen"]
CHART_FAIL_COLOR = "#" + COLORS["failRed"]
CHART_LIMIT_LINE_COLOR = "red"
CHART_CONCRETE_COLOR = "#8C8C8C"
CHART_REBAR_COLOR = "#B5651D"


def geometry_tex():
    """The geometry package line built from the page layout above."""
    return (
        r"\usepackage[" + PAPER
        + ", top=" + MARGIN_TOP + ", bottom=" + MARGIN_BOTTOM
        + ", left=" + MARGIN_LEFT + ", right=" + MARGIN_RIGHT
        + ", headheight=" + HEAD_HEIGHT + ", footskip=" + FOOT_SKIP
        + "]{geometry}"
    )


def colors_tex():
    """definecolor lines for every colour in COLORS."""
    return "\n".join(
        r"\definecolor{" + name + "}{HTML}{" + hexcode + "}"
        for name, hexcode in COLORS.items()
    )


def table_settings_tex():
    """Global table spacing, row height and rule settings."""
    return "\n".join([
        r"\setlength{\tabcolsep}{" + TABLE_COL_SEP + "}",
        r"\renewcommand{\arraystretch}{" + TABLE_ARRAY_STRETCH + "}",
        r"\setlength{\LTpre}{" + LONGTABLE_PRE + "}",
        r"\setlength{\LTpost}{" + LONGTABLE_POST + "}",
        r"\setlength{\arrayrulewidth}{" + TABLE_RULE_WIDTH + "}",
        r"\setlength{\extrarowheight}{" + TABLE_EXTRA_ROW_HEIGHT + "}",
        r"\newcommand{\rowgap}{" + TABLE_ROW_GAP + "}",
        r"\newcommand{\colsepcompact}{" + TABLE_COL_SEP_COMPACT + "}",
        r"\newcommand{\colsepnarrow}{" + TABLE_COL_SEP_NARROW + "}",
        r"\newcommand{\colseptight}{" + TABLE_COL_SEP_TIGHT + "}",
        r"\newcommand{\stretchloose}{" + TABLE_ARRAY_STRETCH_LOOSE + "}",
    ])


def figure_tex(image_path, caption):
    """A centred figure that fills the text width, with a caption."""
    return (
        r"\begin{figure}[H]" + "\n"
        + r"\centering" + "\n"
        + r"\includegraphics[width=" + FIGURE_WIDTH + "]{" + image_path.replace("\\", "/") + "}\n"
        + r"\caption{" + caption + "}\n"
        + r"\end{figure}"
    )
