"""Generator aset SVG animasi untuk profil GitHub AndhikaRizky04 (tema cyberpunk)."""
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets"
os.makedirs(os.path.join(OUT, "titles"), exist_ok=True)

CY, MG, YL, BG, BG2, PU = "#00f0ff", "#ff2bd6", "#f9f002", "#07051a", "#0f0c29", "#302b63"
FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
DISP = "'Orbitron','Rajdhani','Segoe UI','Arial Black',Arial,sans-serif"


def w(name, s):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)


def f(x):
    r = f"{x:.1f}"
    r = r[:-2] if r.endswith(".0") else r
    return "0" if r in ("-0", "") else r


# ---------------------------------------------------------------- 3D helpers
def rot(p, ax, ay, az):
    x, y, z = p
    y, z = y * math.cos(ax) - z * math.sin(ax), y * math.sin(ax) + z * math.cos(ax)
    x, z = x * math.cos(ay) + z * math.sin(ay), -x * math.sin(ay) + z * math.cos(ay)
    x, y = x * math.cos(az) - y * math.sin(az), x * math.sin(az) + y * math.cos(az)
    return x, y, z


def proj(p, cx, cy, s, d=4.0):
    x, y, z = p
    k = d / (d + z)
    return cx + x * s * k, cy + y * s * k, k


def wire_frames(verts, edges, cx, cy, s, frames, spin):
    """Return list of path 'd' strings, one per frame (same command structure)."""
    out = []
    for i in range(frames):
        t = i / frames * 2 * math.pi
        pts = [proj(rot(v, *spin(t)), cx, cy, s) for v in verts]
        out.append(" ".join(f"M{f(pts[a][0])} {f(pts[a][1])}L{f(pts[b][0])} {f(pts[b][1])}" for a, b in edges))
    return out


def vert_frames(verts, cx, cy, s, frames, spin):
    res = [[] for _ in verts]
    for i in range(frames):
        t = i / frames * 2 * math.pi
        for j, v in enumerate(verts):
            res[j].append(proj(rot(v, *spin(t)), cx, cy, s))
    return res


