import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(32, 52))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")
ax.set_xlim(0, 10)
ax.set_ylim(0, 16)
ax.axis("off")

ax.text(5, 15.3, "Domain Info Lookup", fontsize=42, fontweight="bold",
        color="white", ha="center", va="center")
ax.text(5, 14.8, "OSINT and Threat Intelligence Tool", fontsize=28,
        color="#8b949e", ha="center", va="center")

phases = [
    {
        "title": "Phase 1: Input",
        "color": "#1f6feb",
        "y": 13.0,
        "cards": [
            {"title": "Domain Name", "body": "User provides a target\ndomain via --domain flag"},
            {"title": "Demo Mode", "body": "Use --demo to run with\nsample data, no network needed"},
        ]
    },
    {
        "title": "Phase 2: DNS Resolution",
        "color": "#238636",
        "y": 10.5,
        "cards": [
            {"title": "A Records", "body": "Resolve IPv4 addresses\nusing socket.getaddrinfo"},
            {"title": "AAAA Records", "body": "Resolve IPv6 addresses\nfor the target domain"},
            {"title": "Deduplication", "body": "Remove duplicate IPs\nfrom the results"},
        ]
    },
    {
        "title": "Phase 3: Reverse Lookup",
        "color": "#da3633",
        "y": 8.0,
        "cards": [
            {"title": "Reverse DNS", "body": "Map each IPv4 address\nback to a hostname"},
            {"title": "FQDN Resolution", "body": "Get fully qualified domain\nname for each IP"},
        ]
    },
    {
        "title": "Phase 4: Reporting",
        "color": "#a371f7",
        "y": 5.5,
        "cards": [
            {"title": "Build Report", "body": "Combine DNS records and\nreverse lookups into one report"},
            {"title": "Print Output", "body": "Display formatted report\nwith timestamps to terminal"},
        ]
    },
    {
        "title": "Phase 5: SOC Use Cases",
        "color": "#f0883e",
        "y": 3.0,
        "cards": [
            {"title": "Threat Triage", "body": "Quickly check what IPs\na suspicious domain resolves to"},
            {"title": "Indicator Enrichment", "body": "Add DNS context to\nIOCs during investigations"},
            {"title": "Infrastructure Mapping", "body": "Understand the hosting\nsetup behind a domain"},
        ]
    },
]

for phase in phases:
    ax.text(5, phase["y"] + 1.1, phase["title"], fontsize=26, fontweight="bold",
            color=phase["color"], ha="center", va="center")

    num_cards = len(phase["cards"])
    total_width = num_cards * 2.6 + (num_cards - 1) * 0.4
    start_x = 5 - total_width / 2

    for i, card in enumerate(phase["cards"]):
        cx = start_x + i * 3.0 + 1.3
        cy = phase["y"]
        rect = mpatches.FancyBboxPatch(
            (cx - 1.2, cy - 0.7), 2.4, 1.4,
            boxstyle="round,pad=0.1",
            facecolor="#161b22", edgecolor=phase["color"], linewidth=2
        )
        ax.add_patch(rect)
        ax.text(cx, cy + 0.35, card["title"], fontsize=18, fontweight="bold",
                color="white", ha="center", va="center")
        ax.text(cx, cy - 0.15, card["body"], fontsize=14,
                color="#c9d1d9", ha="center", va="center", linespacing=1.4)

for i in range(len(phases) - 1):
    y_top = phases[i]["y"] - 0.7
    y_bot = phases[i + 1]["y"] + 1.1 + 0.3
    ax.annotate("", xy=(5, y_bot), xytext=(5, y_top),
                arrowprops=dict(arrowstyle="->", color="#8b949e", lw=2))

plt.savefig("/tmp/soc-projects/18-domain-info-lookup/diagram.png",
            dpi=180, bbox_inches="tight", facecolor="#0d1117")
plt.close()
print("Diagram saved.")
