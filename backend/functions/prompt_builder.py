"""
Prompt Builder for Timetable Wallpaper Generation

Constructs prompts for Imagen 3 to generate timetable wallpapers
with different design styles and themes.
"""

from typing import Literal

DesignStyleType = Literal["minimal", "gradient", "neon", "pastel", "glass", "retro"]
ThemeType = Literal["light", "dark"]


# Style descriptions for each design style
STYLE_DESCRIPTIONS = {
    "minimal": {
        "light": """
- Background: Clean white or very light gray with subtle gradient
- Color palette: Muted pastels or monochromatic grays (2-3 colors maximum)
- Typography: Clean sans-serif fonts (similar to Inter, SF Pro, or Helvetica)
- Class blocks: Simple rectangles with thin dark borders or subtle shadows
- No decorative elements, icons, or illustrations
- High contrast dark text on light blocks
- Professional, clean, paper-like appearance
- Emphasis on negative space and minimalism
""",
        "dark": """
- Background: Deep charcoal, dark navy, or near-black
- Color palette: Muted dark tones with subtle accent colors
- Typography: Clean sans-serif fonts in white or light gray
- Class blocks: Dark rectangles with subtle lighter borders or soft glow
- No decorative elements, icons, or illustrations
- High contrast light text on dark blocks
- Sleek, modern, OLED-friendly appearance
- Emphasis on negative space and minimalism
"""
    },
    "gradient": {
        "light": """
- Background: Smooth gradient blend of soft pastels (pink to lavender, peach to mint)
- Color palette: Flowing gradients with harmonious color transitions
- Typography: Modern sans-serif fonts with subtle gradient fills
- Class blocks: Rounded rectangles with horizontal or diagonal gradient fills
- Smooth color transitions between elements
- Contemporary, elegant, flowing aesthetic
- Each module has its own unique gradient color scheme
""",
        "dark": """
- Background: Deep gradient from dark purple to midnight blue or charcoal to deep teal
- Color palette: Rich, saturated gradients in jewel tones
- Typography: Clean fonts in white or light colors with subtle glow
- Class blocks: Rounded rectangles with vibrant gradient fills on dark backgrounds
- Smooth color transitions with depth
- Modern, sophisticated night-sky aesthetic
- Each module has its own unique bold gradient
"""
    },
    "neon": {
        "light": """
- Background: White or very light gray with electric accent colors
- Color palette: Bright neon colors (electric pink, lime green, cyan, yellow)
- Typography: Bold, geometric fonts with neon-colored text
- Class blocks: White rectangles with bright neon borders and subtle glow effects
- Energetic, vibrant, electric aesthetic
- High contrast with pop of neon colors
- Modern, youthful, cyberpunk-lite style
""",
        "dark": """
- Background: Pure black or very dark navy
- Color palette: Glowing neon colors (hot pink, electric blue, lime, orange)
- Typography: Bold fonts with neon glow effect
- Class blocks: Dark rectangles with bright glowing neon borders
- Strong neon glow effects around all elements
- Cyberpunk aesthetic with OLED-friendly true blacks
- Each module has its own unique neon color
- Futuristic, electric, nightclub vibe
"""
    },
    "pastel": {
        "light": """
- Background: Cream, light beige, or soft blush with decorative corner elements
- Color palette: Soft pastels (baby pink, mint, lavender, peach, sky blue, soft yellow)
- Typography: Rounded, friendly fonts in darker complementary shades
- Class blocks: Rounded rectangles with soft pastel fills and gentle shadows
- Small kawaii-style decorative elements: tiny books, coffee cups, stars, clouds
- Each module block can have a small cute emoji or icon
- Warm, cozy, inviting aesthetic
- Hand-drawn style accents and soft textures
""",
        "dark": """
- Background: Deep purple, midnight blue, or soft charcoal with stars/sparkles
- Color palette: Darker pastels and dusty tones (dusty pink, teal, muted lavender)
- Typography: Rounded, friendly fonts in cream or light colors
- Class blocks: Rounded rectangles with muted pastel fills and soft glow
- Small kawaii-style decorative elements: moons, stars, sparkles
- Cozy, dreamy, nighttime aesthetic
- Each module has a soft glowing pastel color
"""
    },
    "glass": {
        "light": """
- Background: Soft gradient with frosted glass effect (light blue to pink or white to lavender)
- Color palette: Translucent whites and soft colors with glass reflections
- Typography: Clean sans-serif fonts with subtle shadow depth
- Class blocks: Frosted glass rectangles with white/translucent fill and blur effect
- Glassmorphism style with backdrop blur appearance
- Subtle shadows and highlights for 3D depth
- Modern iOS-inspired aesthetic
- Light refractions and glass highlights
""",
        "dark": """
- Background: Deep gradient with frosted glass panels (dark purple to black)
- Color palette: Translucent dark colors with subtle color tints
- Typography: Clean fonts in white with glass-on-dark effect
- Class blocks: Dark frosted glass rectangles with subtle transparency
- Glassmorphism on dark mode with subtle glows
- Modern, premium, sophisticated aesthetic
- Each module has subtle colored glass tint
- Apple-style frosted glass on dark backgrounds
"""
    },
    "retro": {
        "light": """
- Background: Warm cream, off-white, or vintage paper texture
- Color palette: Retro 70s/80s colors (mustard, burnt orange, olive green, rusty red)
- Typography: Groovy, rounded retro fonts or classic serif fonts
- Class blocks: Rectangles with vintage color fills and aged paper texture
- Retro grid lines or sunburst patterns in background
- Nostalgic, warm, vintage aesthetic
- Slight grain or texture overlay for aged look
- Mid-century modern or 80s Memphis style influences
""",
        "dark": """
- Background: Deep brown, vintage navy, or maroon with subtle texture
- Color palette: Dark retro tones (deep teal, burgundy, forest green, mustard)
- Typography: Classic serif or retro fonts in cream/gold colors
- Class blocks: Dark vintage colored rectangles with subtle worn texture
- Art deco or vintage gothic influences
- Nostalgic, moody, evening aesthetic
- Film grain or noise texture overlay
- Classic poster or vinyl record cover style
"""
    }
}


