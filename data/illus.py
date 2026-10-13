"""Brand-coloured medical illustrations (SVG) for the treatments brochure."""
NAVY = "#24507A"; CY = "#22AFC4"; CYL = "#3DD5E6"; AQ = "#1EE6CF"; GR = "#8DC63F"; GRD = "#6FA52B"
BG = "#E8F9FB"; BGG = "#EEF7E2"; WHITE = "#FFFFFF"

import itertools, re
_c = itertools.count()
def wrap(inner, bg=BG, vb="0 0 240 180"):
    n = next(_c)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" width="100%">
<defs>
 <linearGradient id="gA" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYL}"/><stop offset="1" stop-color="{AQ}"/></linearGradient>
 <linearGradient id="gG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#B5E07A"/><stop offset="1" stop-color="{GR}"/></linearGradient>
 <linearGradient id="gN" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2F6A9C"/><stop offset="1" stop-color="{NAVY}"/></linearGradient>
 <radialGradient id="gel" cx="0.38" cy="0.32" r="0.75"><stop offset="0" stop-color="#FFFFFF"/><stop offset="0.45" stop-color="#D9F6F9"/><stop offset="1" stop-color="#8FD9E4"/></radialGradient>
</defs>
<rect x="0" y="0" width="240" height="180" rx="18" fill="{bg}"/>
<circle cx="205" cy="28" r="40" fill="#FFFFFF" opacity=".55"/><circle cx="30" cy="160" r="34" fill="#FFFFFF" opacity=".5"/>
{inner}</svg>'''
    svg = re.sub(r'id="(g\w+|gel)"', lambda m: f'id="{m.group(1)}{n}"', svg)
    svg = re.sub(r'url\(#(g\w+|gel)\)', lambda m: f'url(#{m.group(1)}{n})', svg)
    return svg

def breast_implant():
    return wrap(f'''
<ellipse cx="118" cy="146" rx="70" ry="9" fill="{NAVY}" opacity=".10"/>
<path d="M58 132 C52 92 82 52 118 52 C154 52 184 92 178 132 C176 142 160 146 118 146 C76 146 60 142 58 132 Z" fill="#C7F1F6" stroke="{CY}" stroke-width="2.5"/>
<path d="M84 84 C92 70 104 64 116 64" fill="none" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round" opacity=".9"/>
<path d="M66 128 C90 136 146 136 170 128" fill="none" stroke="{CY}" stroke-width="1.5" opacity=".6"/>
<g transform="translate(26 38)"><rect width="16" height="96" rx="3" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.5"/>
{"".join(f'<line x1="0" y1="{8+i*8}" x2="{8 if i%2 else 11}" y2="{8+i*8}" stroke="{NAVY}" stroke-width="1.2"/>' for i in range(11))}</g>
<g transform="translate(188 46)"><circle r="16" fill="{GR}"/><path d="M-7 0 l5 5 l9 -10" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>''')

def liposuction():
    return wrap(f'''
<path d="M96 22 C84 44 80 62 86 82 C90 96 80 112 78 132 C77 146 82 160 86 172 L150 172 C154 160 159 146 158 132 C156 112 146 96 150 82 C156 62 152 44 140 22 Z" fill="{WHITE}" stroke="{NAVY}" stroke-width="2.2"/>
<path d="M86 82 C70 92 64 112 72 132" fill="none" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 4" opacity=".45"/>
<path d="M150 82 C166 92 172 112 164 132" fill="none" stroke="{NAVY}" stroke-width="2" stroke-dasharray="4 4" opacity=".45"/>
<path d="M64 106 l14 0 m-5 -5 l5 5 l-5 5" stroke="{GRD}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M172 106 l-14 0 m5 -5 l-5 5 l5 5" stroke="{GRD}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M98 120 C110 126 126 126 138 120" fill="none" stroke="{CY}" stroke-width="2" opacity=".7"/>
<g transform="rotate(-28 190 140)"><rect x="150" y="134" width="70" height="7" rx="3.5" fill="#C9D7DF" stroke="{NAVY}" stroke-width="1.4"/>
<rect x="206" y="128" width="22" height="19" rx="5" fill="#2B5E8C"/><circle cx="156" cy="137.5" r="1.6" fill="{NAVY}"/></g>
<g fill="{AQ}" opacity=".9"><circle cx="40" cy="60" r="5"/><circle cx="52" cy="44" r="3.5"/><circle cx="34" cy="38" r="2.5"/></g>''')

def rhinoplasty():
    return wrap(f'''
