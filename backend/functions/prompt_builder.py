"""
Prompt Builder for Timetable Wallpaper Generation

Constructs text-to-image prompts for Imagen to generate NUSMods timetable
phone wallpapers from scratch.
"""

from typing import Literal, Dict, List, Any, Optional

DesignStyleType = Literal[
    "minimalist", "gradient", "neon", "pastel", "glass", "retro", "kawaii"
]
ThemeType = Literal["light", "dark"]


# Base generation prompt - tells Imagen what image to create
GENERATION_PROMPT_TEMPLATE = """Create a clean, READABLE university timetable wallpaper ({aspect_ratio} aspect ratio, portrait orientation).

SCHEDULE DATA TO DISPLAY:
{schedule_data}

YOUR TASK:
Generate a timetable wallpaper that displays this exact schedule in a flat, visually beautiful layout. THIS IS WALLPAPER ONLY - NO DEVICE FRAME, NO PHONE MOCKUP.

CRITICAL REQUIREMENTS (in order of priority):

1. WALLPAPER CONTENT ONLY:
   - GENERATE ONLY THE TIMETABLE/SCHEDULE ITSELF
   - NO iPhone frame, NO phone border, NO device bezel
   - NO status bar, NO notch, NO home indicator
   - NO phone mockup or device frame of any kind
   - Just the raw timetable/wallpaper content filling the entire image
   - Portrait orientation ({aspect_ratio})

2. READABILITY FIRST:
   - Use LARGE, LEGIBLE text (minimum 14pt for body text, 18pt+ for course codes)
   - High contrast between text and background
   - Clear visual hierarchy (course codes most prominent, then times, then venues)
   - Generous line spacing between entries

3. TIMETABLE LAYOUT (NO CARDS):
   - Design as a FLAT timetable grid/list layout
   - Organize by days of the week (Monday through Friday columns or sections)
   - Show time slots running vertically
   - Each class entry should be a simple colored block/rectangle
   - Use consistent color coding for each course across all sessions
   - Include day headers (Mon, Tue, Wed, Thu, Fri)
   - Include time markers on the side (08:00, 10:00, 12:00, etc.)

4. VISUAL STYLE:
   - Apply the {style_name} aesthetic described below
   - NO card UI elements (no shadows, no borders, no rounded corners on cards)
   - Flat design with direct text on background
   - Use color blocks to distinguish different courses
   - Clean, minimal, functional design

5. DISPLAY ALL SCHEDULE DATA:
   - Show ALL courses, times, days, lesson types, and venues listed above
   - Format each entry as: "[Course Code] [Lesson Type] @ [Venue]"
   - Place entries in their corresponding day/time slots
   - Use consistent colors for each course
   - Leave margins on all sides (at least 5% of width/height)

STYLE SPECIFICATIONS:
{style_description}

OUTPUT FORMAT:
- Portrait orientation
- Grid/timetable layout (columns for days, rows for time slots)
- Maximum visual clarity and readability
- Beautiful design that people want to use as wallpaper
- All schedule information clearly displayed in timetable format
- Professional, polished appearance
- NO card UI, NO shadows, NO rounded card containers
- ABSOLUTELY NO DEVICE MOCKUP, PHONE FRAME, OR UI CHROME

Remember: This is a TIMETABLE WALLPAPER - just the schedule layout itself, no device frame. Organize by day and time. Make it READABLE first, pretty second. Fill the entire {aspect_ratio} portrait space with pure timetable content.
"""


