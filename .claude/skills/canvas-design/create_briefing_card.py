from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

# Canvas dimensions
WIDTH = 1200
HEIGHT = 1600

# Color palette - Dawn transition colors
DEEP_INDIGO = (28, 35, 64)  # Deep night blue
TWILIGHT_BLUE = (58, 80, 120)  # Transition blue
DAWN_PURPLE = (88, 86, 124)  # Purple dawn
SOFT_AMBER = (218, 165, 100)  # Warm amber
GENTLE_GOLD = (242, 211, 152)  # Soft gold
WARM_CREAM = (252, 244, 230)  # Morning cream
ACCENT_GOLD = (198, 146, 68)  # Accent color
COOL_GRAY = (160, 170, 185)  # Cool gray for subtle elements

def create_gradient(draw, width, height, start_color, end_color):
    """Create a vertical gradient"""
    for y in range(height):
        # Calculate color at this y position
        ratio = y / height
        r = int(start_color[0] + (end_color[0] - start_color[0]) * ratio)
        g = int(start_color[1] + (end_color[1] - start_color[1]) * ratio)
        b = int(start_color[2] + (end_color[2] - start_color[2]) * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b))

def create_radial_gradient_overlay(width, height, center, max_radius, inner_color, outer_color):
    """Create a radial gradient overlay"""
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Create radial gradient with multiple circles
    steps = 100
    for i in range(steps, 0, -1):
        ratio = i / steps
        radius = max_radius * ratio

        # Interpolate color
        r = int(outer_color[0] + (inner_color[0] - outer_color[0]) * ratio)
        g = int(outer_color[1] + (inner_color[1] - outer_color[1]) * ratio)
        b = int(outer_color[2] + (inner_color[2] - outer_color[2]) * ratio)
        a = int(80 * (1 - ratio))  # Fade out towards edges

        bbox = [
            center[0] - radius,
            center[1] - radius,
            center[0] + radius,
            center[1] + radius
        ]
        draw.ellipse(bbox, fill=(r, g, b, a))

    return overlay

