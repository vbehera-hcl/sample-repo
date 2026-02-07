"""
Instagram Profile Photo Generator for Viswa AI Agents
Dimensions: 1080x1080 (displayed as circle)
Theme: Blue & Cyan (matching Facebook cover)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Blue & Cyan Color Scheme
COLORS = {
    'bg_dark': (8, 15, 30),
    'bg_medium': (15, 30, 55),
    'primary': (0, 180, 255),
    'secondary': (0, 120, 220),
    'accent': (100, 220, 255),
    'highlight': (180, 240, 255),
    'glow': (0, 200, 255),
    'text_white': (255, 255, 255),
    'shadow': (5, 10, 20),
}

def get_fonts():
    """Load fonts."""
    fonts = {}
    try:
        fonts['main'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 380)
        fonts['sub'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 160)
    except:
        try:
            fonts['main'] = ImageFont.truetype("arial.ttf", 380)
            fonts['sub'] = ImageFont.truetype("arial.ttf", 160)
        except:
            default = ImageFont.load_default()
            fonts = {'main': default, 'sub': default}
    return fonts

def create_radial_gradient(size):
    """Create radial gradient background."""
    img = Image.new('RGB', (size, size), COLORS['bg_dark'])
    center = size // 2
    max_dist = center
    
    for y in range(size):
        for x in range(size):
            dist = math.sqrt((x - center)**2 + (y - center)**2) / max_dist
            dist = min(1, dist)
            
            # Brighter in center
            brightness = 1 - (dist * 0.7)
            r = int(COLORS['bg_medium'][0] * brightness + COLORS['bg_dark'][0] * (1 - brightness))
            g = int(COLORS['bg_medium'][1] * brightness + COLORS['bg_dark'][1] * (1 - brightness))
            b = int(COLORS['bg_medium'][2] * brightness + COLORS['bg_dark'][2] * (1 - brightness))
            img.putpixel((x, y), (r, g, b))
    
    return img

def draw_tech_rings(draw, center, size):
    """Draw concentric tech rings."""
    # Outer glow rings
    for i in range(6):
        radius = (size // 2) - 40 - i * 8
        alpha = 30 + i * 10
        draw.ellipse([center - radius, center - radius, 
                      center + radius, center + radius],
                    outline=(*COLORS['glow'][:3], alpha), width=2)
    
    # Main circle border
    radius = (size // 2) - 50
    draw.ellipse([center - radius, center - radius,
                  center + radius, center + radius],
                outline=COLORS['primary'], width=6)
    
    # Inner decorative ring
    inner_radius = (size // 2) - 100
    draw.ellipse([center - inner_radius, center - inner_radius,
                  center + inner_radius, center + inner_radius],
                outline=(*COLORS['accent'][:3], 100), width=2)

def draw_corner_accents(draw, size):
    """Draw tech accent lines in corners."""
    margin = 80
    length = 100
    
    positions = [
        # Top-left
        ((margin, margin), (margin, margin + length), (margin + length, margin)),
        # Top-right
        ((size - margin, margin), (size - margin, margin + length), (size - margin - length, margin)),
        # Bottom-left
        ((margin, size - margin), (margin, size - margin - length), (margin + length, size - margin)),
        # Bottom-right
        ((size - margin, size - margin), (size - margin, size - margin - length), (size - margin - length, size - margin)),
    ]
    
    for corner, vert, horiz in positions:
        # Vertical line with glow
        for i in range(3):
            alpha = 150 - i * 40
            draw.line([corner, vert], fill=(*COLORS['primary'][:3], alpha), width=4 - i)
        # Horizontal line
        for i in range(3):
            alpha = 150 - i * 40
            draw.line([corner, horiz], fill=(*COLORS['primary'][:3], alpha), width=4 - i)
        
        # Corner node
        draw.ellipse([corner[0] - 6, corner[1] - 6, corner[0] + 6, corner[1] + 6],
                    fill=COLORS['accent'])

def draw_floating_nodes(draw, size):
    """Draw small floating tech nodes."""
    import random
    random.seed(42)
    
    center = size // 2
    
    for _ in range(12):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(size * 0.25, size * 0.42)
        
        x = center + dist * math.cos(angle)
        y = center + dist * math.sin(angle)
        
        node_size = random.randint(4, 8)
        alpha = random.randint(60, 150)
        
        # Glow
        draw.ellipse([x - node_size * 2, y - node_size * 2,
                      x + node_size * 2, y + node_size * 2],
                    fill=(*COLORS['glow'][:3], alpha // 3))
        # Node
        draw.ellipse([x - node_size, y - node_size,
                      x + node_size, y + node_size],
                    fill=(*COLORS['accent'][:3], alpha))

def draw_center_glow(image, center, radius):
    """Draw glowing effect behind text."""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for i in range(10, 0, -1):
        r = radius + i * 20
        alpha = int(25 * i / 10)
        draw.ellipse([center - r, center - r, center + r, center + r],
                    fill=(*COLORS['glow'][:3], alpha))
    
    return Image.alpha_composite(image.convert('RGBA'), overlay)

def create_instagram_profile():
    """Create Instagram profile photo."""
    size = 1080  # Instagram recommended size
    center = size // 2
    
    # Create gradient background
    profile = create_radial_gradient(size)
    profile = profile.convert('RGBA')
    draw = ImageDraw.Draw(profile, 'RGBA')
    
    fonts = get_fonts()
    
    # Draw tech rings
    draw_tech_rings(draw, center, size)
    
    # Draw corner accents
    draw_corner_accents(draw, size)
    
    # Draw floating nodes
    draw_floating_nodes(draw, size)
    
    # Add center glow
    profile = draw_center_glow(profile, center, 150)
    draw = ImageDraw.Draw(profile, 'RGBA')
    
    # Main letters "VA"
    text = "VA"
    bbox = draw.textbbox((0, 0), text, font=fonts['main'])
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 80
    
    # Text shadow layers
    for i in range(5, 0, -1):
        shadow_alpha = int(100 - i * 15)
        draw.text((text_x + i * 3, text_y + i * 3), text, font=fonts['main'],
                 fill=(*COLORS['shadow'][:3], shadow_alpha))
    
    # Text glow
    for i in range(3, 0, -1):
        glow_alpha = int(60 * i / 3)
        for dx in [-i, 0, i]:
            for dy in [-i, 0, i]:
                if dx != 0 or dy != 0:
                    draw.text((text_x + dx, text_y + dy), text, font=fonts['main'],
                             fill=(*COLORS['glow'][:3], glow_alpha))
    
    # Main text
    draw.text((text_x, text_y), text, font=fonts['main'], fill=COLORS['text_white'])
    
    # "AI" subscript
    sub_text = "AI"
    bbox = draw.textbbox((0, 0), sub_text, font=fonts['sub'])
    sub_width = bbox[2] - bbox[0]
    sub_x = (size - sub_width) // 2
    sub_y = text_y + text_height - 60
    
    # Subscript glow
    for i in range(2, 0, -1):
        draw.text((sub_x + i, sub_y + i), sub_text, font=fonts['sub'],
                 fill=(*COLORS['primary'][:3], 80))
    
    draw.text((sub_x, sub_y), sub_text, font=fonts['sub'], fill=COLORS['accent'])
    
    # Decorative line under AI
    line_y = sub_y + 130
    line_width = 200
    line_x = (size - line_width) // 2
    
    for i in range(line_width):
        progress = abs(i - line_width / 2) / (line_width / 2)
        alpha = int(200 * (1 - progress))
        draw.point((line_x + i, line_y), fill=(*COLORS['primary'][:3], alpha))
    
    # Save
    profile = profile.convert('RGB')
    profile.save("instagram_profile_viswa_ai.png", "PNG", quality=95)
    
    file_size = os.path.getsize("instagram_profile_viswa_ai.png") / 1024
    print(f"[OK] Instagram profile created: instagram_profile_viswa_ai.png")
    print(f"     Dimensions: {size}x{size} pixels")
    print(f"     File size: {file_size:.0f} KB")
    print()
    print("DESIGN FEATURES:")
    print("-" * 50)
    print("  - 'VA' monogram with 'AI' subscript")
    print("  - Tech rings and glow effects")
    print("  - Corner accent brackets")
    print("  - Floating tech nodes")
    print("  - Blue & Cyan color scheme")
    print("  - Optimized for circular display")
    print()
    print("UPLOAD INSTRUCTIONS:")
    print("-" * 50)
    print("  1. Open Instagram app")
    print("  2. Go to Profile > Edit Profile")
    print("  3. Tap on profile picture")
    print("  4. Select 'New profile picture'")
    print("  5. Choose instagram_profile_viswa_ai.png")
    print()
    print("NOTE: Instagram displays profile photos as circles,")
    print("      so corners will be cropped. Design is optimized for this.")
    
    return profile

if __name__ == "__main__":
    create_instagram_profile()