<path d="M150 20 C142 40 128 56 120 74 C112 92 100 104 96 114 C93 122 100 128 110 128 C116 128 118 132 116 138 C114 146 120 152 128 152 C136 152 140 160 138 172" fill="none" stroke="{NAVY}" stroke-width="3" stroke-linecap="round"/>
<path d="M120 74 C114 84 102 92 94 108" fill="none" stroke="{CY}" stroke-width="3" stroke-dasharray="5 5" stroke-linecap="round"/>
<path d="M124 112 c4 -2 9 -1 11 3" fill="none" stroke="{NAVY}" stroke-width="2.4" stroke-linecap="round"/>
<path d="M172 52 C178 50 186 52 190 58" fill="none" stroke="{NAVY}" stroke-width="2.4" stroke-linecap="round" opacity=".7"/>
<g transform="translate(46 60)"><rect width="44" height="26" rx="6" fill="{WHITE}" stroke="{CY}" stroke-width="1.6"/>
<text x="22" y="17" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="{CY}">PLAN</text></g>
<path d="M90 73 C98 74 104 78 108 84" fill="none" stroke="{CY}" stroke-width="1.6" stroke-dasharray="2 3"/>
<g transform="translate(58 128)"><circle r="14" fill="{GR}"/><path d="M-6 0 l4 4 l8 -9" fill="none" stroke="#fff" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></g>''')

def obesity():
    return wrap(f'''
<path d="M104 30 C96 34 92 44 96 54 C80 60 66 80 70 104 C74 132 104 150 134 144 C160 138 176 114 170 90 C166 72 150 58 130 56 C128 44 118 32 104 30 Z" fill="#FFE1D6" stroke="{NAVY}" stroke-width="2.2"/>
<path d="M104 32 C100 40 102 50 112 56 C124 64 132 76 134 92 C136 112 128 128 112 136" fill="none" stroke="{CY}" stroke-width="3" stroke-dasharray="6 5" stroke-linecap="round"/>
<path d="M112 56 C124 64 132 76 134 92 C136 112 128 128 112 136 C104 140 98 136 100 128 C114 120 120 108 118 92 C116 78 108 68 98 62 Z" fill="#4FD9E6" opacity=".55"/>
<path d="M134 144 C140 156 150 162 160 164" fill="none" stroke="{NAVY}" stroke-width="2.2"/>
<g transform="translate(172 116)"><rect width="50" height="44" rx="9" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.8"/>
<path d="M12 20 a13 13 0 0 1 26 0" fill="none" stroke="{GRD}" stroke-width="3"/><line x1="25" y1="20" x2="32" y2="12" stroke="{NAVY}" stroke-width="2" stroke-linecap="round"/>
<text x="25" y="36" text-anchor="middle" font-family="Inter" font-size="8" font-weight="700" fill="{NAVY}">BMI</text></g>''')

def cancer_surgery():
    return wrap(f'''
<path d="M120 40 C102 40 96 58 106 76 L138 130 L152 120 L124 74 C120 66 122 58 128 58 C134 58 136 66 132 74 L104 120 L118 130 L150 76 C160 58 154 40 136 40 Z" fill="#9ED35A" stroke="{GRD}" stroke-width="2"/>
<g transform="translate(36 112)"><rect x="0" y="0" width="54" height="10" rx="3" fill="#C9D7DF" stroke="{NAVY}" stroke-width="1.4"/><path d="M54 0 L74 5 L54 10 Z" fill="#E9EEF1" stroke="{NAVY}" stroke-width="1.4"/></g>
<g transform="translate(176 54)"><rect width="34" height="44" rx="5" fill="{WHITE}" stroke="{CY}" stroke-width="1.6"/>
<line x1="7" y1="12" x2="27" y2="12" stroke="{CY}" stroke-width="2"/><line x1="7" y1="20" x2="27" y2="20" stroke="{CY}" stroke-width="2"/><line x1="7" y1="28" x2="20" y2="28" stroke="{CY}" stroke-width="2"/></g>
<g fill="{CY}" opacity=".85"><circle cx="58" cy="54" r="10" fill="{WHITE}" stroke="{CY}" stroke-width="2"/><path d="M58 48 v12 M52 54 h12" stroke="{CY}" stroke-width="2.4"/></g>''')

def thyroid():
    return wrap(f'''
