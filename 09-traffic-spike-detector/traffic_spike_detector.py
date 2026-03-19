#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import random

random.seed(42)

HOURS = [f"{h:02d}:00" for h in range(24)]
TRAFFIC = [random.randint(80, 400) for _ in range(24)]
TRAFFIC[3] = 1950
TRAFFIC[14] = 2300
TRAFFIC[20] = 1700

THRESHOLD = 1000


def save_graph():
    fig, ax = plt.subplots(figsize=(16, 6))
    colors = ["crimson" if v > THRESHOLD else "#3a86ff" for v in TRAFFIC]
    bars = ax.bar(HOURS, TRAFFIC, color=colors, edgecolor="black", linewidth=0.8)
    ax.axhline(THRESHOLD, color="crimson", linestyle="--", linewidth=2.5, label=f"THRESHOLD ({THRESHOLD})")
    ax.set_title("NETWORK TRAFFIC — 24 HOURS", fontsize=22, fontweight="bold", pad=15)
    ax.set_xlabel("TIME", fontsize=16, fontweight="bold")
    ax.set_ylabel("PACKETS", fontsize=16, fontweight="bold")
    ax.tick_params(axis="x", rotation=45, labelsize=11)
    ax.tick_params(axis="y", labelsize=11)
    normal = mpatches.Patch(color="#3a86ff", label="NORMAL")
    spike = mpatches.Patch(color="crimson", label="SPIKE")
    ax.legend(handles=[normal, spike, ax.get_lines()[0]], fontsize=13, loc="upper right")
    for bar, val in zip(bars, TRAFFIC):
        if val > THRESHOLD:
            ax.text(bar.get_x() + bar.get_width() / 2, val + 30, f"{val}", ha="center", fontsize=11, fontweight="bold", color="crimson")
    plt.tight_layout()
    plt.savefig("traffic_graph.png", dpi=130)
    plt.close()
    print("Saved: traffic_graph.png")


def save_diagram():
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis("off")
    ax.set_facecolor("#f8f9fa")
    fig.patch.set_facecolor("#f8f9fa")

    steps = [
        (1.2, 2.0, "LOG\nFILE", "#4361ee"),
        (3.8, 2.0, "PARSER", "#3a0ca3"),
        (6.4, 2.0, "SPIKE\nDETECTOR", "#7209b7"),
        (9.0, 2.0, "ALERT\nOUTPUT", "#d62828"),
    ]

    for x, y, label, color in steps:
        rect = mpatches.FancyBboxPatch(
            (x - 1.0, y - 0.7), 2.0, 1.4,
            boxstyle="round,pad=0.15",
            facecolor=color, edgecolor="black", linewidth=2
        )
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=17, fontweight="bold", color="white")

    for i in range(len(steps) - 1):
        x1 = steps[i][0] + 1.0
        x2 = steps[i + 1][0] - 1.0
        y = steps[i][1]
        ax.annotate(
            "", xy=(x2, y), xytext=(x1, y),
            arrowprops=dict(arrowstyle="-|>", lw=2.5, color="#333333", mutation_scale=22)
        )

    ax.set_title("HOW THE TOOL WORKS", fontsize=22, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig("diagram.png", dpi=130)
    plt.close()
    print("Saved: diagram.png")


def print_report():
    spikes = [(HOURS[i], TRAFFIC[i]) for i in range(len(TRAFFIC)) if TRAFFIC[i] > THRESHOLD]
    print("\n" + "=" * 46)
    print("    TRAFFIC SPIKE DETECTOR — REPORT")
    print("=" * 46)
    print(f"Threshold : {THRESHOLD} packets/hour")
    print(f"Period    : 24 hours\n")
    if spikes:
        for hour, packets in spikes:
            print(f"  SPIKE at {hour}  —  {packets} packets  [ALERT]")
    else:
        print("  No spikes detected.")
    print("=" * 46 + "\n")


save_graph()
save_diagram()
print_report()
