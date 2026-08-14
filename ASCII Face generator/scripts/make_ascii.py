from pathlib import Path

# Input & Output Paths
IMAGE_PATH = Path("ascii-face.svg")       # Your existing SVG image
OUTPUT_PATH = Path("assets/profile-card.svg") # Final output SVG

# -------------------------------------------------------------------------
# 1. Right Side Content (Skills + Contact Info)
# -------------------------------------------------------------------------
INFO_BLOCKS = [
    ("header", "Srishti@portfolio"),
    ("item", "OS", "Linux, Windows 11"),
    ("item", "Uptime", "Continuous Learning and Building"),
    ("item", "Role", "Data Analyst / Python Developer"),
    ("item", "IDE", "VSCode, Jupyter Notebook, Colab"),
    ("blank", ""),
    ("section", "Skills & Tech Stack"),
    ("item", "Programming", "Python, SQL"),
    ("item", "Data.Analytics", "Pandas, NumPy, Matplotlib, EDA"),
    ("item", "Databases", "MySQL, PostgreSQL"),
    ("item", "Visualization", "Tableau, Matplotlib"),
    ("item", "Development", "Jupyter Notebook, Google Colab"),
    ("item", "Design", "Figma"),
    ("item", "Collaboration", "GitHub"),
    ("blank", ""),
    ("section", "Contact Information"),
    ("item", "Email.Personal", "srishtikumari168@gmail.com"),
    ("item", "LinkedIn", "linkedin.com/in/srishti-kumari-psk816"),
    ("item", "GitHub", "github.com/Srishti160"),
    ("item", "Location", "India"),
]

# -------------------------------------------------------------------------
# 2. Geometry & Typography Settings
# -------------------------------------------------------------------------
FONT_SIZE = 15          
LINE_HEIGHT = 23.5      
TOTAL_TEXT_COLS = 50    # Monospace columns for dot leader alignment

# Layout dimensions
PAD_X = 35
PAD_Y = 40

# --- CHANGE: Image is made even smaller (65% scale) ---
IMG_SCALE = 0.75
IMG_DISPLAY_WIDTH = int(340 * IMG_SCALE)  # Adjusted reserved space

# --- CHANGE: Text shifted left further to maintain balance ---
INFO_X_START = 440      

# Canvas Dimensions
total_info_lines = len(INFO_BLOCKS)
content_height = int(total_info_lines * LINE_HEIGHT)
SVG_HEIGHT = max(content_height + (PAD_Y * 2), 560)
SVG_WIDTH = 900        # Kept expanded width for larger text

# -------------------------------------------------------------------------
# 3. Read and Prepare Embedded SVG
# -------------------------------------------------------------------------
raw_svg = IMAGE_PATH.read_text(encoding="utf-8").strip()

if "<?xml" in raw_svg:
    raw_svg = raw_svg.split("?>", 1)[-1].strip()

svg_open_idx = raw_svg.find("<svg")
if svg_open_idx != -1:
    tag_close_idx = raw_svg.find(">", svg_open_idx)
    raw_svg_body = raw_svg[tag_close_idx + 1 : raw_svg.rfind("</svg>")].strip()
else:
    raw_svg_body = raw_svg

def escape(t):
    return str(t).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# -------------------------------------------------------------------------
# 4. Build Output SVG
# -------------------------------------------------------------------------
svg = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVG_WIDTH}" height="{SVG_HEIGHT}" viewBox="0 0 {SVG_WIDTH} {SVG_HEIGHT}">',
    '  <rect width="100%" height="100%" rx="18" fill="#0d1117" stroke="#30363d" stroke-width="1.5"/>',
    '  <style>',
    f'    .mono {{ font-family: ui-monospace, "SF Mono", "Fira Code", "JetBrains Mono", Consolas, monospace; font-size: {FONT_SIZE}px; }}',
    '    .title { fill: #58a6ff; font-weight: bold; }',
    '    .sec { fill: #d2a8ff; font-weight: bold; }',
    '    .label { fill: #ff9b54; }',
    '    .val { fill: #8cb4d9; }',
    '    .dim { fill: #484f58; }',
    '    .row { opacity: 0; animation: fadeSlide 0.2s ease-out forwards; }',
    '    @keyframes fadeSlide {',
    '      from { opacity: 0; transform: translateY(4px); }',
    '      to { opacity: 1; transform: translateY(0); }',
    '    }',
    '  </style>',
    '',
    '  <!-- Left Column: Embedded Image (Scaled Even Smaller) -->',
    # --- CHANGE: Apply smaller scale transform here ---
    f'  <g transform="translate({PAD_X}, {PAD_Y}) scale({IMG_SCALE})">',
    f'    {raw_svg_body}',
    '  </g>',
    '',
    '  <!-- Right Column: Larger, Positioned Profile Info -->',
]

delay_idx = 0
y_info = PAD_Y + 16

for item in INFO_BLOCKS:
    delay = delay_idx * 0.015
    delay_idx += 1
    itype = item[0]

    if itype == "header":
        title = escape(item[1])
        sep = "-" * max(4, TOTAL_TEXT_COLS - len(title) - 1)
        svg.append(
            f'  <text x="{INFO_X_START}" y="{y_info}" class="mono row" style="animation-delay:{delay:.3f}s;">'
            f'<tspan class="title">{title}</tspan> <tspan class="dim">{sep}</tspan>'
            f'</text>'
        )
        y_info += int(LINE_HEIGHT)

    elif itype == "section":
        sec_title = f"- {escape(item[1])} "
        sep = "-" * max(4, TOTAL_TEXT_COLS - len(sec_title))
        svg.append(
            f'  <text x="{INFO_X_START}" y="{y_info}" class="mono row" style="animation-delay:{delay:.3f}s;">'
            f'<tspan class="sec">{sec_title}</tspan><tspan class="dim">{sep}</tspan>'
            f'</text>'
        )
        y_info += int(LINE_HEIGHT)

    elif itype == "item":
        key, val = escape(item[1]), escape(item[2])
        lead = f". {key}:"
        dots_count = max(2, TOTAL_TEXT_COLS - (len(lead) + len(val) + 2))
        dots = " " + ("." * dots_count) + " "

        svg.append(
            f'  <text x="{INFO_X_START}" y="{y_info}" class="mono row" style="animation-delay:{delay:.3f}s;">'
            f'<tspan class="label">{lead}</tspan>'
            f'<tspan class="dim">{dots}</tspan>'
            f'<tspan class="val">{val}</tspan>'
            f'</text>'
        )
        y_info += int(LINE_HEIGHT)

    elif itype == "blank":
        y_info += int(LINE_HEIGHT * 0.5)

svg.append("</svg>")

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH.write_text("\n".join(svg), encoding="utf-8")

print(f"Card generated successfully: {OUTPUT_PATH}")