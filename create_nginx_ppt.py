"""
Script to create a professionally designed PowerPoint presentation 
for Nautilus EC2 Web Server Setup
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Color Scheme - Modern Blue Theme
PRIMARY_DARK = RGBColor(0, 51, 102)      # Dark Blue
PRIMARY_LIGHT = RGBColor(0, 120, 215)    # Light Blue
ACCENT_COLOR = RGBColor(255, 152, 0)     # Orange Accent
WHITE = RGBColor(255, 255, 255)
LIGHT_GRAY = RGBColor(245, 245, 245)
DARK_GRAY = RGBColor(60, 60, 60)
CODE_GREEN = RGBColor(0, 128, 64)

def add_header_bar(slide, prs):
    """Add a colored header bar at the top"""
    header = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        prs.slide_width, Inches(1.0)
    )
    header.fill.solid()
    header.fill.fore_color.rgb = PRIMARY_DARK
    header.line.fill.background()
    return header

def add_footer_bar(slide, prs):
    """Add a colored footer bar at the bottom"""
    footer = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(6.8),
        prs.slide_width, Inches(0.7)
    )
    footer.fill.solid()
    footer.fill.fore_color.rgb = PRIMARY_LIGHT
    footer.line.fill.background()
    
    # Add footer text
    footer_text = slide.shapes.add_textbox(Inches(0.3), Inches(6.9), Inches(9), Inches(0.4))
    tf = footer_text.text_frame
    p = tf.paragraphs[0]
    p.text = "Nautilus DevOps Team | AWS Infrastructure Setup"
    p.font.size = Pt(10)
    p.font.color.rgb = WHITE
    p.font.bold = True
    return footer

def add_accent_line(slide, top):
    """Add an accent line under title"""
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0.5), Inches(top),
        Inches(2), Inches(0.08)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_COLOR
    line.line.fill.background()
    return line

def add_slide_number(slide, number, total):
    """Add slide number"""
    num_box = slide.shapes.add_textbox(Inches(9), Inches(6.9), Inches(0.8), Inches(0.4))
    tf = num_box.text_frame
    p = tf.paragraphs[0]
    p.text = f"{number}/{total}"
    p.font.size = Pt(10)
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.RIGHT

def add_title_slide(prs, title, subtitle):
    """Add a professionally designed title slide"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Full background gradient effect using shapes
    bg_top = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        prs.slide_width, Inches(4.5)
    )
    bg_top.fill.solid()
    bg_top.fill.fore_color.rgb = PRIMARY_DARK
    bg_top.line.fill.background()
    
    bg_bottom = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(4.5),
        prs.slide_width, Inches(3)
    )
    bg_bottom.fill.solid()
    bg_bottom.fill.fore_color.rgb = PRIMARY_LIGHT
    bg_bottom.line.fill.background()
    
    # Add decorative accent bar
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(4.3),
        prs.slide_width, Inches(0.2)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = ACCENT_COLOR
    accent.line.fill.background()
    
    # AWS/Cloud icon placeholder (circle)
    icon_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(4.25), Inches(0.8),
        Inches(1.5), Inches(1.5)
    )
    icon_circle.fill.solid()
    icon_circle.fill.fore_color.rgb = ACCENT_COLOR
    icon_circle.line.fill.background()
    
    # Icon text (AWS)
    icon_text = slide.shapes.add_textbox(Inches(4.25), Inches(1.2), Inches(1.5), Inches(0.7))
    tf = icon_text.text_frame
    p = tf.paragraphs[0]
    p.text = "AWS"
    p.font.size = Pt(24)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(2.6), Inches(9), Inches(1.2))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(40)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # Subtitle
    subtitle_box = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(1.5))
    tf = subtitle_box.text_frame
    tf.word_wrap = True
    for i, line in enumerate(subtitle.split('\n')):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = line
        p.font.size = Pt(20)
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER
        p.space_after = Pt(8)
    
    return slide

