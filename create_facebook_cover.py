"""
Facebook Cover Photo Generator for Viswa AI Agents
Dimensions: 820x312 (desktop) with safe zone considerations
Theme: Red & Orange (Energetic) with 3D Depth Effects
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Brand Colors - Red & Orange Theme (matching YouTube assets)
COLORS = {
    'bg_dark': (15, 10, 20),
    'bg_medium': (35, 15, 25),
    'primary': (255, 80, 50),
    'secondary': (255, 140, 50),
    'accent': (255, 200, 100),
    'highlight': (255, 100, 80),
    'glow': (255, 120, 60),
    'text_white': (255, 255, 255),
    'text_light': (255, 230, 220),
    'text_muted': (200, 180, 170),
    'shadow': (10, 5, 15),
}

def get_fonts():
    """Load fonts with fallbacks."""
    fonts = {}
    font_paths = [
        ("C:/Windows/Fonts/seguibold.ttf", "C:/Windows/Fonts/segoeui.ttf"),
        ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"),
    ]
    
    for bold_path, regular_path in font_paths:
        try:
            fonts['title'] = ImageFont.truetype(bold_path, 72)
            fonts['subtitle'] = ImageFont.truetype(bold_path, 32)
            fonts['tagline'] = ImageFont.truetype(regular_path, 24)
            fonts['small'] = ImageFont.truetype(regular_path, 18)
            return fonts
        except:
            continue
    
    default = ImageFont.load_default()
    return {k: default for k in ['title', 'subtitle', 'tagline', 'small']}

def create_gradient_3d(width, height, colors):
    """Create a radial gradient with 3D depth feel."""
    base = Image.new('RGB', (width, height), colors[0])
    
    center_x, center_y = width // 2, height // 2
    max_dist = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2) / max_dist
            dist = min(1, dist * 1.3)
            
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * dist)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * dist)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * dist)
            base.putpixel((x, y), (r, g, b))
    
    return base

def draw_3d_glow(image, center, radius, color, layers=6):
    """Draw glowing orb effect."""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for i in range(layers, 0, -1):
        r = int(radius * (1 + (layers - i) * 0.35))
        alpha = int(50 * i / layers)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r],
                    fill=(*color[:3], alpha))
    
    return Image.alpha_composite(image.convert('RGBA'), overlay)

def draw_perspective_grid(draw, width, height, color):
    """Draw subtle perspective grid."""
    vanishing_y = height // 4
    
    for i in range(8):
        y = vanishing_y + int((height - vanishing_y) * (i / 7) ** 1.4)
        alpha = int(25 + 20 * i / 7)
        draw.line([(0, y), (width, y)], fill=(*color[:3], alpha), width=1)
    
    vanishing_x = width // 2
    for i in range(-6, 7):
        bottom_x = vanishing_x + i * 80
        alpha = int(35 - abs(i) * 4)
        if alpha > 0:
            draw.line([(vanishing_x, vanishing_y), (bottom_x, height)],
                     fill=(*color[:3], alpha), width=1)

def draw_floating_particles(draw, width, height, color, count=15):
    """Draw floating particle effects."""
    import random
    random.seed(42)
    
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(2, 5)
        alpha = random.randint(30, 80)
        
        draw.ellipse([x-size*2, y-size*2, x+size*2, y+size*2],
                    fill=(*color[:3], alpha//3))
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=(*color[:3], alpha))

def draw_3d_cube(draw, center, size, colors):
    """Draw 3D AI chip icon."""
    cx, cy = center
    s = size
    angle = math.radians(15)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    
    # Front face
    front = [
        (cx - s * cos_a, cy - s),
        (cx + s * cos_a, cy - s),
        (cx + s * cos_a, cy + s),
        (cx - s * cos_a, cy + s),
    ]
    
    # Top face
    depth = s * 0.35
    top = [
        (cx - s * cos_a, cy - s),
        (cx + s * cos_a, cy - s),
        (cx + s * cos_a - depth * sin_a, cy - s - depth),
        (cx - s * cos_a - depth * sin_a, cy - s - depth),
    ]
    
    # Right face
    right = [
        (cx + s * cos_a, cy - s),
        (cx + s * cos_a, cy + s),
        (cx + s * cos_a - depth * sin_a, cy + s - depth),
        (cx + s * cos_a - depth * sin_a, cy - s - depth),
    ]
    
    draw.polygon(top, fill=colors['secondary'], outline=colors['accent'])
    draw.polygon(right, fill=colors['primary'], outline=colors['accent'])
    draw.polygon(front, fill=colors['highlight'], outline=colors['accent'])
    
    # Inner pattern
    inner = s * 0.5
    inner_box = [
        (cx - inner * cos_a, cy - inner),
        (cx + inner * cos_a, cy - inner),
        (cx + inner * cos_a, cy + inner),
        (cx - inner * cos_a, cy + inner),
    ]
    draw.polygon(inner_box, fill=colors['bg_dark'], outline=colors['primary'])
    
    # Center node
    draw.ellipse([cx-6, cy-6, cx+6, cy+6], fill=colors['accent'])

def draw_3d_text(draw, pos, text, font, main_color, shadow_color, depth=3):
    """Draw text with 3D shadow effect."""
    x, y = pos
    
    for i in range(depth, 0, -1):
        shadow_alpha = int(120 - i * 35)
        draw.text((x + i*2, y + i*2), text, font=font,
                 fill=(*shadow_color[:3], shadow_alpha))
    
    draw.text((x, y), text, font=font, fill=main_color)

def create_facebook_cover():
    """Create Facebook cover photo (820x312)."""
    # Facebook cover dimensions
    width, height = 820, 312
    
    # Create gradient background
    cover = create_gradient_3d(width, height, [COLORS['bg_medium'], COLORS['bg_dark']])
    cover = cover.convert('RGBA')
    draw = ImageDraw.Draw(cover, 'RGBA')
    
    fonts = get_fonts()
    
    # Add perspective grid
    draw_perspective_grid(draw, width, height, COLORS['primary'])
    
    # Add floating particles
    draw_floating_particles(draw, width, height, COLORS['secondary'])
    
    # Add glowing orbs
    cover = draw_3d_glow(cover, (120, 156), 100, COLORS['glow'])
    cover = draw_3d_glow(cover, (700, 140), 80, COLORS['secondary'])
    draw = ImageDraw.Draw(cover, 'RGBA')
    
    # Draw 3D AI cube on left side
    draw_3d_cube(draw, (130, 156), 45, COLORS)
    
    # Main title - positioned to right of icon, accounting for profile pic overlap
    # Profile pic is typically on left side, so we center-right the text
    title = "VISWA AI AGENTS"
    bbox = draw.textbbox((0, 0), title, font=fonts['title'])
    title_width = bbox[2] - bbox[0]
    title_x = 250
    title_y = 85
    
    draw_3d_text(draw, (title_x, title_y), title, fonts['title'],
                 COLORS['text_white'], COLORS['shadow'], depth=4)
    
    # Subtitle
    subtitle = "Building Practical AI Agents"
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_x = title_x + 5
    subtitle_y = title_y + 80
    
    # Background bar for subtitle
    draw.rounded_rectangle(
        [subtitle_x - 15, subtitle_y - 5, subtitle_x + (bbox[2] - bbox[0]) + 15, subtitle_y + 40],
        radius=8,
        fill=(*COLORS['primary'][:3], 50),
        outline=(*COLORS['secondary'][:3], 80)
    )
    
    draw_3d_text(draw, (subtitle_x, subtitle_y), subtitle, fonts['subtitle'],
                 COLORS['accent'], COLORS['shadow'], depth=2)
    
    # Tagline
    tagline = "Agentic AI  |  Automation  |  Autonomous Systems"
    bbox = draw.textbbox((0, 0), tagline, font=fonts['tagline'])
    tagline_x = subtitle_x + 5
    tagline_y = subtitle_y + 55
    
    draw.text((tagline_x, tagline_y), tagline, font=fonts['tagline'],
              fill=COLORS['text_light'])
    
    # Decorative elements
    # Top-left corner bracket
    draw.line([(20, 25), (20, 60)], fill=COLORS['primary'], width=3)
    draw.line([(20, 25), (55, 25)], fill=COLORS['primary'], width=3)
    
    # Top-right corner bracket
    draw.line([(800, 25), (800, 60)], fill=COLORS['secondary'], width=3)
    draw.line([(800, 25), (765, 25)], fill=COLORS['secondary'], width=3)
    
    # Bottom-right corner bracket
    draw.line([(800, 287), (800, 252)], fill=COLORS['primary'], width=3)
    draw.line([(800, 287), (765, 287)], fill=COLORS['primary'], width=3)
    
    # Bottom accent line
    draw.rectangle([250, 275, 650, 280], fill=COLORS['primary'])
    draw.rectangle([250, 275, 650, 277], fill=COLORS['secondary'])
    
    # Topics/keywords at bottom
    topics = "N8N  *  ChatGPT  *  Claude  *  Cursor AI"
    bbox = draw.textbbox((0, 0), topics, font=fonts['small'])
    topics_x = 250
    topics_y = 255
    draw.text((topics_x, topics_y), topics, font=fonts['small'],
              fill=COLORS['text_muted'])
    
    # Save
    cover = cover.convert('RGB')
    cover.save("facebook_cover_viswa_ai.png", "PNG", quality=95)
    
    file_size = os.path.getsize("facebook_cover_viswa_ai.png") / 1024
    print(f"[OK] Facebook cover created: facebook_cover_viswa_ai.png")
    print(f"     Dimensions: {width}x{height} pixels")
    print(f"     File size: {file_size:.0f} KB")
    print()
    print("UPLOAD INSTRUCTIONS:")
    print("-" * 45)
    print("  1. Go to your Facebook Page or Profile")
    print("  2. Click on your cover photo area")
    print("  3. Select 'Upload Photo'")
    print("  4. Choose facebook_cover_viswa_ai.png")
    print("  5. Adjust position if needed and save")
    print()
    print("NOTE: The design accounts for profile picture")
    print("      overlap on the left side.")
    
    return cover

if __name__ == "__main__":
    create_facebook_cover()
