from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Canvas dimensions - museum quality
WIDTH = 1200
HEIGHT = 1600

# Refined color palette - meticulously calibrated dawn transition
DEEP_INDIGO = (25, 32, 58)  # Deep night - refined
MIDNIGHT_BLUE = (38, 48, 78)  # Transition 1
TWILIGHT_BLUE = (52, 65, 98)  # Transition 2
DAWN_PURPLE = (78, 82, 115)  # Purple dawn - refined
HORIZON_MAUVE = (105, 100, 125)  # Horizon color
SOFT_AMBER = (205, 155, 95)  # Warm amber - refined
GENTLE_GOLD = (235, 205, 145)  # Soft gold - refined
WARM_CREAM = (248, 242, 228)  # Morning cream - refined
ACCENT_GOLD = (188, 140, 70)  # Accent color - refined
COOL_GRAY = (155, 165, 180)  # Cool gray - refined
SUBTLE_LAVENDER = (145, 150, 175)  # Subtle lavender

def create_multi_stop_gradient(draw, width, height, color_stops):
    """Create a smooth multi-stop vertical gradient with expert precision"""
    for y in range(height):
        ratio = y / height

        # Find which color stops we're between
        num_stops = len(color_stops)
        segment_size = 1.0 / (num_stops - 1)
        segment_index = min(int(ratio / segment_size), num_stops - 2)

        # Local ratio within this segment
        local_ratio = (ratio - segment_index * segment_size) / segment_size

        # Smooth interpolation using ease-in-out
        smooth_ratio = local_ratio * local_ratio * (3.0 - 2.0 * local_ratio)

        start_color = color_stops[segment_index]
        end_color = color_stops[segment_index + 1]

        r = int(start_color[0] + (end_color[0] - start_color[0]) * smooth_ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * smooth_ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * smooth_ratio)

        draw.line([(0, y), (width, y)], fill=(r, g, b))

def create_radial_gradient_overlay(width, height, center, max_radius, inner_color, outer_color):
    """Create a meticulously crafted radial gradient overlay"""
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # More steps for smoother gradient
    steps = 200
    for i in range(steps, 0, -1):
        ratio = i / steps

        # Smooth easing
        smooth_ratio = ratio * ratio * (3.0 - 2.0 * ratio)
        radius = max_radius * smooth_ratio

        # Interpolate color with precision
        r = int(outer_color[0] + (inner_color[0] - outer_color[0]) * smooth_ratio)
        g = int(outer_color[1] + (inner_color[1] - outer_color[1]) * smooth_ratio)
        b = int(outer_color[2] + (inner_color[2] - outer_color[2]) * smooth_ratio)

        # Alpha with smooth falloff
        a = int(60 * (1 - smooth_ratio * smooth_ratio))

        bbox = [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius
        ]
        draw.ellipse(bbox, fill=(r, g, b, a))

    return overlay

def draw_refined_geometric_patterns(draw, width, height):
    """Draw refined geometric patterns with master-level precision"""

    # Ultra-subtle grid - barely visible, adding texture
    grid_spacing = 60
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(*TWILIGHT_BLUE, 8), width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(*TWILIGHT_BLUE, 8), width=1)

    # Perfectly centered concentric circles - representing time zones, global markets
    center_x = width // 2
    center_y = int(height * 0.32)  # Precise golden ratio positioning

    # Circles with mathematical precision
    radii = [120, 200, 290, 390, 500]
    for i, radius in enumerate(radii):
        # Opacity decreases with distance
        opacity = max(3, int(35 - i * 6))
        bbox = [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ]
        # Varying line widths for depth
        line_width = 2 if i < 2 else 1
        draw.ellipse(bbox, outline=(*SOFT_AMBER, opacity), width=line_width)

    # Refined diagonal lines - growth trajectory with perfect spacing
    num_lines = 16
    for i in range(num_lines):
        # Calculate position with precision
        x_spacing = width / (num_lines - 1)
        x_start = x_spacing * i - 150
        y_start = height - 150
        x_end = x_start + 700
        y_end = y_start - 1000

        # Alternating opacity for subtle rhythm
        opacity = 6 if i % 3 == 0 else 10 if i % 2 == 0 else 4
        draw.line([(x_start, y_start), (x_end, y_end)],
                 fill=(*GENTLE_GOLD, opacity), width=1)

