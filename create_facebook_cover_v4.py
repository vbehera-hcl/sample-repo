"""
Facebook Cover Photo V4 - Tech Lines Design
Clean tech lines with centered layout
Theme: Blue & Cyan (Cool Tech)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
import random

# Blue & Cyan Color Scheme
COLORS = {
    'bg_dark': (8, 15, 30),
    'bg_medium': (15, 30, 55),
    'primary': (0, 180, 255),       # Cyan
    'secondary': (0, 120, 220),     # Blue
    'accent': (100, 220, 255),      # Light cyan
    'highlight': (180, 240, 255),   # Very light
    'glow': (0, 200, 255),
    'text_white': (255, 255, 255),
    'text_light': (200, 235, 255),
    'text_muted': (120, 160, 200),
    'shadow': (5, 10, 20),
}

def get_fonts():
    """Load fonts."""
    fonts = {}
    try:
        fonts['title'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 60)
        fonts['subtitle'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 26)
        fonts['tagline'] = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
        fonts['small'] = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    except:
        try:
            fonts['title'] = ImageFont.truetype("arial.ttf", 60)
            fonts['subtitle'] = ImageFont.truetype("arial.ttf", 26)
            fonts['tagline'] = ImageFont.truetype("arial.ttf", 18)
            fonts['small'] = ImageFont.truetype("arial.ttf", 14)
        except:
            default = ImageFont.load_default()
            fonts = {k: default for k in ['title', 'subtitle', 'tagline', 'small']}
    return fonts

def create_gradient_bg(width, height):
    """Create smooth radial gradient background."""
    img = Image.new('RGB', (width, height), COLORS['bg_dark'])
    
    center_x, center_y = width // 2, height // 2
    max_dist = math.sqrt((width/2)**2 + (height/2)**2)
    
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2) / max_dist
            # Brighter in center, darker at edges
            brightness = 1 - (dist * 0.6)
            r = int(COLORS['bg_medium'][0] * brightness + COLORS['bg_dark'][0] * (1 - brightness))
            g = int(COLORS['bg_medium'][1] * brightness + COLORS['bg_dark'][1] * (1 - brightness))
            b = int(COLORS['bg_medium'][2] * brightness + COLORS['bg_dark'][2] * (1 - brightness))
            img.putpixel((x, y), (r, g, b))
    
    return img

def draw_tech_lines(draw, width, height):
    """Draw sleek tech lines emanating from center."""
    center_x, center_y = width // 2, height // 2
    
    # Horizontal tech lines
    for i, y_offset in enumerate([-80, -40, 40, 80]):
        y = center_y + y_offset
        alpha = 150 - abs(y_offset)
        
        # Left line
        left_start = 50 + abs(y_offset) * 2
        left_end = center_x - 180 - abs(y_offset)
        
        # Gradient line effect
        for x in range(int(left_start), int(left_end), 3):
            progress = (x - left_start) / (left_end - left_start)
            line_alpha = int(alpha * progress)
            draw.line([(x, y), (x + 2, y)], fill=(*COLORS['primary'][:3], line_alpha), width=2)
        
        # End node
        draw.ellipse([left_end - 4, y - 4, left_end + 4, y + 4], 
                    fill=(*COLORS['accent'][:3], alpha))
        
        # Right line
        right_start = center_x + 180 + abs(y_offset)
        right_end = width - 50 - abs(y_offset) * 2
        
        for x in range(int(right_start), int(right_end), 3):
            progress = (x - right_start) / (right_end - right_start)
            line_alpha = int(alpha * (1 - progress))
            draw.line([(x, y), (x + 2, y)], fill=(*COLORS['primary'][:3], line_alpha), width=2)
        
        # Start node
        draw.ellipse([right_start - 4, y - 4, right_start + 4, y + 4], 
                    fill=(*COLORS['accent'][:3], alpha))
    
    # Diagonal lines from corners
    corner_lines = [
        # (start_x, start_y, angle, length)
        (0, 0, 35, 200),
        (width, 0, 145, 200),
        (0, height, -35, 200),
        (width, height, -145, 200),
    ]
    
    for start_x, start_y, angle, length in corner_lines:
        rad = math.radians(angle)
        for i in range(0, length, 3):
            progress = i / length
            x = start_x + i * math.cos(rad)
            y = start_y + i * math.sin(rad)
            alpha = int(80 * (1 - progress))
            if 0 <= x < width and 0 <= y < height:
                draw.ellipse([x-1, y-1, x+1, y+1], fill=(*COLORS['secondary'][:3], alpha))

def draw_connection_nodes(draw, width, height):
    """Draw connected nodes around the center."""
    center_x, center_y = width // 2, height // 2
    
    # Inner ring of nodes
    inner_radius = 140
    for i in range(6):
        angle = i * 60 + 30
        rad = math.radians(angle)
        x = center_x + inner_radius * math.cos(rad)
        y = center_y + inner_radius * math.sin(rad) * 0.6  # Flatten for perspective
        
        # Skip nodes that would be behind text
        if abs(x - center_x) < 100 and abs(y - center_y) < 60:
            continue
        
        # Node glow
        for j in range(4, 0, -1):
            glow_r = 6 + j * 3
            alpha = int(30 * j / 4)
            draw.ellipse([x-glow_r, y-glow_r, x+glow_r, y+glow_r],
                        fill=(*COLORS['glow'][:3], alpha))
        
        # Node
        draw.ellipse([x-5, y-5, x+5, y+5], fill=COLORS['accent'])
        
        # Connection to center area
        draw.line([(x, y), (center_x + (x - center_x) * 0.3, center_y + (y - center_y) * 0.3)],
                 fill=(*COLORS['primary'][:3], 60), width=1)

def draw_center_glow(image, center_x, center_y):
    """Draw glowing effect behind center text area."""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    # Multiple glow layers
    for i in range(8, 0, -1):
        radius_x = 200 + i * 20
        radius_y = 100 + i * 10
        alpha = int(20 * i / 8)
        
        draw.ellipse([center_x - radius_x, center_y - radius_y,
                      center_x + radius_x, center_y + radius_y],
                    fill=(*COLORS['glow'][:3], alpha))
    
    return Image.alpha_composite(image.convert('RGBA'), overlay)

def draw_frame_accents(draw, width, height):
    """Draw subtle frame accents."""
    # Top line with fade
    for x in range(100, width - 100):
        progress = abs(x - width/2) / (width/2 - 100)
        alpha = int(80 * (1 - progress))
        draw.point((x, 15), fill=(*COLORS['primary'][:3], alpha))
    
    # Bottom line with fade
    for x in range(100, width - 100):
        progress = abs(x - width/2) / (width/2 - 100)
        alpha = int(80 * (1 - progress))
        draw.point((x, height - 15), fill=(*COLORS['secondary'][:3], alpha))
    
    # Corner brackets
    bracket_size = 30
    bracket_width = 2
    
    # Top-left
    draw.line([(20, 20), (20, 20 + bracket_size)], fill=COLORS['primary'], width=bracket_width)
    draw.line([(20, 20), (20 + bracket_size, 20)], fill=COLORS['primary'], width=bracket_width)
    
    # Top-right
    draw.line([(width - 20, 20), (width - 20, 20 + bracket_size)], fill=COLORS['primary'], width=bracket_width)
    draw.line([(width - 20, 20), (width - 20 - bracket_size, 20)], fill=COLORS['primary'], width=bracket_width)
    
    # Bottom-left
    draw.line([(20, height - 20), (20, height - 20 - bracket_size)], fill=COLORS['secondary'], width=bracket_width)
    draw.line([(20, height - 20), (20 + bracket_size, height - 20)], fill=COLORS['secondary'], width=bracket_width)
    
    # Bottom-right
    draw.line([(width - 20, height - 20), (width - 20, height - 20 - bracket_size)], fill=COLORS['secondary'], width=bracket_width)
    draw.line([(width - 20, height - 20), (width - 20 - bracket_size, height - 20)], fill=COLORS['secondary'], width=bracket_width)

def create_facebook_cover_v4():
    """Create Facebook cover with tech lines centered design."""
    width, height = 820, 312
    
    # Create gradient background
    cover = create_gradient_bg(width, height)
    cover = cover.convert('RGBA')
    draw = ImageDraw.Draw(cover, 'RGBA')
    
    fonts = get_fonts()
    center_x, center_y = width // 2, height // 2
    
    # Draw tech lines
    draw_tech_lines(draw, width, height)
    
    # Draw connection nodes
    draw_connection_nodes(draw, width, height)
    
    # Add center glow
    cover = draw_center_glow(cover, center_x, center_y)
    draw = ImageDraw.Draw(cover, 'RGBA')
    
    # Draw frame accents
    draw_frame_accents(draw, width, height)
    
    # === CENTERED TEXT ===
    
    # Main title
    title = "VISWA AI AGENTS"
    bbox = draw.textbbox((0, 0), title, font=fonts['title'])
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = center_y - 65
    
    # Title shadow
    draw.text((title_x + 2, title_y + 2), title, font=fonts['title'],
              fill=(*COLORS['shadow'][:3], 180))
    # Title main
    draw.text((title_x, title_y), title, font=fonts['title'],
              fill=COLORS['text_white'])
    
    # Subtitle
    subtitle = "Building Practical AI Agents"
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 70
    
    draw.text((subtitle_x, subtitle_y), subtitle, font=fonts['subtitle'],
              fill=COLORS['accent'])
    
    # Decorative line under subtitle
    line_width = subtitle_width + 40
    line_y = subtitle_y + 38
    
    # Gradient line
    for i in range(int(line_width)):
        x = (width - line_width) // 2 + i
        progress = abs(i - line_width/2) / (line_width/2)
        alpha = int(200 * (1 - progress))
        draw.point((x, line_y), fill=(*COLORS['primary'][:3], alpha))
        draw.point((x, line_y + 1), fill=(*COLORS['primary'][:3], alpha // 2))
    
    # Tagline
    tagline = "Agentic AI  |  Automation  |  Autonomous Systems"
    bbox = draw.textbbox((0, 0), tagline, font=fonts['tagline'])
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (width - tagline_width) // 2
    tagline_y = line_y + 15
    
    draw.text((tagline_x, tagline_y), tagline, font=fonts['tagline'],
              fill=COLORS['text_light'])
    
    # Topics at bottom
    topics = "N8N  *  ChatGPT  *  Claude  *  Cursor AI  *  Business Automation"
    bbox = draw.textbbox((0, 0), topics, font=fonts['small'])
    topics_width = bbox[2] - bbox[0]
    topics_x = (width - topics_width) // 2
    topics_y = tagline_y + 30
    
    draw.text((topics_x, topics_y), topics, font=fonts['small'],
              fill=COLORS['text_muted'])
    
    # Save
    cover = cover.convert('RGB')
    cover.save("facebook_cover_viswa_ai.png", "PNG", quality=95)
    
    file_size = os.path.getsize("facebook_cover_viswa_ai.png") / 1024
    print(f"[OK] Facebook cover created: facebook_cover_viswa_ai.png")
    print(f"     Design: Tech Lines - Centered Layout")
    print(f"     Colors: Blue & Cyan")
    print(f"     Dimensions: {width}x{height} pixels")
    print(f"     File size: {file_size:.0f} KB")
    print()
    print("DESIGN FEATURES:")
    print("-" * 50)
    print("  - Clean tech lines emanating from center")
    print("  - Connection nodes with glow effects")
    print("  - Centered text layout")
    print("  - Smooth gradient background")
    print("  - Corner bracket accents")
    print("  - Blue & Cyan color scheme")
    print()
    print("UPLOAD: Facebook Page/Profile > Cover Photo > Upload")
    
    return cover

if __name__ == "__main__":
    create_facebook_cover_v4()
