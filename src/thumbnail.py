"""
Professional YouTube Thumbnail Generator
Creates high-quality cinematic thumbnails with:
- Pexels background images with cinematic color grading
- Multi-layer gradient overlays (top, bottom, vignette)
- Text glow and outline effects using RGBA compositing
- Adaptive layout (number + title vs full-width title)
- Auto-detected color schemes per topic niche
- Professional font sizing and spacing

Author: Muhammad Saboor
"""

import os
import random
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from io import BytesIO

OUTPUT_DIR = "C:/Users/ashai/OneDrive/Desktop/YouTube Videos"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PEXELS_API_KEY = "EtVbiQuEYMalKR7MNeCZg5B0hUGDTIX3uS7WYDOpyQddIDVqZP6TU8BD"

# Color schemes for different moods
COLOR_SCHEMES = {
    "fire":    {"accent": (220, 50, 30),  "glow": (255, 80, 20, 150),  "tag_bg": (200, 35, 25)},
    "gold":    {"accent": (255, 185, 0),  "glow": (255, 200, 50, 150), "tag_bg": (200, 150, 0)},
    "ice":     {"accent": (0, 160, 255),  "glow": (50, 140, 255, 150), "tag_bg": (0, 120, 210)},
    "mystery": {"accent": (170, 50, 220), "glow": (150, 50, 200, 150), "tag_bg": (140, 40, 180)},
    "blood":   {"accent": (170, 10, 10),  "glow": (200, 20, 20, 150),  "tag_bg": (150, 10, 10)},
}


def detect_color_scheme(title):
    """Pick the best color scheme based on title keywords."""
    t = title.lower()
    if any(w in t for w in ["scar", "horror", "terrif", "creep", "dark", "death", "murder", "crime"]):
        return "blood"
    if any(w in t for w in ["ocean", "sea", "water", "ice", "frozen", "arctic", "deep"]):
        return "ice"
    if any(w in t for w in ["gold", "treasure", "rich", "ancient", "egypt", "pyramid"]):
        return "gold"
    if any(w in t for w in ["space", "alien", "ufo", "mysteri", "unknown", "strange", "cosmic"]):
        return "mystery"
    return "fire"


def detect_category_tag(title):
    """Pick a category label for the corner tag."""
    t = title.lower()
    # Check ocean/space/unsolved BEFORE ancient (avoid "discover" false positive)
    if any(w in t for w in ["ocean", "sea", "underwater", "deep", "marine"]):
        return "OCEAN MYSTERIES"
    if any(w in t for w in ["space", "universe", "cosmic", "planet", "star"]):
        return "SPACE MYSTERIES"
    if any(w in t for w in ["scar", "horror", "creep", "terrif"]):
        return "DISTURBING FACTS"
    if any(w in t for w in ["unsolved", "disappear", "mystery", "crime", "murder"]):
        return "UNSOLVED MYSTERIES"
    if any(w in t for w in ["ancient", "ruins", "pyramid", "archaeol", "temple"]):
        return "ANCIENT MYSTERIES"
    return "MIND-BLOWING FACTS"


def derive_bg_query(title):
    """Generate a good Pexels search query from the title."""
    t = title.lower()
    if any(w in t for w in ["ocean", "sea", "underwater", "deep"]):
        return "dark ocean underwater cinematic"
    if any(w in t for w in ["space", "universe", "cosmic", "star", "planet"]):
        return "dark space nebula stars"
    if any(w in t for w in ["ancient", "ruins", "pyramid", "temple"]):
        return "ancient ruins dark cinematic atmosphere"
    if any(w in t for w in ["mystery", "disappear", "unsolved", "crime"]):
        return "dark forest fog mysterious"
    if any(w in t for w in ["scar", "horror", "creep"]):
        return "dark abandoned building horror"
    return "dark cinematic dramatic landscape"


# ── Helper functions ─────────────────────────────────────────────


def fetch_background_image(query, num_results=5):
    """Fetch a high-res background image from Pexels."""
    try:
        headers = {"Authorization": PEXELS_API_KEY}
        params = {
            "query": query,
            "per_page": num_results,
            "orientation": "landscape",
            "size": "large",
        }
        response = requests.get(
            "https://api.pexels.com/v1/search", headers=headers, params=params, timeout=15
        )
        data = response.json()

        if "photos" in data and data["photos"]:
            photo = random.choice(data["photos"][:min(3, len(data["photos"]))])
            photo_url = photo["src"]["large2x"]
            img_resp = requests.get(photo_url, timeout=30)
            return Image.open(BytesIO(img_resp.content))
    except Exception as e:
        print(f"  Could not fetch background: {e}")
    return None


