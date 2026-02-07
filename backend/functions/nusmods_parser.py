"""
NUSMods URL Parser and Timetable Data Fetcher

Parses NUSMods share URLs and fetches full timetable data from the NUSMods API.
"""

import re
from urllib.parse import urlparse, parse_qs
from typing import TypedDict
import requests


class LessonInfo(TypedDict):
    module: str
    title: str
    day: str
    start_time: str
    end_time: str
    venue: str
    lesson_type: str


class ParsedUrl(TypedDict):
    semester: int
    acad_year: str
    modules: dict[str, dict[str, str]]


# Mapping from full lesson type names to abbreviations
LESSON_TYPE_MAP = {
    "Lecture": "LEC",
    "Tutorial": "TUT",
    "Laboratory": "LAB",
    "Recitation": "REC",
    "Sectional Teaching": "SEC",
    "Seminar-Style Module Class": "SEM",
    "Design Lecture": "DLEC",
    "Packaged Lecture": "PLEC",
    "Packaged Tutorial": "PTUT",
    "Workshop": "WS",
}


def get_current_acad_year() -> str:
    """
    Determine the current academic year based on the current date.
    NUS academic year runs from August to July.
    """
    from datetime import datetime
    
    now = datetime.now()
    year = now.year
    month = now.month
    
    # If before August, we're in the previous academic year
    if month < 8:
        return f"{year - 1}-{year}"
    else:
        return f"{year}-{year + 1}"


def parse_nusmods_url(url: str) -> ParsedUrl:
    """
    Parse a NUSMods share URL and extract semester and module selections.
    
    Example URL:
    https://nusmods.com/timetable/sem-2/share?BT2102=LEC:1,LAB:01&CS2040=TUT:01,LEC:1
    
    Returns:
        ParsedUrl with semester, academic year, and modules dict
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
    
    # Parse query string: ?BT2102=LEC:1,LAB:01&CS2040=TUT:01
    query = parse_qs(parsed.query)
    
    modules: dict[str, dict[str, str]] = {}
    for module_code, lessons_list in query.items():
        # lessons_list is ["LEC:1,LAB:01,TUT:01"]
        if not lessons_list:
            continue
            
        lesson_str = lessons_list[0]
        lesson_dict: dict[str, str] = {}
        
        for lesson in lesson_str.split(","):
            if ":" not in lesson:
                continue
            lesson_type, class_no = lesson.split(":", 1)
            lesson_dict[lesson_type.upper()] = class_no
        
        modules[module_code.upper()] = lesson_dict
    
    return ParsedUrl(
        semester=semester,
        acad_year=get_current_acad_year(),
        modules=modules
    )


def get_lesson_type_abbrev(full_name: str) -> str:
    """Convert full lesson type name to abbreviation."""
    return LESSON_TYPE_MAP.get(full_name, full_name[:3].upper())


def fetch_module_info(module_code: str, acad_year: str) -> dict:
    """
    Fetch module information from NUSMods API.
    
    Args:
        module_code: The module code (e.g., "CS2040")
        acad_year: Academic year in format "2025-2026"
    
    Returns:
        Full module data from NUSMods API
    """
    url = f"https://api.nusmods.com/v2/{acad_year}/modules/{module_code}.json"
    
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    return response.json()


def get_module_timetable(
    module_code: str,
    selected_lessons: dict[str, str],
    acad_year: str,
    semester: int
) -> list[LessonInfo]:
    """
    Fetch module data and filter to only selected lessons.
    
    Args:
        module_code: The module code
        selected_lessons: Dict of lesson type to class number
        acad_year: Academic year
        semester: Semester number (1 or 2)
    
    Returns:
        List of LessonInfo for the selected lessons
    """
    module_data = fetch_module_info(module_code, acad_year)
    
    # Find the semester's timetable data
    semester_data = next(
        (s for s in module_data.get("semesterData", []) if s.get("semester") == semester),
        None
    )
    
    if not semester_data:
        return []
    
    timetable: list[LessonInfo] = []
    
    for lesson in semester_data.get("timetable", []):
        lesson_type_full = lesson.get("lessonType", "")
        lesson_type_abbrev = get_lesson_type_abbrev(lesson_type_full)
        class_no = lesson.get("classNo", "")
        
        # Check if this lesson matches a selected one
        if lesson_type_abbrev in selected_lessons:
            if selected_lessons[lesson_type_abbrev] == class_no:
                timetable.append(LessonInfo(
                    module=module_code,
                    title=module_data.get("title", ""),
                    day=lesson.get("day", ""),
                    start_time=lesson.get("startTime", ""),
                    end_time=lesson.get("endTime", ""),
                    venue=lesson.get("venue", ""),
                    lesson_type=lesson_type_abbrev
                ))
    
    return timetable


def fetch_full_timetable(parsed_url: ParsedUrl) -> list[LessonInfo]:
    """
    Fetch complete timetable data for all modules in a parsed URL.
    
    Args:
        parsed_url: Output from parse_nusmods_url()
    
    Returns:
        List of all LessonInfo entries for the timetable
    """
    all_lessons: list[LessonInfo] = []
    
    for module_code, selected_lessons in parsed_url["modules"].items():
        lessons = get_module_timetable(
            module_code=module_code,
            selected_lessons=selected_lessons,
            acad_year=parsed_url["acad_year"],
            semester=parsed_url["semester"]
        )
        all_lessons.extend(lessons)
    
    return all_lessons


def build_timetable_grid(lessons: list[LessonInfo]) -> str:
    """
    Build a markdown table representation of the timetable for the prompt.
    
    Args:
        lessons: List of LessonInfo entries
    
    Returns:
        Markdown table string
    """
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day_abbrev = {"Monday": "Mon", "Tuesday": "Tue", "Wednesday": "Wed", 
                  "Thursday": "Thu", "Friday": "Fri"}
    
    # Find the time range needed
    if not lessons:
        return "No classes scheduled."
    
    start_hours = [int(l["start_time"][:2]) for l in lessons]
    end_hours = [int(l["end_time"][:2]) for l in lessons]
    
    min_hour = min(start_hours)
    max_hour = max(end_hours)
    
    # Build grid: grid[day][hour] = cell content
    grid: dict[str, dict[int, str]] = {day: {} for day in days}
    
    for lesson in lessons:
        day = lesson["day"]
        if day not in grid:
            continue
            
        start_hour = int(lesson["start_time"][:2])
        cell = f"{lesson['module']} {lesson['lesson_type']}\\n{lesson['venue']}"
        grid[day][start_hour] = cell
    
    # Build markdown table
    lines = []
    header = "| Time  | " + " | ".join(day_abbrev[d] for d in days) + " |"
    separator = "|-------|" + "|".join(["----------" for _ in days]) + "|"
    lines.append(header)
    lines.append(separator)
    
    for hour in range(min_hour, max_hour + 1):
        time_str = f"{hour:02d}:00"
        cells = []
        for day in days:
            cell = grid[day].get(hour, "")
            cells.append(cell if cell else "")
        
        row = f"| {time_str} | " + " | ".join(cells) + " |"
        lines.append(row)
    
    return "\n".join(lines)