# Style descriptions optimized for flat timetable wallpaper (NO CARDS)
STYLE_DESCRIPTIONS = {
    "minimalist": {
        "light": """
MINIMALIST LIGHT STYLE:
- Clean white or light gray background (#F8F9FA)
- Large course code text (20-24pt, bold, dark gray/black) directly on background
- Simple flat color blocks for each course (muted pastels: pale blue, mint, lavender)
- Thin grid lines separating days and time slots
- Clean sans-serif typography throughout
- Time and venue info in 14-16pt directly on colored blocks
- NO cards, NO shadows - pure flat design
- Thin divider lines between time slots and days
- Professional, clean, paper-like timetable appearance
- Focus on whitespace and breathing room
""",
        "dark": """
MINIMALIST DARK STYLE:
- Deep charcoal background (#121212)
- Large white course codes (20-24pt, bold) directly on background
- Muted dark color blocks for each class (dark blue, dark green, dark amber)
- Clean white/light gray text for readability
- Thin grid lines in dark gray
- Time and venue info in 14-16pt white text
- NO cards, NO elevation - flat timetable design
- OLED-friendly with generous spacing
- Sleek, modern aesthetic
- Emphasis on maximum readability
""",
    },
    "gradient": {
        "light": """
GRADIENT LIGHT STYLE:
- Soft gradient background (pink to lavender or peach to mint)
- Large, bold course codes (22-26pt) with gradient fills directly on background
- Each class slot has a smooth gradient background matching the course
- Modern flat design - NO rounded corners on blocks
- High contrast text with subtle shadows for readability
- Time and venue in 14-16pt
- Flowing color transitions for course blocks
- Thin grid lines for timetable structure
- Contemporary, elegant timetable aesthetic
- Generous spacing for touch-friendly layout
""",
        "dark": """
GRADIENT DARK STYLE:
- Deep gradient background (navy to purple)
- Large white/cream course codes (22-26pt, bold) directly on blocks
- Vibrant gradient blocks for each class (magenta-purple, cyan-blue, amber-orange)
- Soft glow effects around class blocks
- Rich saturated colors with readable text
- Time and venue in 14-16pt white text
- Flat timetable grid optimized for vertical viewing
- Thin divider lines between slots
- Sophisticated night aesthetic
- Each course has unique gradient identity
""",
    },
    "neon": {
        "light": """
NEON LIGHT STYLE:
- White or light gray background
- Large bold course codes (24-28pt) with neon colored text directly on background
- Bright neon colored blocks for each class (electric pink, lime, cyan, yellow)
- Thin neon colored grid lines (2-3px)
- Bold geometric typography for maximum impact
- Time and venue in 16-18pt
- Energetic, electric feel with high contrast
- Each course has unique neon accent color
- Flat timetable layout with neon grid dividers
- NO cards - direct neon blocks on white background
- Touch-friendly spacing between elements
""",
        "dark": """
NEON DARK STYLE:
- Pure black background (#000000)
- Large glowing neon course codes (24-28pt) directly on blocks
- Strong neon glow effects on class blocks (hot pink, electric blue, lime green, orange)
- High contrast white text on blocks
- Time and venue in 16-18pt with subtle glow
- Flat timetable grid layout with glowing dividers
- Cyberpunk aesthetic with maximum readability
- OLED-friendly true blacks
- Each course gets unique neon signature color
- NO card containers - just glowing blocks in grid
- Generous spacing for futuristic look
""",
    },
    "pastel": {
        "light": """
PASTEL LIGHT STYLE:
- Cream or light blush background (#FFF5F0)
- Large, friendly course codes (22-26pt, rounded font) directly on blocks
- Soft pastel blocks for each class (baby pink, mint, lavender, peach, sky blue)
- Rounded corners on class blocks only (8-12px) - NOT on cards
- Time and venue in 14-16pt
- Small cute decorative elements in margins (tiny stars ★, hearts ♡)
- Flat timetable grid layout with gentle spacing
- Thin pastel divider lines between slots
- Warm, cozy, inviting aesthetic
- Each course gets soft pastel identity
- Clean grid structure, touch-friendly spacing
""",
        "dark": """
PASTEL DARK STYLE:
- Deep purple or midnight blue background (#1A1025) with subtle stars
- Large cream/white course codes (22-26pt) directly on blocks
- Muted dark pastel blocks for classes (dusty pink, teal, lavender)
- Cream/light text for readability
- Time and venue in 14-16pt
- Small moon ☾ and star ☆ decorations in margins
- Flat timetable grid layout
- Thin divider lines in muted colors
- Dreamy, nighttime aesthetic
- Cozy and comfortable vibe
- NO cards - just colored blocks in grid
- Generous spacing for relaxed feel
""",
    },
    "glass": {
        "light": """
GLASSMORPHISM LIGHT STYLE:
- Soft gradient background (light blue to lavender)
- Large bold course codes (22-26pt, dark text) directly on glass blocks
- Frosted glass effect on class blocks (white at 60% opacity with blur)
- Subtle white borders around blocks for depth
- Time and venue in 14-16pt through glass effect
- Light refractions on blocks
- Flat timetable grid layout with glass separation
- Thin grid lines for structure
- iOS/macOS inspired aesthetic
- Premium, modern feel with excellent readability
- NO card containers - just glass blocks in grid
""",
        "dark": """
GLASSMORPHISM DARK STYLE:
- Deep gradient background (dark purple to blue)
- Large white course codes (22-26pt, bold) directly on glass blocks
- Dark frosted glass blocks with subtle transparency for each class
- Soft glow effects for depth and readability
- Time and venue in 14-16pt white text
- Flat timetable grid with glass block separation
- Thin glowing divider lines
- Apple-style glassmorphism
- Sophisticated, premium dark mode
- Each block has distinct glass effect
- NO card UI - just glass blocks in timetable grid
- Touch-friendly spacing
""",
    },
    "retro": {
        "light": """
RETRO LIGHT STYLE:
- Warm cream background (#F5F1E8) with subtle paper texture
- Large bold course codes (24-28pt, retro rounded font) directly on blocks
- Retro colored blocks for classes (mustard, burnt orange, olive, teal, rusty red)
- Rounded retro typography throughout
- Time and venue in 16-18pt
- 70s/80s inspired palette with high contrast
- Flat timetable grid with vintage borders
- Thin colored divider lines
- Mid-century modern influence
- Slight vintage aesthetic with modern readability
- NO cards - just colored blocks in grid
- Generous spacing for retro chunky look
""",
        "dark": """
RETRO DARK STYLE:
- Deep brown or dark navy background (#1A0F0A)
- Large gold/cream course codes (24-28pt, bold retro font) directly on blocks
- Dark retro colored blocks for classes (deep teal, burgundy, forest green, mustard)
- Gold/cream text for contrast
- Time and venue in 16-18pt
- Art deco influences with geometric patterns
- Flat timetable grid layout
- Thin gold divider lines
- Film noir aesthetic
- Sophisticated vintage feel
- NO card containers - just colored blocks in grid
- Touch-friendly spacing
""",
    },
    "kawaii": {
        "light": """
KAWAII LIGHT STYLE:
- Warm cream or pale pink background (#FFF8F0)
- Large, cute course codes (24-28pt, rounded bubbly font) directly on blocks
- Soft pastel blocks for classes (peach, mint, lavender, baby blue, soft yellow)
- Rounded friendly fonts throughout
- Time and venue in 16-18pt
- Small cute decorative elements in margins: tiny stars ★, hearts ♡, sparkles ✨
- Small emoji icons near course codes (books 📚, coffee ☕, pencil ✏️)
- Flat timetable grid layout with generous spacing
- Soft beige grid lines between slots
- Rounded corners on class blocks only (12-16px)
- Japanese stationery/bullet journal inspired
- Planner-style timetable with hand-drawn feel
- Weekly schedule header at top
- NO card containers - just colored blocks in grid
- Touch-friendly spacing
""",
        "dark": """
KAWAII DARK STYLE:
- Deep purple background (#1A1025) with subtle star pattern
- Large cream/white course codes (24-28pt, rounded cute font) directly on blocks
- Muted dark pastel blocks for classes (dusty pink, sage green, muted lavender)
- Cream colored text for readability
- Time and venue in 16-18pt
- Celestial decorations in margins: stars ☆, moons ☾, sparkles ✦
- Small emoji touches (moon 🌙, stars ⭐, clouds ☁️)
- Soft glowing effects on class blocks like fairy lights
- Flat timetable grid layout
- Thin glowing divider lines
- Dreamy, cozy night aesthetic
- Night-mode bullet journal style planner
- Each block has subtle inner glow
- NO card UI - just glowing blocks in grid
- Generous spacing for kawaii aesthetic
- Weekly schedule header with stars
""",
    },
}