PROMPT_TEMPLATE = """Generate a {style_name} horizontal phone wallpaper featuring a weekly class timetable.

## Timetable Data
{timetable_grid}

## Design Requirements
- Orientation: HORIZONTAL (landscape mode)
- Aspect ratio: {aspect_ratio}
- Resolution: High quality, suitable for phone wallpaper
- Grid layout: 5 columns (Mon, Tue, Wed, Thu, Fri) with hourly time rows
- Each class block displays: Module Code, Lesson Type (abbreviated), Venue
- Include a title header like "My Semester Timetable" or "Weekly Schedule"

## Style: {style_name}
{style_description}

## Layout Constraints (iPhone Safe Zones)
- Leave margins on all edges for iPhone UI elements
- Top-center area should be minimal (Dynamic Island safe zone)
- Use legible fonts with strong contrast against background
- Color-code classes by module for easy identification
- Days of week clearly labeled at top of each column
- Time slots clearly labeled on left side

## Content Rules
- DO NOT include exam dates or schedules
- DO NOT include week numbers inside class blocks
- DO NOT add any text outside the timetable except the title
- Keep class block text minimal: just module code, type, and venue
- Empty time slots should be visually distinct but not distracting
"""


def build_prompt(
    timetable_grid: str,
    design_style: DesignStyleType = "minimal",
    theme: ThemeType = "light",
    aspect_ratio: str = "16:9"
) -> str:
    """
    Build the full prompt for image generation.
    
    Args:
        timetable_grid: Markdown table of the timetable
        design_style: One of "minimal", "gradient", "neon", "pastel", "glass", "retro"
        theme: Either "light" or "dark"
        aspect_ratio: Aspect ratio string (e.g., "16:9", "19.5:9")
    
    Returns:
        Complete prompt string for Imagen 3
    """
    # Get style description for the combination
    style_desc = STYLE_DESCRIPTIONS.get(design_style, STYLE_DESCRIPTIONS["minimal"])
    style_description = style_desc.get(theme, style_desc["light"])
    
    # Build style name
    style_name = f"{design_style.capitalize()} ({theme} mode)"
    
    return PROMPT_TEMPLATE.format(
        style_name=style_name,
        timetable_grid=timetable_grid,
        style_description=style_description,
        aspect_ratio=aspect_ratio
    )
