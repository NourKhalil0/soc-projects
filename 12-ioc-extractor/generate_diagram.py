import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(32, 52))
fig.patch.set_facecolor("#0d1117")
ax.set_facecolor("#0d1117")
ax.set_xlim(0, 100)
ax.set_ylim(0, 130)
ax.axis("off")

ax.text(50, 126, "IOC Extractor", fontsize=42, fontweight="bold",
        color="white", ha="center", va="center")
ax.text(50, 123, "Indicator of Compromise Extraction Pipeline",
        fontsize=24, color="#8b949e", ha="center", va="center")

phases = [
    {
        "title": "PHASE 1: INPUT",
        "color": "#1f6feb",
        "y_start": 108,
        "cards": [
            ("Text File", "Read a .txt or .log file\nfrom disk using --file flag"),
            ("Stdin Pipe", "Pipe text from another\ncommand into the extractor"),
            ("Demo Mode", "Use built in sample data\nwith the --demo flag"),
        ],
    },
    {
        "title": "PHASE 2: EXTRACTION",
        "color": "#238636",
        "y_start": 86,
        "cards": [
            ("IPv4 Addresses", "Regex matches dotted quads\nand validates each octet <= 255"),
            ("Domains", "Finds hostnames ending in\ncommon TLDs like com, net, org"),
            ("URLs", "Captures full http and https\nlinks from the input text"),
            ("MD5 Hashes", "Matches 32 character hex\nstrings for MD5 fingerprints"),
            ("SHA256 Hashes", "Matches 64 character hex\nstrings for SHA256 fingerprints"),
            ("Email Addresses", "Finds email patterns with\nuser@domain format"),
        ],
    },
    {
        "title": "PHASE 3: PROCESSING",
        "color": "#a371f7",
        "y_start": 56,
        "cards": [
            ("Deduplication", "Remove duplicate entries\nfrom each IOC category"),
            ("Categorization", "Group all findings into\nseparate named categories"),
            ("Counting", "Track total IOCs found\nacross all categories"),
        ],
    },
    {
        "title": "PHASE 4: OUTPUT",
        "color": "#f0883e",
        "y_start": 34,
        "cards": [
            ("Table View", "Print each category with\ncount and sorted items"),
            ("JSON Export", "Use --json flag for\nmachine readable output"),
            ("Summary Line", "Show total IOC count\nat the end of output"),
        ],
    },
    {
        "title": "PHASE 5: SOC USE CASES",
        "color": "#f85149",
        "y_start": 12,
        "cards": [
            ("Threat Hunting", "Search logs for known\nbad IPs and domains"),
            ("Incident Response", "Quickly pull IOCs from\nalert emails or reports"),
            ("Intel Sharing", "Export JSON to feed into\nother security tools"),
        ],
    },
]

for phase in phases:
    title = phase["title"]
    color = phase["color"]
    y_start = phase["y_start"]
    cards = phase["cards"]

    bg = mpatches.FancyBboxPatch(
        (3, y_start - 2), 94, 20,
        boxstyle="round,pad=0.5",
        facecolor=color + "18",
        edgecolor=color,
        linewidth=2,
    )
    ax.add_patch(bg)

    ax.text(50, y_start + 16.5, title, fontsize=26, fontweight="bold",
            color=color, ha="center", va="center")

    num_cards = len(cards)
    card_width = 25
    total_width = num_cards * card_width + (num_cards - 1) * 3
    start_x = (100 - total_width) / 2

    for i, (card_title, card_body) in enumerate(cards):
        cx = start_x + i * (card_width + 3)
        cy = y_start

        card = mpatches.FancyBboxPatch(
            (cx, cy), card_width, 13,
            boxstyle="round,pad=0.4",
            facecolor=color + "30",
            edgecolor=color,
            linewidth=1.5,
        )
        ax.add_patch(card)

        ax.text(cx + card_width / 2, cy + 10.5, card_title,
                fontsize=18, fontweight="bold", color="white",
                ha="center", va="center")

        ax.text(cx + card_width / 2, cy + 5, card_body,
                fontsize=14, color="#c9d1d9",
                ha="center", va="center", linespacing=1.6)

for i in range(len(phases) - 1):
    y_from = phases[i]["y_start"] - 1
    y_to = phases[i + 1]["y_start"] + 18
    ax.annotate("", xy=(50, y_to), xytext=(50, y_from),
                arrowprops=dict(arrowstyle="->", color="#8b949e",
                                lw=2.5, mutation_scale=25))

plt.tight_layout(pad=2)
plt.savefig("/tmp/soc-projects/12-ioc-extractor/diagram.png",
            dpi=180, facecolor="#0d1117", bbox_inches="tight")
plt.close()
print("Diagram saved.")
