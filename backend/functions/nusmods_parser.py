"""
NUSMods URL Parser and API Integration

Parses NUSMods share URLs and enriches schedule data with NUSMods API.
"""

import re
import json
import logging
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from typing import TypedDict, Optional, List, Dict
import requests


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ParsedUrl(TypedDict):
    semester: int
    modules: dict[str, dict[str, list[int]]]


class EnrichedLesson(TypedDict):
    day: str
    startTime: str
    endTime: str
    venue: str
    lessonType: str
    classNo: str


EnrichedSchedule = Dict[str, List[EnrichedLesson]]


def parse_nusmods_url(url: str) -> ParsedUrl:
    """
    Parse a NUSMods share URL and extract semester and module selections.
    
    Example URL:
    https://nusmods.com/timetable/sem-2/share?BT2102=LAB:(7);LEC:(11)&CS2040=TUT:(33);LAB:(20);LEC:(34,35)
    
    Returns:
        ParsedUrl with semester and modules dict (lesson types with class numbers as lists)
    """
    parsed = urlparse(url)
    
    # Validate domain
    if "nusmods.com" not in parsed.netloc:
        raise ValueError("Invalid URL: must be a nusmods.com URL")
    
    # Extract semester from path: /timetable/sem-2/share
    path_parts = parsed.path.strip("/").split("/")
    
    if len(path_parts) < 2 or "sem-" not in path_parts[1]:
        raise ValueError("Invalid URL: could not find semester in path")
    
    semester_match = re.search(r"sem-(\d+)", path_parts[1])
    if not semester_match:
        raise ValueError("Invalid URL: could not parse semester number")
    
    semester = int(semester_match.group(1))
    
    # Parse query string
    query = parse_qs(parsed.query)
    
    modules: dict[str, dict[str, list[int]]] = {}
    for module_code, lessons_list in query.items():
        if not lessons_list or not lessons_list[0]:
            continue
            
        lesson_str = lessons_list[0]
        lesson_dict: dict[str, list[int]] = {}
        
        # Split by semicolon (new format) or comma (old format)
        if ";" in lesson_str:
            lessons = lesson_str.split(";")
        else:
            lessons = lesson_str.split(",")
        
        for lesson in lessons:
            if ":" not in lesson:
                continue
            lesson_type, class_no_raw = lesson.split(":", 1)
            
            # Remove parentheses: "(7)" -> "7", "(34,35)" -> "34,35"
            class_no_str = class_no_raw.strip("()")
            
            # Parse class numbers (can be comma-separated for multiple sessions)
            class_numbers = []
            for num in class_no_str.split(","):
                try:
                    class_numbers.append(int(num.strip()))
                except ValueError:
                    continue
            
            if class_numbers:
                # Keep abbreviated type for API matching (e.g., "LEC", "TUT", "LAB")
                lesson_dict[lesson_type.upper().strip()] = class_numbers
        
        if lesson_dict:
            modules[module_code.upper()] = lesson_dict
    
    return ParsedUrl(semester=semester, modules=modules)


def get_current_academic_year() -> str:
    """
    Determine the current academic year based on today's date.
    
    NUS academic year logic:
    - August to December: AY is current_year to next_year (e.g., Aug 2025 -> AY2025-2026)
    - January to July: AY is (current_year - 1) to current_year (e.g., Feb 2026 -> AY2025-2026)
    
    Returns:
        Academic year string in format "YYYY-YYYY" (e.g., "2025-2026")
    """
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    
    if current_month >= 8:  # August onwards
        return f"{current_year}-{current_year + 1}"
    else:  # January to July
        return f"{current_year - 1}-{current_year}"


def fetch_module_data(module_code: str, academic_year: str, semester: int) -> Optional[dict]:
    """
    Fetch module data from NUSMods API.
    
    Args:
        module_code: Module code (e.g., "CS2040")
        academic_year: Academic year string (e.g., "2025-2026")
        semester: Semester number (1 or 2)
    
    Returns:
        Module data dict with semesterData containing lessons, or None if failed
    """
    url = f"https://api.nusmods.com/v2/{academic_year}/semesters/{semester}/modules/{module_code}.json"
    
    try:
        logger.info(f"Fetching module data: {module_code} from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch module data for {module_code}: {str(e)}")
        return None


def enrich_schedule_with_api_data(parsed_url: ParsedUrl) -> EnrichedSchedule:
    """
    Enrich parsed URL data with actual schedule information from NUSMods API.
    
    Args:
        parsed_url: Parsed URL data with semester and modules
    
    Returns:
        Enriched schedule dict mapping module codes to lists of lesson details
    """
    semester = parsed_url["semester"]
    modules = parsed_url["modules"]
    academic_year = get_current_academic_year()
    
    logger.info(f"Enriching schedule data for AY{academic_year}, Semester {semester}")
    
    enriched_schedule: EnrichedSchedule = {}
    
    for module_code, lesson_types in modules.items():
        enriched_schedule[module_code] = []
        
        # Fetch module data from NUSMods API
        module_data = fetch_module_data(module_code, academic_year, semester)
        
        if not module_data or "semesterData" not in module_data:
            logger.warning(f"No semester data for {module_code}, skipping API enrichment")
            continue
        
        # Extract timetable lessons
        timetable = module_data.get("semesterData", {}).get("timetable", [])
        
        for lesson_type, class_numbers in lesson_types.items():
            # Find matching lessons in timetable
            for class_no in class_numbers:
                for lesson in timetable:
                    if (lesson.get("lessonType") == lesson_type and 
                        lesson.get("classNo") == str(class_no)):
                        enriched_schedule[module_code].append(EnrichedLesson(
                            day=lesson.get("day", "TBA"),
                            startTime=lesson.get("startTime", "TBA"),
                            endTime=lesson.get("endTime", "TBA"),
                            venue=lesson.get("venue", "TBA"),
                            lessonType=lesson.get("lessonType", lesson_type),
                            classNo=lesson.get("classNo", str(class_no))
                        ))
    
    return enriched_schedule

