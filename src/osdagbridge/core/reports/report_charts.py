"""Charts embedded in the design report (generated with matplotlib)."""

import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


UR_GROUPS = [
    ("Steel Plate Girders", "Girder"),
    ("Concrete Deck Slab", "Deck"),
    ("Cross Bracing", "Cross Bracing"),
    ("End Diaphragms", "End Diaphragm"),
]


def _to_float(text):
    """Pull the first number out of a cell like '0.45' or '\\textcolor{red}{1.20}'."""
    match = re.search(r"\d+(\.\d+)?", str(text or ""))
    return float(match.group()) if match else None


def _group_and_name(label):
    """Map a summary-table row label to (member group, short check name)."""
    if "(slab)" in label:
        return "Deck", label.replace("(slab)", "").strip()
    for _title, prefix in UR_GROUPS:
        if label.startswith(prefix):
            return prefix, label.split("---")[-1].strip()
    return None, label


def ur_summary_chart(rows, out_path):
    """Save a 2x2 bar chart of UR per check for each primary member.

    rows: list of (row label, UR cell text) from the Overall Design Check Summary.
    Returns out_path, or None when no row has a numeric UR.
    """
    data = {prefix: [] for _title, prefix in UR_GROUPS}
    for label, ur_text in rows:
        value = _to_float(ur_text)
        group, name = _group_and_name(label)
        if group is not None and value is not None:
            data[group].append((name, value))

    if not any(data.values()):
        return None

    fig, axes = plt.subplots(2, 2, figsize=(10, 7.5))
    for ax, (title, prefix) in zip(axes.flat, UR_GROUPS):
        points = data[prefix]
        ax.set_title(title, fontsize=11, fontweight="bold")
        ax.set_ylabel("Utilization Ratio")
        if not points:
            ax.text(0.5, 0.5, "No UR data", ha="center", va="center", transform=ax.transAxes)
            ax.set_xticks([])
            ax.set_ylim(0, 1.2)
        else:
            names = [p[0] for p in points]
            values = [p[1] for p in points]
            colors = ["#c0392b" if v > 1.0 else "#7a9a01" for v in values]
            bars = ax.bar(range(len(values)), values, color=colors, width=0.6)
            ax.set_xticks(range(len(values)))
            ax.set_xticklabels(names, rotation=30, ha="right", fontsize=8)
            ax.set_ylim(0, max(1.2, max(values) * 1.15))
            for bar, v in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, v, f"{v:.2f}",
                        ha="center", va="bottom", fontsize=7)
        ax.axhline(1.0, color="red", linestyle="--", linewidth=1.5, label="UR = 1.0")
        ax.legend(loc="upper right", fontsize=7)
        ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path


def material_quantity_chart(quantities, out_path):
    """Save bar charts of steel tonnage and concrete vs reinforcement.

    quantities: the Chapter 7 dict (values like "32.89" or "N.A.").
    Returns out_path, or None when there is nothing to plot.
    """
    def _num(key):
        return _to_float(quantities.get(key)) if quantities.get(key) not in (None, "N.A.") else None

    girders = _num("steel_girders_wt_total")
    bracing_parts = [_num(k) for k in ("bracing_top_wt_total", "bracing_bot_wt_total", "bracing_diag_wt_total")]
    bracing = sum(v for v in bracing_parts if v is not None) if any(v is not None for v in bracing_parts) else None
    concrete = _num("concrete_deck_vol_total")
    rebar = _num("rebar_deck_wt_total")

    if all(v is None for v in (girders, bracing, concrete, rebar)):
        return None

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.2))

    # Left: structural steel tonnage
    names = ["Girders", "Cross Bracing", "End Diaphragms"]
    values = [girders, bracing, None]
    shown = [v if v is not None else 0 for v in values]
    bars = ax1.bar(names, shown, color="#7a9a01", width=0.55)
    for bar, v in zip(bars, values):
        label = f"{v:.2f}" if v is not None else "not in BOM"
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), label,
                 ha="center", va="bottom", fontsize=8)
    ax1.set_title("Structural Steel Tonnage", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Weight (MT)")
    ax1.set_ylim(0, max(shown) * 1.2 if max(shown) > 0 else 1)
    ax1.grid(axis="y", alpha=0.3)

    # Right: concrete volume vs reinforcement weight (different units, separate axes)
    ax2.set_title("Deck: Concrete vs Reinforcement", fontsize=11, fontweight="bold")
    c_val = concrete if concrete is not None else 0
    r_val = rebar if rebar is not None else 0
    b1 = ax2.bar([0], [c_val], color="#8c8c8c", width=0.5)
    ax2.set_ylabel("Concrete Volume (m³)")
    ax2.set_ylim(0, c_val * 1.2 if c_val > 0 else 1)
    ax2r = ax2.twinx()
    b2 = ax2r.bar([1], [r_val], color="#b5651d", width=0.5)
    ax2r.set_ylabel("Reinforcement Weight (MT)")
    ax2r.set_ylim(0, r_val * 1.2 if r_val > 0 else 1)
    ax2.set_xticks([0, 1])
    ax2.set_xticklabels(["Concrete (m³)", "Reinforcement (MT)"])
    ax2.text(0, c_val, f"{concrete:.2f} m³" if concrete is not None else "N.A.", ha="center", va="bottom", fontsize=8)
    ax2r.text(1, r_val, f"{rebar:.2f} MT" if rebar is not None else "N.A.", ha="center", va="bottom", fontsize=8)
    ax2.grid(axis="y", alpha=0.3)

    fig.tight_layout()
    fig.savefig(out_path, dpi=200)
    plt.close(fig)
    return out_path