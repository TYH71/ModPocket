"""
Prompt Builder for Timetable Wallpaper Generation

Constructs optimized text-to-image prompts for Imagen 4.0 Ultra to generate 
NUSMods timetable phone wallpapers with iPhone-specific layout constraints.
"""

from typing import Literal, Dict, List, Any, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

DesignStyleType = Literal[
    "minimalist", "gradient", "neon", "pastel", "glass", "retro", "kawaii"
]
ThemeType = Literal["light", "dark"]

# ---------------------------------------------------------------------------
# OPTIMIZED PROMPT TEMPLATE (CONDENSED)
# ---------------------------------------------------------------------------
GENERATION_PROMPT_TEMPLATE = """iPhone {aspect_ratio} wallpaper. University timetable schedule.

CRITICAL LAYOUT:
- TOP 10%: Empty 
- BOTTOM 10%: Empty 
- MIDDLE: Schedule grid

{schedule_table}

STYLE: {style_name}
{style_description}

REQUIREMENTS: Grid layout, readable typography, color-coded modules, no device frames, no invented data
"""

# ---------------------------------------------------------------------------
# STYLE DESCRIPTIONS (CONDENSED)
# ---------------------------------------------------------------------------
STYLE_DESCRIPTIONS = {
    "minimalist": {
        "light": "White background, sans-serif font, soft color blocks, clean lines.",
        "dark": "Charcoal #1C1C1E background, white text, muted color blocks, OLED black.",
    },
    "gradient": {
        "light": "Pastel mesh gradient (peach/periwinkle), glass containers, dark text.",
        "dark": "Aurora gradient (violet/cyan/blue), translucent containers, white text.",
    },
    "neon": {
        "light": "White background, neon outlines (pink/blue), bold geometric type.",
        "dark": "Black background, glowing neon borders, cyberpunk HUD style.",
    },
    "pastel": {
        "light": "Cream background, marshmallow colors, rounded corners.",
        "dark": "Navy background, dusty pastels, soft rounded elements.",
    },
    "glass": {
        "light": "Blurred background, frosted glass cards, iOS style.",
        "dark": "Dark blur, smoked glass cards, subtle white borders.",
    },
    "retro": {
        "light": "Paper texture, 70s colors (mustard/orange), serif font.",
        "dark": "Grainy texture, synthwave colors, terminal font.",
    },
    "kawaii": {
        "light": "Pastel dots, handwriting font, sticky-note blocks, doodle decorations.",
        "dark": "Dark purple with stars, chalk-style blocks, cozy planner theme.",
    },
}

# ---------------------------------------------------------------------------
# DATA FORMATTING
# ---------------------------------------------------------------------------
def format_schedule_data(enriched_schedule: Any) -> str:
    """
    Format schedule into a structured Markdown representation for the prompt.
    """
    if not enriched_schedule:
        return "No classes scheduled."

    # Pre-processing: flatten list
    flat_lessons = []
    
    # Map abbreviated lesson types to readable full names (if not already done by parser)
    # But parser should have done it. We keep a fallback just in case.
    LESSON_SCOPES = {
        "LEC": "Lecture", "TUT": "Tutorial", "LAB": "Lab", 
        "SEC": "Sectional", "REC": "Recitation"
    }

    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for module_code, lessons in enriched_schedule.items():
        for lesson in lessons:
            day = lesson.get("day", "TBA")
            start = lesson.get("startTime", "0000")
            end = lesson.get("endTime", "0000")
            venue = lesson.get("venue", "TBA")
            l_type = lesson.get("lessonType", "Class")
            
            # Format Time
            if len(start) == 4: start = f"{start[:2]}:{start[2:]}"
            if len(end) == 4: end = f"{end[:2]}:{end[2:]}"
            
            # Shorten types for table compactness
            l_type_short = LESSON_SCOPES.get(l_type, l_type.split(" ")[0]) 

            flat_lessons.append({
                "Module": module_code,
                "Type": l_type,
                "Day": day,
                "Time": f"{start}-{end}",
                "Venue": venue
            })

    # Sort by Day then Time
    try:
        flat_lessons.sort(key=lambda x: (days_order.index(x["Day"]) if x["Day"] in days_order else 99, x["Time"]))
    except ValueError:
        pass # Fallback if random day string

    # Construct Markdown Table
    md_output = []
    current_day = ""
    
    for l in flat_lessons:
        # Group visually by Day in the text
        if l["Day"] != current_day:
            md_output.append(f"\n## {l['Day']}")
            current_day = l["Day"]
        
        # Format: - [CS1010] Lecture: 10:00-12:00 @ COM1
        md_output.append(f"- **{l['Module']}** ({l['Type']}): {l['Time']} @ {l['Venue']}")

    return "\n".join(md_output)

# ---------------------------------------------------------------------------
# BUILDER FUNCTION
# ---------------------------------------------------------------------------
def build_prompt(
    design_style: DesignStyleType = "minimalist",
    theme: ThemeType = "light",
    aspect_ratio: str = "9:16",
    enriched_schedule: Optional[Any] = None,
) -> str:
    """
    Build the text-to-image prompt.
    """
    # 1. Get Style Description
    style_category = STYLE_DESCRIPTIONS.get(design_style, STYLE_DESCRIPTIONS["minimalist"])
    style_desc = style_category.get(theme, style_category["light"])
    style_full_name = f"{design_style.capitalize()} ({theme.capitalize()} Mode)"

    # 2. Format Schedule
    schedule_table = format_schedule_data(enriched_schedule)
    
    # 3. Assemble Prompt
    prompt = GENERATION_PROMPT_TEMPLATE.format(
        aspect_ratio=aspect_ratio,
        schedule_table=schedule_table,
        style_name=style_full_name,
        style_description=style_desc
    )

    logger.info(f"Generated Prompt ({len(prompt)} chars) for {design_style} {theme}")
    return prompt
