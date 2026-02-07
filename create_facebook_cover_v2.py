"""
Facebook Cover Photo V2 - Robot Minimal Design
Clean design with robot/AI face icon, content on right side
Theme: Red & Orange (Energetic)
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

# Brand Colors
COLORS = {
    'bg_dark': (12, 8, 18),
    'bg_medium': (25, 15, 30),
    'primary': (255, 80, 50),
    'secondary': (255, 140, 50),
    'accent': (255, 200, 100),
    'highlight': (255, 100, 80),
    'glow': (255, 120, 60),
    'text_white': (255, 255, 255),
    'text_light': (255, 230, 220),
    'text_muted': (180, 160, 155),
    'shadow': (8, 4, 12),
}

def get_fonts():
    """Load fonts."""
    fonts = {}
    try:
        fonts['title'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 58)
        fonts['subtitle'] = ImageFont.truetype("C:/Windows/Fonts/seguibold.ttf", 26)
        fonts['tagline'] = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 20)
        fonts['small'] = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    except:
        try:
            fonts['title'] = ImageFont.truetype("arial.ttf", 58)
            fonts['subtitle'] = ImageFont.truetype("arial.ttf", 26)
            fonts['tagline'] = ImageFont.truetype("arial.ttf", 20)
            fonts['small'] = ImageFont.truetype("arial.ttf", 16)
        except:
            default = ImageFont.load_default()
            fonts = {k: default for k in ['title', 'subtitle', 'tagline', 'small']}
    return fonts

def draw_clean_gradient(width, height):
    """Create a clean, subtle gradient background."""
    img = Image.new('RGB', (width, height), COLORS['bg_dark'])
    draw = ImageDraw.Draw(img)
    
    # Subtle horizontal gradient
    for x in range(width):
        ratio = x / width
        r = int(COLORS['bg_dark'][0] + (COLORS['bg_medium'][0] - COLORS['bg_dark'][0]) * ratio * 0.5)
        g = int(COLORS['bg_dark'][1] + (COLORS['bg_medium'][1] - COLORS['bg_dark'][1]) * ratio * 0.5)
        b = int(COLORS['bg_dark'][2] + (COLORS['bg_medium'][2] - COLORS['bg_dark'][2]) * ratio * 0.5)
        draw.line([(x, 0), (x, height)], fill=(r, g, b))
    
    return img

def draw_subtle_grid(draw, width, height, color, alpha=20):
    """Draw a very subtle grid pattern."""
    spacing = 40
    for x in range(0, width, spacing):
        draw.line([(x, 0), (x, height)], fill=(*color[:3], alpha), width=1)
    for y in range(0, height, spacing):
        draw.line([(0, y), (width, y)], fill=(*color[:3], alpha), width=1)

def draw_robot_face(draw, center_x, center_y, size):
    """Draw a minimal, modern robot/AI face icon."""
    # Outer glow
    for i in range(8, 0, -1):
        glow_size = size + i * 8
        alpha = int(15 * i / 8)
        draw.rounded_rectangle(
            [center_x - glow_size, center_y - glow_size,
             center_x + glow_size, center_y + glow_size],
            radius=glow_size // 3,
            fill=(*COLORS['glow'][:3], alpha)
        )
    
    # Head - rounded square
    head_size = size
    draw.rounded_rectangle(
        [center_x - head_size, center_y - head_size,
         center_x + head_size, center_y + head_size],
        radius=head_size // 3,
        fill=COLORS['bg_dark'],
        outline=COLORS['primary'],
        width=4
    )
    
    # Inner frame
    inner_size = head_size - 12
    draw.rounded_rectangle(
        [center_x - inner_size, center_y - inner_size,
         center_x + inner_size, center_y + inner_size],
        radius=inner_size // 4,
        outline=(*COLORS['secondary'][:3], 150),
        width=2
    )
    
    # Eyes - glowing circles
    eye_offset_x = head_size * 0.4
    eye_offset_y = head_size * 0.15
    eye_size = head_size * 0.22
    
    for eye_x in [center_x - eye_offset_x, center_x + eye_offset_x]:
        eye_y = center_y - eye_offset_y
        
        # Eye glow
        for i in range(4, 0, -1):
            glow_r = eye_size + i * 4
            alpha = int(40 * i / 4)
            draw.ellipse(
                [eye_x - glow_r, eye_y - glow_r,
                 eye_x + glow_r, eye_y + glow_r],
                fill=(*COLORS['accent'][:3], alpha)
            )
        
        # Eye outer
        draw.ellipse(
            [eye_x - eye_size, eye_y - eye_size,
             eye_x + eye_size, eye_y + eye_size],
            fill=COLORS['primary'],
            outline=COLORS['accent'],
            width=2
        )
        
        # Eye inner (pupil)
        pupil_size = eye_size * 0.5
        draw.ellipse(
            [eye_x - pupil_size, eye_y - pupil_size,
             eye_x + pupil_size, eye_y + pupil_size],
            fill=COLORS['text_white']
        )
    
    # Mouth - horizontal line with slight curve effect
    mouth_y = center_y + head_size * 0.45
    mouth_width = head_size * 0.5
    
    # Mouth glow
    draw.line(
        [(center_x - mouth_width, mouth_y),
         (center_x + mouth_width, mouth_y)],
        fill=COLORS['secondary'],
        width=4
    )
    
    # Mouth segments (gives it a digital look)
    segment_width = mouth_width * 2 / 5
    for i in range(5):
        seg_x = center_x - mouth_width + i * segment_width + segment_width / 2
        if i % 2 == 0:
            draw.ellipse(
                [seg_x - 3, mouth_y - 3, seg_x + 3, mouth_y + 3],
                fill=COLORS['accent']
            )
    
    # Antenna
    antenna_base_y = center_y - head_size
    antenna_top_y = antenna_base_y - head_size * 0.4
    
    # Antenna stem
    draw.line(
        [(center_x, antenna_base_y), (center_x, antenna_top_y)],
        fill=COLORS['primary'],
        width=3
    )
    
    # Antenna ball with glow
    antenna_ball_size = 8
    for i in range(3, 0, -1):
        glow_r = antenna_ball_size + i * 4
        alpha = int(50 * i / 3)
        draw.ellipse(
            [center_x - glow_r, antenna_top_y - glow_r,
             center_x + glow_r, antenna_top_y + glow_r],
            fill=(*COLORS['accent'][:3], alpha)
        )
    draw.ellipse(
        [center_x - antenna_ball_size, antenna_top_y - antenna_ball_size,
         center_x + antenna_ball_size, antenna_top_y + antenna_ball_size],
        fill=COLORS['accent']
    )
    
    # Side antennas / ears
    ear_size = head_size * 0.15
    ear_offset = head_size + 8
    
    for ear_x in [center_x - ear_offset, center_x + ear_offset]:
        draw.rounded_rectangle(
            [ear_x - ear_size//2, center_y - ear_size,
             ear_x + ear_size//2, center_y + ear_size],
            radius=4,
            fill=COLORS['primary'],
            outline=COLORS['secondary'],
            width=2
        )

def draw_accent_lines(draw, width, height):
    """Draw decorative accent lines."""
    # Top accent line
    draw.line([(350, 30), (width - 30, 30)], fill=COLORS['primary'], width=2)
    draw.line([(350, 30), (350, 50)], fill=COLORS['primary'], width=2)
    
    # Bottom accent line
    draw.line([(350, height - 30), (width - 30, height - 30)], 
              fill=COLORS['secondary'], width=2)
    draw.line([(width - 30, height - 30), (width - 30, height - 50)], 
              fill=COLORS['secondary'], width=2)
    
    # Decorative dots
    dot_y = height - 30
    for i, x in enumerate(range(380, 500, 25)):
        alpha = 255 - i * 40
        if alpha > 0:
            draw.ellipse([x-3, dot_y-3, x+3, dot_y+3], 
                        fill=(*COLORS['accent'][:3], alpha))

def create_facebook_cover_v2():
    """Create Facebook cover with robot minimal design."""
    width, height = 820, 312
    
    # Create clean gradient background
    cover = draw_clean_gradient(width, height)
    cover = cover.convert('RGBA')
    draw = ImageDraw.Draw(cover, 'RGBA')
    
    fonts = get_fonts()
    
    # Subtle grid pattern
    draw_subtle_grid(draw, width, height, COLORS['primary'], alpha=15)
    
    # Draw robot face on left side (accounting for profile pic area)
    # Profile pic typically covers left side, so robot goes slightly right of center-left
    robot_x = 180
    robot_y = height // 2
    draw_robot_face(draw, robot_x, robot_y, 70)
    
    # Content on right side
    content_x = 340
    
    # Main title
    title = "VISWA AI AGENTS"
    title_y = 70
    
    # Title shadow
    draw.text((content_x + 2, title_y + 2), title, font=fonts['title'],
              fill=(*COLORS['shadow'][:3], 150))
    draw.text((content_x, title_y), title, font=fonts['title'],
              fill=COLORS['text_white'])
    
    # Subtitle with accent bar
    subtitle = "Building Practical AI Agents"
    subtitle_y = title_y + 70
    
    bbox = draw.textbbox((0, 0), subtitle, font=fonts['subtitle'])
    subtitle_width = bbox[2] - bbox[0]
    
    # Accent bar behind subtitle
    draw.rounded_rectangle(
        [content_x - 10, subtitle_y - 4, 
         content_x + subtitle_width + 10, subtitle_y + 32],
        radius=6,
        fill=(*COLORS['primary'][:3], 40),
        outline=(*COLORS['secondary'][:3], 100)
    )
    
    draw.text((content_x, subtitle_y), subtitle, font=fonts['subtitle'],
              fill=COLORS['accent'])
    
    # Tagline
    tagline = "Agentic AI  |  Automation  |  Autonomous Systems"
    tagline_y = subtitle_y + 50
    draw.text((content_x, tagline_y), tagline, font=fonts['tagline'],
              fill=COLORS['text_light'])
    
    # Topics
    topics = "N8N  *  ChatGPT  *  Claude  *  Cursor AI"
    topics_y = tagline_y + 35
    draw.text((content_x, topics_y), topics, font=fonts['small'],
              fill=COLORS['text_muted'])
    
    # Accent lines
    draw_accent_lines(draw, width, height)
    
    # Small decorative elements on right
    # Floating dots
    for i, (x, y) in enumerate([(750, 80), (780, 120), (760, 160)]):
        size = 4 - i
        alpha = 200 - i * 50
        draw.ellipse([x-size, y-size, x+size, y+size],
                    fill=(*COLORS['accent'][:3], alpha))
    
    # Save
    cover = cover.convert('RGB')
    cover.save("facebook_cover_viswa_ai.png", "PNG", quality=95)
    
    file_size = os.path.getsize("facebook_cover_viswa_ai.png") / 1024
    print(f"[OK] Facebook cover created: facebook_cover_viswa_ai.png")
    print(f"     Design: Robot Minimal with content on right")
    print(f"     Dimensions: {width}x{height} pixels")
    print(f"     File size: {file_size:.0f} KB")
    print()
    print("DESIGN FEATURES:")
    print("-" * 45)
    print("  - Clean minimal robot/AI face icon")
    print("  - Glowing eyes and antenna")
    print("  - Content positioned on right side")
    print("  - Subtle grid background")
    print("  - Accent lines and decorative elements")
    print()
    print("UPLOAD: Facebook Page/Profile > Cover Photo > Upload")
    
    return cover

if __name__ == "__main__":
    create_facebook_cover_v2()