def format_schedule_data(enriched_schedule: Any) -> str:
    """
    Format enriched schedule data into a readable text description for Imagen.

    Args:
        enriched_schedule: Enriched schedule data with day, time, venue info

    Returns:
        Formatted text describing the schedule
    """
    # Map abbreviated lesson types to readable full names
    LESSON_TYPE_NAMES = {
        "LEC": "Lecture",
        "TUT": "Tutorial",
        "LAB": "Laboratory",
        "REC": "Recitation",
        "SEC": "Sectional",
        "SEM": "Seminar",
        "DLEC": "Design Lecture",
        "PLEC": "Packaged Lecture",
        "PTUT": "Packaged Tutorial",
        "WS": "Workshop",
    }
    
    # Map different day formats to standard names
    DAY_NAMES = {
        "Monday": "Monday", "Mon": "Monday", "M": "Monday", "1": "Monday",
        "Tuesday": "Tuesday", "Tue": "Tuesday", "T": "Tuesday", "2": "Tuesday",
        "Wednesday": "Wednesday", "Wed": "Wednesday", "W": "Wednesday", "3": "Wednesday",
        "Thursday": "Thursday", "Thu": "Thursday", "Th": "Thursday", "4": "Thursday",
        "Friday": "Friday", "Fri": "Friday", "F": "Friday", "5": "Friday",
        "Saturday": "Saturday", "Sat": "Saturday", "S": "Saturday", "6": "Saturday",
        "Sunday": "Sunday", "Sun": "Sunday", "U": "Sunday", "7": "Sunday",
    }
    
    if not enriched_schedule:
        return "No schedule data available"

    schedule_lines = ["Schedule:"]
    schedule_lines.append("")

    # Group lessons by day for better readability
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    lessons_by_day: Dict[str, List[tuple[str, Any]]] = {day: [] for day in days_of_week}

    for module_code, lessons in enriched_schedule.items():
        for lesson in lessons:
            day_raw = lesson.get("day", "TBA")
            # Normalize day format
            day = DAY_NAMES.get(str(day_raw), day_raw)
            
            if day in lessons_by_day:
                lessons_by_day[day].append((module_code, lesson))

    # Format by day
    for day in days_of_week:
        day_lessons = lessons_by_day[day]
        if not day_lessons:
            continue

        schedule_lines.append(f"**{day}:**")
        for module_code, lesson in day_lessons:
            # Format time: "1000" -> "10:00"
            start_time = lesson.get("startTime", "TBA")
            end_time = lesson.get("endTime", "TBA")

            if start_time != "TBA" and len(start_time) == 4:
                start_time = f"{start_time[:2]}:{start_time[2:]}"
            if end_time != "TBA" and len(end_time) == 4:
                end_time = f"{end_time[:2]}:{end_time[2:]}"

            venue = lesson.get("venue", "TBA")
            lesson_type_abbr = lesson.get("lessonType", "")
            # Convert abbreviated type to readable name
            lesson_type = LESSON_TYPE_NAMES.get(lesson_type_abbr, lesson_type_abbr)

            schedule_lines.append(
                f"  - {module_code} {lesson_type} - {start_time}-{end_time} @ {venue}"
            )

        schedule_lines.append("")

    return "\n".join(schedule_lines)


def build_prompt(
    design_style: DesignStyleType = "minimalist",
    theme: ThemeType = "light",
    aspect_ratio: str = "9:16",
    enriched_schedule: Optional[Any] = None,
) -> str:
    """
    Build the text-to-image prompt for Imagen to generate timetable wallpaper.

    Args:
        design_style: One of the supported design styles
        theme: Either "light" or "dark"
        aspect_ratio: Target aspect ratio for the wallpaper (e.g., "9:16")
        enriched_schedule: Enriched schedule data with day, time, venue info

    Returns:
        Complete prompt string for Imagen image generation
    """
    style_desc = STYLE_DESCRIPTIONS.get(design_style, STYLE_DESCRIPTIONS["minimalist"])
    style_description = style_desc.get(theme, style_desc["light"])

    style_name = f"{design_style.capitalize()} {theme.capitalize()}"

    # Format schedule data if provided
    if enriched_schedule:
        schedule_data = format_schedule_data(enriched_schedule)
    else:
        schedule_data = "No schedule data provided"

    return GENERATION_PROMPT_TEMPLATE.format(
        style_name=style_name,
        style_description=style_description,
        aspect_ratio=aspect_ratio,
        schedule_data=schedule_data,
    )
