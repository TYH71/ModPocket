"""
ModPocket Firebase Functions - Timetable Wallpaper Generator

Generates timetables as stylized phone wallpapers using Imagen.
Uses static timetable data from assets/timetable.txt.
"""

import os
import json
import logging
import traceback
import firebase_admin
from firebase_functions import https_fn
from firebase_functions.options import set_global_options, CorsOptions
from typing import Dict, List, TypedDict

from prompt_builder import build_prompt, DesignStyleType, ThemeType
from image_generator import generate_image_base64

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

firebase_admin.initialize_app()
set_global_options(max_instances=10)

VALID_STYLES = ("minimalist", "gradient", "neon", "pastel", "glass", "retro", "kawaii")
VALID_THEMES = ("light", "dark")
CORE_ASPECT_RATIO = "9:16"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]


class EnrichedLesson(TypedDict):
    day: str
    startTime: str
    endTime: str
    venue: str
    lessonType: str
    classNo: str


def load_static_timetable() -> Dict[str, List[EnrichedLesson]]:
    """
    Load timetable from assets/timetable.txt.
    Format per entry (3 lines + blank):
        MA1521 Lecture
        LT32
        Monday 0800-1000
    """
    timetable_path = os.path.join(os.path.dirname(__file__), "assets", "timetable.txt")
    
    with open(timetable_path, "r") as f:
        content = f.read().strip()
    
    entries = content.split("\n\n")
    schedule: Dict[str, List[EnrichedLesson]] = {}
    
    for entry in entries:
        lines = entry.strip().split("\n")
        if len(lines) < 3:
            continue
        
        # Parse: "MA1521 Lecture" -> module="MA1521", type="Lecture"
        first_line_parts = lines[0].split(" ", 1)
        module_code = first_line_parts[0]
        lesson_type = first_line_parts[1] if len(first_line_parts) > 1 else "Class"
        
        venue = lines[1]
        
        # Parse: "Monday 0800-1000" -> day="Monday", time="0800-1000"
        day_time_parts = lines[2].split(" ")
        day = day_time_parts[0]
        time_range = day_time_parts[1] if len(day_time_parts) > 1 else "0000-0000"
        start_time, end_time = time_range.split("-")
        
        lesson = EnrichedLesson(
            day=day,
            startTime=start_time,
            endTime=end_time,
            venue=venue,
            lessonType=lesson_type,
            classNo="1"
        )
        
        if module_code not in schedule:
            schedule[module_code] = []
        schedule[module_code].append(lesson)
        
        logger.info(f"Loaded: {module_code} {lesson_type} on {day} {start_time}-{end_time} @ {venue}")
    
    return schedule


@https_fn.on_request(
    region="asia-southeast1",
    memory=512,
    timeout_sec=120,
    cors=CorsOptions(cors_origins="*", cors_methods=["POST", "OPTIONS"])
)
def generate_wallpaper(req: https_fn.Request) -> https_fn.Response:
    """
    Generate a stylized timetable wallpaper.
    Uses static timetable from assets/timetable.txt.
    """
    if req.method != "POST":
        return https_fn.Response(
            json.dumps({"error": "Method not allowed. Use POST."}),
            status=405, content_type="application/json"
        )
    
    try:
        body = req.get_json(force=True)
    except Exception:
        body = {}
    
    design_style: DesignStyleType = body.get("design_style", "minimalist").lower()
    theme: ThemeType = body.get("theme", "light").lower()
    
    if design_style not in VALID_STYLES:
        return https_fn.Response(
            json.dumps({"error": f"Invalid design_style. Use one of: {', '.join(VALID_STYLES)}"}),
            status=400, content_type="application/json"
        )
    
    if theme not in VALID_THEMES:
        return https_fn.Response(
            json.dumps({"error": "Invalid theme. Use 'light' or 'dark'."}),
            status=400, content_type="application/json"
        )
    
    try:
        logger.info(f"Generating wallpaper: style={design_style}, theme={theme}")
        
        # Step 1: Load static timetable
        schedule = load_static_timetable()
        module_codes = list(schedule.keys())
        total_lessons = sum(len(l) for l in schedule.values())
        logger.info(f"Loaded {total_lessons} lessons for {len(module_codes)} modules")
        
        # Step 2: Build prompt
        prompt = build_prompt(design_style, theme, CORE_ASPECT_RATIO, schedule)
        logger.info(f"Prompt built: {len(prompt)} chars")
        
        # Step 3: Generate image
        image_base64 = generate_image_base64(b"", prompt, CORE_ASPECT_RATIO)
        logger.info(f"Image generated: {len(image_base64)} base64 chars")
        
        return https_fn.Response(
            json.dumps({"success": True, "image_base64": image_base64, "modules": module_codes}),
            status=200, content_type="application/json"
        )
        
    except Exception as e:
        logger.error(f"Error: {type(e).__name__}: {str(e)}")
        logger.error(traceback.format_exc())
        return https_fn.Response(
            json.dumps({"error": f"Internal error: {str(e)}"}),
            status=500, content_type="application/json"
        )