CUBE_V = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
CUBE_E = [(a, b) for a in range(8) for b in range(a + 1, 8) if sum(CUBE_V[a][k] != CUBE_V[b][k] for k in range(3)) == 1]
OCTA_V = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
OCTA_E = [(a, b) for a in range(6) for b in range(a + 1, 6) if a // 2 != b // 2]
P = (1 + 5 ** 0.5) / 2
ICO_V = [(0, s1, s2 * P) for s1 in (-1, 1) for s2 in (-1, 1)] + \
        [(s1, s2 * P, 0) for s1 in (-1, 1) for s2 in (-1, 1)] + \
        [(s2 * P, 0, s1) for s1 in (-1, 1) for s2 in (-1, 1)]
ICO_V = [(x / 1.902, y / 1.902, z / 1.902) for x, y, z in ICO_V]
ICO_E = [(a, b) for a in range(12) for b in range(a + 1, 12)
         if abs(math.dist(ICO_V[a], ICO_V[b]) - 1.0515) < 0.01]

SCANLINES = """<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
<rect width="4" height="2" fill="#000" opacity=".28"/></pattern>"""


# ============================================================== HEADER
def header():
    W, H, HZ = 1200, 440, 300
    vx = W / 2
    # perspective floor: vertical lines
    vlines = []
    for i in range(-24, 25):
        xb = vx + i * 90
        vlines.append(f'<line x1="{f(vx + i * 6)}" y1="{HZ}" x2="{f(xb)}" y2="{H}"/>')
    # horizontal lines moving toward viewer
    hl = []
    N, dur = 10, 3.0
    for i in range(N):
        ys, ops = [], []
        for k in range(21):
            z = 10 - 9.2 * (k / 20)          # far -> near
            y = HZ + 140 / z * 1.0
            ys.append(f(min(y, H + 5)))
            ops.append(f(min(1, (k / 20) * 1.6)))
        begin = -i * dur / N
        hl.append(f'''<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}">
<animate attributeName="y1" values="{';'.join(ys)}" dur="{dur}s" begin="{f(begin)}s" repeatCount="indefinite"/>
<animate attributeName="y2" values="{';'.join(ys)}" dur="{dur}s" begin="{f(begin)}s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="{';'.join(ops)}" dur="{dur}s" begin="{f(begin)}s" repeatCount="indefinite"/></line>''')
    # skyline buildings
    import random
    random.seed(7)
    bld, wins = [], []
    x = 0
    while x < W:
        bw = random.randint(28, 70)
        bh = random.randint(40, 150)
        if 470 < x < 730:
            bh = random.randint(25, 60)
        bld.append(f'<rect x="{x}" y="{HZ - bh}" width="{bw}" height="{bh}"/>')
        for wy in range(HZ - bh + 8, HZ - 6, 12):
            for wx in range(x + 5, x + bw - 6, 9):
                if random.random() < 0.22:
                    c = random.choice([CY, MG, YL, CY])
                    d = random.uniform(1.5, 6)
                    wins.append(f'<rect x="{wx}" y="{wy}" width="4" height="5" fill="{c}" style="animation:blink {f(d)}s {f(-random.uniform(0, 6))}s infinite"/>')
        # antenna
        if random.random() < 0.25:
            ax = x + bw // 2
            bld.append(f'<rect x="{ax}" y="{HZ - bh - 22}" width="2" height="22"/>')
            wins.append(f'<circle cx="{ax + 1}" cy="{HZ - bh - 23}" r="2.5" fill="{MG}" style="animation:blink 1.2s {f(-random.uniform(0, 2))}s infinite"/>')
        x += bw + random.randint(0, 6)
    # sun stripes (moving down)
    stripes = []
    for i in range(7):
        stripes.append(f'''<rect x="420" width="360" y="0" height="4" fill="#000">
<animate attributeName="y" values="{HZ - 120};{HZ}" dur="3.5s" begin="{f(-i * 0.5)}s" repeatCount="indefinite"/>
<animate attributeName="height" values="1;12" dur="3.5s" begin="{f(-i * 0.5)}s" repeatCount="indefinite"/></rect>''')
    # rain / data particles
    random.seed(3)
    rain = []
    for i in range(46):
        rx = random.randint(0, W)
        ln = random.randint(10, 40)
        d = random.uniform(1.2, 3.2)
        rain.append(f'<line x1="{rx}" x2="{rx}" y1="-40" y2="{-40 + ln}" stroke="{random.choice([CY, MG, CY])}" opacity="{f(random.uniform(.15, .5))}"><animateTransform attributeName="transform" type="translate" values="0 0;0 {H + 60}" dur="{f(d)}s" begin="{f(-random.uniform(0, 3))}s" repeatCount="indefinite"/></line>')

    name = "ANDHIKA RIZKY NUR WAHYU"
    sub = "SOFTWARE ENGINEER  //  FULL-STACK WEB DEVELOPER"
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#05030f"/><stop offset=".55" stop-color="{BG2}"/><stop offset="1" stop-color="#3a0d4f"/></linearGradient>
<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="{YL}"/><stop offset=".45" stop-color="#ff7a3d"/><stop offset="1" stop-color="{MG}"/></linearGradient>
<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#1a0630"/><stop offset="1" stop-color="#05030f"/></linearGradient>
<linearGradient id="nameG" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{CY}"/><stop offset=".5" stop-color="#ffffff"/><stop offset="1" stop-color="{MG}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/></linearGradient>
<radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{MG}" stop-opacity=".55"/><stop offset="1" stop-color="{MG}" stop-opacity="0"/></radialGradient>
<filter id="neon" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="soft"><feGaussianBlur stdDeviation="6"/></filter>
<mask id="sunMask"><rect width="{W}" height="{H}" fill="#fff"/>{"".join(stripes).replace('fill="#000"', 'fill="#000"')}</mask>
<clipPath id="above"><rect width="{W}" height="{HZ}"/></clipPath>
<clipPath id="subClip"><rect x="0" y="0" height="40" width="0">
<animate attributeName="width" values="0;0;{W};{W};0" keyTimes="0;.08;.45;.92;1" dur="9s" repeatCount="indefinite" calcMode="spline" keySplines="0 0 1 1;.4 0 .2 1;0 0 1 1;.4 0 .2 1"/></rect></clipPath>
{SCANLINES}
</defs>
<style>
@keyframes blink{{0%,100%{{opacity:.15}}40%{{opacity:1}}55%{{opacity:.4}}70%{{opacity:1}}}}
@keyframes gl1{{0%,86%,100%{{transform:translate(0,0)}}88%{{transform:translate(-6px,2px)}}90%{{transform:translate(5px,-2px)}}92%{{transform:translate(-3px,0)}}94%{{transform:translate(4px,1px)}}}}
@keyframes gl2{{0%,86%,100%{{transform:translate(0,0)}}88%{{transform:translate(6px,-2px)}}90%{{transform:translate(-5px,2px)}}92%{{transform:translate(3px,0)}}94%{{transform:translate(-4px,-1px)}}}}
@keyframes slice{{0%,86%,100%{{opacity:0}}87%,95%{{opacity:1}}}}
@keyframes sliceY{{0%{{transform:translateY(0)}}100%{{transform:translateY(90px)}}}}
@keyframes scanmove{{from{{transform:translateY(0)}}to{{transform:translateY(8px)}}}}
@keyframes pulse{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
@keyframes hud{{0%,100%{{opacity:.35}}50%{{opacity:1}}}}
@keyframes cur{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes sweep{{from{{transform:translateX(-300px)}}to{{transform:translateX(1500px)}}}}
.g1{{animation:gl1 5s infinite}} .g2{{animation:gl2 5s infinite}}
.sl{{animation:slice 5s infinite}}
.hud{{animation:hud 3s infinite}}
</style>
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<!-- stars -->
<g fill="#fff">{"".join(f'<circle cx="{(i * 137) % W}" cy="{(i * 61) % 200}" r="{1 if i % 3 else 1.6}" style="animation:blink {2 + i % 5}s {-(i % 7)}s infinite"/>' for i in range(60))}</g>
<!-- retro sun -->
<circle cx="{vx}" cy="{HZ - 40}" r="230" fill="url(#glow)"/>
<g clip-path="url(#above)"><circle cx="{vx}" cy="{HZ - 30}" r="150" fill="url(#sun)" mask="url(#sunMask)" style="animation:pulse 4s infinite"/></g>
<!-- skyline -->
<g fill="#0a0418" stroke="{MG}" stroke-opacity=".35" stroke-width="1">{"".join(bld)}</g>
<g>{"".join(wins)}</g>
<!-- floor -->
<rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#floor)"/>
<g stroke="{MG}" stroke-width="1.4" opacity=".75" filter="url(#neon)">{"".join(vlines)}</g>
<g stroke="{CY}" stroke-width="1.4" filter="url(#neon)">{"".join(hl)}</g>
<line x1="0" x2="{W}" y1="{HZ}" y2="{HZ}" stroke="{CY}" stroke-width="2" filter="url(#neon)"/>
<!-- rain -->
<g stroke-width="1.2">{"".join(rain)}</g>
<!-- glass panel behind title -->
<rect x="150" y="70" width="900" height="150" rx="4" fill="#05030f" fill-opacity=".55" stroke="{CY}" stroke-opacity=".35"/>
<!-- name with glitch -->
<g font-family="{DISP}" font-weight="900" font-size="58" text-anchor="middle" letter-spacing="4">
<text x="{vx}" y="150" fill="{MG}" opacity=".85" class="g1">{name}</text>
<text x="{vx}" y="150" fill="{CY}" opacity=".85" class="g2">{name}</text>
<text x="{vx}" y="150" fill="url(#nameG)" filter="url(#neon)">{name}</text>
</g>
<!-- glitch slice bars -->
<g class="sl"><rect x="150" y="100" width="900" height="6" fill="{CY}" opacity=".6" style="animation:sliceY .6s steps(6) infinite"/><rect x="150" y="128" width="900" height="3" fill="{MG}" opacity=".7" style="animation:sliceY .4s steps(4) infinite"/></g>
<!-- subtitle typing -->
<g transform="translate(0,170)"><g clip-path="url(#subClip)">
<text x="{vx}" y="25" font-family="{FONT}" font-size="20" fill="{CY}" text-anchor="middle" letter-spacing="3" filter="url(#neon)">&gt; {sub}<tspan fill="{MG}" style="animation:cur 1s infinite"> _</tspan></text></g></g>
<!-- HUD -->
<g stroke="{CY}" stroke-width="2" fill="none" class="hud">
<path d="M20 50V20H50"/><path d="M{W - 50} 20H{W - 20}V50"/><path d="M20 {H - 50}V{H - 20}H50"/><path d="M{W - 50} {H - 20}H{W - 20}V{H - 50}"/></g>
<g font-family="{FONT}" font-size="12" fill="{CY}" opacity=".85">
<text x="30" y="70">SYS://ARNW.04</text><text x="30" y="86" fill="{MG}">NODE: ID-JKT</text>
<text x="{W - 30}" y="70" text-anchor="end">NEURAL_LINK <tspan fill="{YL}" style="animation:cur 1.4s infinite">● ONLINE</tspan></text>
<text x="{W - 30}" y="86" text-anchor="end" fill="{MG}">REACT · LARAVEL · AI</text></g>
<!-- light sweep -->
<rect x="0" y="0" width="120" height="{H}" fill="#fff" opacity=".05" transform="skewX(-20)" style="animation:sweep 7s linear infinite"/>
<rect width="{W}" height="{H}" fill="url(#scan)" style="animation:scanmove .5s linear infinite"/>
</svg>'''
    w("header.svg", s)


# ============================================================== ABOUT (terminal + 3D hologram)
def about():
    W, H = 1000, 420
    lines = [
        ("$ ", "whoami", CY),
        ("", "andhika_rizky_nur_wahyu  // software engineer", "#e6e6ff"),
        ("$ ", "cat profile.json", CY),
        ("", '{ "role"  : "Full-Stack Web Developer",', YL),
        ("", '  "edu"   : "B.Sc. Informatics @ UDINUS",', YL),
        ("", '  "loc"   : "Indonesia",', YL),
        ("", '  "stack" : ["React","Laravel","AI"] }', YL),
        ("$ ", "./status --live", CY),
        ("", "[#########-] frontend redesign (React) ..BUILD", MG),
        ("", "[######----] AI integration in web apps ..R&D", MG),
        ("$ ", "echo $FUN_FACT", CY),
        ("", "coffee + bugs  ==>  features", "#9dff9d"),
    ]
    fs, cw, lh = 14.5, 8.75, 24
    total = 14.0
    t = 0.04
    out = []
    for i, (pr, txt, col) in enumerate(lines):
        full = pr + txt
        n = len(full)
        typing = pr != ""
        dt = (0.045 * len(txt)) if typing else 0.12
        t0 = t + (0.25 if typing else 0.05)
        t1 = t0 + dt
        k0, k1 = t0 / total, t1 / total
        steps = max(1, len(txt)) if typing else 1
        vals = ["0"] if not typing else ["0", f(len(pr) * cw)]
        kt = ["0"] if not typing else ["0", f"{k0:.4f}"]
        if typing:
            for s_ in range(1, steps + 1):
                vals.append(f((len(pr) + s_) * cw + 2))
                kt.append(f"{k0 + (k1 - k0) * s_ / steps:.4f}")
        else:
            vals += ["0", f(n * cw + 4)]
            kt += [f"{k0:.4f}", f"{k1:.4f}"]
        vals += [vals[-1], "0"]
        kt += ["0.96", "1"]
        cid = f"c{i}"
        y = 70 + i * lh
        prefix = f'<tspan fill="{MG}">{pr}</tspan>' if pr else ""
        txt_x = txt.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        out.append(f'''<clipPath id="{cid}"><rect x="30" y="{y - 17}" height="{lh}" width="0"><animate attributeName="width" values="{';'.join(vals)}" keyTimes="{';'.join(kt)}" dur="{total}s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>
<text x="32" y="{y}" clip-path="url(#{cid})" fill="{col}">{prefix}{txt_x}</text>''')
        t = t1
    cursor_y = 70 + len(lines) * lh

    # 3D hologram on right
    cx, cy = 790, 205
    spin_a = lambda t: (t, t * 2, t * 0.5)
    spin_b = lambda t: (-t * 2, t, -t)
    spin_c = lambda t: (t * 0.5, -t, t * 2)
    FR = 72
    cube = wire_frames(CUBE_V, CUBE_E, cx, cy, 78, FR, spin_a)
    ico = wire_frames(ICO_V, ICO_E, cx, cy, 52, FR, spin_b)
    octa = wire_frames(OCTA_V, OCTA_E, cx, cy, 28, FR, spin_c)
    vf = vert_frames(CUBE_V, cx, cy, 78, FR, spin_a)
    nodes = []
    for j, fr in enumerate(vf):
        cxs = ";".join(f(p[0]) for p in fr + [fr[0]])
        cys = ";".join(f(p[1]) for p in fr + [fr[0]])
        rs = ";".join(f(2 + 3 * (p[2] - .6)) for p in fr + [fr[0]])
        nodes.append(f'<circle r="3" fill="{YL}"><animate attributeName="cx" values="{cxs}" dur="12s" repeatCount="indefinite"/><animate attributeName="cy" values="{cys}" dur="12s" repeatCount="indefinite"/><animate attributeName="r" values="{rs}" dur="12s" repeatCount="indefinite"/></circle>')

    def anim_path(frames, dur, color, width, op):
        return f'<path fill="none" stroke="{color}" stroke-width="{width}" stroke-opacity="{op}" stroke-linecap="round" d="{frames[0]}"><animate attributeName="d" values="{";".join(frames + [frames[0]])}" dur="{dur}s" repeatCount="indefinite"/></path>'

    # orbit rings (3D tilted circles via precomputed ellipse) + satellites
    rings = ""
    for k, (tilt, col, dur, r) in enumerate([(70, CY, 6, 130), (-60, MG, 9, 145), (0, YL, 12, 118)]):
        rings += f'<g transform="rotate({tilt} {cx} {cy})"><ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.28}" fill="none" stroke="{col}" stroke-opacity=".55" stroke-dasharray="4 8"><animate attributeName="stroke-dashoffset" values="0;-120" dur="{dur / 2}s" repeatCount="indefinite"/></ellipse>'
        rings += f'<circle r="5" fill="{col}" filter="url(#ng)"><animateMotion dur="{dur}s" repeatCount="indefinite" path="M{cx - r} {cy} a{r} {r * 0.28} 0 1 0 {2 * r} 0 a{r} {r * 0.28} 0 1 0 {-2 * r} 0"/></circle></g>'

    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b0820"/><stop offset="1" stop-color="#140b33"/></linearGradient>
<radialGradient id="core" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CY}" stop-opacity=".45"/><stop offset=".6" stop-color="{MG}" stop-opacity=".12"/><stop offset="1" stop-color="{MG}" stop-opacity="0"/></radialGradient>
<filter id="ng" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
{SCANLINES}
<clipPath id="term"><rect x="10" y="10" width="560" height="{H - 20}" rx="10"/></clipPath>
</defs>
<style>
@keyframes cur{{0%,49%{{opacity:1}}50%,100%{{opacity:0}}}}
@keyframes flick{{0%,100%{{opacity:1}}92%{{opacity:1}}93%{{opacity:.3}}94%{{opacity:1}}96%{{opacity:.5}}97%{{opacity:1}}}}
@keyframes float{{0%,100%{{transform:translateY(-6px)}}50%{{transform:translateY(6px)}}}}
@keyframes scanY{{from{{transform:translateY(0)}}to{{transform:translateY({H}px)}}}}
@keyframes beam{{0%,100%{{opacity:.25}}50%{{opacity:.6}}}}
.holo{{animation:float 5s ease-in-out infinite}}
</style>
<!-- terminal -->
<g style="animation:flick 6s infinite">
<rect x="10" y="10" width="560" height="{H - 20}" rx="10" fill="url(#panel)" stroke="{CY}" stroke-opacity=".6"/>
<rect x="10" y="10" width="560" height="32" rx="10" fill="#1b1240"/>
<rect x="10" y="30" width="560" height="12" fill="#1b1240"/>
<circle cx="32" cy="26" r="6" fill="#ff5f56"/><circle cx="52" cy="26" r="6" fill="#ffbd2e"/><circle cx="72" cy="26" r="6" fill="#27c93f"/>
<text x="290" y="31" font-family="{FONT}" font-size="12" fill="#8f8fbf" text-anchor="middle">andhika@cyberdeck: ~/profile</text>
<g font-family="{FONT}" font-size="{fs}" xml:space="preserve">{"".join(out)}</g>
<rect x="32" y="{cursor_y - 15}" width="9" height="17" fill="{CY}" style="animation:cur 1s steps(1) infinite"/>
<g clip-path="url(#term)"><rect x="10" y="-40" width="560" height="40" fill="{CY}" opacity=".06" style="animation:scanY 4s linear infinite"/>
<rect x="10" y="10" width="560" height="{H - 20}" fill="url(#scan)"/></g>
</g>
<!-- hologram projector -->
<ellipse cx="{cx}" cy="{H - 40}" rx="110" ry="16" fill="none" stroke="{CY}" stroke-width="2" filter="url(#ng)"/>
<ellipse cx="{cx}" cy="{H - 40}" rx="70" ry="9" fill="{CY}" opacity=".25"/>
<path d="M{cx - 110} {H - 40} L{cx - 160} 40 L{cx + 160} 40 L{cx + 110} {H - 40}Z" fill="{CY}" fill-opacity=".07" style="animation:beam 3s infinite"/>
<g class="holo">
<circle cx="{cx}" cy="{cy}" r="150" fill="url(#core)"/>
{rings}
<g filter="url(#ng)">
{anim_path(cube, 12, CY, 2, .95)}
{anim_path(ico, 9, MG, 1.6, .9)}
{anim_path(octa, 6, YL, 1.4, .9)}
{"".join(nodes)}
</g>
</g>
<g font-family="{FONT}" font-size="11" fill="{CY}" opacity=".85">
<text x="{cx}" y="{H - 12}" text-anchor="middle" letter-spacing="3">// CORE.MODULE :: FULL-STACK</text></g>
</svg>'''
    w("about.svg", s)


# ============================================================== 3D TECH ORBIT
def orbit():
    W, H = 1000, 360
    cx, cy = W / 2, 175
    techs = [("React", CY), ("Laravel", MG), ("TypeScript", CY), ("Node.js", "#9dff9d"), ("Tailwind", CY),
             ("PHP", MG), ("MySQL", YL), ("PostgreSQL", CY), ("Express", "#e6e6ff"), ("Vite", YL),
             ("JavaScript", YL), ("AI APIs", MG)]
    FR, dur = 90, 24
    R, tilt = 400, math.radians(72)
    items = []
    for i, (name, col) in enumerate(techs):
        ph = i / len(techs) * 2 * math.pi
        tx, sc, op = [], [], []
        for k in range(FR + 1):
            a = ph + k / FR * 2 * math.pi
            x, y, z = R * math.cos(a), 0, R * math.sin(a)
            y, z = y * math.cos(tilt) - z * math.sin(tilt), y * math.sin(tilt) + z * math.cos(tilt)
            d = 1100
            kk = d / (d + z)
            tx.append(f"{f(cx + x * kk)} {f(cy + y * kk * 0.32 + 10)}")
            sc.append(f"{kk:.3f}")
            op.append(f"{max(.18, min(1, (kk - .6) * 1.9)):.2f}")
        bw = len(name) * 10 + 34
        items.append(f'''<g><animateTransform attributeName="transform" type="translate" values="{';'.join(tx)}" dur="{dur}s" repeatCount="indefinite"/>
<animate attributeName="opacity" values="{';'.join(op)}" dur="{dur}s" repeatCount="indefinite"/>
<g><animateTransform attributeName="transform" type="scale" values="{';'.join(sc)}" dur="{dur}s" repeatCount="indefinite"/>
<rect x="{-bw / 2}" y="-17" width="{bw}" height="34" rx="17" fill="#0b0820" stroke="{col}" stroke-width="2" filter="url(#ng)"/>
<text y="6" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="{col}">{name}</text></g></g>''')
    core = wire_frames(ICO_V, ICO_E, cx, cy, 60, 60, lambda t: (t, t * 2, 0))
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<radialGradient id="cg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{MG}" stop-opacity=".5"/><stop offset="1" stop-color="{MG}" stop-opacity="0"/></radialGradient>
<filter id="ng" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>@keyframes pl{{0%,100%{{opacity:.4}}50%{{opacity:1}}}}</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
<ellipse cx="{cx}" cy="{cy + 10}" rx="{R}" ry="{R * 0.95 * 0.32}" fill="none" stroke="{CY}" stroke-opacity=".35" stroke-dasharray="2 10"><animate attributeName="stroke-dashoffset" values="0;-240" dur="8s" repeatCount="indefinite"/></ellipse>
<ellipse cx="{cx}" cy="{cy + 10}" rx="{R * .7}" ry="{R * .7 * 0.3}" fill="none" stroke="{MG}" stroke-opacity=".25" stroke-dasharray="6 6"><animate attributeName="stroke-dashoffset" values="0;120" dur="6s" repeatCount="indefinite"/></ellipse>
<circle cx="{cx}" cy="{cy}" r="120" fill="url(#cg)" style="animation:pl 3s infinite"/>
<path fill="none" stroke="{CY}" stroke-width="1.6" filter="url(#ng)" d="{core[0]}"><animate attributeName="d" values="{';'.join(core + [core[0]])}" dur="10s" repeatCount="indefinite"/></path>
<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="{FONT}" font-size="13" fill="#fff" letter-spacing="2">&lt;/&gt;</text>
{"".join(items)}
</svg>'''
    w("tech-orbit.svg", s)


# ============================================================== WHAT I BUILD (holo cards)
def build():
    W, H = 1000, 270
    cards = [
        ("LANDING PAGES", "fast · responsive", "conversion-focused", CY,
         '<rect x="-22" y="-16" width="44" height="32" rx="3"/><path d="M-22 -8H22M-14 0H6M-14 7H14"/>'),
        ("BOOKING ENGINE", "real-time", "availability", MG,
         '<rect x="-20" y="-16" width="40" height="34" rx="3"/><path d="M-20 -6H20M-10 -22V-12M10 -22V-12"/><path d="M-8 6l5 5 10-10"/>'),
        ("DASHBOARDS", "data · users", "operations", YL,
         '<rect x="-22" y="-18" width="44" height="36" rx="3"/><path d="M-14 10V2M-5 10V-6M4 10V-2M13 10V-10"/>'),
        ("AI INTEGRATION", "smart features", "modern AI APIs", "#9dff9d",
         '<circle r="14"/><circle r="4"/><path d="M0 -14V-22M0 14V22M-14 0H-22M14 0H22M10 -10l6 -6M-10 10l-6 6M10 10l6 6M-10 -10l-6 -6"/>'),
        ("WEB + MOBILE", "end-to-end", "database to UI", CY,
         '<rect x="-24" y="-16" width="32" height="26" rx="2"/><rect x="10" y="-12" width="16" height="28" rx="3"/><path d="M-30 14H12"/>'),
    ]
    cw, gap = 176, 20
    x0 = (W - (cw * 5 + gap * 4)) / 2
    g = []
    for i, (t, a, b, c, icon) in enumerate(cards):
        x = x0 + i * (cw + gap)
        d = i * 0.35
        g.append(f'''<g style="animation:bob 4s {-d * 2:.2f}s ease-in-out infinite">
<rect x="{x}" y="40" width="{cw}" height="190" rx="10" fill="#0b0820" stroke="{c}" stroke-opacity=".35"/>
<rect x="{x}" y="40" width="{cw}" height="190" rx="10" fill="none" stroke="{c}" stroke-width="2" stroke-dasharray="90 600" filter="url(#ng)" style="animation:run 4s {-i * .8:.1f}s linear infinite"/>
<path d="M{x + 12} 52h20M{x + 12} 52v20M{x + cw - 12} 218h-20M{x + cw - 12} 218v-20" stroke="{c}" stroke-width="2" fill="none"/>
<g transform="translate({x + cw / 2} 105)"><g fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#ng)" style="animation:spinY 6s {-i:.0f}s ease-in-out infinite">{icon}</g></g>
<circle cx="{x + cw / 2}" cy="105" r="38" fill="none" stroke="{c}" stroke-opacity=".3" stroke-dasharray="3 6" style="animation:rot 10s linear infinite;transform-origin:{x + cw / 2}px 105px"/>
<text x="{x + cw / 2}" y="172" text-anchor="middle" font-family="{DISP}" font-weight="800" font-size="15" letter-spacing="1.5" fill="#fff">{t}</text>
<text x="{x + cw / 2}" y="194" text-anchor="middle" font-family="{FONT}" font-size="12" fill="{c}">{a}</text>
<text x="{x + cw / 2}" y="211" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#9a9ac8">{b}</text>
<text x="{x + cw - 14}" y="62" text-anchor="end" font-family="{FONT}" font-size="10" fill="{c}" opacity=".7">0{i + 1}</text>
</g>''')
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><filter id="ng" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
@keyframes rise{{from{{opacity:0;transform:translateY(40px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}
@keyframes run{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-690}}}}
@keyframes rot{{to{{transform:rotate(360deg)}}}}
@keyframes spinY{{0%,60%,100%{{transform:scaleX(1)}}70%{{transform:scaleX(-1)}}80%{{transform:scaleX(1)}}}}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
{"".join(g)}
</svg>'''
    w("build.svg", s)


# ============================================================== SECTION TITLES (variasi animasi)
def title(fname, label, style, color):
    W, H = 900, 80
    txt = label.replace("&", "&amp;")
    cx = W / 2
    fsz = 34
    # spinning 3D coin icon (scaleX = rotasi sumbu Y)
    def icon(x):
        return f'''<g transform="translate({x} 40)"><g style="animation:coin 3s linear infinite">
<polygon points="0,-20 17,-10 17,10 0,20 -17,10 -17,-10" fill="none" stroke="{color}" stroke-width="2.5" filter="url(#ng)"/>
<polygon points="0,-10 9,-5 9,5 0,10 -9,5 -9,-5" fill="{color}" opacity=".5"/></g></g>'''
    tw = len(label) * (fsz * 0.8 + 5)
    left, right = cx - tw / 2 - 40, cx + tw / 2 + 40
    base_text = f'font-family="{DISP}" font-weight="900" font-size="{fsz}" letter-spacing="5" text-anchor="middle"'
    extra_css, body = "", ""
    if style == "glitch":
        extra_css = """@keyframes g1{0%,80%,100%{transform:translate(0)}82%{transform:translate(-5px,2px)}84%{transform:translate(4px,-1px)}86%{transform:translate(-2px,1px)}}
@keyframes g2{0%,80%,100%{transform:translate(0)}82%{transform:translate(5px,-2px)}84%{transform:translate(-4px,1px)}86%{transform:translate(2px,-1px)}}"""
        body = f'''<text x="{cx}" y="52" {base_text} fill="{MG}" style="animation:g1 3s infinite">{txt}</text>
<text x="{cx}" y="52" {base_text} fill="{CY}" style="animation:g2 3s infinite">{txt}</text>
<text x="{cx}" y="52" {base_text} fill="#fff">{txt}</text>'''
    elif style == "flicker":
        extra_css = """@keyframes fl{0%,18%,22%,25%,53%,57%,100%{opacity:1}20%,24%,55%{opacity:.15}}"""
        body = f'<text x="{cx}" y="52" {base_text} fill="none" stroke="{color}" stroke-width="1.5" filter="url(#ng)" style="animation:fl 3.5s infinite">{txt}</text><text x="{cx}" y="52" {base_text} fill="{color}" opacity=".9" style="animation:fl 3.5s infinite">{txt}</text>'
    elif style == "sweep":
        body = f'''<defs><linearGradient id="sw" x1="0" x2="1"><stop offset="0" stop-color="{color}"/><stop offset=".45" stop-color="{color}"/><stop offset=".5" stop-color="#fff"/><stop offset=".55" stop-color="{color}"/><stop offset="1" stop-color="{color}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="2.5s" repeatCount="indefinite"/></linearGradient></defs>
<text x="{cx}" y="52" {base_text} fill="url(#sw)" filter="url(#ng)">{txt}</text>'''
    elif style == "type":
        n = len(label)
        x0 = cx - tw / 2 - 10
        ws = [f((tw + 20) * k / n) for k in range(n + 1)]
        xs = [f(x0 + (tw + 20) * k / n) for k in range(n + 1)]
        kt = ";".join(f"{k / n * .6:.3f}" for k in range(n + 1)) + ";.95;1"
        body = f'''<clipPath id="tc"><rect x="{f(x0)}" y="0" height="{H}" width="0"><animate attributeName="width" values="{';'.join(ws)};{ws[-1]};0" keyTimes="{kt}" dur="5s" calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>
<text x="{cx}" y="52" {base_text} fill="{color}" filter="url(#ng)" clip-path="url(#tc)">{txt}</text>
<rect y="18" width="14" height="44" fill="{color}" style="animation:cb 1s steps(1) infinite"><animate attributeName="x" values="{';'.join(xs)};{xs[-1]};{xs[0]}" keyTimes="{kt}" dur="5s" calcMode="discrete" repeatCount="indefinite"/></rect>'''
        extra_css = "@keyframes cb{0%,49%{opacity:1}50%,100%{opacity:0}}"
    elif style == "wave":
        extra_css = "@keyframes wv{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}"
        step = fsz * 0.82
        tw = step * len(label)
        letters = "".join(
            f'<text x="{f(cx - tw / 2 + step * (i + .5))}" y="54" {base_text} fill="{[CY, MG, YL][i % 3] if ch != " " else color}" style="animation:wv 1.6s {i * .08:.2f}s ease-in-out infinite">{ch.replace("&", "&amp;")}</text>'
            for i, ch in enumerate(label) if ch != " ")
        body = f'<g filter="url(#ng)">{letters}</g>'
    elif style == "draw":
        extra_css = "@keyframes dr{0%{stroke-dashoffset:600;fill-opacity:0}50%{stroke-dashoffset:0;fill-opacity:0}70%,90%{stroke-dashoffset:0;fill-opacity:1}100%{stroke-dashoffset:600;fill-opacity:0}}"
        body = f'<text x="{cx}" y="52" {base_text} fill="{color}" stroke="{color}" stroke-width="1.5" stroke-dasharray="300 300" filter="url(#ng)" style="animation:dr 6s ease-in-out infinite">{txt}</text>'
    elif style == "holo":
        extra_css = "@keyframes sk{0%,100%{transform:skewX(0)}48%{transform:skewX(0)}50%{transform:skewX(25deg)}52%{transform:skewX(-15deg)}54%{transform:skewX(0)}} @keyframes ln{from{transform:translateY(-30px)}to{transform:translateY(90px)}}"
        body = f'''<clipPath id="hc"><text x="{cx}" y="52" {base_text}>{txt}</text></clipPath>
<g style="animation:sk 4s infinite;transform-origin:{cx}px 40px"><text x="{cx}" y="52" {base_text} fill="{color}" opacity=".85" filter="url(#ng)">{txt}</text>
<g clip-path="url(#hc)"><rect x="0" y="0" width="{W}" height="6" fill="#fff" opacity=".8" style="animation:ln 1.8s linear infinite"/>
{"".join(f'<rect x="0" y="{y}" width="{W}" height="1.5" fill="#000" opacity=".5"/>' for y in range(14, 60, 4))}</g></g>'''
    elif style == "signal":
        extra_css = "@keyframes rp{0%{r:4;opacity:1}100%{r:34;opacity:0}} @keyframes eq{0%,100%{transform:scaleY(.3)}50%{transform:scaleY(1)}}"
        bars = lambda x0, dirn: "".join(
            f'<rect x="{x0 + dirn * i * 9}" y="20" width="5" height="40" fill="{[CY, MG][i % 2]}" style="animation:eq {0.6 + (i % 4) * .17:.2f}s {i * .1:.1f}s ease-in-out infinite;transform-origin:{x0 + dirn * i * 9}px 40px;transform-box:fill-box"/>'
            for i in range(6))
        body = f'''<text x="{cx}" y="52" {base_text} fill="{color}" filter="url(#ng)">{txt}</text>
{bars(left - 30, -1)}{bars(right + 25, 1)}'''
        left, right = left - 90, right + 90
    lines = f'''<line x1="20" x2="{left - 30}" y1="40" y2="40" stroke="{color}" stroke-width="2" stroke-dasharray="14 6" opacity=".7" style="animation:dash 1.2s linear infinite"/>
<line x1="{right + 30}" x2="{W - 20}" y1="40" y2="40" stroke="{color}" stroke-width="2" stroke-dasharray="14 6" opacity=".7" style="animation:dash2 1.2s linear infinite"/>'''
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><filter id="ng" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<style>
@keyframes coin{{0%{{transform:scaleX(1)}}25%{{transform:scaleX(.05)}}50%{{transform:scaleX(-1)}}75%{{transform:scaleX(.05)}}100%{{transform:scaleX(1)}}}}
@keyframes dash{{to{{stroke-dashoffset:-40}}}} @keyframes dash2{{to{{stroke-dashoffset:40}}}}
{extra_css}
</style>
<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>
{lines}
{icon(left)}{icon(right)}
{body}
</svg>'''
    w(os.path.join("titles", fname), s)


# ============================================================== DIVIDER
def divider():
    W, H = 1000, 24
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="dl" x1="0" x2="1"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset=".5" stop-color="{CY}"/><stop offset="1" stop-color="{MG}" stop-opacity="0"/></linearGradient>
<filter id="ng" x="-10%" y="-200%" width="120%" height="500%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>
<rect y="11" width="{W}" height="2" fill="url(#dl)"/>
<g filter="url(#ng)">
<rect y="9" width="70" height="6" rx="3" fill="{CY}"><animate attributeName="x" values="-80;{W}" dur="2.6s" repeatCount="indefinite"/></rect>
<rect y="10" width="40" height="4" rx="2" fill="{MG}"><animate attributeName="x" values="{W};-50" dur="3.4s" repeatCount="indefinite"/></rect>
<circle cy="12" r="3" fill="{YL}"><animate attributeName="cx" values="-10;{W + 10}" dur="1.7s" repeatCount="indefinite"/></circle></g>
<g fill="{CY}">{"".join(f'<rect x="{x}" y="5" width="3" height="14" opacity=".5"><animate attributeName="opacity" values=".1;1;.1" dur="1.5s" begin="{i * .2:.1f}s" repeatCount="indefinite"/></rect>' for i, x in enumerate(range(470, 535, 10)))}</g>
</svg>'''
    w("divider.svg", s)


# ============================================================== FOOTER
def footer():
    W, H = 1200, 230
    quote = "“Code is like humor. When you have to explain it, it’s bad.”"
    msg = "[ END OF TRANSMISSION ]  ·  THANKS FOR VISITING  ·  JACK IN ANYTIME  ·  "
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs><linearGradient id="fb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}" stop-opacity="0"/><stop offset=".35" stop-color="{BG2}"/><stop offset="1" stop-color="#05030f"/></linearGradient>
<linearGradient id="qg" x1="0" x2="1"><stop offset="0" stop-color="{CY}"/><stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="{MG}"/>
<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="5s" repeatCount="indefinite"/></linearGradient>
<filter id="ng" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="2.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="tk"><rect x="0" y="150" width="{W}" height="40"/></clipPath>
{SCANLINES}</defs>
<style>@keyframes mq{{from{{transform:translateX(0)}}to{{transform:translateX(-{len(msg) * 9.6:.0f}px)}}}}
@keyframes fl{{0%,94%,100%{{opacity:1}}95%{{opacity:.3}}97%{{opacity:.8}}}}</style>
<path fill="url(#fb)" d="M0 40 Q300 0 600 40 T1200 40 V{H} H0Z"><animate attributeName="d" dur="8s" repeatCount="indefinite"
values="M0 40 Q300 0 600 40 T1200 40 V{H} H0Z;M0 40 Q300 80 600 40 T1200 40 V{H} H0Z;M0 40 Q300 0 600 40 T1200 40 V{H} H0Z"/></path>
<path fill="none" stroke="{CY}" stroke-width="2" filter="url(#ng)" d="M0 40 Q300 0 600 40 T1200 40"><animate attributeName="d" dur="8s" repeatCount="indefinite"
values="M0 40 Q300 0 600 40 T1200 40;M0 40 Q300 80 600 40 T1200 40;M0 40 Q300 0 600 40 T1200 40"/></path>
<text x="600" y="115" text-anchor="middle" font-family="{FONT}" font-size="24" font-style="italic" fill="url(#qg)" filter="url(#ng)" style="animation:fl 4s infinite">{quote}</text>
<rect x="0" y="152" width="{W}" height="34" fill="#000" opacity=".4"/>
<line x1="0" x2="{W}" y1="152" y2="152" stroke="{MG}" opacity=".6"/><line x1="0" x2="{W}" y1="186" y2="186" stroke="{MG}" opacity=".6"/>
<g clip-path="url(#tk)"><text y="175" font-family="{FONT}" font-size="16" fill="{YL}" letter-spacing="0" style="animation:mq 14s linear infinite" xml:space="preserve">{msg * 6}</text></g>
<text x="600" y="215" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#8f8fbf">© ANDHIKA RIZKY NUR WAHYU · BUILT WITH NEON &amp; CAFFEINE</text>
<rect width="{W}" height="{H}" fill="url(#scan)"/>
</svg>'''
    w("footer.svg", s)


header(); about(); orbit(); build(); divider(); footer()
for fn, lab, st, col in [
    ("about.svg", "ABOUT_ME", "glitch", CY),
    ("stack.svg", "TECH_STACK", "flicker", MG),
    ("build.svg", "WHAT_I_BUILD", "sweep", CY),
    ("stats.svg", "SYSTEM_STATS", "type", YL),
    ("trophy.svg", "ACHIEVEMENTS", "wave", MG),
    ("snake.svg", "DATA_SNAKE", "draw", CY),
    ("city.svg", "3D_CONTRIB_CITY", "holo", MG),
    ("connect.svg", "CONNECT", "signal", CY),
]:
    title(fn, lab, st, col)
print("ok")
