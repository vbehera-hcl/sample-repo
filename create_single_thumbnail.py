"""Create a single thumbnail for AI's Architectural Blueprints"""
from create_youtube_assets_v2 import get_fonts, create_thumbnail

fonts = get_fonts()
create_thumbnail(
    fonts, 
    "AI Architectural Blueprints", 
    "Design Patterns for AI Agents", 
    "DEEP DIVE", 
    "ai_blueprints"
)
print("Thumbnail created successfully!")
