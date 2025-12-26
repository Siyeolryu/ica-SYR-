from PIL import Image

# Open the final PNG
img = Image.open("briefing-card-final.png")

# Convert to RGB if needed (PDFs don't support transparency)
if img.mode in ('RGBA', 'LA', 'P'):
    background = Image.new('RGB', img.size, (255, 255, 255))
    if img.mode == 'P':
        img = img.convert('RGBA')
    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
    img = background
elif img.mode != 'RGB':
    img = img.convert('RGB')

# Save as PDF with high quality
output_path = "briefing-card-final.pdf"
img.save(output_path, "PDF", resolution=300.0, quality=100)

print(f"PDF version created: {output_path}")
print(f"  Resolution: 300 DPI")
print(f"  Format: PDF")
