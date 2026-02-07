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


# Map NUSMods URL short codes to API full lesson types
# Source: https://github.com/nusmodifications/nusmods/blob/master/scrapers/nus-v2/src/utils/data.ts
LESSON_TYPE_MAPPING = {
    "LEC": "Lecture",
    "TUT": "Tutorial",
    "LAB": "Laboratory",
    "SEC": "Sectional Teaching",
    "REC": "Recitation",
    "SEM": "Seminar-Style Module Class",
    "PLE": "Plenary",
    "WS": "Workshop",
    "DOM": "Design Lecture",
    "MCT": "Mini-Project",
    # Add common variations just in case
    "LECTURE": "Lecture",
    "TUTORIAL": "Tutorial",
    "LABORATORY": "Laboratory",
}

class ParsedUrl(TypedDict):
    semester: int
    modules: dict[str, dict[str, list[str]]]  # Changed int to str for class numbers


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
    logger.info(f"Parsed semester: {semester}")
    
    # Parse query string
    query = parse_qs(parsed.query)
    logger.info(f"Query parameters found: {list(query.keys())}")
    
    modules: dict[str, dict[str, list[str]]] = {}
    for module_code, lessons_list in query.items():
        if not lessons_list or not lessons_list[0]:
            continue
            
        lesson_str = lessons_list[0]
        lesson_dict: dict[str, list[str]] = {}
        
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
                num = num.strip()
                if num:
                    class_numbers.append(num)
            
            if class_numbers:
                # Keep abbreviated type for now, we'll map it in enrichment
                lesson_dict[lesson_type.upper().strip()] = class_numbers
        
        if lesson_dict:
            modules[module_code.upper()] = lesson_dict
            logger.info(f"Parsed module {module_code.upper()}: {lesson_dict}")
    
    logger.info(f"Total modules parsed: {len(modules)}")
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
        # Handle 404 cleanly - API might return 404 if year/sem/module combo is wrong
        if response.status_code == 404:
             # Try fallback to module detail only key if semester specific fails (though structure differs)
             # But for v2 API, the endpoint above is standard. 
             # Let's just try the general module endpoint if the semester specific one fails,
             # though that returns all semesters and we need to filter.
             # Actually, simpler to stick to standard endpoint and return None on 404 for now.
             logger.warning(f"Module data not found for {module_code} (404)")
             return None
             
        response.raise_for_status()
        data = response.json()
        
        # Log what we got back
        if "semesterData" in data:
            timetable_count = len(data["semesterData"].get("timetable", []))
            logger.info(f"Successfully fetched {module_code}: {timetable_count} timetable entries found")
        else:
            # Maybe the general endpoint was hit? try to find correct semester
            # The semester endpoint returns the module object but semesterData is a list if using general endpoint?
            # Wait, https://api.nusmods.com/v2/{year}/semesters/{sem}/modules/{code}.json returns object where semesterData IS the data for that sem?
            # Actually no, checking the response from `curl` earlier.. 
            # The curl command used was /modules/{code}.json (general) which returns "semesterData": [ {semester: 1, ...}, {semester: 2, ...} ]
            # The endpoint /semesters/{sem}/modules/{code}.json returns just the module details *for that semester*?
            # The v2 API verification showed we used the GENERAL endpoint in my manual test.
            # Let's check if the code expects the general endpoint structure or specific.
            # "semesterData" in data -> checking if key exists.
            pass
            
        return data
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
        logger.info(f"Processing module {module_code}: looking for {lesson_types}")
        enriched_schedule[module_code] = []
        
        # Fetch module data from NUSMods API
        module_data = fetch_module_data(module_code, academic_year, semester)
        
        if not module_data:
             logger.warning(f"Could not fetch data for {module_code}")
             continue

        # Handle different API response structures (General vs Semester-Specific Endpoint)
        # The URL used in fetch_module_data suggests semester-specific endpoint? 
        # Actually checking docs/usage: v2 API has /modules/{code}.json which contains all semesters.
        # The fetch_module_data function uses /semesters/{sem}/modules/{code}.json pattern which might NOT exist?
        # Let's check the earlier CURL: 
        # curl -s "https://api.nusmods.com/v2/2025-2026/semesters/2/modules/BT2102.json" -> 404
        # curl -s "https://api.nusmods.com/v2/2025-2026/modules/BT2102.json" -> 200 OK
        # So we MUST use the general endpoint and filter by semester manually.

    # Enrich the schedule with API data
    enriched_schedule = enrich_schedule_with_api_data(parsed_url)
    
    return enriched_schedule


