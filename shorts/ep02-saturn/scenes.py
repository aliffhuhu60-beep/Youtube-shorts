"""Generate the 8 paper-cutout scenes (1080x1920 SVG) for EP02 'Saturn would float'."""
from pathlib import Path

NAVY, NAVY2, TEAL, MUST, TERRA, CREAM = "#14213D", "#264A6E", "#2A9D8F", "#E9C46A", "#E76F51", "#F4EDE1"
OUT = Path(__file__).parent / "svg"
OUT.mkdir(exist_ok=True)

DEFS = f"""<defs>
<filter id="p" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="12" stdDeviation="12" flood-color="#000" flood-opacity=".38"/></filter>
<filter id="g"><feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="5"/>
<feColorMatrix values="0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 .09 0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<clipPath id="sat"><circle r="200"/></clipPath>
</defs>"""

STARS = "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{MUST}"/>' for x, y, r in
                [(120, 160, 6), (900, 120, 5), (300, 420, 4), (980, 520, 6), (160, 780, 5), (760, 300, 3),
                 (520, 90, 4), (60, 1000, 4), (1020, 900, 5), (420, 640, 3)])


def saturn(x, y, s=1.0, tilt=-18, body=TERRA):
    """Paper Saturn: back ring half, banded planet, front ring half."""
    ring = lambda half: (f'<path d="M-340 0 A340 80 0 0 {half} 340 0" fill="none" stroke="{MUST}" '
                         f'stroke-width="34" stroke-linecap="round"/>')
    return (f'<g transform="translate({x} {y}) scale({s}) rotate({tilt})" filter="url(#p)">'
            f'{ring(1)}<circle r="200" fill="{body}"/>'
            f'<g clip-path="url(#sat)" opacity=".55"><rect x="-220" y="-90" width="440" height="40" fill="{MUST}"/>'
            f'<rect x="-220" y="10" width="440" height="28" fill="{CREAM}"/><rect x="-220" y="90" width="440" height="36" fill="#C65A40"/></g>'
            f'{ring(0)}</g>')


def tub(x, y, w=760, h=300, water=TEAL, stain=False):
    feet = "".join(f'<rect x="{fx}" y="{h-10}" width="40" height="70" rx="16" fill="{MUST}"/>' for fx in (60, w - 100))
    st = (f'<path d="M30 70 Q{w/2} 110 {w-30} 70" fill="none" stroke="#8a6a3a" stroke-width="16" '
          f'stroke-dasharray="40 14" opacity=".8"/>') if stain else ""
    wat = f'<path d="M24 40 Q{w/4} 10 {w/2} 40 T{w-24} 40 V{h-40} H24z" fill="{water}"/>' if water else ""
    return (f'<g transform="translate({x} {y})" filter="url(#p)">{feet}'
            f'<path d="M0 0 H{w} Q{w} {h} {w/2} {h} Q0 {h} 0 0z" fill="{CREAM}"/>{wat}'
            f'<path d="M0 0 H{w} Q{w} {h} {w/2} {h} Q0 {h} 0 0z" fill="none" stroke="#d9cdb8" stroke-width="10"/>{st}'
            f'<rect x="-30" y="-24" width="{w+60}" height="36" rx="18" fill="{CREAM}"/></g>')


def bubbles(cx, cy):
    return "".join(f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{CREAM}" fill-opacity=".9" filter="url(#p)"/>'
                   for dx, dy, r in [(-300, -20, 34), (-240, -60, 22), (260, -30, 30), (320, -80, 18), (-60, -40, 16)])


def label(x, y, text, size=64, fill=CREAM, bg=NAVY):
    w = len(text) * size * 0.62 + 60
    return (f'<g filter="url(#p)"><rect x="{x-w/2}" y="{y-size}" width="{w}" height="{size*1.45}" rx="{size*0.7}" fill="{bg}"/>'
            f'<text x="{x}" y="{y+size*0.12}" text-anchor="middle" font-family="Montserrat,Arial Black,Arial,sans-serif" '
            f'font-weight="900" font-size="{size}" fill="{fill}">{text}</text></g>')


def page(body, bg=NAVY):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1920" viewBox="0 0 1080 1920">{DEFS}'
            f'<rect width="1080" height="1920" fill="{bg}"/>{STARS}{body}'
            f'<rect width="1080" height="1920" fill="#fff" filter="url(#g)"/></svg>')


