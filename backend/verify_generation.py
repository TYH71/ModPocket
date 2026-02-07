
import logging
import os
import sys

# Add the directory to sys.path so we can import functions
sys.path.append(os.path.join(os.path.dirname(__file__), 'functions'))

from functions.nusmods_parser import parse_nusmods_url, enrich_schedule_with_api_data
from functions.prompt_builder import build_prompt
# We won't actually call image_generator in this script to save credits/time strictly unless needed, 
# but we will print the prompt to verify it looks correct.

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TEST_URL = "https://nusmods.com/timetable/sem-2/share?BT2102=LEC:1&CS2040=LEC:1&MA1521=LEC:1&UTW1001T=SEC:1"

def test_pipeline():
    logger.info("--- 1. Parsing URL ---")
    parsed_schedule = parse_nusmods_url(TEST_URL)
    if not parsed_schedule:
        logger.error("Failed to parse URL")
        return

    logger.info(f"Parsed Data: {parsed_schedule}")
    
    # It returns a single ParsedUrl object (dict)
    target_schedule = parsed_schedule
    
    if target_schedule.get('semester') != 2:
        logger.warning(f"Parsed semester is {target_schedule.get('semester')}, expected 2. Proceeding anyway.")
    
    logger.info(f"Target Modules: {target_schedule['modules']}")

    logger.info("--- 2. Enriching with API Data ---")
    # This might take a few seconds as it hits nusmods.com API
    enriched_data = enrich_schedule_with_api_data(target_schedule)
    
    if not enriched_data:
        logger.error("Failed to enrich data")
        return

    logger.info(f"Enriched Data Keys: {list(enriched_data.keys())}")
    for mod, lessons in enriched_data.items():
        logger.info(f"Module {mod}: {len(lessons)} lessons")
        for l in lessons:
            logger.info(f"  - {l.get('lessonType')} [{l.get('classNo')}] {l.get('day')} {l.get('startTime')}-{l.get('endTime')}")

    logger.info("--- 3. Building Prompt ---")
    prompt = build_prompt(
        design_style="minimalist",
        theme="light", # Test light mode
        aspect_ratio="9:16",
        enriched_schedule=enriched_data
    )
    
    logger.info("--- Generated Prompt ---")
    print(prompt)
    logger.info("------------------------")
    
    # Check for critical keywords from optimized template
    assert "SAFE ZONES" in prompt
    assert "TOP 25%" in prompt
    assert "Minimalist (Light Mode)" in prompt
    
    logger.info("✅ Verification Passed: Pipeline creates valid prompts from URL.")

if __name__ == "__main__":
    test_pipeline()
