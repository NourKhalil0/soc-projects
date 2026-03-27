import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(32, 52))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')
ax.set_xlim(0, 100)
ax.set_ylim(0, 130)
ax.axis('off')

ax.text(50, 126, 'Email Header Parser', fontsize=42, fontweight='bold',
        color='white', ha='center', va='center')
ax.text(50, 123, 'Phishing Detection Workflow', fontsize=28,
        color='#8b949e', ha='center', va='center')

phases = [
    {
        'title': 'Phase 1: Input',
        'color': '#1f6feb',
        'y_start': 108,
        'cards': [
            {'title': 'Email Header File', 'body': 'Read raw email headers\nfrom a .txt file or use\nbuilt-in demo data'},
            {'title': 'Argparse CLI', 'body': 'Use --file to load headers\nor --demo for sample data\n--json for JSON output'},
        ]
    },
    {
        'title': 'Phase 2: Parse Headers',
        'color': '#da3633',
        'y_start': 88,
        'cards': [
            {'title': 'Split Key/Value Pairs', 'body': 'Break each line into\nheader name and value\nHandle multi-line headers'},
            {'title': 'Extract Key Fields', 'body': 'Pull out From, To, Subject\nReturn-Path, Reply-To\nAuthentication-Results'},
        ]
    },
    {
        'title': 'Phase 3: Security Checks',
        'color': '#f0883e',
        'y_start': 68,
        'cards': [
            {'title': 'SPF / DKIM / DMARC', 'body': 'Check Authentication-Results\nfor spf=fail, dkim=none\nor dmarc=fail flags'},
            {'title': 'Address Mismatch', 'body': 'Compare From vs Reply-To\nand From vs Return-Path\nFlag any differences'},
            {'title': 'Subject Keywords', 'body': 'Scan subject line for\nphishing words like urgent\nverify, suspend, confirm'},
        ]
    },
    {
        'title': 'Phase 4: Risk Scoring',
        'color': '#a371f7',
        'y_start': 48,
        'cards': [
            {'title': 'Count Findings', 'body': 'Each failed check adds\none finding to the list'},
            {'title': 'Assign Risk Level', 'body': '5+ findings = HIGH\n3-4 findings = MEDIUM\n1-2 findings = LOW\n0 findings = CLEAN'},
        ]
    },
    {
        'title': 'Phase 5: Output Report',
        'color': '#3fb950',
        'y_start': 28,
        'cards': [
            {'title': 'Text Report', 'body': 'Show key headers, list\nall findings, and display\nthe final risk level'},
            {'title': 'JSON Output', 'body': 'Use --json flag to get\nmachine-readable output\nwith headers and findings'},
        ]
    },
]

for phase in phases:
    color = phase['color']
    y_top = phase['y_start']

    ax.add_patch(mpatches.FancyBboxPatch(
        (3, y_top - 16), 94, 18,
        boxstyle="round,pad=0.5", facecolor=color + '15',
        edgecolor=color, linewidth=2
    ))

    ax.text(50, y_top, phase['title'], fontsize=26, fontweight='bold',
            color=color, ha='center', va='center')

    cards = phase['cards']
    num = len(cards)
    card_w = 26
    gap = 4
    total_w = num * card_w + (num - 1) * gap
    start_x = (100 - total_w) / 2

    for i, card in enumerate(cards):
        cx = start_x + i * (card_w + gap)
        cy = y_top - 12.5

        ax.add_patch(mpatches.FancyBboxPatch(
            (cx, cy - 3.5), card_w, 8,
            boxstyle="round,pad=0.4", facecolor='#161b22',
            edgecolor=color, linewidth=1.5
        ))

        ax.text(cx + card_w / 2, cy + 3, card['title'],
                fontsize=18, fontweight='bold', color='white',
                ha='center', va='center')

        ax.text(cx + card_w / 2, cy - 0.5, card['body'],
                fontsize=14, color='#c9d1d9',
                ha='center', va='center', linespacing=1.4)

    if y_top > 30:
        ax.annotate('', xy=(50, y_top - 18), xytext=(50, y_top - 20.5),
                     arrowprops=dict(arrowstyle='->', color='#8b949e',
                                     lw=2.5))

plt.tight_layout(pad=2)
plt.savefig('/tmp/soc-projects/11-email-header-parser/diagram.png',
            dpi=180, facecolor='#0d1117', bbox_inches='tight')
plt.close()
print("Diagram saved.")
