#!/usr/bin/env python3
"""
Vintage Cinema Ticket Generator & Slicer for GitHub Profile READMEs
Features:
1. Dynamic Anime Motion Graphics (Manga ink character with counter-rotating spiral eyes,
   floating DEPPAQ mascot, breathing float, and cursed energy ink sparks)
2. Daily rotating literary quotes in English (Frankenstein, Dune, The Myth of Sisyphus,
   The Lord of the Rings, Dante's Inferno, Machado de Assis)
3. Clean modern minimalist stats grid without divider lines
4. Zero-gap modular 6-slice architecture for GitHub Profile READMEs
5. Standalone vector SVGs and animated GIFs
"""

import os
import sys
import argparse
import subprocess
import datetime
import math
import numpy as np
from PIL import Image, ImageOps, ImageDraw, ImageFilter
import cairo
import xml.etree.ElementTree as ET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
DATA_DIR = os.path.join(ASSETS_DIR, "data")
SLICES_DIR = os.path.join(ASSETS_DIR, "slices")
BRAIN_DIR = "/home/gabrielgama/.gemini/antigravity/brain/18274c70-147f-4d8e-8e07-94567acbcf60"

# Ticket Canvas Dimensions
WIDTH = 394
HEIGHT = 705

# 18 Curated English Literary Quotes from Requested Classics
# (Frankenstein, Dune, The Myth of Sisyphus, The Lord of the Rings, Dante's Inferno, Machado de Assis)
BOOK_QUOTES = [
    {
        "id": "dune-fear",
        "book": "Dune",
        "author": "Frank Herbert",
        "lines": [
            "I must not fear. Fear is the mind-killer.",
            "Fear is the little-death that brings obliteration.",
            "Where the fear has gone there will be nothing."
        ],
        "attr": "— Frank Herbert, Dune"
    },
    {
        "id": "frank-fearless",
        "book": "Frankenstein",
        "author": "Mary Shelley",
        "lines": [
            "Beware; for I am fearless,",
            "and therefore powerful.",
            "I will glut the maw of death until it be satiated."
        ],
        "attr": "— Mary Shelley, Frankenstein"
    },
    {
        "id": "sisyphus-happy",
        "book": "The Myth of Sisyphus",
        "author": "Albert Camus",
        "lines": [
            "The struggle itself toward the heights",
            "is enough to fill a man's heart.",
            "One must imagine Sisyphus happy."
        ],
        "attr": "— Albert Camus, The Myth of Sisyphus"
    },
    {
        "id": "lotr-gold",
        "book": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "lines": [
            "All that is gold does not glitter,",
            "Not all those who wander are lost;",
            "The old that is strong does not wither."
        ],
        "attr": "— J.R.R. Tolkien, The Fellowship of the Ring"
    },
    {
        "id": "inferno-hope",
        "book": "Inferno",
        "author": "Dante Alighieri",
        "lines": [
            "Through me the way into the suffering city,",
            "Through me the way to the eternal pain.",
            "Abandon all hope, ye who enter here."
        ],
        "attr": "— Dante Alighieri, Inferno"
    },
    {
        "id": "machado-legacy",
        "book": "The Posthumous Memoirs of Brás Cubas",
        "author": "Machado de Assis",
        "lines": [
            "I had no children,",
            "I transmitted to no one",
            "the legacy of our misery."
        ],
        "attr": "— Machado de Assis, Brás Cubas"
    },
    {
        "id": "dune-mystery",
        "book": "Dune",
        "author": "Frank Herbert",
        "lines": [
            "The mystery of life is not a problem to solve,",
            "but a reality to experience."
        ],
        "attr": "— Frank Herbert, Dune"
    },
    {
        "id": "frank-anguish",
        "book": "Frankenstein",
        "author": "Mary Shelley",
        "lines": [
            "Life, although it may only be an accumulation",
            "of anguish, is dear to me, and I will defend it."
        ],
        "attr": "— Mary Shelley, Frankenstein"
    },
    {
        "id": "sisyphus-shadow",
        "book": "The Myth of Sisyphus",
        "author": "Albert Camus",
        "lines": [
            "There is no sun without shadow,",
            "and it is essential to know the night."
        ],
        "attr": "— Albert Camus, The Myth of Sisyphus"
    },
    {
        "id": "lotr-fighting",
        "book": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "lines": [
            "There is some good in this world, Mr. Frodo,",
            "and it's worth fighting for."
        ],
        "attr": "— J.R.R. Tolkien, The Two Towers"
    },
    {
        "id": "inferno-neutrality",
        "book": "Inferno",
        "author": "Dante Alighieri",
        "lines": [
            "The darkest places in hell are reserved for those",
            "who maintain neutrality in times of moral crisis."
        ],
        "attr": "— Dante Alighieri, Inferno"
    },
    {
        "id": "machado-slate",
        "book": "Dom Casmurro",
        "author": "Machado de Assis",
        "lines": [
            "To forget is a necessity. Life is a slate,",
            "in which fate needs to erase the written."
        ],
        "attr": "— Machado de Assis, Dom Casmurro"
    },
    {
        "id": "dune-universe",
        "book": "Dune",
        "author": "Frank Herbert",
        "lines": [
            "Deep in the human unconscious is a pervasive need",
            "for a logical universe that makes sense."
        ],
        "attr": "— Frank Herbert, Dune"
    },
    {
        "id": "frank-change",
        "book": "Frankenstein",
        "author": "Mary Shelley",
        "lines": [
            "Nothing is so painful to the human mind",
            "as a great and sudden change."
        ],
        "attr": "— Mary Shelley, Frankenstein"
    },
    {
        "id": "sisyphus-summer",
        "book": "The Myth of Sisyphus",
        "author": "Albert Camus",
        "lines": [
            "In the midst of winter, I found there was,",
            "within me, an invincible summer."
        ],
        "attr": "— Albert Camus, The Myth of Sisyphus"
    },
    {
        "id": "lotr-smallest",
        "book": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "lines": [
            "Even the smallest person can change",
            "the course of the future."
        ],
        "attr": "— J.R.R. Tolkien, The Fellowship of the Ring"
    },
    {
        "id": "inferno-stars",
        "book": "Inferno",
        "author": "Dante Alighieri",
        "lines": [
            "And thence we came forth",
            "to see again the stars."
        ],
        "attr": "— Dante Alighieri, Inferno"
    },
    {
        "id": "machado-irony",
        "book": "Philosopher or Dog?",
        "author": "Machado de Assis",
        "lines": [
            "The irony of life is that we look for happiness",
            "far away, when it is woven from everyday threads."
        ],
        "attr": "— Machado de Assis, Philosopher or Dog?"
    }
]

