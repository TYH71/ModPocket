"""
ModPocket Firebase Functions

Serverless backend for generating NUSMods timetable wallpapers.
"""

import json
from firebase_functions import https_fn
from firebase_functions.options import set_global_options, CorsOptions
from firebase_admin import initialize_app

from nusmods_parser import parse_nusmods_url, fetch_full_timetable, build_timetable_grid
from prompt_builder import build_prompt, DesignStyleType, ThemeType
from image_generator import generate_image_base64


# Initialize Firebase Admin
initialize_app()

# Global function options
set_global_options(max_instances=10)

# Valid design styles
VALID_STYLES = ("minimal", "gradient", "neon", "pastel", "glass", "retro")
VALID_THEMES = ("light", "dark")
VALID_ASPECT_RATIOS = {
    "1179x2556": "iPhone 14/15 Pro",
    "1290x2796": "iPhone Pro Max",
    "750x1334": "iPhone SE",
    "1080x2400": "Android (1080p)",
}


@https_fn.on_request(
    region="asia-southeast1",
    memory=512,
    timeout_sec=120,
    cors=CorsOptions(cors_origins="*", cors_methods=["POST", "OPTIONS"])
)
def generate_wallpaper(req: https_fn.Request) -> https_fn.Response:
    """
    Generate a timetable wallpaper from a NUSMods URL.
    
    Request body (JSON):
        {
            "nusmods_url": "https://nusmods.com/timetable/sem-2/share?...",
            "design_style": "minimal" | "gradient" | "neon" | "pastel" | "glass" | "retro",
            "theme": "light" | "dark",
            "aspect_ratio": "16:9" | "19.5:9" | "4:3"
        }
    
    Response (JSON):
        {
            "success": true,
            "image_base64": "<base64-encoded-png>",
            "modules": ["CS2040", "MA1521", ...]
        }
    """
    # Only accept POST requests
    if req.method != "POST":
        return https_fn.Response(
            json.dumps({"error": "Method not allowed. Use POST."}),
            status=405,
            content_type="application/json"
        )
    
    # Parse request body
    try:
        body = req.get_json()
    except Exception:
        return https_fn.Response(
            json.dumps({"error": "Invalid JSON body"}),
            status=400,
            content_type="application/json"
        )
    
    # Extract and validate fields
    nusmods_url = body.get("nusmods_url")
    design_style: DesignStyleType = body.get("design_style", "minimal").lower()
    theme: ThemeType = body.get("theme", "light").lower()
    aspect_ratio = body.get("aspect_ratio", "1179x2556")  # Default: iPhone 14/15 Pro
    
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
    
    if aspect_ratio not in VALID_ASPECT_RATIOS:
        return https_fn.Response(
            json.dumps({
                "error": f"Invalid aspect_ratio. Use one of: {', '.join(VALID_ASPECT_RATIOS.keys())}"
            }),
            status=400,
            content_type="application/json"
        )
    
    try:
        # Step 1: Parse NUSMods URL
        parsed = parse_nusmods_url(nusmods_url)
        module_codes = list(parsed["modules"].keys())
        
        # Step 2: Fetch full timetable data from NUSMods API
        lessons = fetch_full_timetable(parsed)
        
        if not lessons:
            return https_fn.Response(
                json.dumps({"error": "No lessons found for the provided URL"}),
                status=400,
                content_type="application/json"
            )
        
        # Step 3: Build timetable grid for the prompt
        timetable_grid = build_timetable_grid(lessons)
        
        # Step 4: Build the image generation prompt
        prompt = build_prompt(timetable_grid, design_style, theme, aspect_ratio)
        
        # Step 5: Generate the wallpaper image
        image_base64 = generate_image_base64(prompt, aspect_ratio)
        
        # Return success response
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
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=400,
            content_type="application/json"
        )
    except Exception as e:
        return https_fn.Response(
            json.dumps({"error": f"Internal error: {str(e)}"}),
            status=500,
            content_type="application/json"
        )