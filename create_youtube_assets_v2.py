"""
YouTube Channel Assets Generator V2 for Viswa AI Agents
Theme: Red & Orange (Energetic) with 3D Depth Effects
Updated Text: Building Practical AI Agents | Agentic AI
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math

# Brand Colors - Red & Orange Theme (Energetic)
COLORS = {
    'bg_dark': (15, 10, 20),
    'bg_medium': (35, 15, 25),
    'bg_gradient': (50, 20, 30),
    'primary': (255, 80, 50),       # Vibrant Red-Orange
    'secondary': (255, 140, 50),    # Orange
    'accent': (255, 200, 100),      # Golden Orange
    'highlight': (255, 100, 80),    # Bright coral
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
            fonts['title_large'] = ImageFont.truetype(bold_path, 130)
            fonts['title_medium'] = ImageFont.truetype(bold_path, 80)
            fonts['title_small'] = ImageFont.truetype(bold_path, 55)
            fonts['subtitle'] = ImageFont.truetype(bold_path, 52)
            fonts['tagline'] = ImageFont.truetype(regular_path, 38)
            fonts['small'] = ImageFont.truetype(regular_path, 30)
            fonts['thumbnail_title'] = ImageFont.truetype(bold_path, 85)
            fonts['thumbnail_sub'] = ImageFont.truetype(bold_path, 48)
            fonts['profile'] = ImageFont.truetype(bold_path, 260)
            fonts['profile_sub'] = ImageFont.truetype(bold_path, 100)
            return fonts
        except:
            continue
    
    default = ImageFont.load_default()
    return {k: default for k in ['title_large', 'title_medium', 'title_small', 
                                   'subtitle', 'tagline', 'small', 'thumbnail_title',
                                   'thumbnail_sub', 'profile', 'profile_sub']}

def create_gradient_3d(width, height, colors, direction='radial'):
    """Create a 3D-style gradient with depth."""
    base = Image.new('RGB', (width, height), colors[0])
    draw = ImageDraw.Draw(base)
    
    if direction == 'radial':
        center_x, center_y = width // 2, height // 2
        max_dist = math.sqrt(center_x**2 + center_y**2)
        
        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - center_x)**2 + (y - center_y)**2) / max_dist
                dist = min(1, dist * 1.2)  # Extend gradient
                
                r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * dist)
                g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * dist)
                b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * dist)
                base.putpixel((x, y), (r, g, b))
    else:
        for y in range(height):
            ratio = y / height
            r = int(colors[0][0] + (colors[1][0] - colors[0][0]) * ratio)
            g = int(colors[0][1] + (colors[1][1] - colors[0][1]) * ratio)
            b = int(colors[0][2] + (colors[1][2] - colors[0][2]) * ratio)
            draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    return base

def draw_3d_glow(image, center, radius, color, layers=8):
    """Draw a 3D glowing orb effect."""
    overlay = Image.new('RGBA', image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for i in range(layers, 0, -1):
        r = int(radius * (1 + (layers - i) * 0.3))
        alpha = int(60 * i / layers)
        draw.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r],
                    fill=(*color[:3], alpha))
    
    # Bright center core
    core_r = radius // 3
    draw.ellipse([center[0]-core_r, center[1]-core_r, 
                  center[0]+core_r, center[1]+core_r],
                fill=(*COLORS['accent'][:3], 150))
    
    return Image.alpha_composite(image.convert('RGBA'), overlay)

def draw_3d_grid(draw, width, height, color, perspective=True):
    """Draw a 3D perspective grid."""
    vanishing_y = height // 3
    
    # Horizontal lines with perspective
    for i in range(10):
        y = vanishing_y + int((height - vanishing_y) * (i / 9) ** 1.5)
        alpha = int(40 + 30 * i / 9)
        
        # Lines get closer together near horizon
        left_x = int(width * 0.1 - i * 30)
        right_x = int(width * 0.9 + i * 30)
        
        draw.line([(left_x, y), (right_x, y)], 
                 fill=(*color[:3], alpha), width=1)
    
    # Vertical lines converging to vanishing point
    vanishing_x = width // 2
    for i in range(-8, 9):
        bottom_x = vanishing_x + i * 100
        alpha = int(50 - abs(i) * 4)
        if alpha > 0:
            draw.line([(vanishing_x, vanishing_y), (bottom_x, height)],
                     fill=(*color[:3], alpha), width=1)

def draw_3d_cube(draw, center, size, colors, rotation=15):
    """Draw a 3D floating cube/chip."""
    cx, cy = center
    s = size
    
    # Calculate 3D cube vertices with simple rotation
    angle = math.radians(rotation)
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    
    # Front face (slightly rotated)
    front = [
        (cx - s * cos_a, cy - s),
        (cx + s * cos_a, cy - s),
        (cx + s * cos_a, cy + s),
        (cx - s * cos_a, cy + s),
    ]
    
    # Top face (3D effect)
    depth = s * 0.4
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
    
    # Draw faces with depth shading
    draw.polygon(top, fill=colors['secondary'], outline=colors['accent'])
    draw.polygon(right, fill=colors['primary'], outline=colors['accent'])
    draw.polygon(front, fill=colors['highlight'], outline=colors['accent'])
    
    # Inner circuit pattern on front face
    inner_offset = s * 0.3
    inner = [
        (cx - inner_offset * cos_a, cy - inner_offset),
        (cx + inner_offset * cos_a, cy - inner_offset),
        (cx + inner_offset * cos_a, cy + inner_offset),
        (cx - inner_offset * cos_a, cy + inner_offset),
    ]
    draw.polygon(inner, fill=colors['bg_dark'], outline=colors['primary'])
    
    # AI nodes inside
    node_size = 5
    for offset in [(-0.15, -0.15), (0.15, -0.15), (-0.15, 0.15), (0.15, 0.15), (0, 0)]:
        nx = cx + offset[0] * s
        ny = cy + offset[1] * s
        draw.ellipse([nx-node_size, ny-node_size, nx+node_size, ny+node_size],
                    fill=colors['accent'])

def draw_3d_text(draw, pos, text, font, main_color, shadow_color, depth=4):
    """Draw text with 3D shadow effect."""
    x, y = pos
    
    # Multiple shadow layers for 3D depth
    for i in range(depth, 0, -1):
        shadow_alpha = int(150 - i * 30)
        shadow_offset = i * 2
        draw.text((x + shadow_offset, y + shadow_offset), text, font=font,
                 fill=(*shadow_color[:3], shadow_alpha) if len(shadow_color) >= 3 else shadow_color)
    
    # Main text with slight highlight
    draw.text((x, y), text, font=font, fill=main_color)
    
    # Top highlight edge
    draw.text((x, y - 1), text, font=font, fill=(*main_color[:3], 80))

def draw_floating_particles(draw, width, height, color, count=30):
    """Draw floating particle effects."""
    import random
    random.seed(99)
    
    for _ in range(count):
        x = random.randint(0, width)
        y = random.randint(0, height)
        size = random.randint(2, 6)
        alpha = random.randint(30, 100)
        
        # Glowing particle
        draw.ellipse([x-size*2, y-size*2, x+size*2, y+size*2],
                    fill=(*color[:3], alpha//3))
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=(*color[:3], alpha))

def create_banner(fonts):
    """Create YouTube channel banner with 3D effects (2560x1440)."""
    width, height = 2560, 1440
    
    # Create radial gradient background (3D depth feel)
    banner = create_gradient_3d(width, height, 
                                [COLORS['bg_medium'], COLORS['bg_dark']], 'radial')
    banner = banner.convert('RGBA')
    draw = ImageDraw.Draw(banner, 'RGBA')
    
    # Add 3D perspective grid
    draw_3d_grid(draw, width, height, COLORS['primary'])
    
    # Add floating particles
    draw_floating_particles(draw, width, height, COLORS['secondary'])
    
    # Add 3D glowing orbs
    banner = draw_3d_glow(banner, (400, 500), 200, COLORS['glow'])
    banner = draw_3d_glow(banner, (2150, 450), 180, COLORS['secondary'])
    banner = draw_3d_glow(banner, (1280, 1000), 250, COLORS['primary'])
    draw = ImageDraw.Draw(banner, 'RGBA')
    
    # Draw 3D AI cube icon
    draw_3d_cube(draw, (width // 2, 320), 65, COLORS)
    
    # Main title with 3D effect
    title = "VISWA AI AGENTS"
    bbox = draw.textbbox((0, 0), title, font=fonts['title_large'])
    title_width = bbox[2] - bbox[0]
    title_x = (width - title_width) // 2
    title_y = 460
    
    draw_3d_text(draw, (title_x, title_y), title, fonts['title_large'],
                 COLORS['text_white'], COLORS['shadow'], depth=5)
    
    # Subtitle with gradient bar background
    subtitle = "Building Practical AI Agents"
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_width = bbox[2] - bbox[0]
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + 150
    
    # Background bar for subtitle
    bar_padding = 30
    draw.rounded_rectangle(
        [subtitle_x - bar_padding, subtitle_y - 10,
         subtitle_x + subtitle_width + bar_padding, subtitle_y + 70],
        radius=10,
        fill=(*COLORS['primary'][:3], 40),
        outline=(*COLORS['secondary'][:3], 100)
    )
    
    draw_3d_text(draw, (subtitle_x, subtitle_y), subtitle, fonts['subtitle'],
                 COLORS['accent'], COLORS['shadow'], depth=3)
    
    # Decorative 3D lines
    line_y = subtitle_y + 100
    center = width // 2
    
    for i in range(4):
        alpha = 200 - i * 40
        offset = i * 3
        # Left lines with 3D depth
        draw.line([(center - 400 - i*80, line_y + offset), (center - 150, line_y + offset)],
                 fill=(*COLORS['primary'][:3], alpha), width=3-i//2)
        # Right lines
        draw.line([(center + 150, line_y + offset), (center + 400 + i*80, line_y + offset)],
                 fill=(*COLORS['primary'][:3], alpha), width=3-i//2)
    
    # Main tagline
    tagline = "Agentic AI  *  Automation  *  Autonomous Systems"
    bbox = draw.textbbox((0, 0), tagline, font=fonts['tagline'])
    tagline_width = bbox[2] - bbox[0]
    tagline_x = (width - tagline_width) // 2
    tagline_y = line_y + 40
    
    draw.text((tagline_x, tagline_y), tagline, font=fonts['tagline'],
              fill=COLORS['text_light'])
    
    # Topics bar with 3D pill style
    topics = "N8N  |  ChatGPT  |  Claude  |  Cursor AI  |  Business Automation"
    bbox = draw.textbbox((0, 0), topics, font=fonts['small'])
    topics_width = bbox[2] - bbox[0]
    topics_x = (width - topics_width) // 2
    topics_y = tagline_y + 70
    
    # 3D pill background
    pill_padding = 25
    draw.rounded_rectangle(
        [topics_x - pill_padding, topics_y - 8,
         topics_x + topics_width + pill_padding, topics_y + 42],
        radius=20,
        fill=(*COLORS['bg_dark'][:3], 180),
        outline=COLORS['secondary']
    )
    
    draw.text((topics_x, topics_y), topics, font=fonts['small'],
              fill=COLORS['text_muted'])
    
    # Corner 3D accents
    accent_size = 80
    line_width = 4
    
    # Top-left 3D bracket
    for i in range(3):
        offset = i * 2
        alpha = 255 - i * 60
        draw.line([(150 + offset, 180), (150 + offset, 180 + accent_size)], 
                 fill=(*COLORS['primary'][:3], alpha), width=line_width)
        draw.line([(150, 180 + offset), (150 + accent_size, 180 + offset)], 
                 fill=(*COLORS['primary'][:3], alpha), width=line_width)
    
    # Top-right
    for i in range(3):
        offset = i * 2
        alpha = 255 - i * 60
        draw.line([(2410 - offset, 180), (2410 - offset, 180 + accent_size)], 
                 fill=(*COLORS['secondary'][:3], alpha), width=line_width)
        draw.line([(2410, 180 + offset), (2410 - accent_size, 180 + offset)], 
                 fill=(*COLORS['secondary'][:3], alpha), width=line_width)
    
    # Save
    banner = banner.convert('RGB')
    banner.save("youtube_banner_viswa_ai_agents.png", "PNG", quality=95)
    print("[OK] Banner created: youtube_banner_viswa_ai_agents.png (2560x1440)")
    return banner

def create_profile_picture(fonts):
    """Create YouTube profile picture with 3D effects (800x800)."""
    size = 800
    
    # Create radial gradient
    profile = create_gradient_3d(size, size, 
                                  [COLORS['bg_medium'], COLORS['bg_dark']], 'radial')
    profile = profile.convert('RGBA')
    draw = ImageDraw.Draw(profile, 'RGBA')
    
    center = size // 2
    
    # Outer 3D glow rings
    for i in range(5):
        r = 380 - i * 15
        alpha = 20 + i * 10
        draw.ellipse([center-r, center-r, center+r, center+r],
                    outline=(*COLORS['glow'][:3], alpha), width=3)
    
    # 3D beveled circle background
    # Shadow
    draw.ellipse([center-305, center-295, center+315, center+325],
                fill=(*COLORS['shadow'][:3], 150))
    # Main circle
    draw.ellipse([center-300, center-300, center+300, center+300],
                fill=COLORS['bg_dark'])
    # Highlight edge (top-left)
    draw.arc([center-300, center-300, center+300, center+300],
             start=200, end=340,
             fill=COLORS['primary'], width=5)
    # Shadow edge (bottom-right)
    draw.arc([center-300, center-300, center+300, center+300],
             start=20, end=160,
             fill=COLORS['secondary'], width=5)
    
    # Inner ring
    draw.ellipse([center-260, center-260, center+260, center+260],
                outline=(*COLORS['accent'][:3], 80), width=2)
    
    # Letters "VA" with 3D effect
    text = "VA"
    bbox = draw.textbbox((0, 0), text, font=fonts['profile'])
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = (size - text_height) // 2 - 50
    
    # 3D shadow layers
    for i in range(6, 0, -1):
        draw.text((text_x + i*2, text_y + i*2), text, font=fonts['profile'],
                 fill=(*COLORS['shadow'][:3], 180 - i*25))
    
    # Gradient text simulation (main + highlight)
    draw.text((text_x, text_y), text, font=fonts['profile'], fill=COLORS['text_white'])
    draw.text((text_x, text_y - 2), text, font=fonts['profile'], 
              fill=(*COLORS['accent'][:3], 60))
    
    # "AI" subscript with glow
    sub_text = "AI"
    bbox = draw.textbbox((0, 0), sub_text, font=fonts['profile_sub'])
    sub_width = bbox[2] - bbox[0]
    sub_x = (size - sub_width) // 2
    sub_y = text_y + text_height - 40
    
    # Glow behind text
    for i in range(3):
        draw.text((sub_x + i, sub_y + i), sub_text, font=fonts['profile_sub'],
                 fill=(*COLORS['primary'][:3], 100 - i*30))
    draw.text((sub_x, sub_y), sub_text, font=fonts['profile_sub'], fill=COLORS['secondary'])
    
    # Corner accent triangles (3D)
    triangle_size = 50
    # Top-left
    draw.polygon([(80, 80), (80 + triangle_size, 80), (80, 80 + triangle_size)],
                fill=COLORS['primary'])
    draw.polygon([(85, 85), (85 + triangle_size - 10, 85), (85, 85 + triangle_size - 10)],
                fill=COLORS['secondary'])
    # Top-right
    draw.polygon([(720, 80), (720 - triangle_size, 80), (720, 80 + triangle_size)],
                fill=COLORS['primary'])
    # Bottom-left
    draw.polygon([(80, 720), (80 + triangle_size, 720), (80, 720 - triangle_size)],
                fill=COLORS['primary'])
    # Bottom-right
    draw.polygon([(720, 720), (720 - triangle_size, 720), (720, 720 - triangle_size)],
                fill=COLORS['primary'])
    
    profile = profile.convert('RGB')
    profile.save("youtube_profile_viswa_ai.png", "PNG", quality=95)
    print("[OK] Profile picture created: youtube_profile_viswa_ai.png (800x800)")
    return profile

def create_thumbnail(fonts, title, subtitle, badge_text, filename_suffix):
    """Create YouTube thumbnail with 3D effects (1280x720)."""
    width, height = 1280, 720
    
    # Create gradient background
    thumb = create_gradient_3d(width, height,
                               [COLORS['bg_medium'], COLORS['bg_dark']], 'radial')
    thumb = thumb.convert('RGBA')
    draw = ImageDraw.Draw(thumb, 'RGBA')
    
    # 3D perspective grid (subtle)
    draw_3d_grid(draw, width, height, COLORS['primary'])
    
    # Add particles
    draw_floating_particles(draw, width, height, COLORS['secondary'], count=20)
    
    # Left side 3D glow
    thumb = draw_3d_glow(thumb, (200, 360), 180, COLORS['glow'])
    draw = ImageDraw.Draw(thumb, 'RGBA')
    
    # 3D cube icon on left
    draw_3d_cube(draw, (220, 360), 90, COLORS, rotation=20)
    
    # Right content area with 3D panel effect
    # Shadow
    draw.rounded_rectangle([510, 85, 1230, 645], radius=20,
                          fill=(*COLORS['shadow'][:3], 120))
    # Main panel
    draw.rounded_rectangle([500, 80, 1220, 640], radius=20,
                          fill=(*COLORS['bg_dark'][:3], 230),
                          outline=(*COLORS['primary'][:3], 150), width=2)
    # Highlight edge
    draw.arc([500, 80, 1220, 640], start=180, end=270,
             fill=COLORS['accent'], width=2)
    
    # Title with word wrap
    words = title.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        bbox = draw.textbbox((0, 0), test_line, font=fonts['thumbnail_title'])
        if bbox[2] - bbox[0] > 650:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
        else:
            current_line.append(word)
    if current_line:
        lines.append(' '.join(current_line))
    
    # Draw title with 3D effect
    title_y = 160 if len(lines) <= 2 else 130
    for i, line in enumerate(lines[:3]):
        draw_3d_text(draw, (540, title_y + i * 95), line, fonts['thumbnail_title'],
                     COLORS['text_white'], COLORS['shadow'], depth=4)
    
    # Subtitle
    sub_y = title_y + len(lines) * 95 + 20
    draw_3d_text(draw, (540, sub_y), subtitle, fonts['thumbnail_sub'],
                 COLORS['accent'], COLORS['shadow'], depth=2)
    
    # Bottom accent bar with 3D effect
    for i in range(3):
        draw.rectangle([520 + i*2, 598 + i*2, 1200 + i*2, 612 + i*2],
                      fill=(*COLORS['shadow'][:3], 100 - i*30))
    draw.rectangle([520, 598, 1200, 612], fill=COLORS['primary'])
    draw.rectangle([520, 598, 1200, 602], fill=COLORS['secondary'])  # Highlight
    
    # Badge with 3D effect
    bbox = draw.textbbox((0, 0), badge_text, font=fonts['small'])
    badge_width = bbox[2] - bbox[0] + 30
    
    # Badge shadow
    draw.rounded_rectangle([1220 - badge_width + 3, 103, 1223, 150],
                          radius=10, fill=COLORS['shadow'])
    # Badge main
    draw.rounded_rectangle([1220 - badge_width, 100, 1220, 147],
                          radius=10, fill=COLORS['primary'])
    # Badge highlight
    draw.rounded_rectangle([1220 - badge_width, 100, 1220, 110],
                          radius=10, fill=(*COLORS['secondary'][:3], 150))
    
    draw.text((1220 - badge_width + 15, 108), badge_text, font=fonts['small'],
             fill=COLORS['text_white'])
    
    # Left decorative 3D brackets
    for i in range(3):
        offset = i * 2
        alpha = 255 - i * 60
        draw.line([(50 + offset, 100), (50 + offset, 250)],
                 fill=(*COLORS['primary'][:3], alpha), width=4)
        draw.line([(50, 100 + offset), (130, 100 + offset)],
                 fill=(*COLORS['primary'][:3], alpha), width=4)
        draw.line([(50 + offset, 620), (50 + offset, 470)],
                 fill=(*COLORS['secondary'][:3], alpha), width=4)
        draw.line([(50, 620 - offset), (130, 620 - offset)],
                 fill=(*COLORS['secondary'][:3], alpha), width=4)
    
    thumb = thumb.convert('RGB')
    output_name = f"youtube_thumbnail_{filename_suffix}.png"
    thumb.save(output_name, "PNG", quality=95)
    print(f"[OK] Thumbnail created: {output_name} (1280x720)")
    return thumb

def main():
    print("=" * 65)
    print("  VISWA AI AGENTS - YouTube Assets Generator V2")
    print("  Theme: Red & Orange (Energetic) with 3D Depth Effects")
    print("=" * 65)
    print()
    
    fonts = get_fonts()
    
    print("Creating assets with 3D effects...\n")
    
    # 1. Banner
    create_banner(fonts)
    
    # 2. Profile Picture
    create_profile_picture(fonts)
    
    # 3. Thumbnail Templates
    thumbnails = [
        ("N8N AI Agents", "Complete Beginner Guide", "TUTORIAL", "n8n_tutorial"),
        ("ChatGPT API", "Build Your First Agent", "TUTORIAL", "chatgpt_api"),
        ("Business Automation", "AI Tools for Productivity", "GUIDE", "business_automation"),
        ("Claude API Tutorial", "Advanced AI Agents", "ADVANCED", "claude_api"),
        ("Cursor AI", "Coding with AI Agents", "NEW", "cursor_ai"),
        ("Agentic AI", "Build Autonomous Systems", "DEEP DIVE", "agentic_ai"),
    ]
    
    for title, subtitle, badge, suffix in thumbnails:
        create_thumbnail(fonts, title, subtitle, badge, suffix)
    
    print()
    print("=" * 65)
    print("  All assets created successfully with 3D effects!")
    print("=" * 65)
    print()
    print("FILES CREATED:")
    print("-" * 50)
    
    files = [
        ("youtube_banner_viswa_ai_agents.png", "2560x1440", "Channel Banner"),
        ("youtube_profile_viswa_ai.png", "800x800", "Profile Picture"),
        ("youtube_thumbnail_n8n_tutorial.png", "1280x720", "N8N Tutorial"),
        ("youtube_thumbnail_chatgpt_api.png", "1280x720", "ChatGPT API"),
        ("youtube_thumbnail_business_automation.png", "1280x720", "Business Automation"),
        ("youtube_thumbnail_claude_api.png", "1280x720", "Claude API"),
        ("youtube_thumbnail_cursor_ai.png", "1280x720", "Cursor AI (NEW)"),
        ("youtube_thumbnail_agentic_ai.png", "1280x720", "Agentic AI"),
    ]
    
    for filename, dimensions, description in files:
        if os.path.exists(filename):
            size_kb = os.path.getsize(filename) / 1024
            print(f"  {filename}")
            print(f"    -> {dimensions} | {size_kb:.0f} KB | {description}")
    
    print()
    print("UPDATED BRANDING:")
    print("-" * 50)
    print("  Colors: Red & Orange (Energetic)")
    print("  Subtitle: Building Practical AI Agents")
    print("  Tagline: Agentic AI * Automation * Autonomous Systems")
    print("  Style: 3D depth effects with perspective grid")
    print()

if __name__ == "__main__":
    main()
