#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import random

random.seed(42)

HOURS = [f"{h:02d}:00" for h in range(24)]
TRAFFIC = [random.randint(80, 400) for _ in range(24)]
TRAFFIC[3] = 1950
TRAFFIC[14] = 2300
TRAFFIC[20] = 1700

THRESHOLD = 1000


def save_graph():
    fig, ax = plt.subplots(figsize=(18, 7))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")

    colors = ["#ff4444" if v > THRESHOLD else "#00b4d8" for v in TRAFFIC]
    bars = ax.bar(HOURS, TRAFFIC, color=colors, edgecolor="none", width=0.7)

    ax.axhline(THRESHOLD, color="#ff4444", linestyle="--", linewidth=2.5, alpha=0.8)
    ax.text(23.4, THRESHOLD + 70, "THRESHOLD", color="#ff4444", fontsize=13, fontweight="bold", ha="right")

    ax.set_title("NETWORK TRAFFIC — 24 HOURS", fontsize=28, fontweight="bold", color="white", pad=20)
    ax.set_xlabel("TIME", fontsize=16, fontweight="bold", color="#aaaaaa", labelpad=10)
    ax.set_ylabel("PACKETS / HOUR", fontsize=16, fontweight="bold", color="#aaaaaa", labelpad=10)
    ax.tick_params(axis="x", rotation=45, labelsize=11, colors="#aaaaaa")
    ax.tick_params(axis="y", labelsize=11, colors="#aaaaaa")
    for spine in ["bottom", "left"]:
        ax.spines[spine].set_color("#333333")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.yaxis.grid(True, color="#1e1e1e", linewidth=1)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, TRAFFIC):
        if val > THRESHOLD:
            ax.text(bar.get_x() + bar.get_width() / 2, val + 60, f"! {val}",
                    ha="center", fontsize=14, fontweight="bold", color="#ff4444")

    normal = mpatches.Patch(color="#00b4d8", label="NORMAL TRAFFIC")
    spike = mpatches.Patch(color="#ff4444", label="SPIKE DETECTED")
    ax.legend(handles=[normal, spike], fontsize=14, facecolor="#1a1a2e",
              edgecolor="#444", labelcolor="white", loc="upper right")

    plt.tight_layout()
    plt.savefig("traffic_graph.png", dpi=140, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: traffic_graph.png")


def save_diagram():
    fig, ax = plt.subplots(figsize=(20, 7))
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 7)
    ax.axis("off")

    steps = [
        (2.5, 3.5, "LOG\nFILE", "#00b4d8", "#023e8a"),
        (7.0, 3.5, "PARSER", "#f72585", "#560bad"),
        (11.5, 3.5, "SPIKE\nDETECTOR", "#7209b7", "#3a0ca3"),
        (16.0, 3.5, "ALERT\nOUTPUT", "#ff4444", "#7d0000"),
    ]

    for x, y, label, border_color, bg_color in steps:
        shadow = mpatches.FancyBboxPatch(
            (x - 1.55, y - 1.25), 3.1, 2.5,
            boxstyle="round,pad=0.25",
            facecolor=bg_color, edgecolor="none", alpha=0.5, zorder=1
        )
        ax.add_patch(shadow)

        box = mpatches.FancyBboxPatch(
            (x - 1.5, y - 1.2), 3.0, 2.4,
            boxstyle="round,pad=0.2",
            facecolor=bg_color, edgecolor=border_color, linewidth=4, zorder=2
        )
        ax.add_patch(box)

        glow = mpatches.FancyBboxPatch(
            (x - 1.5, y - 1.2), 3.0, 2.4,
            boxstyle="round,pad=0.2",
            facecolor="none", edgecolor=border_color, linewidth=8, alpha=0.2, zorder=3
        )
        ax.add_patch(glow)

        ax.text(x, y, label, ha="center", va="center",
                fontsize=26, fontweight="bold", color="white", zorder=4,
                path_effects=[pe.withStroke(linewidth=4, foreground=bg_color)])

    for i in range(len(steps) - 1):
        x1 = steps[i][0] + 1.5
        x2 = steps[i + 1][0] - 1.5
        y = steps[i][1]
        ax.annotate("", xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="-|>", lw=4, color="white",
                                   mutation_scale=35), zorder=5)
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.55, ["READ", "PARSE", "DETECT"][i],
                ha="center", fontsize=14, color="#aaaaaa", fontweight="bold", zorder=6)

    ax.text(10.0, 6.3, "HOW THE TOOL WORKS",
            ha="center", va="center", fontsize=32, fontweight="bold", color="white",
            path_effects=[pe.withStroke(linewidth=5, foreground="#0d1117")])

    plt.tight_layout()
    plt.savefig("diagram.png", dpi=140, facecolor=fig.get_facecolor())
    plt.close()
    print("Saved: diagram.png")


def print_report():
    spikes = [(HOURS[i], TRAFFIC[i]) for i in range(len(TRAFFIC)) if TRAFFIC[i] > THRESHOLD]
    print("\n" + "=" * 46)
    print("    TRAFFIC SPIKE DETECTOR --- REPORT")
    print("=" * 46)
    print(f"Threshold : {THRESHOLD} packets/hour")
    print(f"Period    : 24 hours\n")
    if spikes:
        for hour, packets in spikes:
            print(f"  SPIKE at {hour}  ---  {packets} packets  [ALERT]")
    else:
        print("  No spikes detected.")
    print("=" * 46 + "\n")


save_graph()
save_diagram()
print_report()