def add_content_slide(prs, title, bullet_points, code_block=None, slide_num=1, total_slides=11):
    """Add a professionally designed content slide"""
    slide_layout = prs.slide_layouts[6]  # Blank layout
    slide = prs.slides.add_slide(slide_layout)
    
    # Add header and footer
    add_header_bar(slide, prs)
    add_footer_bar(slide, prs)
    add_slide_number(slide, slide_num, total_slides)
    
    # Add title on header
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(0.25), Inches(9), Inches(0.6))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = WHITE
    
    # Add accent line under header
    add_accent_line(slide, 1.1)
    
    # Add bullet points
    content_top = 1.3
    if bullet_points:
        content_box = slide.shapes.add_textbox(Inches(0.5), Inches(content_top), Inches(9), Inches(2.8))
        tf = content_box.text_frame
        tf.word_wrap = True
        
        for i, point in enumerate(bullet_points):
            if i == 0:
                p = tf.paragraphs[0]
            else:
                p = tf.add_paragraph()
            
            # Add bullet icon
            run = p.add_run()
            run.text = "▸ "
            run.font.size = Pt(16)
            run.font.color.rgb = ACCENT_COLOR
            run.font.bold = True
            
            run2 = p.add_run()
            run2.text = point
            run2.font.size = Pt(16)
            run2.font.color.rgb = DARK_GRAY
            
            p.space_after = Pt(10)
        
        content_top = 4.0 if len(bullet_points) > 3 else 3.5
    
    # Add code block if provided
    if code_block:
        # Code container background
        code_bg = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(0.3), Inches(content_top),
            Inches(9.4), Inches(2.5)
        )
        code_bg.fill.solid()
        code_bg.fill.fore_color.rgb = RGBColor(40, 44, 52)  # Dark code background
        code_bg.line.color.rgb = PRIMARY_LIGHT
        code_bg.line.width = Pt(2)
        
        # Code header
        code_header = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE,
            Inches(0.3), Inches(content_top),
            Inches(9.4), Inches(0.35)
        )
        code_header.fill.solid()
        code_header.fill.fore_color.rgb = RGBColor(30, 34, 42)
        code_header.line.fill.background()
        
        # Terminal dots
        for j, color in enumerate([RGBColor(255, 95, 86), RGBColor(255, 189, 46), RGBColor(39, 201, 63)]):
            dot = slide.shapes.add_shape(
                MSO_SHAPE.OVAL,
                Inches(0.45 + j * 0.25), Inches(content_top + 0.1),
                Inches(0.15), Inches(0.15)
            )
            dot.fill.solid()
            dot.fill.fore_color.rgb = color
            dot.line.fill.background()
        
        # Code text
        code_box = slide.shapes.add_textbox(Inches(0.5), Inches(content_top + 0.4), Inches(9), Inches(2))
        tf = code_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = code_block
        p.font.size = Pt(10)
        p.font.name = "Consolas"
        p.font.color.rgb = RGBColor(171, 178, 191)  # Light gray code text
    
    return slide

def add_section_slide(prs, title, subtitle, slide_num, total_slides):
    """Add a section divider slide"""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    
    # Background
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(0), Inches(0),
        prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = PRIMARY_DARK
    bg.line.fill.background()
    
    # Accent circle
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(4), Inches(1.5),
        Inches(2), Inches(2)
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = ACCENT_COLOR
    circle.line.fill.background()
    
    # Step number
    num_box = slide.shapes.add_textbox(Inches(4), Inches(1.9), Inches(2), Inches(1))
    tf = num_box.text_frame
    p = tf.paragraphs[0]
    p.text = str(slide_num - 3)  # Adjust for section number
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # Title
    title_box = slide.shapes.add_textbox(Inches(0.5), Inches(4), Inches(9), Inches(1))
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER
    
    # Subtitle
    sub_box = slide.shapes.add_textbox(Inches(0.5), Inches(5), Inches(9), Inches(0.8))
    tf = sub_box.text_frame
    p = tf.paragraphs[0]
    p.text = subtitle
    p.font.size = Pt(18)
    p.font.color.rgb = RGBColor(180, 200, 220)
    p.alignment = PP_ALIGN.CENTER
    
    # Slide number
    add_slide_number(slide, slide_num, total_slides)
    
    return slide