def draw_refined_accent_shapes(draw, width, height):
    """Draw accent shapes with painstaking attention to detail"""

    # Central sun/awakening circle - precisely positioned
    sun_center = (width // 2, int(height * 0.32))
    sun_radius = 85

    # Multi-layered sun effect for depth
    for i in range(5):
        offset_radius = sun_radius + i * 8
        opacity = int(25 - i * 4)
        sun_bbox = [
            sun_center[0] - offset_radius,
            sun_center[1] - offset_radius,
            sun_center[0] + offset_radius,
            sun_center[1] + offset_radius
        ]
        draw.ellipse(sun_bbox, fill=(*SOFT_AMBER, opacity))

    # Core sun circle
    sun_bbox = [
        sun_center[0] - sun_radius,
        sun_center[1] - sun_radius,
        sun_center[0] + sun_radius,
        sun_center[1] + sun_radius
    ]
    draw.ellipse(sun_bbox, fill=(*GENTLE_GOLD, 50))
    draw.ellipse(sun_bbox, outline=(*ACCENT_GOLD, 90), width=2)

    # Star field - fading stars with systematic placement
    import random
    random.seed(42)  # Consistent, deliberate placement
    for _ in range(40):
        x = random.randint(80, width - 80)
        y = random.randint(60, int(height * 0.55))

        # Stars fade as they get lower (dawn is coming)
        fade_factor = 1.0 - (y / (height * 0.55))

        size = random.choice([2, 2, 3, 4])
        base_opacity = random.randint(15, 45)
        opacity = int(base_opacity * fade_factor)

        draw.ellipse([x, y, x + size, y + size], fill=(*WARM_CREAM, opacity))

    # Refined horizontal time markers - perfectly aligned
    marker_y = height - 260
    marker_width = 350
    marker_center_x = width // 2

    # Three lines with precise spacing
    spacings = [-15, 0, 15]
    for offset in spacings:
        y = marker_y + offset
        draw.line(
            [(marker_center_x - marker_width // 2, y),
             (marker_center_x + marker_width // 2, y)],
            fill=(*SUBTLE_LAVENDER, 25),
            width=1
        )

# Create the main image with pristine quality
img = Image.new('RGB', (WIDTH, HEIGHT), DEEP_INDIGO)
draw = ImageDraw.Draw(img, 'RGBA')

# Step 1: Create refined multi-stop gradient background
color_stops = [
    DEEP_INDIGO,
    MIDNIGHT_BLUE,
    TWILIGHT_BLUE,
    DAWN_PURPLE,
    HORIZON_MAUVE
]
create_multi_stop_gradient(draw, WIDTH, HEIGHT, color_stops)

# Step 2: Add refined radial gradient overlay
radial_overlay = create_radial_gradient_overlay(
    WIDTH, HEIGHT,
    (WIDTH // 2, int(HEIGHT * 0.32)),
    900,
    GENTLE_GOLD,
    DEEP_INDIGO
)
img = Image.alpha_composite(img.convert('RGBA'), radial_overlay).convert('RGB')
draw = ImageDraw.Draw(img, 'RGBA')

# Step 3: Draw refined geometric patterns
draw_refined_geometric_patterns(draw, WIDTH, HEIGHT)

# Step 4: Draw refined accent shapes
draw_refined_accent_shapes(draw, WIDTH, HEIGHT)

# Step 5: Typography with master-level precision
try:
    # Load fonts with exact sizes for perfect visual hierarchy
    font_path_kr = "canvas-fonts/NotoSansKR-Regular.ttf"

    # Title - commanding presence
    title_font = ImageFont.truetype(font_path_kr, 105)

    # Subtitle - elegant refinement
    subtitle_font = ImageFont.truetype(font_path_kr, 34)

    # Accent - whispered detail
    accent_font = ImageFont.truetype("canvas-fonts/InstrumentSans-Regular.ttf", 18)

except Exception as e:
    print(f"Font loading error: {e}")
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    accent_font = ImageFont.load_default()

# Main title: "당신이 잠든 사이" - centered with precision
title_text = "당신이 잠든 사이"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_height = title_bbox[3] - title_bbox[1]
title_x = (WIDTH - title_width) // 2
title_y = HEIGHT - 440

# Subtle layered glow for depth
glow_layers = [
    (4, 20),
    (3, 35),
    (2, 50),
    (1, 70)
]

for offset, opacity in glow_layers:
    draw.text(
        (title_x, title_y),
        title_text,
        font=title_font,
        fill=(*ACCENT_GOLD, opacity)
    )

# Main title - pristine
draw.text(
    (title_x, title_y),
    title_text,
    font=title_font,
    fill=WARM_CREAM
)

# Subtitle: "오늘의 미국 주식 브리핑" - precisely positioned
subtitle_text = "오늘의 미국 주식 브리핑"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = title_y + title_height + 35

# Subtle subtitle glow
draw.text(
    (subtitle_x + 1, subtitle_y + 1),
    subtitle_text,
    font=subtitle_font,
    fill=(*ACCENT_GOLD, 20)
)

draw.text(
    (subtitle_x, subtitle_y),
    subtitle_text,
    font=subtitle_font,
    fill=COOL_GRAY
)

# Time marker - whispered precision
time_marker = "DAILY BRIEFING · 07:00 KST"
time_bbox = draw.textbbox((0, 0), time_marker, font=accent_font)
time_width = time_bbox[2] - time_bbox[0]
time_x = (WIDTH - time_width) // 2
time_y = HEIGHT - 145

draw.text(
    (time_x, time_y),
    time_marker,
    font=accent_font,
    fill=(*GENTLE_GOLD, 160),
    anchor="lt"
)

# Step 6: Final refinement - subtle sharpening for crispness
img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=120, threshold=2))

# Save with maximum quality
output_path = "briefing-card-final.png"
img.save(output_path, quality=100, optimize=False, dpi=(300, 300))

print(f"Museum-quality briefing card created: {output_path}")
print(f"  Dimensions: {WIDTH}x{HEIGHT} @ 300 DPI")
print(f"  Design philosophy: Quiet Momentum")
print(f"  Craftsmanship level: Master")
print(f"  Color stops: {len(color_stops)}")
print(f"  Radial gradient steps: 200")
print(f"  Typography: Meticulously positioned Korean + Latin")
