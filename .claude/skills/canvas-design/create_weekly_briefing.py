from PIL import Image, ImageDraw, ImageFont
import os

# Canvas dimensions
WIDTH = 1200
HEIGHT = 630

# Nocturnal Precision color palette
BG_PRIMARY = '#0d1117'
BG_ELEVATED = '#161b22'
TEXT_PRIMARY = '#f0f6fc'
TEXT_SECONDARY = '#8b949e'
SIGNAL_GREEN = '#3fb950'
BORDER_SUBTLE = '#21262d'

def hex_to_rgb(hex_color):
    """Convert hex color to RGB tuple"""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

# Create new image
img = Image.new('RGB', (WIDTH, HEIGHT), hex_to_rgb(BG_PRIMARY))
draw = ImageDraw.Draw(img)

# Load fonts (Korean font for proper rendering)
script_dir = os.path.dirname(os.path.abspath(__file__))
font_dir = os.path.join(script_dir, 'canvas-fonts')

try:
    # Korean font for Korean text
    font_path_kr = os.path.join(font_dir, 'NotoSansKR-Regular.ttf')
    
    # Title font - large and bold
    font_title = ImageFont.truetype(font_path_kr, 36)
    
    # Heading font - medium size
    font_heading = ImageFont.truetype(font_path_kr, 24)
    
    # Body font - regular size
    font_body = ImageFont.truetype(font_path_kr, 16)
    
    # Small font - for secondary text
    font_small = ImageFont.truetype(font_path_kr, 14)
    
    # Date font - medium size
    font_date = ImageFont.truetype(font_path_kr, 18)
    
    print(f"Korean fonts loaded successfully from: {font_dir}")
except Exception as e:
    print(f"Font loading error: {e}")
    print("Falling back to default fonts (may not support Korean)")
    # Fallback to default fonts
    font_title = ImageFont.load_default()
    font_heading = ImageFont.load_default()
    font_body = ImageFont.load_default()
    font_small = ImageFont.load_default()
    font_date = ImageFont.load_default()

# Header section
header_height = 100
draw.rectangle([(0, 0), (WIDTH, header_height)], fill=hex_to_rgb(BG_ELEVATED))
draw.line([(0, header_height), (WIDTH, header_height)], fill=hex_to_rgb(SIGNAL_GREEN), width=3)

# Title
title_text = "당신이 잠든 사이 - 주간 보고"
title_bbox = draw.textbbox((0, 0), title_text, font=font_title)
title_width = title_bbox[2] - title_bbox[0]
draw.text((40, 25), title_text, fill=hex_to_rgb(TEXT_PRIMARY), font=font_title)

# Date
date_text = "2025.12.26"
draw.text((WIDTH - 150, 35), date_text, fill=hex_to_rgb(TEXT_SECONDARY), font=font_date)

# Content area - 3 achievement cards
card_y_start = header_height + 40
card_height = 140
card_spacing = 20
card_width = (WIDTH - 100) // 3

# Achievement 1: Subagent System
card1_x = 40
draw.rounded_rectangle(
    [(card1_x, card_y_start), (card1_x + card_width, card_y_start + card_height)],
    radius=8,
    fill=hex_to_rgb(BG_ELEVATED),
    outline=hex_to_rgb(BORDER_SUBTLE),
    width=1
)
draw.text((card1_x + 15, card_y_start + 15), "[Bot] Subagent", fill=hex_to_rgb(SIGNAL_GREEN), font=font_heading)
draw.text((card1_x + 15, card_y_start + 50), "5개 에이전트", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card1_x + 15, card_y_start + 72), "구현 완료", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card1_x + 15, card_y_start + 100), "test, refactor", fill=hex_to_rgb(TEXT_SECONDARY), font=font_small)
draw.text((card1_x + 15, card_y_start + 118), "bug, doc, security", fill=hex_to_rgb(TEXT_SECONDARY), font=font_small)

# Achievement 2: Refactoring
card2_x = card1_x + card_width + card_spacing
draw.rounded_rectangle(
    [(card2_x, card_y_start), (card2_x + card_width, card_y_start + card_height)],
    radius=8,
    fill=hex_to_rgb(BG_ELEVATED),
    outline=hex_to_rgb(BORDER_SUBTLE),
    width=1
)
draw.text((card2_x + 15, card_y_start + 15), "[Recycle] Refactoring", fill=hex_to_rgb(SIGNAL_GREEN), font=font_heading)
draw.text((card2_x + 15, card_y_start + 50), "Magic: 25+ → 0", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card2_x + 15, card_y_start + 72), "중복: 5 → 0", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card2_x + 15, card_y_start + 94), "테스트: 29/29", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card2_x + 15, card_y_start + 118), "100% 통과", fill=hex_to_rgb(TEXT_SECONDARY), font=font_small)

# Achievement 3: GitHub Actions
card3_x = card2_x + card_width + card_spacing
draw.rounded_rectangle(
    [(card3_x, card_y_start), (card3_x + card_width, card_y_start + card_height)],
    radius=8,
    fill=hex_to_rgb(BG_ELEVATED),
    outline=hex_to_rgb(BORDER_SUBTLE),
    width=1
)
draw.text((card3_x + 15, card_y_start + 15), "[Gear] Automation", fill=hex_to_rgb(SIGNAL_GREEN), font=font_heading)
draw.text((card3_x + 15, card_y_start + 50), "매일 07:00 실행", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card3_x + 15, card_y_start + 72), "Slack + 이슈", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card3_x + 15, card_y_start + 94), "Artifact 저장", fill=hex_to_rgb(TEXT_PRIMARY), font=font_body)
draw.text((card3_x + 15, card_y_start + 118), "7일간 보관", fill=hex_to_rgb(TEXT_SECONDARY), font=font_small)

# Footer - Tech stack
footer_y = card_y_start + card_height + 40
draw.line([(40, footer_y), (WIDTH - 40, footer_y)], fill=hex_to_rgb(BORDER_SUBTLE), width=1)

tech_y = footer_y + 25
draw.text((40, tech_y), "Tech Stack:", fill=hex_to_rgb(TEXT_SECONDARY), font=font_small)
draw.text((150, tech_y), "Next.js 14", fill=hex_to_rgb(TEXT_PRIMARY), font=font_small)
draw.text((250, tech_y), "Python 3.12", fill=hex_to_rgb(TEXT_PRIMARY), font=font_small)
draw.text((370, tech_y), "FastAPI", fill=hex_to_rgb(TEXT_PRIMARY), font=font_small)
draw.text((460, tech_y), "GitHub Actions", fill=hex_to_rgb(TEXT_PRIMARY), font=font_small)
draw.text((600, tech_y), "pytest", fill=hex_to_rgb(TEXT_PRIMARY), font=font_small)

# Accent dots (terminal-inspired)
dot_radius = 4
dot_y = 30
dot_colors = [SIGNAL_GREEN, '#f59e0b', '#dc2626']
for i, color in enumerate(dot_colors):
    dot_x = WIDTH - 220 + (i * 15)
    draw.ellipse([(dot_x, dot_y), (dot_x + dot_radius * 2, dot_y + dot_radius * 2)], fill=hex_to_rgb(color))

# Save the image
output_path = os.path.join('..', '..', '..', 'backend', 'output', 'reports', 'weekly_briefing_card_20251226.png')
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path, 'PNG', quality=95)
print(f"Briefing card created: {output_path}")
