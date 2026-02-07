"""
ModPocket Firebase Functions - NUSMods Timetable Wallpaper Generator

Generates NUSMods timetables as stylized phone wallpapers using
Imagen text-to-image generation.
"""

import json
import time
import logging
import traceback
import firebase_admin
from firebase_functions import https_fn
from firebase_functions.options import set_global_options, CorsOptions

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from nusmods_parser import parse_nusmods_url, enrich_schedule_with_api_data
from prompt_builder import build_prompt, DesignStyleType, ThemeType
from image_generator import generate_image_base64


# Initialize Firebase
firebase_admin.initialize_app()

# Global function options
set_global_options(max_instances=10)

# Valid design styles
VALID_STYLES = ("minimalist", "gradient", "neon", "pastel", "glass", "retro", "kawaii")
VALID_THEMES = ("light", "dark")

# Core aspect ratio used for all generations (for consistency)
CORE_ASPECT_RATIO = "9:16"


@https_fn.on_request(
    region="asia-southeast1",
    memory=512,
    timeout_sec=120,
    cors=CorsOptions(
        cors_origins="*",
        cors_methods=["POST", "OPTIONS"]
    )
)
def generate_wallpaper(req: https_fn.Request) -> https_fn.Response:
    """
    Generate a stylized timetable wallpaper from a NUSMods URL.
    
    Pipeline:
    1. Parse NUSMods share URL to extract schedule data
    2. Enrich schedule with day/time/venue info from NUSMods API
    3. Build comprehensive text-to-image prompt with enriched schedule
    4. Generate wallpaper image using Imagen 04 Ultra
    5. Return base64-encoded wallpaper image
    """
    # Only accept POST requests
    if req.method != "POST":
        return https_fn.Response(
            json.dumps({"error": "Method not allowed. Use POST."}),
            status=405,
            content_type="application/json"
        )
    
    # Parse JSON body
    try:
        body = req.get_json(force=True)
    except Exception:
        return https_fn.Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type="application/json"
        )
    
    # Extract and validate fields
    nusmods_url = body.get("nusmods_url")
    design_style: DesignStyleType = body.get("design_style", "kawaii").lower()
    theme: ThemeType = body.get("theme", "light").lower()
    # Accept any aspect_ratio from user, but use core ratio for generation
    aspect_ratio = body.get("aspect_ratio", CORE_ASPECT_RATIO)
    
    if not nusmods_url:
        return https_fn.Response(
            json.dumps({"error": "Missing required field: nusmods_url"}),
            status=400,
            content_type="application/json"
        )
    
    if design_style not in VALID_STYLES:
        return https_fn.Response(
            json.dumps({
                "error": f"Invalid design_style. Use one of: {', '.join(VALID_STYLES)}"
            }),
            status=400,
            content_type="application/json"
        )
    
    if theme not in VALID_THEMES:
        return https_fn.Response(
            json.dumps({"error": "Invalid theme. Use 'light' or 'dark'."}),
            status=400,
            content_type="application/json"
        )
    
    try:
        logger.info(f"Processing request: style={design_style}, theme={theme}, aspect_ratio={aspect_ratio}")
        
        # Step 1: Parse NUSMods URL
        logger.info("Step 1: Parsing NUSMods URL")
        parsed = parse_nusmods_url(nusmods_url)
        module_codes = list(parsed["modules"].keys())
        logger.info(f"Parsed {len(module_codes)} modules: {module_codes}")
        
        if not module_codes:
            return https_fn.Response(
                json.dumps({"error": "No modules found in the provided URL"}),
                status=400,
                content_type="application/json"
            )
        
        # Step 2: Enrich schedule data with NUSMods API
        logger.info("Step 2: Fetching schedule data from NUSMods API")
        enriched_schedule = enrich_schedule_with_api_data(parsed)
        logger.info(f"Enriched schedule with {sum(len(lessons) for lessons in enriched_schedule.values())} lessons")
        
        # Step 3: Build text-to-image prompt with enriched schedule data
        logger.info("Step 3: Building text-to-image prompt with schedule data")
        # Always use core aspect ratio for consistency
        style_prompt = build_prompt(design_style, theme, CORE_ASPECT_RATIO, enriched_schedule)
        logger.info(f"Prompt built: {len(style_prompt)} characters")
        
        # Step 4: Generate image with Imagen (no source image needed)
        logger.info(f"Step 4: Generating wallpaper with Imagen (using core ratio: {CORE_ASPECT_RATIO})")
        # Pass empty bytes for source_image (kept for API compatibility but not used)
        source_image = b""
        image_base64 = generate_image_base64(source_image, style_prompt, CORE_ASPECT_RATIO)
        logger.info(f"Image generation complete: {len(image_base64)} base64 characters")
        
        # Return success response
        logger.info("Request completed successfully")
        return https_fn.Response(
            json.dumps({
                "success": True,
                "image_base64": image_base64,
                "modules": module_codes
            }),
            status=200,
            content_type="application/json"
        )
        
    except ValueError as e:
        logger.error(f"ValueError: {str(e)}")
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=400,
            content_type="application/json"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        return https_fn.Response(
            json.dumps({
                "error": f"Internal error: {type(e).__name__}: {str(e)}",
                "type": type(e).__name__
            }),
            status=500,
            content_type="application/json"
        )