def create_presentation():
    """Create the PowerPoint presentation with professional design"""
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)
    
    total_slides = 11
    
    # Slide 1: Title Slide
    add_title_slide(
        prs,
        "Nautilus EC2 Web Server Setup",
        "AWS CLI Commands for Nginx Deployment\nNautilus DevOps Team"
    )
    
    # Slide 2: Overview
    add_content_slide(
        prs,
        "Project Overview",
        [
            "Create an EC2 instance to serve as a web server for Nautilus project",
            "Instance Name: nautilus-ec2",
            "Web Server: Nginx - High-performance HTTP server",
            "AMI: Ubuntu 22.04 LTS - Stable and well-supported",
            "Security: HTTP traffic allowed on port 80 from internet",
            "Automation: User data script for automatic Nginx installation"
        ],
        slide_num=2,
        total_slides=total_slides
    )
    
    # Slide 3: Architecture
    add_content_slide(
        prs,
        "Infrastructure Components",
        [
            "EC2 Instance (t2.micro) - Cost-effective for initial setup",
            "Ubuntu 22.04 LTS AMI - Long-term support with latest security patches",
            "Security Group (nautilus-web-sg) - Controls inbound/outbound traffic",
            "Nginx Web Server - Lightweight, high-performance HTTP server",
            "User Data Script - Automates server configuration on launch"
        ],
        slide_num=3,
        total_slides=total_slides
    )
    
    # Slide 4: Step 1 - Security Group
    add_content_slide(
        prs,
        "Step 1: Create Security Group",
        [
            "Create a security group to control network access",
            "Group Name: nautilus-web-sg"
        ],
        code_block='''aws ec2 create-security-group \\
    --group-name nautilus-web-sg \\
    --description "Security group for Nautilus web server"''',
        slide_num=4,
        total_slides=total_slides
    )
    
    # Slide 5: Step 2 - Security Group Rules
    add_content_slide(
        prs,
        "Step 2: Configure Inbound Rules",
        [
            "Allow HTTP traffic on port 80 from the internet",
            "CIDR 0.0.0.0/0 allows access from any IP address"
        ],
        code_block='''aws ec2 authorize-security-group-ingress \\
    --group-name nautilus-web-sg \\
    --protocol tcp \\
    --port 80 \\
    --cidr 0.0.0.0/0''',
        slide_num=5,
        total_slides=total_slides
    )
    
    # Slide 6: Step 3 - Launch EC2 Instance
    add_content_slide(
        prs,
        "Step 3: Launch EC2 Instance",
        [
            "Launch Ubuntu EC2 instance with Nginx user data script",
            "Instance tagged as 'nautilus-ec2' for easy identification"
        ],
        code_block='''aws ec2 run-instances \\
    --image-id ami-0c7217cdde317cfec \\
    --instance-type t2.micro \\
    --security-groups nautilus-web-sg \\
    --tag-specifications 'ResourceType=instance,
        Tags=[{Key=Name,Value=nautilus-ec2}]' \\
    --user-data '#!/bin/bash
        apt-get update -y && apt-get install -y nginx
        systemctl start nginx && systemctl enable nginx' \\
    --count 1''',
        slide_num=6,
        total_slides=total_slides
    )
    
    # Slide 7: User Data Script
    add_content_slide(
        prs,
        "User Data Script Breakdown",
        [
            "#!/bin/bash - Specifies bash shell interpreter",
            "apt-get update -y - Updates package repository index",
            "apt-get install -y nginx - Installs Nginx web server package",
            "systemctl start nginx - Starts the Nginx service immediately",
            "systemctl enable nginx - Enables Nginx to start on system boot"
        ],
        slide_num=7,
        total_slides=total_slides
    )
    
    # Slide 8: Verification
    add_content_slide(
        prs,
        "Verification & Testing",
        [
            "Check instance status and retrieve public IP address",
            "Access Nginx default page via web browser"
        ],
        code_block='''# Verify instance is running
aws ec2 describe-instances \\
    --filters "Name=tag:Name,Values=nautilus-ec2" \\
    --query 'Reservations[*].Instances[*].
        [InstanceId,State.Name,PublicIpAddress]' \\
    --output table

# Access in browser: http://<public-ip-address>''',
        slide_num=8,
        total_slides=total_slides
    )
    
    # Slide 9: Important Notes
    add_content_slide(
        prs,
        "Important Notes",
        [
            "Ensure AWS CLI is configured with proper credentials (aws configure)",
            "Replace AMI ID with appropriate one for your AWS region",
            "For VPC setup: use --vpc-id and --subnet-id parameters",
            "Use --security-group-ids instead of --security-groups in VPC",
            "Instance may take 2-3 minutes to be fully accessible after launch"
        ],
        slide_num=9,
        total_slides=total_slides
    )
    
    # Slide 10: Finding Ubuntu AMIs
    add_content_slide(
        prs,
        "Finding Ubuntu AMIs",
        [
            "Use AWS CLI to find the latest Ubuntu AMI for your region",
            "Canonical (099720109477) is the official Ubuntu publisher"
        ],
        code_block='''aws ec2 describe-images \\
    --owners 099720109477 \\
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/
        ubuntu-jammy-22.04-amd64-server-*" \\
    --query 'Images[*].[ImageId,Name]' \\
    --output table''',
        slide_num=10,
        total_slides=total_slides
    )
    
    # Slide 11: Summary
    add_content_slide(
        prs,
        "Summary",
        [
            "Created security group allowing HTTP traffic on port 80",
            "Launched Ubuntu EC2 instance named 'nautilus-ec2'",
            "Automated Nginx installation via user data script",
            "Web server accessible from the internet immediately",
            "Ready for Nautilus project deployment phase"
        ],
        slide_num=11,
        total_slides=total_slides
    )
    
    # Save the presentation
    output_path = "Nautilus_EC2_Nginx_Setup_v2.pptx"
    prs.save(output_path)
    print(f"Presentation saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    create_presentation()