<path d="M84 18 C86 60 76 96 60 120 C50 136 40 150 30 176 L210 176 C200 150 190 136 180 120 C164 96 154 60 156 18" fill="{WHITE}" stroke="{NAVY}" stroke-width="2.2"/>
<rect x="110" y="40" width="20" height="78" rx="8" fill="#E6F3F7" stroke="{NAVY}" stroke-width="1.6"/>
{"".join(f'<line x1="111" y1="{50+i*10}" x2="129" y2="{50+i*10}" stroke="{NAVY}" stroke-width="1" opacity=".5"/>' for i in range(7))}
<path d="M120 88 C112 72 92 66 88 84 C84 102 96 116 112 108 C116 106 118 100 120 96 C122 100 124 106 128 108 C144 116 156 102 152 84 C148 66 128 72 120 88 Z" fill="#4FD9E6" stroke="{CY}" stroke-width="2"/>
<path d="M98 82 c3 -4 8 -4 10 0" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>
<g transform="translate(192 58)"><circle r="15" fill="{GR}"/><text y="4" text-anchor="middle" font-family="Inter" font-size="10" font-weight="700" fill="#fff">T3·T4</text></g>''')

def dental_implant():
    return wrap(f'''
<rect x="20" y="112" width="200" height="60" fill="#F6C9C2" opacity=".55"/>
<path d="M20 112 C60 104 80 116 120 108 C160 100 180 114 220 108 L220 120 L20 120 Z" fill="#F2A99F" opacity=".7"/>
<path d="M92 34 C84 36 80 48 84 62 C88 76 90 86 104 86 L136 86 C150 86 152 76 156 62 C160 48 156 36 148 34 C140 32 132 40 120 40 C108 40 100 32 92 34 Z" fill="{WHITE}" stroke="{NAVY}" stroke-width="2.2"/>
<path d="M98 46 c4 -6 10 -6 14 -2" fill="none" stroke="{CYL}" stroke-width="3" stroke-linecap="round"/>
<rect x="108" y="86" width="24" height="18" rx="3" fill="#C9D7DF" stroke="{NAVY}" stroke-width="1.8"/>
<path d="M110 104 L130 104 L128 160 L120 170 L112 160 Z" fill="#2B5E8C"/>
{"".join(f'<path d="M110 {112+i*9} L130 {108+i*9}" stroke="{CYL}" stroke-width="2.2"/>' for i in range(6))}
<g transform="translate(186 50)"><circle r="16" fill="{GR}"/><path d="M-7 0 l5 5 l9 -10" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g>
<text x="52" y="72" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="{NAVY}">CROWN</text>
<text x="52" y="100" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="{NAVY}">ABUTMENT</text>
<text x="52" y="146" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="{NAVY}">IMPLANT</text>
<g stroke="{NAVY}" stroke-width="1" opacity=".5"><line x1="76" y1="69" x2="88" y2="62"/><line x1="82" y1="97" x2="106" y2="95"/><line x1="72" y1="143" x2="108" y2="135"/></g>''')

def hollywood():
    teeth = ""
    xs = [56, 74, 92, 110, 128, 146, 164]
    ws = [16, 17, 18, 19, 18, 17, 16]
    for i, (x, w) in enumerate(zip([48, 66, 85, 104, 124, 143, 161], ws)):
        h = 30 + (6 if i in (2, 3, 4) else 0) - abs(3 - i) * 2
        y = 76 + abs(3 - i) * 3
        teeth += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{WHITE}" stroke="{NAVY}" stroke-width="1.6"/>'
    return wrap(f'''
<path d="M30 80 C60 58 180 58 210 80 C200 132 160 150 120 150 C80 150 40 132 30 80 Z" fill="#F2A99F" opacity=".55"/>
<path d="M34 82 C70 128 170 128 206 82" fill="none" stroke="{NAVY}" stroke-width="2.4"/>
{teeth}
<path d="M52 82 c6 -2 10 -2 14 0" stroke="{CYL}" stroke-width="2" fill="none" opacity=".8"/>
<g fill="{AQ}"><path d="M198 34 l3 8 l8 3 l-8 3 l-3 8 l-3 -8 l-8 -3 l8 -3 z"/><path d="M42 36 l2 5 l5 2 l-5 2 l-2 5 l-2 -5 l-5 -2 l5 -2 z" opacity=".8"/></g>
<g transform="translate(186 128)"><rect x="-22" y="-12" width="44" height="24" rx="12" fill="{GR}"/><text y="4" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="#fff">BL1</text></g>''')

def second_opinion():
    return wrap(f'''
