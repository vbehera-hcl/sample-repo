"""
Facebook Cover Photo V3 - Neural Network Design
Connected glowing nodes with brain-like patterns
Theme: Green & Black (Matrix Style)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math
import random

# Matrix Green Color Scheme
COLORS = {
    'bg_dark': (5, 10, 5),
    'bg_medium': (10, 20, 10),
    'primary': (0, 255, 65),        # Bright matrix green
    'secondary': (0, 200, 50),      # Medium green
    'accent': (150, 255, 150),      # Light green
    'dim': (0, 100, 30),            # Dim green
    'glow': (50, 255, 100),
    'text_white': (220, 255, 220),
    'text_light': (150, 230, 150),
    'text_muted': (80, 150, 80),
    'shadow': (0, 5, 0),
}

def get_fonts():
    """Load fonts."""
    fonts = {}
    try:
        fonts['title'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 56)
        fonts['subtitle'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 24)
        fonts['tagline'] = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 18)
        fonts['small'] = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 14)
        fonts['code'] = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 10)
    except:
        try:
            fonts['title'] = ImageFont.truetype("arial.ttf", 56)
            fonts['subtitle'] = ImageFont.truetype("arial.ttf", 24)
            fonts['tagline'] = ImageFont.truetype("arial.ttf", 18)
            fonts['small'] = ImageFont.truetype("arial.ttf", 14)
            fonts['code'] = ImageFont.truetype("arial.ttf", 10)
        except:
            default = ImageFont.load_default()
            fonts = {k: default for k in ['title', 'subtitle', 'tagline', 'small', 'code']}
    return fonts

def create_dark_gradient(width, height):
    """Create dark gradient with subtle green tint."""
    img = Image.new('RGB', (width, height), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # Radial gradient from center
    center_x, center_y = width // 2, height // 2
    max_dist = math.sqrt(center_x**2 + center_y**2)
    
    for y in range(height):
        for x in range(width):
            dist = math.sqrt((x - center_x)**2 + (y - center_y)**2) / max_dist
            # Darker at edges
            brightness = 1 - (dist * 0.7)
            r = int(COLORS['bg_medium'][0] * brightness)
            g = int(COLORS['bg_medium'][1] * brightness)
            b = int(COLORS['bg_medium'][2] * brightness)
            img.putpixel((x, y), (max(0, r), max(0, g), max(0, b)))
    
    return img

def draw_matrix_rain(draw, width, height, density=40):
    """Draw subtle matrix-style falling code in background."""
    random.seed(42)
    chars = "01アイウエオカキクケコサシスセソタチツテト"
    
    for _ in range(density):
        x = random.randint(0, width)
        start_y = random.randint(-50, height)
        length = random.randint(5, 15)
        
        for i in range(length):
            y = start_y + i * 12
            if 0 <= y < height:
                char = random.choice(chars)
                # Fade effect - brighter at top of stream
                alpha = int(80 - i * 5)
                if alpha > 0:
                    draw.text((x, y), char, font=ImageFont.load_default(),
                             fill=(*COLORS['dim'][:3], alpha))

def draw_neural_network(draw, width, height):
    """Draw neural network with connected nodes."""
    random.seed(123)
    
    # Create layers of nodes
    layers = [
        # Layer 1 (left) - input layer
        [(80, 80), (80, 156), (80, 232)],
        # Layer 2
        [(180, 60), (180, 130), (180, 200), (180, 270)],
        # Layer 3 (hidden)
        [(280, 90), (280, 156), (280, 222)],
    ]
    
    all_nodes = []
    for layer in layers:
        all_nodes.extend(layer)
    
    # Draw connections first (behind nodes)
    for i, layer in enumerate(layers[:-1]):
        next_layer = layers[i + 1]
        for node1 in layer:
            for node2 in next_layer:
                # Calculate connection strength (visual)
                dist = math.sqrt((node2[0]-node1[0])**2 + (node2[1]-node1[1])**2)
                alpha = int(80 - dist * 0.2)
                if alpha > 20:
                    # Draw glowing connection
                    draw.line([node1, node2], fill=(*COLORS['dim'][:3], alpha), width=1)
                    
                    # Pulse effect - brighter segment
                    mid_x = (node1[0] + node2[0]) // 2
                    mid_y = (node1[1] + node2[1]) // 2
                    draw.ellipse([mid_x-2, mid_y-2, mid_x+2, mid_y+2],
                                fill=(*COLORS['secondary'][:3], alpha))
    
    # Draw nodes with glow
    for x, y in all_nodes:
        # Outer glow
        for i in range(5, 0, -1):
            glow_r = 8 + i * 4
            alpha = int(30 * i / 5)
            draw.ellipse([x-glow_r, y-glow_r, x+glow_r, y+glow_r],
                        fill=(*COLORS['glow'][:3], alpha))
        
        # Node outer ring
        draw.ellipse([x-10, y-10, x+10, y+10],
                    fill=COLORS['bg_dark'],
                    outline=COLORS['primary'],
                    width=2)
        
        # Node inner core
        draw.ellipse([x-5, y-5, x+5, y+5], fill=COLORS['primary'])
    
    # Add some random floating smaller nodes for depth
    for _ in range(15):
        x = random.randint(50, 320)
        y = random.randint(30, height - 30)
        size = random.randint(2, 4)
        alpha = random.randint(40, 100)
        
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=(*COLORS['secondary'][:3], alpha))

def draw_brain_outline(draw, center_x, center_y, size):
    """Draw a subtle brain outline."""
    # Simplified brain shape using curves
    points = []
    for angle in range(0, 360, 10):
        rad = math.radians(angle)
        # Create brain-like wavy shape
        r = size * (0.8 + 0.2 * math.sin(rad * 3) + 0.1 * math.cos(rad * 5))
        x = center_x + r * math.cos(rad)
        y = center_y + r * math.sin(rad) * 0.75  # Flatten slightly
        points.append((x, y))
    
    # Draw outline with glow
    for i in range(3, 0, -1):
        alpha = int(20 * i / 3)
        for j in range(len(points) - 1):
            draw.line([points[j], points[j+1]], 
                     fill=(*COLORS['dim'][:3], alpha), width=i)
        draw.line([points[-1], points[0]], 
                 fill=(*COLORS['dim'][:3], alpha), width=i)

def draw_scan_lines(draw, width, height, spacing=4, alpha=15):
    """Draw CRT-style scan lines for matrix effect."""
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=(*COLORS['bg_dark'][:3], alpha), width=1)

def draw_glowing_text(draw, pos, text, font, color, glow_color, glow_size=2):
    """Draw text with glow effect."""
    x, y = pos
    
    # Glow layers
    for i in range(glow_size, 0, -1):
        alpha = int(60 * i / glow_size)
        for dx in [-i, 0, i]:
            for dy in [-i, 0, i]:
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), text, font=font,
                             fill=(*glow_color[:3], alpha))
    
    # Main text
    draw.text((x, y), text, font=font, fill=color)

def create_facebook_cover_v3():
    """Create Facebook cover with neural network matrix design."""
    width, height = 820, 312
    
    # Create dark gradient background
    cover = create_dark_gradient(width, height)
    cover = cover.convert('RGBA')
    draw = ImageDraw.Draw(cover, 'RGBA')
    
    fonts = get_fonts()
    
    # Draw matrix rain in background
    draw_matrix_rain(draw, width, height, density=50)
    
    # Draw brain outline (subtle)
    draw_brain_outline(draw, 180, 156, 100)
    
    # Draw neural network nodes and connections
    draw_neural_network(draw, width, height)
    
    # Add scan lines for CRT effect
    draw_scan_lines(draw, width, height)
    
    # Content on right side
    content_x = 380
    
    # Main title with glow
    title = "VISWA AI AGENTS"
    title_y = 65
    
    draw_glowing_text(draw, (content_x, title_y), title, fonts['title'],
                      COLORS['text_white'], COLORS['primary'], glow_size=3)
    
    # Subtitle
    subtitle = "Building Practical AI Agents"
    subtitle_y = title_y + 70
    
    # Terminal-style bracket
    draw.text((content_x - 15, subtitle_y), ">", font=fonts['subtitle'],
              fill=COLORS['primary'])
    
    draw_glowing_text(draw, (content_x + 5, subtitle_y), subtitle, fonts['subtitle'],
                      COLORS['accent'], COLORS['secondary'], glow_size=2)
    
    # Tagline
    tagline = "Agentic AI  |  Automation  |  Autonomous Systems"
    tagline_y = subtitle_y + 45
    draw.text((content_x + 5, tagline_y), tagline, font=fonts['tagline'],
              fill=COLORS['text_light'])
    
    # Terminal-style info line
    info_line = "$ ./neural_network --mode=autonomous"
    info_y = tagline_y + 35
    draw.text((content_x + 5, info_y), info_line, font=fonts['small'],
              fill=COLORS['text_muted'])
    
    # Blinking cursor effect
    draw.rectangle([content_x + 5 + len(info_line) * 8, info_y, 
                    content_x + 5 + len(info_line) * 8 + 8, info_y + 14],
                   fill=COLORS['primary'])
    
    # Corner decorations
    # Top-left
    draw.line([(340, 25), (width - 30, 25)], fill=COLORS['primary'], width=1)
    draw.line([(340, 25), (340, 45)], fill=COLORS['primary'], width=1)
    draw.text((350, 28), "// NEURAL_NET_v2.0", font=fonts['code'],
              fill=COLORS['dim'])
    
    # Bottom-right
    draw.line([(340, height - 25), (width - 30, height - 25)], 
              fill=COLORS['secondary'], width=1)
    draw.line([(width - 30, height - 25), (width - 30, height - 45)], 
              fill=COLORS['secondary'], width=1)
    
    # Status indicators
    status_y = height - 40
    for i, (label, color) in enumerate([("ONLINE", COLORS['primary']), 
                                          ("LEARNING", COLORS['secondary']),
                                          ("ACTIVE", COLORS['accent'])]):
        x = 400 + i * 100
        draw.ellipse([x, status_y, x+6, status_y+6], fill=color)
        draw.text((x + 12, status_y - 2), label, font=fonts['code'],
                  fill=COLORS['text_muted'])
    
    # Add some floating data points on right
    random.seed(456)
    for _ in range(8):
        x = random.randint(700, 800)
        y = random.randint(50, height - 50)
        size = random.randint(1, 3)
        draw.ellipse([x-size, y-size, x+size, y+size], fill=COLORS['primary'])
    
    # Save
    cover = cover.convert('RGB')
    cover.save("facebook_cover_viswa_ai.png", "PNG", quality=95)
    
    file_size = os.path.getsize("facebook_cover_viswa_ai.png") / 1024
    print(f"[OK] Facebook cover created: facebook_cover_viswa_ai.png")
    print(f"     Design: Neural Network - Matrix Style")
    print(f"     Dimensions: {width}x{height} pixels")
    print(f"     File size: {file_size:.0f} KB")
    print()
    print("DESIGN FEATURES:")
    print("-" * 50)
    print("  - Connected neural network nodes with glow")
    print("  - Matrix-style falling code background")
    print("  - Brain outline silhouette")
    print("  - CRT scan lines effect")
    print("  - Terminal-style text elements")
    print("  - Green & Black matrix color scheme")
    print()
    print("UPLOAD: Facebook Page/Profile > Cover Photo > Upload")
    
    return cover

if __name__ == "__main__":
    create_facebook_cover_v3()