def crop_to_fill(img, target_w, target_h):
    """Crop and resize image to exactly fill target dimensions."""
    w, h = img.size
    ratio = max(target_w / w, target_h / h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    img = img.resize((new_w, new_h), Image.LANCZOS)
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def color_grade_background(img):
    """Apply cinematic color grading to the background."""
    img = ImageEnhance.Brightness(img).enhance(0.45)
    img = ImageEnhance.Contrast(img).enhance(1.5)
    img = ImageEnhance.Color(img).enhance(1.15)
    img = img.filter(ImageFilter.GaussianBlur(radius=2.0))
    return img


def add_gradient_overlay(img):
    """Add multi-layer gradient overlay for depth and text readability."""
    width, height = img.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Top gradient (subtle darkening)
    for y in range(height // 3):
        alpha = int(90 * (1 - y / (height // 3)))
        draw.line([(0, y), (width, y)], fill=(0, 0, 15, alpha))

    # Bottom gradient (strong, for text area)
    for y in range(height // 3, height):
        progress = (y - height // 3) / (height - height // 3)
        alpha = int(210 * (progress ** 1.5))
        draw.line([(0, y), (width, y)], fill=(5, 0, 20, alpha))

    # Left edge gradient (for number area)
    for x in range(width // 4):
        alpha = int(70 * (1 - x / (width // 4)))
        draw.line([(x, 0), (x, height)], fill=(0, 0, 0, alpha))

    return Image.alpha_composite(img, overlay)


def add_vignette(img, strength=0.5):
    """Darken the edges for a cinematic vignette effect."""
    width, height = img.size
    vignette = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(vignette)

    steps = 80
    for i in range(steps):
        progress = i / steps
        alpha = int(strength * 200 * (progress ** 2.5))
        inset_x = int(width * 0.55 * (1 - progress))
        inset_y = int(height * 0.55 * (1 - progress))
        x1 = max(0, width // 2 - inset_x)
        y1 = max(0, height // 2 - inset_y)
        x2 = min(width, width // 2 + inset_x)
        y2 = min(height, height // 2 + inset_y)
        if x2 > x1 and y2 > y1:
            draw.rectangle([x1, y1, x2, y2], outline=(0, 0, 0, min(alpha, 255)))

    return Image.alpha_composite(img, vignette)


def draw_text_with_glow(img, xy, text, font, text_color, glow_color, glow_radius=12):
    """Draw text with: glow layer -> black outline -> sharp text."""
    x, y = xy

    # ── 1) Glow layer ──
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            gd.text((x + dx, y + dy), text, fill=glow_color, font=font)
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=glow_radius))
    img = Image.alpha_composite(img, glow_layer)

    # ── 2) Black outline ──
    outline_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(outline_layer)
    ow = 4
    for dx in range(-ow, ow + 1):
        for dy in range(-ow, ow + 1):
            if dx * dx + dy * dy <= (ow + 1) * (ow + 1):
                od.text((x + dx, y + dy), text, fill=(0, 0, 0, 255), font=font)
    img = Image.alpha_composite(img, outline_layer)

    # ── 3) Sharp text ──
    text_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    td = ImageDraw.Draw(text_layer)
    fill = text_color if len(text_color) == 4 else text_color + (255,)
    td.text((x, y), text, fill=fill, font=font)
    img = Image.alpha_composite(img, text_layer)

    return img


def load_font(name, size):
    """Load a Windows font with fallback."""
    paths = {
        "impact": "C:/Windows/Fonts/impact.ttf",
        "arial_bold": "C:/Windows/Fonts/arialbd.ttf",
        "arial": "C:/Windows/Fonts/arial.ttf",
    }
    try:
        return ImageFont.truetype(paths.get(name, paths["impact"]), size)
    except (OSError, IOError):
        try:
            return ImageFont.truetype(paths["arial_bold"], size)
        except (OSError, IOError):
            return ImageFont.load_default()


def word_wrap(draw, text, font, max_width):
    """Wrap text into lines that fit within max_width pixels."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        bbox = draw.textbbox((0, 0), test, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


# ── Main function ────────────────────────────────────────────────


def create_thumbnail(title, output_path=None, bg_query=None, color_scheme=None):
    """Create a professional YouTube thumbnail."""
    print("\nGenerating professional thumbnail...")

    if not output_path:
        output_path = os.path.join(OUTPUT_DIR, "thumbnail.png")

    width, height = 1280, 720

    # Auto-detect color scheme
    scheme_name = color_scheme or detect_color_scheme(title)
    colors = COLOR_SCHEMES.get(scheme_name, COLOR_SCHEMES["fire"])
    print(f"  Color scheme: {scheme_name}")

    # ── Background ──
    query = bg_query or derive_bg_query(title)
    print(f"  Background query: '{query}'")
    bg = fetch_background_image(query)

    if bg:
        bg = crop_to_fill(bg, width, height)
        bg = color_grade_background(bg)
        print("  Background: Pexels image (color graded)")
    else:
        bg = Image.new("RGB", (width, height), (8, 8, 20))
        draw_bg = ImageDraw.Draw(bg)
        for y in range(height):
            r = int(8 + 15 * (y / height))
            g = int(8 + 5 * (y / height))
            b = int(20 + 30 * (y / height))
            draw_bg.line([(0, y), (width, y)], fill=(r, g, b))
        print("  Background: gradient fallback")

    # Convert to RGBA for compositing
    img = bg.convert("RGBA")

    # ── Overlays ──
    img = add_gradient_overlay(img)
    img = add_vignette(img, strength=0.5)

    # ── Parse title ──
    words = title.upper().split()
    number = ""
    rest_title = title.upper()
    if words and words[0].isdigit():
        number = words[0]
        rest_title = " ".join(words[1:])

    # ── Draw big number with glow ──
    if number:
        num_font = load_font("impact", 180)
        img = draw_text_with_glow(
            img, (35, height // 2 - 130),
            number, num_font,
            text_color=colors["accent"],
            glow_color=colors["glow"],
            glow_radius=22,
        )

    # ── Word-wrap and draw title ──
    title_font = load_font("impact", 78)
    temp_draw = ImageDraw.Draw(img)

    max_text_w = width - 260 if number else width - 120
    start_x = 235 if number else 60
    lines = word_wrap(temp_draw, rest_title, title_font, max_text_w)

    line_height = 92
    total_h = len(lines) * line_height
    start_y = (height - total_h) // 2

    for i, line in enumerate(lines):
        lx = start_x
        ly = start_y + i * line_height
        img = draw_text_with_glow(
            img, (lx, ly),
            line, title_font,
            text_color=(255, 255, 255, 255),
            glow_color=(0, 0, 0, 200),
            glow_radius=8,
        )

    # ── Category tag ──
    tag_font = load_font("arial_bold", 21)
    tag_text = detect_category_tag(title)

    tag_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    tag_draw = ImageDraw.Draw(tag_layer)
    bbox = tag_draw.textbbox((0, 0), tag_text, font=tag_font)
    tag_w = bbox[2] - bbox[0] + 28
    tag_h = bbox[3] - bbox[1] + 16
    tag_x = width - tag_w - 20
    tag_y = 22

    tag_draw.rounded_rectangle(
        [tag_x, tag_y, tag_x + tag_w, tag_y + tag_h],
        radius=4,
        fill=colors["tag_bg"] + (230,),
    )
    tag_draw.text(
        (tag_x + 14, tag_y + 6), tag_text,
        fill=(255, 255, 255, 255), font=tag_font,
    )
    img = Image.alpha_composite(img, tag_layer)

    # ── Accent bars (top + bottom) ──
    bar_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    bar_draw = ImageDraw.Draw(bar_layer)
    bar_draw.rectangle([(0, 0), (width, 5)], fill=colors["accent"] + (210,))
    bar_draw.rectangle([(0, height - 5), (width, height)], fill=colors["accent"] + (210,))
    img = Image.alpha_composite(img, bar_layer)

    # ── Save ──
    final = img.convert("RGB")
    final.save(output_path, quality=95)
    print(f"  Thumbnail saved: {output_path}")
    print(f"  Size: {width}x{height}")
    return output_path


if __name__ == "__main__":
    create_thumbnail("7 IMPOSSIBLE Ancient Discoveries We Still Can't Explain")