<g transform="translate(28 34)"><rect width="70" height="92" rx="8" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>
<rect x="10" y="12" width="50" height="30" rx="4" fill="#DDEFF4"/><path d="M14 36 l10 -10 l8 8 l8 -12 l16 18" fill="none" stroke="{CY}" stroke-width="2"/>
<line x1="10" y1="54" x2="60" y2="54" stroke="#C9D7DF" stroke-width="3"/><line x1="10" y1="64" x2="52" y2="64" stroke="#C9D7DF" stroke-width="3"/><line x1="10" y1="74" x2="56" y2="74" stroke="#C9D7DF" stroke-width="3"/></g>
<path d="M104 80 L128 80" stroke="{CY}" stroke-width="3" stroke-dasharray="4 4"/><path d="M124 74 l6 6 l-6 6" fill="none" stroke="{CY}" stroke-width="3" stroke-linecap="round"/>
<g transform="translate(134 50)"><rect width="60" height="60" rx="12" fill="#4FD9E6"/><rect x="16" y="16" width="28" height="28" rx="5" fill="none" stroke="#fff" stroke-width="2.4"/>
{"".join(f'<line x1="{20+i*10}" y1="4" x2="{20+i*10}" y2="12" stroke="#fff" stroke-width="2.4"/><line x1="{20+i*10}" y1="48" x2="{20+i*10}" y2="56" stroke="#fff" stroke-width="2.4"/>' for i in range(3))}
<text x="30" y="35" text-anchor="middle" font-family="Inter" font-size="11" font-weight="700" fill="#fff">AI</text></g>
<path d="M164 116 L164 132" stroke="{CY}" stroke-width="3" stroke-dasharray="4 4"/>
<g transform="translate(164 150)"><circle r="18" fill="#2B5E8C"/><circle cy="-5" r="6" fill="#fff"/><path d="M-10 10 c2 -9 18 -9 20 0" fill="#fff"/></g>
<g transform="translate(64 148)"><rect x="-26" y="-12" width="52" height="24" rx="12" fill="{GR}"/><text y="4" text-anchor="middle" font-family="Inter" font-size="9" font-weight="700" fill="#fff">REPORT</text></g>''')

def chronic():
    return wrap(f'''
<g transform="translate(26 30)"><rect width="108" height="78" rx="10" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>
<rect width="108" height="20" rx="10" fill="#2B5E8C"/><rect y="10" width="108" height="10" fill="#2B5E8C"/>
{"".join(f'<rect x="{10+(i%6)*16}" y="{28+(i//6)*16}" width="11" height="11" rx="2" fill="{GR if i in (3, 9, 15) else "#E6F3F7"}"/>' for i in range(18))}</g>
<path d="M20 140 L64 140 L74 120 L86 160 L98 128 L106 140 L150 140" fill="none" stroke="{CY}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"/>
<g transform="translate(160 56)"><rect width="56" height="86" rx="12" fill="{WHITE}" stroke="{NAVY}" stroke-width="2"/>
<rect x="9" y="12" width="38" height="26" rx="4" fill="#DDEFF4"/><text x="28" y="30" text-anchor="middle" font-family="Inter" font-size="11" font-weight="700" fill="{NAVY}">112</text>
<text x="28" y="50" text-anchor="middle" font-family="Inter" font-size="7" font-weight="700" fill="{CY}">mg/dL</text>
<circle cx="28" cy="66" r="9" fill="#4FD9E6"/></g>
<path d="M202 150 c-6 -8 -16 -4 -16 4 c0 8 16 16 16 16 s16 -8 16 -16 c0 -8 -10 -12 -16 -4z" fill="#F07C7C"/>''')

def cover_heart():
    return ""

ILL = {
    "breast": breast_implant, "lipo": liposuction, "rhino": rhinoplasty, "obesity": obesity, "cancer": cancer_surgery,
    "thyroid": thyroid, "implant": dental_implant, "hollywood": hollywood, "second": second_opinion, "chronic": chronic,
}