def draw_geometric_patterns(draw, width, height):
    """Draw subtle geometric patterns representing market data and time"""

    # Grid lines - very subtle
    grid_spacing = 80
    for x in range(0, width, grid_spacing):
        draw.line([(x, 0), (x, height)], fill=(*TWILIGHT_BLUE, 15), width=1)
    for y in range(0, height, grid_spacing):
        draw.line([(0, y), (width, y)], fill=(*TWILIGHT_BLUE, 15), width=1)

    # Concentric circles - representing global markets, time zones
    center_x = width // 2
    center_y = height // 3

    for i, radius in enumerate([150, 250, 350, 450]):
        opacity = max(5, 25 - i * 5)
        bbox = [
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius
        ]
        draw.ellipse(bbox, outline=(*SOFT_AMBER, opacity), width=2)

    # Rising diagonal lines - suggesting growth and upward momentum
    num_lines = 12
    for i in range(num_lines):
        x_start = (width // num_lines) * i - 100
        y_start = height - 200
        x_end = x_start + 600
        y_end = y_start - 800

        opacity = 8 if i % 2 == 0 else 12
        draw.line([(x_start, y_start), (x_end, y_end)],
                 fill=(*GENTLE_GOLD, opacity), width=1)

def draw_accent_shapes(draw, width, height):
    """Draw accent geometric shapes"""

    # Large circle accent - representing awakening, the rising sun
    sun_center = (width // 2, height // 3)
    sun_radius = 100
    sun_bbox = [
        sun_center[0] - sun_radius,
        sun_center[1] - sun_radius,
        sun_center[0] + sun_radius,
        sun_center[1] + sun_radius
    ]
    draw.ellipse(sun_bbox, fill=(*SOFT_AMBER, 40))
    draw.ellipse(sun_bbox, outline=(*ACCENT_GOLD, 80), width=3)

    # Small accent dots - like stars fading
    import random
    random.seed(42)  # Consistent placement
    for _ in range(30):
        x = random.randint(100, width - 100)
        y = random.randint(100, height // 2)
        size = random.randint(2, 4)
        opacity = random.randint(20, 60)
        draw.ellipse([x, y, x + size, y + size], fill=(*WARM_CREAM, opacity))

    # Thin horizontal lines - time markers
    line_y_positions = [height - 350, height - 320, height - 290]
    for y in line_y_positions:
        draw.line([(width // 2 - 200, y), (width // 2 + 200, y)],
                 fill=(*COOL_GRAY, 30), width=1)

# Create the main image
img = Image.new('RGB', (WIDTH, HEIGHT), DEEP_INDIGO)
draw = ImageDraw.Draw(img, 'RGBA')

# Step 1: Create main gradient background
create_gradient(draw, WIDTH, HEIGHT, DEEP_INDIGO, DAWN_PURPLE)

# Step 2: Add radial gradient overlay (the awakening light)
radial_overlay = create_radial_gradient_overlay(
    WIDTH, HEIGHT,
    (WIDTH // 2, HEIGHT // 3),  # Center point
    800,  # Max radius
    GENTLE_GOLD,  # Inner color
    DEEP_INDIGO  # Outer color
)
img = Image.alpha_composite(img.convert('RGBA'), radial_overlay).convert('RGB')
draw = ImageDraw.Draw(img, 'RGBA')

# Step 3: Draw geometric patterns
draw_geometric_patterns(draw, WIDTH, HEIGHT)

# Step 4: Draw accent shapes
draw_accent_shapes(draw, WIDTH, HEIGHT)

# Step 5: Add typography
# Load fonts
try:
    # Korean font
    font_path_kr = "canvas-fonts/NotoSansKR-Regular.ttf"

    # Title font - large and bold
    title_font = ImageFont.truetype(font_path_kr, 110)

    # Subtitle font - elegant and refined
    subtitle_font = ImageFont.truetype(font_path_kr, 36)

    # Small accent font
    accent_font = ImageFont.truetype("canvas-fonts/InstrumentSans-Regular.ttf", 20)

except Exception as e:
    print(f"Font loading error: {e}")
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()
    accent_font = ImageFont.load_default()

# Main title: "당신이 잠든 사이"
title_text = "당신이 잠든 사이"
title_bbox = draw.textbbox((0, 0), title_text, font=title_font)
title_width = title_bbox[2] - title_bbox[0]
title_height = title_bbox[3] - title_bbox[1]
title_x = (WIDTH - title_width) // 2
title_y = HEIGHT - 500

# Add subtle glow to title
for offset in range(3, 0, -1):
    draw.text(
        (title_x, title_y),
        title_text,
        font=title_font,
        fill=(*ACCENT_GOLD, 30 * offset)
    )

# Main title
draw.text(
    (title_x, title_y),
    title_text,
    font=title_font,
    fill=WARM_CREAM
)

# Subtitle: "오늘의 미국 주식 브리핑"
subtitle_text = "오늘의 미국 주식 브리핑"
subtitle_bbox = draw.textbbox((0, 0), subtitle_text, font=subtitle_font)
subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
subtitle_x = (WIDTH - subtitle_width) // 2
subtitle_y = title_y + title_height + 40

draw.text(
    (subtitle_x, subtitle_y),
    subtitle_text,
    font=subtitle_font,
    fill=COOL_GRAY
)

# Small accent text - time marker
time_marker = "DAILY BRIEFING · 07:00 KST"
time_bbox = draw.textbbox((0, 0), time_marker, font=accent_font)
time_width = time_bbox[2] - time_bbox[0]
time_x = (WIDTH - time_width) // 2
time_y = HEIGHT - 180

draw.text(
    (time_x, time_y),
    time_marker,
    font=accent_font,
    fill=(*GENTLE_GOLD, 180)
)

# Step 6: Apply subtle overall blur to certain areas for depth
# Create a copy for selective blur
img_copy = img.copy()
img_copy = img_copy.filter(ImageFilter.GaussianBlur(radius=0.5))

# Save the final image
output_path = "briefing-card.png"
img.save(output_path, quality=100, optimize=True)

print(f"Briefing card created: {output_path}")
print(f"  Dimensions: {WIDTH}x{HEIGHT}")
print(f"  Design philosophy: Quiet Momentum")
print(f"  Visual language: Dawn transition, geometric precision, minimal typography")
