"""
YouTube Channel Banner Generator for Viswa AI Agents
Creates a 2560x1440px banner optimized for YouTube
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_gradient(width, height, color1, color2, direction='horizontal'):
    """Create a gradient image."""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        for x in range(width):
            if direction == 'horizontal':
                mask_data.append(int(255 * x / width))
            else:
                mask_data.append(int(255 * y / height))
    
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_circuit_pattern(draw, width, height, color):
    """Draw subtle circuit-like pattern for tech feel."""
    import random
    random.seed(42)  # Consistent pattern
    
    for _ in range(50):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        
        # Horizontal lines
        x2 = x1 + random.randint(50, 200)
        draw.line([(x1, y1), (x2, y1)], fill=color, width=1)
        
        # Vertical segments
        if random.random() > 0.5:
            y2 = y1 + random.randint(30, 100)
            draw.line([(x2, y1), (x2, y2)], fill=color, width=1)
        
        # Node dots
        if random.random() > 0.7:
            draw.ellipse([x1-4, y1-4, x1+4, y1+4], fill=color)

def draw_ai_nodes(draw, width, height):
    """Draw connected nodes representing AI network."""
    import random
    random.seed(123)
    
    nodes = []
    # Create nodes in strategic positions
    for _ in range(15):
        x = random.randint(100, width - 100)
        y = random.randint(200, height - 200)
        nodes.append((x, y))
    
    # Draw connections
    for i, node1 in enumerate(nodes):
        for node2 in nodes[i+1:i+3]:
            draw.line([node1, node2], fill=(100, 180, 255, 80), width=2)
    
    # Draw nodes
    for x, y in nodes:
        # Outer glow
        draw.ellipse([x-15, y-15, x+15, y+15], fill=(100, 180, 255, 50))
        # Inner node
        draw.ellipse([x-8, y-8, x+8, y+8], fill=(150, 220, 255))

def create_banner():
    """Create the YouTube channel banner."""
    # YouTube banner dimensions
    width, height = 2560, 1440
    
    # Create gradient background (dark blue to purple - tech/AI feel)
    banner = create_gradient(width, height, (15, 20, 50), (40, 20, 80), 'horizontal')
    draw = ImageDraw.Draw(banner, 'RGBA')
    
    # Add circuit pattern
    draw_circuit_pattern(draw, width, height, (60, 80, 140, 100))
    
    # Add AI network nodes
    draw_ai_nodes(draw, width, height)
    
    # Add glowing orbs for visual interest
    for pos, size, color in [
        ((400, 400), 300, (100, 150, 255, 30)),
        ((2200, 500), 250, (150, 100, 255, 25)),
        ((1280, 900), 400, (80, 120, 200, 20)),
    ]:
        for i in range(5, 0, -1):
            s = size * i // 5
            alpha = color[3] // i
            draw.ellipse([pos[0]-s, pos[1]-s, pos[0]+s, pos[1]+s], 
                        fill=(color[0], color[1], color[2], alpha))
    
    # Try to load fonts (use default if not available)
    try:
        # Try common Windows fonts
        title_font = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 140)
        subtitle_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 60)
        tagline_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 45)
    except:
        try:
            title_font = ImageFont.truetype("arial.ttf", 140)
            subtitle_font = ImageFont.truetype("arial.ttf", 60)
            tagline_font = ImageFont.truetype("arial.ttf", 45)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            tagline_font = ImageFont.load_default()
    
    # Main title - centered in the safe zone (middle 1546x423 area)
    title = "VISWA AI AGENTS"
    
    # Get text bounding box for centering
    bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = 520
    
    # Draw title shadow
    draw.text((title_x + 4, title_y + 4), title, font=title_font, fill=(0, 0, 0, 150))
    
    # Draw title with gradient effect (simulate with multiple layers)
    draw.text((title_x, title_y), title, font=title_font, fill=(255, 255, 255))
    
    # Subtitle
    subtitle = "Build • Automate • Innovate"
    bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 160
    
    draw.text((subtitle_x, subtitle_y), subtitle, font=subtitle_font, fill=(150, 220, 255))
    
    # Tagline
    tagline = "AI Agents Tutorials | Automation | LangChain | No-Code AI"
    bbox = draw.textbbox((0, 0), tagline, font=tagline_font)
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (width - tagline_width) // 2
    tagline_y = subtitle_y + 100
    
    draw.text((tagline_x, tagline_y), tagline, font=tagline_font, fill=(180, 180, 200))
    
    # Add decorative lines
    line_y = subtitle_y - 20
    line_width = 300
    center_x = width // 2
    
    # Left line
    draw.line([(center_x - subtitle_width//2 - 50, line_y), 
               (center_x - subtitle_width//2 - 50 - line_width, line_y)], 
              fill=(100, 180, 255), width=3)
    
    # Right line
    draw.line([(center_x + subtitle_width//2 + 50, line_y), 
               (center_x + subtitle_width//2 + 50 + line_width, line_y)], 
              fill=(100, 180, 255), width=3)
    
    # Add AI robot icon placeholder (simple geometric representation)
    icon_center_x = width // 2
    icon_center_y = 380
    
    # Robot head (rounded rectangle simulation)
    head_size = 60
    draw.rounded_rectangle(
        [icon_center_x - head_size, icon_center_y - head_size,
         icon_center_x + head_size, icon_center_y + head_size],
        radius=15,
        fill=(100, 180, 255),
        outline=(150, 220, 255),
        width=3
    )
    
    # Robot eyes
    eye_offset = 25
    eye_size = 12
    draw.ellipse([icon_center_x - eye_offset - eye_size, icon_center_y - 15 - eye_size,
                  icon_center_x - eye_offset + eye_size, icon_center_y - 15 + eye_size],
                 fill=(255, 255, 255))
    draw.ellipse([icon_center_x + eye_offset - eye_size, icon_center_y - 15 - eye_size,
                  icon_center_x + eye_offset + eye_size, icon_center_y - 15 + eye_size],
                 fill=(255, 255, 255))
    
    # Robot antenna
    draw.line([(icon_center_x, icon_center_y - head_size),
               (icon_center_x, icon_center_y - head_size - 30)],
              fill=(150, 220, 255), width=4)
    draw.ellipse([icon_center_x - 8, icon_center_y - head_size - 45,
                  icon_center_x + 8, icon_center_y - head_size - 30],
                 fill=(255, 220, 100))
    
    # Save the banner
    output_path = "youtube_banner_viswa_ai_agents.png"
    banner.save(output_path, "PNG", quality=95)
    print(f"✓ Banner created successfully: {output_path}")
    print(f"  Dimensions: {width}x{height}px")
    print(f"  File size: {os.path.getsize(output_path) / 1024:.1f} KB")
    print("\n📋 Upload Instructions:")
    print("  1. Go to YouTube Studio → Customization → Branding")
    print("  2. Click 'UPLOAD' under Banner image")
    print("  3. Select this file and adjust the visible area if needed")
    print("\n💡 The safe zone (visible on all devices) is the center 1546x423px area")
    
    return output_path

if __name__ == "__main__":
    try:
        from PIL import Image, ImageDraw, ImageFont
        create_banner()
    except ImportError:
        print("Installing Pillow library...")
        import subprocess
        subprocess.check_call(['pip', 'install', 'Pillow'])
        from PIL import Image, ImageDraw, ImageFont
        create_banner()
