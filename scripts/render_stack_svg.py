#!/usr/bin/env python3
"""
Render the domains / tech-stack / now-shipping card as a terminal-window SVG
matching contrib-heatmap.svg and stats.svg. Lines fade in top -> bottom once,
then hold. Static content: edit SECTIONS and re-run by hand (not in the daily
workflow).

    python scripts/render_stack_svg.py [output.svg]
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "stack.svg")

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#e6edf3"
GREEN = "#39d353"
ACCENT = "#22d3ee"

# (command, [(key, value), ...])
SECTIONS = [
    ("cat domains.txt", [
        ("full-stack platforms", "ERPs, CRMs, internal ops tools, NAS, multi-brand CMS"),
        ("multi-tenant saas", "web console + resident app + offline-first gate app"),
        ("motion & web", "scroll-driven GSAP / Three.js sites, ad landing pages"),
        ("ai & automation", "AI-drafted content with human approval, RAG chatbots"),
        ("edge ai / cv", "ESP32 face recognition, YOLO hotspot detection, NLP"),
        ("devops", "VPS, Docker, nginx, wildcard TLS, CI/CD deploys"),
    ]),
    ("ls ~/stack", [
        ("languages", "TypeScript · JavaScript · Python · PHP · C++ · SQL"),
        ("frontend", "React 19 · Next.js 16 · Vite · SvelteKit · Tailwind 4"),
        ("motion", "GSAP · Three.js · Framer Motion"),
        ("backend", "FastAPI · Express · Slim 4 · Flask"),
        ("data", "PostgreSQL · MongoDB · Supabase · SQLite"),
        ("mobile", "Expo · React Native"),
        ("infra", "Docker · nginx · Vercel · Cloudflare · GitHub Actions"),
        ("ai / ml", "Claude API · PyTorch · TF Lite · YOLO · OpenCV · FAISS"),
    ]),
    ("ps aux | grep shipping", [
        ("erp", "real-estate developer: bookings, CRM, finance, payroll"),
        ("ops platform", "media agency: tickets, task graphs, vault, approvals"),
        ("society os", "gated-community management, web + 2 mobile apps"),
        ("social portal", "industry federation: AI drafts posts, people publish"),
    ]),
]

W = 900
PAD = 24
TITLEBAR_H = 30
LINE_H = 24
FONT = 14
KEY_W = 210            # key column width
CMD_GAP = 14           # extra space above each command
STAGGER = 0.07         # seconds between lines
DUR = 0.4

# ---- layout ---------------------------------------------------------------
lines = []             # (y, svg_text)
y = TITLEBAR_H + PAD
for si, (cmd, rows) in enumerate(SECTIONS):
    if si:
        y += CMD_GAP
    y += LINE_H
    lines.append((y, f'<text x="{PAD}" y="{y}" font-size="{FONT}" fill="{GREEN}">$ '
                     f'<tspan fill="{INK}">{html.escape(cmd)}</tspan></text>'))
    for key, val in rows:
        y += LINE_H
        lines.append((y, f'<text x="{PAD + 16}" y="{y}" font-size="{FONT}" fill="{ACCENT}">'
                         f'{html.escape(key)}</text>'
                         f'<text x="{PAD + 16 + KEY_W}" y="{y}" font-size="{FONT}" fill="{INK}">'
                         f'{html.escape(val)}</text>'))
H = y + PAD

parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<style>'
    f'.l{{opacity:0;animation:in {DUR}s ease-out both}}'
    '@keyframes in{0%{opacity:0;transform:translateX(-8px)}100%{opacity:1;transform:translateX(0)}}'
    '@media (prefers-reduced-motion: reduce){.l{opacity:1!important;transform:none!important;animation:none!important}}'
    '</style>',
    f'<defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#bg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}"/>',
]
for i, dot in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dot}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">lightxlk@github: ~$ ./stack.sh</text>')

for i, (_, txt) in enumerate(lines):
    parts.append(f'<g class="l" style="animation-delay:{i * STAGGER:.2f}s">{txt}</g>')

parts.append('</svg>')
svg = "".join(parts)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(svg)
print(f"wrote {OUT}: {W} x {H}, {len(lines)} lines")