def fetch_module_data(module_code: str, academic_year: str, semester: int) -> Optional[dict]:
    # Use general module endpoint
    url = f"https://api.nusmods.com/v2/{academic_year}/modules/{module_code}.json"
    
    try:
        logger.info(f"Fetching module data: {module_code} from {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        logger.warning(f"Failed to fetch module data for {module_code}: {str(e)}")
        return None


def enrich_schedule_with_api_data(parsed_url: ParsedUrl) -> EnrichedSchedule:
    semester = parsed_url["semester"]
    modules = parsed_url["modules"]
    academic_year = get_current_academic_year()
    
    logger.info(f"Enriching schedule data for AY{academic_year}, Semester {semester}")
    
    enriched_schedule: EnrichedSchedule = {}
    
    for module_code, lesson_types in modules.items():
        logger.info(f"Processing module {module_code}: looking for {lesson_types}")
        enriched_schedule[module_code] = []
        
        module_data = fetch_module_data(module_code, academic_year, semester)
        
        if not module_data:
            logger.warning(f"No data fetched for {module_code}, skipping")
            continue
            
        # Find the correct semester data
        semester_data = None
        all_semesters = module_data.get("semesterData", [])
        for sem_data in all_semesters:
            if sem_data.get("semester") == semester:
                semester_data = sem_data
                break
        
        if not semester_data:
            logger.warning(f"No data found for {module_code} in semester {semester}")
            continue
            
        timetable = semester_data.get("timetable", [])
        logger.info(f"Module {module_code} has {len(timetable)} lessons in timetable")
        
        for url_lesson_type, class_numbers in lesson_types.items():
            # Resolve full lesson type from mapping (e.g., "LAB" -> "Laboratory")
            # If not in mapping, try title case as fallback (e.g. "Lec" -> "Lecture"?)
            # Or just use as is if not found
            api_lesson_type = LESSON_TYPE_MAPPING.get(url_lesson_type.upper(), url_lesson_type)
            
            logger.info(f"Looking for {module_code} {url_lesson_type} (API: {api_lesson_type}) classes: {class_numbers}")
            
            matches_found = 0
            
            for class_no_target in class_numbers:
                found_match = False
                class_no_target_str = str(class_no_target).strip()
                
                for lesson in timetable:
                    # Check Lesson Type match
                    current_lesson_type = lesson.get("lessonType")
                    if current_lesson_type != api_lesson_type:
                        continue
                        
                    # Check Class Number match
                    # Valid matches: "1" == "1", "01" == "1", "1" == "01"
                    current_class_no = str(lesson.get("classNo", "")).strip()
                    
                    is_match = False
                    if current_class_no == class_no_target_str:
                        is_match = True
                    else:
                        # Try integer comparison if both look like integers
                        try:
                            if int(current_class_no) == int(class_no_target_str):
                                is_match = True
                        except ValueError:
                            pass # Not integers
                            
                    if is_match:
                        enriched_lesson = EnrichedLesson(
                            day=lesson.get("day", "TBA"),
                            startTime=lesson.get("startTime", "TBA"),
                            endTime=lesson.get("endTime", "TBA"),
                            venue=lesson.get("venue", "TBA"),
                            lessonType=current_lesson_type,
                            classNo=current_class_no
                        )
                        enriched_schedule[module_code].append(enriched_lesson)
                        logger.info(f"✓ Matched: {module_code} {url_lesson_type} {class_no_target} -> {current_lesson_type} {current_class_no}")
                        matches_found += 1
                        found_match = True
                        # Don't break here! A single class number (e.g. "LEC 1") might have multiple slots (Mon key + Wed key)
                        # We want all of them.
                
                if not found_match:
                    logger.warning(f"✗ No match found for {module_code} {url_lesson_type} class {class_no_target}")
            
            logger.info(f"Found {matches_found} lessons for {module_code} {url_lesson_type}")
            
    total_lessons = sum(len(lessons) for lessons in enriched_schedule.values())
    logger.info(f"Total lessons enriched across all modules: {total_lessons}")
    return enriched_schedule