def get_daily_quote(day_index=None, quote_id=None):
    """Selects quote based on explicit ID, day index, or day of the year."""
    if quote_id:
        for q in BOOK_QUOTES:
            if q["id"] == quote_id:
                return q
    if day_index is not None:
        return BOOK_QUOTES[day_index % len(BOOK_QUOTES)]
    day_of_year = datetime.datetime.now().timetuple().tm_yday
    return BOOK_QUOTES[(day_of_year - 1) % len(BOOK_QUOTES)]

def load_path_file(filename):
    """Loads SVG path from assets/data or fallback brain dir."""
    local_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(local_path):
        with open(local_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    brain_path = os.path.join(BRAIN_DIR, filename)
    if os.path.exists(brain_path):
        with open(brain_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def get_arrow_svg(x, y, size=11):
    return f"""<g transform="translate({x}, {y})">
      <line x1="0" y1="{size}" x2="{size}" y2="0" stroke="#111111" stroke-width="1.8" stroke-linecap="round" />
      <line x1="{size*0.4}" y1="0" x2="{size}" y2="0" stroke="#111111" stroke-width="1.8" stroke-linecap="round" />
      <line x1="{size}" y1="0" x2="{size}" y2="{size*0.6}" stroke="#111111" stroke-width="1.8" stroke-linecap="round" />
    </g>"""

def get_umbrella_svg(x, y, scale=1.0):
    return f"""
    <g transform="translate({x}, {y}) scale({scale}) rotate(15)">
      <path d="M -12 0 C -12 -10 12 -10 12 0 C 8 -2 4 -2 0 -1 C -4 -2 -8 -2 -12 0 Z" fill="#111111" />
      <line x1="0" y1="-8" x2="0" y2="-11" stroke="#111111" stroke-width="1.1" stroke-linecap="round" />
      <line x1="0" y1="-1" x2="0" y2="10" stroke="#111111" stroke-width="1.3" stroke-linecap="round" />
      <path d="M 0 10 C 0 13 -4 13 -4 10" fill="none" stroke="#111111" stroke-width="1.3" stroke-linecap="round" />
    </g>"""

def cairo_text_to_path(lines_spec, width, height):
    """
    lines_spec: list of tuples: (x, y, text, font_family, font_size, is_bold)
    returns SVG path string containing all text as vector curves.
    """
    temp_svg = os.path.join(ASSETS_DIR, "_temp_cairo.svg")
    surf = cairo.SVGSurface(temp_svg, width, height)
    ctx = cairo.Context(surf)
    
    for item in lines_spec:
        x, y, text, font_family, font_size, is_bold = item
        weight = cairo.FONT_WEIGHT_BOLD if is_bold else cairo.FONT_WEIGHT_NORMAL
        ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, weight)
        ctx.set_font_size(font_size)
        ctx.move_to(x, y)
        ctx.text_path(text)
        
    ctx.set_source_rgb(0.07, 0.07, 0.08)
    ctx.fill()
    surf.finish()
    
    tree = ET.parse(temp_svg)
    root = tree.getroot()
    paths = [p.attrib["d"] for p in root.findall(".//{http://www.w3.org/2000/svg}path")]
    if os.path.exists(temp_svg):
        os.remove(temp_svg)
    return " ".join(paths)

def render_quote_to_path(quote_obj):
    """Renders literary quote in Caveat cursive to SVG vector path."""
    lines = quote_obj["lines"]
    attr = quote_obj["attr"]
    n_lines = len(lines)
    
    if n_lines == 3:
        start_y = 22
        lh = 19
        font_size = 16.0
    elif n_lines == 2:
        start_y = 28
        lh = 22
        font_size = 16.5
    else:
        start_y = 35
        lh = 24
        font_size = 17.0
        
    spec = []
    for i, line in enumerate(lines):
        spec.append((32, start_y + i * lh, line, "Caveat", font_size, True))
    attr_y = start_y + n_lines * lh + 2
    spec.append((40, attr_y, attr, "Caveat", 13.5, True))
    
    return cairo_text_to_path(spec, WIDTH, 133)

class TicketGenerator:
    def __init__(self):
        self.d_ticket = load_path_file("ticket_perimeter_path.txt")
        self.d_art = load_path_file("art_ink_path.txt")
        self.d_quote_orig = load_path_file("quote_clean_path.txt")
        os.makedirs(ASSETS_DIR, exist_ok=True)
        os.makedirs(DATA_DIR, exist_ok=True)
        os.makedirs(SLICES_DIR, exist_ok=True)
        os.makedirs(os.path.join(SLICES_DIR, "original"), exist_ok=True)
        os.makedirs(os.path.join(SLICES_DIR, "profile"), exist_ok=True)

    def generate_character_motion_gif(self, output_gif_path, full_ticket=False, profile_data=None, quote_obj=None):
        """
        Synthesizes a 24-frame seamless looping manga motion animation.
        - Hypnotic counter-rotating spiral eyes
        - Floating DEPPAQ mascot with subtle tilt
        - Character breathing bob
        - Crackling cursed energy ink sparks
        - Alpha masked to scalloped ticket perforations
        """
        sketch_path = os.path.join(ASSETS_DIR, "character_sketch.png")
        if not os.path.exists(sketch_path):
            raise FileNotFoundError(f"Missing character sketch asset: {sketch_path}")
            
        print(f"Generating Anime Motion Graphic -> {os.path.basename(output_gif_path)}...")
        im_orig = Image.open(sketch_path).convert("RGBA")
        w_orig, h_orig = im_orig.size

        # Extract ink channel
        gray = ImageOps.grayscale(im_orig)
        ink_arr = 255 - np.array(gray)
        alpha = np.clip(ink_arr.astype(float) * 1.35, 0, 255).astype(np.uint8)

        ink_full = np.zeros((h_orig, w_orig, 4), dtype=np.uint8)
        ink_full[:, :, 0] = 17
        ink_full[:, :, 1] = 17
        ink_full[:, :, 2] = 17
        ink_full[:, :, 3] = alpha
        ink_img = Image.fromarray(ink_full)

        # Isolated spiral pupils
        PUPIL_L = (413, 301)
        PUPIL_R = (546, 304)
        R_PUPIL = 15

        def extract_feathered_patch(img, cx, cy, r):
            patch = img.crop((cx - r, cy - r, cx + r, cy + r))
            mask = Image.new("L", (2*r, 2*r), 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((1, 1, 2*r - 2, 2*r - 2), fill=255)
            mask = mask.filter(ImageFilter.GaussianBlur(radius=0.8))
            patch.putalpha(Image.fromarray(np.minimum(np.array(patch.split()[3]), np.array(mask))))
            return patch

        pupil_l = extract_feathered_patch(ink_img, PUPIL_L[0], PUPIL_L[1], R_PUPIL)
        pupil_r = extract_feathered_patch(ink_img, PUPIL_R[0], PUPIL_R[1], R_PUPIL)

        # Clear pupil area on base character
        base_char = ink_img.copy()
        erase_mask = Image.new("L", (w_orig, h_orig), 0)
        draw_e = ImageDraw.Draw(erase_mask)
        draw_e.ellipse((PUPIL_L[0] - R_PUPIL + 1, PUPIL_L[1] - R_PUPIL + 1, PUPIL_L[0] + R_PUPIL - 1, PUPIL_L[1] + R_PUPIL - 1), fill=255)
        draw_e.ellipse((PUPIL_R[0] - R_PUPIL + 1, PUPIL_R[1] - R_PUPIL + 1, PUPIL_R[0] + R_PUPIL - 1, PUPIL_R[1] + R_PUPIL - 1), fill=255)
        erase_mask = erase_mask.filter(ImageFilter.GaussianBlur(radius=0.5))

        b_arr = np.array(base_char)
        b_alpha = b_arr[:, :, 3].astype(float)
        e_alpha = np.array(erase_mask).astype(float) / 255.0
        b_arr[:, :, 3] = np.clip(b_alpha * (1.0 - e_alpha), 0, 255).astype(np.uint8)

        # Extract DEPPAQ mascot
        deppaq_box = (680, 150, 860, 280)
        deppaq = ink_img.crop(deppaq_box)
        b_arr[150:280, 680:860, 3] = 0
        base_char_clean = Image.fromarray(b_arr)

        # Ticket paper base
        paper_path = os.path.join(ASSETS_DIR, "ticket_paper_slice1.png")
        if not os.path.exists(paper_path):
            raise FileNotFoundError(f"Missing paper base: {paper_path}")
        paper_base = Image.open(paper_path).convert("RGBA")
        paper_mask = paper_base.split()[3]

        # Target dimensions
        scale = 322 / w_orig
        char_w = 322
        char_h = int(h_orig * scale)

        NUM_FRAMES = 24
        frames = []

        # If rendering full ticket GIF, prepare static background of slices 2..6
        if full_ticket:
            full_static_svg = self.build_full_svg(edition="profile", profile_data=profile_data, quote_obj=quote_obj, include_art=False)
            tmp_svg = os.path.join(ASSETS_DIR, "_full_static.svg")
            tmp_png = os.path.join(ASSETS_DIR, "_full_static.png")
            with open(tmp_svg, "w", encoding="utf-8") as f:
                f.write(full_static_svg)
            subprocess.run([
                "google-chrome", "--headless",
                f"--screenshot={tmp_png}",
                f"--window-size={WIDTH},{HEIGHT}",
                "--default-background-color=00000000",
                f"file://{tmp_svg}"
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            full_base_img = Image.open(tmp_png).convert("RGBA")
            if os.path.exists(tmp_svg):
                os.remove(tmp_svg)
            if os.path.exists(tmp_png):
                os.remove(tmp_png)

        frames_dir = os.path.join(ASSETS_DIR, f"_frames_{'full' if full_ticket else 'slice1'}")
        os.makedirs(frames_dir, exist_ok=True)

        for f in range(NUM_FRAMES):
            t = f / NUM_FRAMES
            rad = t * 2 * math.pi

            # Breathing float
            body_dy = 2.0 * math.sin(rad)
            body_scale = 1.0 + 0.007 * math.sin(rad)
            cur_w = int(char_w * body_scale)
            cur_h = int(char_h * body_scale)

            # Counter-rotating spiral pupils
            rot_deg = t * 360
            rot_pl = pupil_l.rotate(rot_deg, resample=Image.Resampling.BICUBIC)
            rot_pr = pupil_r.rotate(-rot_deg, resample=Image.Resampling.BICUBIC)

            # Reassemble character
            full_char = base_char_clean.copy()
            full_char.alpha_composite(rot_pl, (PUPIL_L[0] - R_PUPIL, PUPIL_L[1] - R_PUPIL))
            full_char.alpha_composite(rot_pr, (PUPIL_R[0] - R_PUPIL, PUPIL_R[1] - R_PUPIL))

            scaled_char = full_char.resize((cur_w, cur_h), Image.Resampling.LANCZOS)

            # Canvas frame
            frame = paper_base.copy()
            char_x = 19 + (326 - cur_w) // 2
            char_y = int(35 + body_dy)
            frame.alpha_composite(scaled_char, (char_x, char_y))

            # Floating DEPPAQ mascot
            deppaq_dy = 3.8 * math.sin(rad + 1.4)
            deppaq_rot = 3.0 * math.sin(rad)
            dep_w = int(deppaq.width * scale)
            dep_h = int(deppaq.height * scale)
            dep_scaled = deppaq.resize((dep_w, dep_h), Image.Resampling.LANCZOS)
            dep_rotated = dep_scaled.rotate(deppaq_rot, resample=Image.Resampling.BICUBIC)

            dep_x = int(char_x + deppaq_box[0] * scale)
            dep_y = int(char_y + deppaq_box[1] * scale + deppaq_dy)
            frame.alpha_composite(dep_rotated, (dep_x, dep_y))


            # Alpha mask with scalloped ticket teeth
            r, g, b, a = frame.split()
            final_a = Image.fromarray(np.minimum(np.array(a), np.array(paper_mask)))
            frame.putalpha(final_a)

            if full_ticket:
                full_canvas = full_base_img.copy()
                full_canvas.alpha_composite(frame, (0, 0))
                full_canvas.save(os.path.join(frames_dir, f"frame_{f:03d}.png"))
                frames.append(full_canvas)
            else:
                frame.save(os.path.join(frames_dir, f"frame_{f:03d}.png"))
                frames.append(frame)

        # High quality palette compilation with ffmpeg
        cmd = [
            "ffmpeg", "-y",
            "-framerate", "22",
            "-i", os.path.join(frames_dir, "frame_%03d.png"),
            "-filter_complex", "[0:v] split [a][b];[a] palettegen=reserve_transparent=on:transparency_color=00000000 [p];[b][p] paletteuse=alpha_threshold=128",
            output_gif_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Cleanup frame directory
        for f in os.listdir(frames_dir):
            os.remove(os.path.join(frames_dir, f))
        os.rmdir(frames_dir)
        print(f"  -> Generated {output_gif_path} ({os.path.getsize(output_gif_path):,} bytes)")

    def build_slice_1_svg(self):
        """Slice 1 static vector fallback."""
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} 365" width="{WIDTH}" height="365">
  <defs>
    <clipPath id="t-clip-1"><path d="{self.d_ticket}" /></clipPath>
  </defs>
  <path d="{self.d_ticket}" fill="#efeee9" />
  <g clip-path="url(#t-clip-1)">
    <image href="slice_01_art.gif" width="{WIDTH}" height="365" />
  </g>
</svg>"""

    def build_slice_2_svg(self, edition="profile", profile_data=None):
        """Slice 2: Title & Badge Header (y: 365..415, height 50)"""
        umbrellas = f"{get_umbrella_svg(270, 392, 0.95)} {get_umbrella_svg(295, 392, 0.95)} {get_umbrella_svg(320, 392, 0.95)}"
        
        if edition == "original":
            text_spec = [
                (32, 21, "纽约的一个雨天(2019)", "Noto Serif CJK SC", 17, True),
                (33, 37, "A Rainy Day in New York", "Courier New", 10.5, True)
            ]
        else:
            title = profile_data.get("title", "GABRIEL GAMA · 2026")
            subtitle = profile_data.get("subtitle", "Front-end Developer • Brazil")
            text_spec = [
                (32, 21, title, "Noto Serif CJK SC", 15.5, True),
                (33, 37, subtitle, "Courier New", 10.5, True)
            ]
            
        text_d = cairo_text_to_path(text_spec, WIDTH, 50)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 365 {WIDTH} 50" width="{WIDTH}" height="50">
  <defs>
    <clipPath id="t-clip-2"><path d="{self.d_ticket}" /></clipPath>
  </defs>
  <path d="{self.d_ticket}" fill="#efeee9" />
  <g clip-path="url(#t-clip-2)">
    <g transform="translate(0, 365)">
      <path d="{text_d}" fill="#111111" />
    </g>
    {umbrellas}
    <line x1="30" y1="413" x2="335" y2="413" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
  </g>
</svg>"""

    def build_slice_3_portfolio_svg(self):
        """Slice 3: Portfólio with authentic organic pen underline (height 44)"""
        p_text = cairo_text_to_path([
            (34, 26, "PORTFÓLIO", "DejaVu Serif", 16.5, True),
            (274, 25, "VISIT", "Courier New", 11, True),
        ], WIDTH, 44)
        arrow = get_arrow_svg(316, 16, 10)
        pen_underline = '''
  <path d="M 32 32.0 C 58 31.2, 92 32.6, 122 31.4 C 135 30.9, 143 31.6, 150 31.0" 
        stroke="#111111" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.9" />
  <path d="M 38 33.8 C 65 33.2, 98 34.2, 130 33.0 C 139 32.6, 144 33.0, 148 32.4" 
        stroke="#111111" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.75" />
'''
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} 44" width="{WIDTH}" height="44">
  <rect x="19" y="0" width="326" height="44" fill="#efeee9" />
  {pen_underline}
  <path d="{p_text}" fill="#111111" />
  {arrow}
  <line x1="30" y1="43" x2="335" y2="43" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
</svg>"""

    def build_slice_4_linkedin_svg(self):
        """Slice 4: LinkedIn (height 44) - Clean, matching portfolio"""
        l_text = cairo_text_to_path([
            (34, 27, "LINKEDIN", "DejaVu Serif", 16.5, True),
            (264, 26, "CONNECT", "Courier New", 11, True),
        ], WIDTH, 44)
        arrow = get_arrow_svg(316, 17, 10)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} 44" width="{WIDTH}" height="44">
  <rect x="19" y="0" width="326" height="44" fill="#efeee9" />
  <path d="{l_text}" fill="#111111" />
  {arrow}
  <line x1="30" y1="43" x2="335" y2="43" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
</svg>"""

    def build_slice_5_stats_svg(self, edition="profile", profile_data=None):
        """Slice 5: Clean modern minimalist stats grid without divider lines (height 108, y: 464..572)"""
        if profile_data is None:
            profile_data = {}
        c_val = profile_data.get("commits", "+54 / wk")
        s_val = profile_data.get("streak", "28 days")
        r_val = profile_data.get("rank", "Top 5%")
        l_val = profile_data.get("location", "Salvador, BR")
        d_val = profile_data.get("date", "03/Oct/2026")

        text_spec = [
            (34, 38, "COMMITS", "Fira Sans Condensed", 10.5, True),
            (142, 38, "STREAK", "Fira Sans Condensed", 10.5, True),
            (248, 38, "RANK", "Fira Sans Condensed", 10.5, True),
            (34, 55, c_val, "Fira Mono", 13.5, True),
            (142, 55, s_val, "Fira Mono", 13.5, True),
            (248, 55, r_val, "Fira Mono", 13.5, True),
            (34, 79, "LOCATION", "Fira Sans Condensed", 10.5, True),
            (180, 79, "UPDATED", "Fira Sans Condensed", 10.5, True),
            (34, 96, l_val, "Fira Mono", 13.5, True),
            (180, 96, d_val, "Fira Mono", 13.5, True),
        ]
        text_d = cairo_text_to_path(text_spec, WIDTH, 108)
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 464 {WIDTH} 108" width="{WIDTH}" height="108">
  <defs>
    <clipPath id="t-clip-5"><path d="{self.d_ticket}" /></clipPath>
  </defs>
  <path d="{self.d_ticket}" fill="#efeee9" />
  <g clip-path="url(#t-clip-5)">
    <g transform="translate(0, 464)">
      <path d="{text_d}" fill="#111111" />
    </g>
    <!-- Clean layout: inner divider lines removed per design spec -->
    <!-- Bottom line -->
    <line x1="30" y1="571" x2="335" y2="571" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
  </g>
</svg>"""

    def build_slice_6_note_svg(self, edition="profile", quote_obj=None):
        """Slice 6: Handwritten Literary Note & Bottom Scalloped Perforation (y: 572..705, height 133)"""
        if edition == "original":
            quote_content = f'<path d="{self.d_quote_orig}" fill="#111111" fill-rule="evenodd" />'
        else:
            if quote_obj is None:
                quote_obj = get_daily_quote()
            quote_d = render_quote_to_path(quote_obj)
            quote_content = f'<g transform="translate(0, 572)"><path d="{quote_d}" fill="#111111" /></g>'
            
        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 572 {WIDTH} 133" width="{WIDTH}" height="133">
  <defs>
    <clipPath id="t-clip-6"><path d="{self.d_ticket}" /></clipPath>
  </defs>
  <path d="{self.d_ticket}" fill="#efeee9" />
  <g clip-path="url(#t-clip-6)">
    {quote_content}
  </g>
</svg>"""

    def build_full_svg(self, edition="profile", profile_data=None, quote_obj=None, include_art=True):
        """Builds full monolithic master SVG ticket."""
        umbrellas = f"{get_umbrella_svg(270, 392, 0.95)} {get_umbrella_svg(295, 392, 0.95)} {get_umbrella_svg(320, 392, 0.95)}"
        
        if edition == "original":
            t2 = cairo_text_to_path([
                (32, 21, "纽约的一个雨天(2019)", "Noto Serif CJK SC", 17, True),
                (33, 37, "A Rainy Day in New York", "Courier New", 10.5, True)
            ], WIDTH, 50)
            t3 = cairo_text_to_path([
                (32, 17, "〔美国〕伍迪·艾伦 Woody Allen", "Noto Serif CJK SC", 11.5, True),
                (33, 31, "Comedy/Romance", "Courier New", 10, True),
                (32, 45, "26/Jul/2019(波兰) / 2022-02-25(中国大陆) / 92分钟", "Noto Serif CJK SC", 9, False)
            ], WIDTH, 63)
            t4 = cairo_text_to_path([
                (33, 22, "HALL :", "Courier New", 11, True),
                (145, 22, "SEAT :", "Courier New", 11, True),
                (255, 22, "PRICE :", "Courier New", 11, True),
                (33, 39, "06", "Courier New", 12, True),
                (145, 39, "06-08", "Courier New", 12, True),
                (255, 39, "39.9", "Courier New", 12, True),
                (33, 62, "DATE :", "Courier New", 11, True),
                (145, 62, "TIME :", "Courier New", 11, True),
                (33, 79, "20/Jul/2025", "Courier New", 12, True),
                (145, 79, "20:00 - 21:32", "Courier New", 12, True),
            ], WIDTH, 94)
            q_elem = f'<path d="{self.d_quote_orig}" fill="#111111" fill-rule="evenodd" />'
        else:
            title = profile_data.get("title", "GABRIEL GAMA · 2026")
            subtitle = profile_data.get("subtitle", "Front-end Developer • Brazil")
            c_val = profile_data.get("commits", "+54 / wk")
            s_val = profile_data.get("streak", "28 days")
            r_val = profile_data.get("rank", "Top 5%")
            l_val = profile_data.get("location", "Salvador, BR")
            d_val = profile_data.get("date", "03/Oct/2026")
            
            t2 = cairo_text_to_path([
                (32, 21, title, "Noto Serif CJK SC", 15.5, True),
                (33, 37, subtitle, "Courier New", 10.5, True)
            ], WIDTH, 50)
            
            p_text = cairo_text_to_path([
                (34, 26, "PORTFÓLIO", "DejaVu Serif", 16.5, True),
                (274, 25, "VISIT", "Courier New", 11, True),
            ], WIDTH, 44)
            arrow_p = get_arrow_svg(316, 16, 10)
            pen_underline = '''
      <path d="M 32 32.0 C 58 31.2, 92 32.6, 122 31.4 C 135 30.9, 143 31.6, 150 31.0" 
            stroke="#111111" stroke-width="2.0" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.9" />
      <path d="M 38 33.8 C 65 33.2, 98 34.2, 130 33.0 C 139 32.6, 144 33.0, 148 32.4" 
            stroke="#111111" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.75" />
'''
            l_text = cairo_text_to_path([
                (34, 27, "LINKEDIN", "DejaVu Serif", 16.5, True),
                (264, 26, "CONNECT", "Courier New", 11, True),
            ], WIDTH, 44)
            arrow_l = get_arrow_svg(316, 17, 10)

            t_stats = cairo_text_to_path([
                (34, 38, "COMMITS", "Fira Sans Condensed", 10.5, True),
                (142, 38, "STREAK", "Fira Sans Condensed", 10.5, True),
                (248, 38, "RANK", "Fira Sans Condensed", 10.5, True),
                (34, 55, c_val, "Fira Mono", 13.5, True),
                (142, 55, s_val, "Fira Mono", 13.5, True),
                (248, 55, r_val, "Fira Mono", 13.5, True),
                (34, 79, "LOCATION", "Fira Sans Condensed", 10.5, True),
                (180, 79, "UPDATED", "Fira Sans Condensed", 10.5, True),
                (34, 96, l_val, "Fira Mono", 13.5, True),
                (180, 96, d_val, "Fira Mono", 13.5, True),
            ], WIDTH, 108)

            if quote_obj is None:
                quote_obj = get_daily_quote()
            quote_d = render_quote_to_path(quote_obj)
            q_elem = f'<g transform="translate(0, 572)"><path d="{quote_d}" fill="#111111" /></g>'

        art_element = ""
        if include_art:
            if edition == "original":
                art_element = f'<path d="{self.d_art}" fill="#111111" fill-rule="evenodd" />'
            else:
                art_element = f'<image href="slices/slice_01_art.gif" width="{WIDTH}" height="365" />'

        if edition == "original":
            body_content = f"""
    {art_element}
    <g transform="translate(0, 365)"><path d="{t2}" fill="#111111" /></g>
    {umbrellas}
    <line x1="30" y1="413" x2="335" y2="413" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
    <g transform="translate(0, 415)"><path d="{t3}" fill="#111111" /></g>
    <line x1="30" y1="478" x2="335" y2="478" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
    <g transform="translate(0, 478)"><path d="{t4}" fill="#111111" /></g>
    <line x1="30" y1="571" x2="335" y2="571" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
    {q_elem}
"""
        else:
            body_content = f"""
    {art_element}
    <!-- Section 2: Header -->
    <g transform="translate(0, 365)"><path d="{t2}" fill="#111111" /></g>
    {umbrellas}
    <line x1="30" y1="413" x2="335" y2="413" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />

    <!-- Section 3: Portfólio Strip -->
    <g transform="translate(0, 415)">
      {pen_underline}
      <path d="{p_text}" fill="#111111" />
      {arrow_p}
      <line x1="30" y1="43" x2="335" y2="43" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
    </g>

    <!-- Section 4: LinkedIn Strip -->
    <g transform="translate(0, 459)">
      <path d="{l_text}" fill="#111111" />
      {arrow_l}
      <line x1="30" y1="43" x2="335" y2="43" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
    </g>

    <!-- Section 5: Clean Stats Grid -->
    <g transform="translate(0, 464)">
      <path d="{t_stats}" fill="#111111" />
      <line x1="30" y1="107" x2="335" y2="107" stroke="#111111" stroke-width="1.5" stroke-dasharray="1 3" stroke-linecap="round" />
    </g>

    <!-- Section 6: Handwritten Literary Quote -->
    {q_elem}
"""

        return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}">
  <defs>
    <clipPath id="ticket-clip"><path d="{self.d_ticket}" /></clipPath>
  </defs>
  <path d="{self.d_ticket}" fill="#efeee9" stroke="#dfded9" stroke-width="0.5" />
  <g clip-path="url(#ticket-clip)">
{body_content}
  </g>
</svg>"""

    def generate_all(self, profile_data=None, quote_obj=None, force_gif=False):
        if profile_data is None:
            profile_data = {
                "title": "GABRIEL GAMA · 2026",
                "subtitle": "Front-end Developer • Brazil",
                "commits": "+54 / wk",
                "streak": "28 days",
                "rank": "Top 5%",
                "location": "Salvador, BR",
                "date": datetime.datetime.now().strftime("%d/%b/%Y")
            }

        if quote_obj is None:
            quote_obj = get_daily_quote()

        print(f"Active Daily Quote: [{quote_obj['book']}] \"{quote_obj['lines'][0]}\" ({quote_obj['attr']})")

        print("=== Generating Master SVGs ===")
        orig_svg = self.build_full_svg("original")
        with open(os.path.join(ASSETS_DIR, "ticket_original.svg"), "w", encoding="utf-8") as f:
            f.write(orig_svg)
        print("Generated ticket_original.svg")

        prof_svg = self.build_full_svg("profile", profile_data, quote_obj)
        with open(os.path.join(ASSETS_DIR, "ticket_profile.svg"), "w", encoding="utf-8") as f:
            f.write(prof_svg)
        print("Generated ticket_profile.svg")

        print("=== Generating Slices ===")
        # Slices for profile
        with open(os.path.join(SLICES_DIR, "slice_02_header.svg"), "w", encoding="utf-8") as f:
            f.write(self.build_slice_2_svg("profile", profile_data))
        with open(os.path.join(SLICES_DIR, "slice_03_portfolio.svg"), "w", encoding="utf-8") as f:
            f.write(self.build_slice_3_portfolio_svg())
        with open(os.path.join(SLICES_DIR, "slice_04_linkedin.svg"), "w", encoding="utf-8") as f:
            f.write(self.build_slice_4_linkedin_svg())
        with open(os.path.join(SLICES_DIR, "slice_05_stats.svg"), "w", encoding="utf-8") as f:
            f.write(self.build_slice_5_stats_svg("profile", profile_data))
        with open(os.path.join(SLICES_DIR, "slice_06_note.svg"), "w", encoding="utf-8") as f:
            f.write(self.build_slice_6_note_svg("profile", quote_obj))

        # Mirror slices to profile subdirectory
        prof_slices_dir = os.path.join(SLICES_DIR, "profile")
        for s_name in ["slice_02_header.svg", "slice_03_portfolio.svg", "slice_04_linkedin.svg", "slice_05_stats.svg", "slice_06_note.svg"]:
            src = os.path.join(SLICES_DIR, s_name)
            dst = os.path.join(prof_slices_dir, s_name)
            with open(src, "r", encoding="utf-8") as f_in, open(dst, "w", encoding="utf-8") as f_out:
                f_out.write(f_in.read())

        print("=== Generating Animated GIFs ===")
        slice_1_gif = os.path.join(SLICES_DIR, "slice_01_art.gif")
        if force_gif or not os.path.exists(slice_1_gif):
            self.generate_character_motion_gif(slice_1_gif, full_ticket=False)
        # Also copy to profile subdirectory
        dst_slice1 = os.path.join(prof_slices_dir, "slice_01_art.gif")
        if os.path.exists(slice_1_gif):
            with open(slice_1_gif, "rb") as f_in, open(dst_slice1, "wb") as f_out:
                f_out.write(f_in.read())

        full_prof_gif = os.path.join(ASSETS_DIR, "ticket_profile.gif")
        if force_gif or not os.path.exists(full_prof_gif):
            self.generate_character_motion_gif(full_prof_gif, full_ticket=True, profile_data=profile_data, quote_obj=quote_obj)

        print("=== Generating Profile Markdown Snippet ===")
        self.generate_profile_snippet()

        print("=== Generating Interactive Preview HTML ===")
        self.generate_preview_html(quote_obj)
        print("All assets generated successfully!")

    def generate_profile_snippet(self):
        snippet = """<!-- VINTAGE CINEMA TICKET PROFILE COMPONENT -->
<!-- Engineered with zero-gap p + align=top slicing for GitHub Markdown -->
<p align="center">
  <img src="ticket-profile/assets/slices/slice_01_art.gif" width="394" align="top" alt="Manga Character Motion Art" /><br><img src="ticket-profile/assets/slices/slice_02_header.svg" width="394" align="top" alt="Ticket Header" /><br><a href="https://gabrielbaiano.vercel.app/" title="Portfólio"><img src="ticket-profile/assets/slices/slice_03_portfolio.svg" width="394" align="top" alt="Portfólio" /></a><br><a href="https://www.linkedin.com/in/gabriel-gama-6301633b2/" title="Connect on LinkedIn"><img src="ticket-profile/assets/slices/slice_04_linkedin.svg" width="394" align="top" alt="LinkedIn" /></a><br><img src="ticket-profile/assets/slices/slice_05_stats.svg" width="394" align="top" alt="Commit Activity & Stats" /><br><img src="ticket-profile/assets/slices/slice_06_note.svg" width="394" align="top" alt="Handwritten Literary Quote" />
</p>
"""
        with open(os.path.join(BASE_DIR, "profile_snippet.md"), "w", encoding="utf-8") as f:
            f.write(snippet)

    def generate_preview_html(self, quote_obj=None):
        quote_title = f"{quote_obj['book']} ({quote_obj['author']})" if quote_obj else "Daily Literary Classic"
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Vintage Cinema Ticket Profile - Preview</title>
<style>
  body {{
    margin: 0;
    padding: 40px 20px;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    transition: background-color 0.3s ease, color 0.3s ease;
  }}
  .theme-dark {{
    background-color: #0d1117;
    color: #e6edf3;
  }}
  .theme-light {{
    background-color: #ffffff;
    color: #1f2328;
  }}
  .container {{
    max-width: 900px;
    margin: 0 auto;
    text-align: center;
  }}
  .controls {{
    margin-bottom: 30px;
    display: flex;
    justify-content: center;
    gap: 12px;
  }}
  button {{
    background: #238636;
    color: #fff;
    border: none;
    padding: 8px 16px;
    font-size: 14px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
  }}
  button.secondary {{
    background: #30363d;
  }}
  .ticket-wrapper {{
    display: inline-block;
    padding: 20px;
  }}
  .grid-preview {{
    display: flex;
    justify-content: center;
    gap: 40px;
    flex-wrap: wrap;
    margin-top: 20px;
  }}
  .card {{
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    padding: 20px;
  }}
  h2 {{
    font-size: 18px;
    margin-top: 0;
    margin-bottom: 8px;
  }}
  .meta {{
    font-size: 13px;
    color: #8b949e;
    margin-bottom: 16px;
  }}
</style>
</head>
<body class="theme-dark" id="preview-body">
<div class="container">
  <h1>Vintage Cinema Ticket GitHub Profile</h1>
  <p>Anime Motion Graphic · Clean Stats Grid · Rotating Literary Quotes</p>
  
  <div class="controls">
    <button onclick="setTheme('dark')">GitHub Dark Theme</button>
    <button class="secondary" onclick="setTheme('light')">GitHub Light Theme</button>
  </div>

  <div class="grid-preview">
    <div class="card">
      <h2>Sliced GitHub README Component</h2>
      <div class="meta">Only Portfólio & LinkedIn Clickable · Zero Gap</div>
      <div class="ticket-wrapper">
        <p align="center" style="margin: 0; padding: 0;">
          <img src="assets/slices/slice_01_art.gif" width="394" align="top" /><br><img src="assets/slices/slice_02_header.svg" width="394" align="top" /><br><a href="https://gabrielbaiano.vercel.app/" target="_blank"><img src="assets/slices/slice_03_portfolio.svg" width="394" align="top" /></a><br><a href="https://www.linkedin.com/in/gabriel-gama-6301633b2/" target="_blank"><img src="assets/slices/slice_04_linkedin.svg" width="394" align="top" /></a><br><img src="assets/slices/slice_05_stats.svg" width="394" align="top" /><br><img src="assets/slices/slice_06_note.svg" width="394" align="top" />
        </p>
      </div>
    </div>

    <div class="card">
      <h2>Full Monolithic Ticket</h2>
      <div class="meta">Quote: {quote_title}</div>
      <div class="ticket-wrapper">
        <img src="assets/ticket_profile.gif" width="394" height="705" />
      </div>
    </div>
  </div>
</div>

<script>
  function setTheme(t) {{
    document.getElementById('preview-body').className = t === 'dark' ? 'theme-dark' : 'theme-light';
  }}
</script>
</body>
</html>"""
        with open(os.path.join(BASE_DIR, "preview.html"), "w", encoding="utf-8") as f:
            f.write(html)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Vintage Cinema Ticket")
    parser.add_argument("--commits", default="+54 / wk", help="Weekly commits count")
    parser.add_argument("--streak", default="28 days", help="Active streak")
    parser.add_argument("--rank", default="Top 5%", help="Rank or badge")
    parser.add_argument("--date", default=None, help="Ticket date (defaults to today)")
    parser.add_argument("--location", default="Salvador, BR", help="Location")
    parser.add_argument("--quote-id", default=None, help="Specific quote ID")
    parser.add_argument("--quote-index", type=int, default=None, help="Specific quote index (0..17)")
    parser.add_argument("--force-gif", action="store_true", help="Force regenerate animated GIFs")
    args = parser.parse_args()

    date_val = args.date if args.date else datetime.datetime.now().strftime("%d/%b/%Y")

    gen = TicketGenerator()
    data = {
        "title": "GABRIEL GAMA · 2026",
        "subtitle": "Front-end Developer • Brazil",
        "commits": args.commits,
        "streak": args.streak,
        "rank": args.rank,
        "location": args.location,
        "date": date_val
    }

    selected_quote = get_daily_quote(day_index=args.quote_index, quote_id=args.quote_id)
    gen.generate_all(profile_data=data, quote_obj=selected_quote, force_gif=args.force_gif)