WAVES = (f'<path filter="url(#p)" fill="{TEAL}" d="M0 980 Q270 920 540 980 T1080 980 V1920 H0z"/>'
         f'<path filter="url(#p)" fill="{NAVY2}" d="M0 1120 Q270 1060 540 1120 T1080 1120 V1920 H0z"/>'
         f'<path filter="url(#p)" fill="#1B3354" d="M0 1300 Q270 1250 540 1300 T1080 1300 V1920 H0z"/>')

scenes = {
    # 1 Hook: Saturn floating in a bathtub
    "01": page(tub(160, 820) + saturn(540, 700, 0.9) + bubbles(540, 820) + label(540, 260, "SATURN", 80)),
    # 2 Huge: 95x Earth's mass
    "02": page(saturn(560, 640, 1.15) + f'<g filter="url(#p)"><circle cx="190" cy="960" r="38" fill="{TEAL}"/>'
               f'<path d="M172 946 q14-12 30 0 q-6 18-22 14z" fill="{CREAM}"/></g>'
               + label(190, 1050, "EARTH", 44) + label(600, 1120, "× 95 THE MASS", 66, NAVY, MUST)),
    # 3 Hydrogen & helium
    "03": page(f'<g transform="translate(540 700)" filter="url(#p)"><circle r="330" fill="{TERRA}"/>'
               f'<circle r="250" fill="#f08a6c"/><circle r="160" fill="{MUST}"/></g>'
               + "".join(f'<g filter="url(#p)"><circle cx="{x}" cy="{y}" r="{r}" fill="{CREAM}"/>'
                         f'<text x="{x}" y="{y+r*0.35}" text-anchor="middle" font-family="Montserrat,Arial Black,Arial" '
                         f'font-weight="900" font-size="{r}" fill="{NAVY}">{t}</text></g>'
                         for x, y, r, t in [(400, 560, 70, "H"), (660, 520, 60, "H"), (560, 800, 80, "He"),
                                            (380, 860, 54, "H"), (720, 760, 66, "He")])
               + label(540, 1120, "LIGHTEST GASES", 64)),
    # 4 Density lower than water
    "04": page(f'<g filter="url(#p)"><rect x="140" y="560" width="800" height="24" rx="12" fill="{CREAM}"/>'
               f'<path d="M540 584 L500 1000 H580z" fill="{CREAM}"/><rect x="380" y="990" width="320" height="40" rx="20" fill="{CREAM}"/></g>'
               + f'<g filter="url(#p)"><rect x="140" y="320" width="220" height="240" rx="20" fill="{TEAL}"/></g>'
               + label(250, 460, "1.0", 60, CREAM, NAVY2) + saturn(800, 470, 0.38)
               + label(250, 680, "WATER", 44) + label(800, 680, "SATURN 0.69", 44, NAVY, MUST)
               + label(540, 1120, "LESS DENSE THAN WATER", 54), bg=NAVY),
    # 5 Bobbing on a giant ocean
    "05": page(saturn(540, 860, 1.0, tilt=-10) + WAVES),
    # 6 Bathtub wider than Jupiter
    "06": page(f'<g filter="url(#p)"><circle cx="540" cy="560" r="360" fill="#d9a46a"/>'
               f'<rect x="180" y="440" width="720" height="50" fill="#b9784a"/><rect x="180" y="580" width="720" height="70" fill="#f1d3a1"/>'
               f'<ellipse cx="660" cy="700" rx="70" ry="40" fill="{TERRA}"/></g>'
               + label(540, 150, "JUPITER", 64)
               + f'<g transform="scale(1.35 1) translate(-70 0)">{tub(0, 860, 1080, 240)}</g>'),
    # 7 Saturn leaves a ring
    "07": page(tub(120, 760, 840, 320, water=None, stain=True) + saturn(860, 520, 0.42, tilt=-30)
               + label(540, 260, "…AND A RING", 66, NAVY, MUST)),
    # 8 Loop back to the hook
    "08": page(tub(160, 800) + saturn(560, 380, 0.85, tilt=-25) + bubbles(540, 800)),
}
for name, svg in scenes.items():
    (OUT / f"{name}.svg").write_text(svg)
print("wrote", len(scenes), "scenes to", OUT)
