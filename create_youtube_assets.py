"""
YouTube Channel Assets Generator for Viswa AI Agents
Creates: Banner, Profile Picture, and Thumbnail Templates
Color Scheme: Blue & Cyan (Modern/Fresh)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Brand Colors - Blue & Cyan Theme
COLORS = {
    'bg_dark': (8, 15, 35),
    'bg_medium': (15, 30, 60),
    'primary': (0, 180, 255),      # Cyan
    'secondary': (0, 120, 200),    # Blue
    'accent': (100, 220, 255),     # Light cyan
    'glow': (0, 200, 255),
    'text_white': (255, 255, 255),
    'text_light': (200, 230, 255),
    'text_muted': (150, 180, 210),
}

def get_fonts():
    """Load fonts with fallbacks."""
    fonts = {}
    font_paths = [
        ("C:/Windows/Fonts/seguibold.ttf", "C:/Windows/Fonts/segoeui.ttf"),
        ("arial.ttf", "arial.ttf"),
    ]
    
    for bold_path, regular_path in font_paths:
        try:
            fonts['title_large'] = ImageFont.truetype(bold_path, 140)
            fonts['title_medium'] = ImageFont.truetype(bold_path, 80)
            fonts['title_small'] = ImageFont.truetype(bold_path, 60)
            fonts['subtitle'] = ImageFont.truetype(regular_path, 55)
            fonts['tagline'] = ImageFont.truetype(regular_path, 42)
            fonts['small'] = ImageFont.truetype(regular_path, 32)
            fonts['thumbnail_title'] = ImageFont.truetype(bold_path, 90)
            fonts['thumbnail_sub'] = ImageFont.truetype(bold_path, 50)
            fonts['profile'] = ImageFont.truetype(bold_path, 280)
            fonts['profile_sub'] = ImageFont.truetype(bold_path, 120)
            return fonts
        except:
            continue
    
    # Fallback to default
    default = ImageFont.load_default()
    return {k: default for k in ['title_large', 'title_medium', 'title_small', 
                                   'subtitle', 'tagline', 'small', 'thumbnail_title',
                                   'thumbnail_sub', 'profile', 'profile_sub']}

def create_gradient(width, height, color1, color2, direction='diagonal'):
    """Create a gradient image."""
    base = Image.new('RGB', (width, height), color1)
    top = Image.new('RGB', (width, height), color2)
    mask = Image.new('L', (width, height))
    mask_data = []
    
    for y in range(height):
        for x in range(width):
            if direction == 'horizontal':
                val = int(255 * x / width)
            elif direction == 'vertical':
                val = int(255 * y / height)
            else:  # diagonal
                val = int(255 * (x + y) / (width + height))
            mask_data.append(val)
    
    mask.putdata(mask_data)
    base.paste(top, (0, 0), mask)
    return base

def draw_glow_circle(draw, center, radius, color, intensity=5):
    """Draw a glowing circle effect."""
    for i in range(intensity, 0, -1):
        r = radius + (intensity - i) * 15
        alpha = int(40 * i / intensity)
        glow_color = (*color[:3], alpha) if len(color) == 4 else (*color, alpha)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], 
                    fill=glow_color)

def draw_hex_pattern(draw, width, height, color, size=60, spacing=80):
    """Draw hexagonal pattern for tech feel."""
    for y in range(-size, height + size, spacing):
        offset = (y // spacing % 2) * (spacing // 2)
        for x in range(-size + offset, width + size, spacing):
            points = []
            for i in range(6):
                angle = math.pi / 6 + i * math.pi / 3
                px = x + size * 0.4 * math.cos(angle)
                py = y + size * 0.4 * math.sin(angle)
                points.append((px, py))
            draw.polygon(points, outline=color, width=1)

def draw_flowing_lines(draw, width, height, color):
    """Draw flowing tech lines."""
    import random
    random.seed(42)
    
    for _ in range(8):
        start_x = random.randint(0, width // 3)
        start_y = random.randint(0, height)
        
        points = [(start_x, start_y)]
        x, y = start_x, start_y
        
        for _ in range(random.randint(4, 8)):
            x += random.randint(100, 300)
            y += random.randint(-50, 50)
            points.append((x, y))
        
        if len(points) >= 2:
            draw.line(points, fill=color, width=2)
            # Add node dots
            for px, py in points[::2]:
                draw.ellipse([px-5, py-5, px+5, py+5], fill=COLORS['accent'])

def draw_ai_icon(draw, center_x, center_y, size, colors):
    """Draw a stylized AI brain/chip icon."""
    # Main chip body
    chip_size = size
    draw.rounded_rectangle(
        [center_x - chip_size, center_y - chip_size,
         center_x + chip_size, center_y + chip_size],
        radius=size // 5,
        fill=colors['secondary'],
        outline=colors['accent'],
        width=3
    )
    
    # Inner circuit pattern
    inner = chip_size * 0.6
    draw.rounded_rectangle(
        [center_x - inner, center_y - inner,
         center_x + inner, center_y + inner],
        radius=size // 8,
        fill=colors['bg_dark'],
        outline=colors['primary'],
        width=2
    )
    
    # AI "brain" nodes
    node_positions = [
        (0, -inner * 0.5), (0, inner * 0.5),
        (-inner * 0.5, 0), (inner * 0.5, 0),
        (-inner * 0.35, -inner * 0.35), (inner * 0.35, -inner * 0.35),
        (-inner * 0.35, inner * 0.35), (inner * 0.35, inner * 0.35),
    ]
    
    # Draw connections
    for i, (x1, y1) in enumerate(node_positions):
        for x2, y2 in node_positions[i+1:i+3]:
            draw.line([(center_x + x1, center_y + y1), 
                      (center_x + x2, center_y + y2)],
                     fill=colors['primary'], width=2)
    
    # Draw nodes
    for x, y in node_positions:
        nx, ny = center_x + x, center_y + y
        draw.ellipse([nx-6, ny-6, nx+6, ny+6], fill=colors['accent'])
    
    # Center core
    draw.ellipse([center_x-12, center_y-12, center_x+12, center_y+12], 
                fill=colors['glow'])
    
    # Connection pins on edges
    pin_positions = [-chip_size*0.6, -chip_size*0.2, chip_size*0.2, chip_size*0.6]
    for offset in pin_positions:
        # Top pins
        draw.rectangle([center_x + offset - 4, center_y - chip_size - 15,
                       center_x + offset + 4, center_y - chip_size],
                      fill=colors['accent'])
        # Bottom pins
        draw.rectangle([center_x + offset - 4, center_y + chip_size,
                       center_x + offset + 4, center_y + chip_size + 15],
                      fill=colors['accent'])
        # Left pins
        draw.rectangle([center_x - chip_size - 15, center_y + offset - 4,
                       center_x - chip_size, center_y + offset + 4],
                      fill=colors['accent'])
        # Right pins
        draw.rectangle([center_x + chip_size, center_y + offset - 4,
                       center_x + chip_size + 15, center_y + offset + 4],
                      fill=colors['accent'])

def create_banner(fonts):
    """Create YouTube channel banner (2560x1440)."""
    width, height = 2560, 1440
    
    # Create gradient background
    banner = create_gradient(width, height, COLORS['bg_dark'], COLORS['bg_medium'], 'diagonal')
    draw = ImageDraw.Draw(banner, 'RGBA')
    
    # Add hex pattern
    draw_hex_pattern(draw, width, height, (*COLORS['secondary'], 40))
    
    # Add flowing lines
    draw_flowing_lines(draw, width, height, (*COLORS['primary'], 60))
    
    # Add glowing orbs
    glow_positions = [(350, 450), (2200, 400), (1280, 1100), (600, 1000), (1900, 900)]
    for pos in glow_positions:
        draw_glow_circle(draw, pos, 150, COLORS['glow'])
    
    # Draw AI icon
    draw_ai_icon(draw, width // 2, 350, 70, COLORS)
    
    # Main title
    title = "VISWA AI AGENTS"
    bbox = draw.textbbox((0, 0), title, font=fonts['title_large'])
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = 480
    
    # Title shadow
    draw.text((title_x + 3, title_y + 3), title, font=fonts['title_large'], 
              fill=(0, 0, 0, 180))
    # Main title
    draw.text((title_x, title_y), title, font=fonts['title_large'], 
              fill=COLORS['text_white'])
    
    # Subtitle with icon bullets
    subtitle = "Build  |  Automate  |  Scale"
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 160
    draw.text((subtitle_x, subtitle_y), subtitle, font=fonts['subtitle'], 
              fill=COLORS['accent'])
    
    # Decorative lines
    line_y = subtitle_y + 80
    line_length = 200
    center = width // 2
    
    # Gradient lines
    for i in range(3):
        alpha = 255 - i * 60
        draw.line([(center - 350 - i*100, line_y), (center - 150, line_y)],
                 fill=(*COLORS['primary'][:3], alpha), width=2)
        draw.line([(center + 150, line_y), (center + 350 + i*100, line_y)],
                 fill=(*COLORS['primary'][:3], alpha), width=2)
    
    # Tagline
    tagline = "AI Agents Tutorials  |  Step-by-Step Guides  |  Automation"
    bbox = draw.textbbox((0, 0), tagline, font=fonts['tagline'])
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (width - tagline_width) // 2
    tagline_y = line_y + 30
    draw.text((tagline_x, tagline_y), tagline, font=fonts['tagline'], 
              fill=COLORS['text_muted'])
    
    # Topics/tools bar at bottom
    topics = "N8N  *  ChatGPT  *  Claude API  *  Business Automation  *  No-Code AI"
    bbox = draw.textbbox((0, 0), topics, font=fonts['small'])
    topics_width = bbox[2] - bbox[0]
    topics_x = (width - topics_width) // 2
    topics_y = tagline_y + 80
    draw.text((topics_x, topics_y), topics, font=fonts['small'], 
              fill=COLORS['text_light'])
    
    # Save banner
    banner.save("youtube_banner_viswa_ai_agents.png", "PNG", quality=95)
    print("[OK] Banner created: youtube_banner_viswa_ai_agents.png (2560x1440)")
    return banner

def create_profile_picture(fonts):
    """Create YouTube profile picture (800x800)."""
    size = 800
    
    # Create gradient background
    profile = create_gradient(size, size, COLORS['bg_dark'], COLORS['secondary'], 'diagonal')
    draw = ImageDraw.Draw(profile, 'RGBA')
    
    # Add subtle hex pattern
    draw_hex_pattern(draw, size, size, (*COLORS['primary'], 30), size=40, spacing=50)
    
    # Outer glow ring
    center = size // 2
    for i in range(20, 0, -1):
        r = 350 + i * 3
        alpha = int(15 * i / 20)
        draw.ellipse([center-r, center-r, center+r, center+r],
                    outline=(*COLORS['glow'], alpha), width=2)
    
    # Main circle background
    draw.ellipse([center-320, center-320, center+320, center+320],
                fill=COLORS['bg_dark'], outline=COLORS['primary'], width=5)
    
    # Inner decorative ring
    draw.ellipse([center-280, center-280, center+280, center+280],
                outline=(*COLORS['accent'], 100), width=2)
    
    # Letters "VA" for Viswa AI
    text = "VA"
    bbox = draw.textbbox((0, 0), text, font=fonts['profile'])
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 60
    
    # Text glow
    for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
        draw.text((text_x + offset[0], text_y + offset[1]), text, 
                 font=fonts['profile'], fill=(*COLORS['glow'], 100))
    
    # Main text
    draw.text((text_x, text_y), text, font=fonts['profile'], fill=COLORS['text_white'])
    
    # "AI" subscript
    sub_text = "AI"
    bbox = draw.textbbox((0, 0), sub_text, font=fonts['profile_sub'])
    sub_width = bbox[2] - bbox[0]
    sub_x = (size - sub_width) // 2
    sub_y = text_y + text_height - 30
    draw.text((sub_x, sub_y), sub_text, font=fonts['profile_sub'], fill=COLORS['accent'])
    
    # Corner accents
    accent_size = 40
    # Top-left
    draw.line([(100, 100), (100, 100 + accent_size)], fill=COLORS['primary'], width=3)
    draw.line([(100, 100), (100 + accent_size, 100)], fill=COLORS['primary'], width=3)
    # Top-right
    draw.line([(700, 100), (700, 100 + accent_size)], fill=COLORS['primary'], width=3)
    draw.line([(700, 100), (700 - accent_size, 100)], fill=COLORS['primary'], width=3)
    # Bottom-left
    draw.line([(100, 700), (100, 700 - accent_size)], fill=COLORS['primary'], width=3)
    draw.line([(100, 700), (100 + accent_size, 700)], fill=COLORS['primary'], width=3)
    # Bottom-right
    draw.line([(700, 700), (700, 700 - accent_size)], fill=COLORS['primary'], width=3)
    draw.line([(700, 700), (700 - accent_size, 700)], fill=COLORS['primary'], width=3)
    
    # Save profile picture
    profile.save("youtube_profile_viswa_ai.png", "PNG", quality=95)
    print("[OK] Profile picture created: youtube_profile_viswa_ai.png (800x800)")
    return profile

def create_thumbnail_template(fonts, title="AI Agents Tutorial", subtitle="Step-by-Step Guide", filename_suffix="template"):
    """Create YouTube video thumbnail (1280x720)."""
    width, height = 1280, 720
    
    # Create gradient background
    thumb = create_gradient(width, height, COLORS['bg_dark'], COLORS['bg_medium'], 'diagonal')
    draw = ImageDraw.Draw(thumb, 'RGBA')
    
    # Add subtle pattern
    draw_hex_pattern(draw, width, height, (*COLORS['secondary'], 25), size=30, spacing=40)
    
    # Left side glow
    draw_glow_circle(draw, (150, 360), 200, COLORS['glow'])
    
    # Right side content area background
    draw.rounded_rectangle([600, 80, 1220, 640], radius=20,
                          fill=(*COLORS['bg_dark'], 200))
    
    # Left side - AI Icon
    draw_ai_icon(draw, 280, 360, 100, COLORS)
    
    # Right side - Text content
    # Main title (word wrap if needed)
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=fonts['thumbnail_title'])
        if bbox[2] - bbox[0] > 580:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title lines
    title_y = 180 if len(lines) <= 2 else 140
    for i, line in enumerate(lines[:3]):  # Max 3 lines
        # Shadow
        draw.text((642, title_y + i * 100 + 2), line, font=fonts['thumbnail_title'],
                 fill=(0, 0, 0, 200))
        # Main text
        draw.text((640, title_y + i * 100), line, font=fonts['thumbnail_title'],
                 fill=COLORS['text_white'])
    
    # Subtitle
    sub_y = title_y + len(lines) * 100 + 20
    draw.text((640, sub_y), subtitle, font=fonts['thumbnail_sub'],
             fill=COLORS['accent'])
    
    # Bottom accent bar
    draw.rectangle([620, 600, 1200, 610], fill=COLORS['primary'])
    
    # Top-right corner badge
    badge_text = "TUTORIAL"
    bbox = draw.textbbox((0, 0), badge_text, font=fonts['small'])
    badge_width = bbox[2] - bbox[0] + 30
    draw.rounded_rectangle([1220 - badge_width, 100, 1220, 145], radius=10,
                          fill=COLORS['primary'])
    draw.text((1220 - badge_width + 15, 105), badge_text, font=fonts['small'],
             fill=COLORS['text_white'])
    
    # Left decorative elements
    draw.line([(50, 100), (50, 250)], fill=COLORS['primary'], width=4)
    draw.line([(50, 100), (150, 100)], fill=COLORS['primary'], width=4)
    draw.line([(50, 620), (50, 470)], fill=COLORS['primary'], width=4)
    draw.line([(50, 620), (150, 620)], fill=COLORS['primary'], width=4)
    
    # Save thumbnail
    output_name = f"youtube_thumbnail_{filename_suffix}.png"
    thumb.save(output_name, "PNG", quality=95)
    print(f"[OK] Thumbnail created: {output_name} (1280x720)")
    return thumb

def main():
    print("=" * 60)
    print("  VISWA AI AGENTS - YouTube Assets Generator")
    print("  Theme: Blue & Cyan (Modern/Fresh)")
    print("=" * 60)
    print()
    
    fonts = get_fonts()
    
    # Create all assets
    print("Creating assets...\n")
    
    # 1. Banner
    create_banner(fonts)
    
    # 2. Profile Picture
    create_profile_picture(fonts)
    
    # 3. Thumbnail Templates
    create_thumbnail_template(fonts, 
                             "N8N AI Agents", 
                             "Complete Beginner Guide",
                             "n8n_tutorial")
    
    create_thumbnail_template(fonts, 
                             "ChatGPT API", 
                             "Build Your First Agent",
                             "chatgpt_api")
    
    create_thumbnail_template(fonts, 
                             "Business Automation", 
                             "AI Tools for Productivity",
                             "business_automation")
    
    create_thumbnail_template(fonts, 
                             "Claude API Tutorial", 
                             "Advanced AI Agents",
                             "claude_api")
    
    print()
    print("=" * 60)
    print("  All assets created successfully!")
    print("=" * 60)
    print()
    print("FILES CREATED:")
    print("-" * 40)
    
    files = [
        ("youtube_banner_viswa_ai_agents.png", "2560x1440", "Channel Banner"),
        ("youtube_profile_viswa_ai.png", "800x800", "Profile Picture"),
        ("youtube_thumbnail_n8n_tutorial.png", "1280x720", "N8N Tutorial Thumb"),
        ("youtube_thumbnail_chatgpt_api.png", "1280x720", "ChatGPT API Thumb"),
        ("youtube_thumbnail_business_automation.png", "1280x720", "Business Thumb"),
        ("youtube_thumbnail_claude_api.png", "1280x720", "Claude API Thumb"),
    ]
    
    for filename, dimensions, description in files:
        if os.path.exists(filename):
            size_kb = os.path.getsize(filename) / 1024
            print(f"  {filename}")
            print(f"    -> {dimensions} | {size_kb:.0f} KB | {description}")
    
    print()
    print("UPLOAD INSTRUCTIONS:")
    print("-" * 40)
    print("  Banner:  YouTube Studio > Customization > Branding > Banner")
    print("  Profile: YouTube Studio > Customization > Branding > Picture")
    print("  Thumbs:  Upload when publishing videos or in Video Details")
    print()

if __name__ == "__main__":
    main()
