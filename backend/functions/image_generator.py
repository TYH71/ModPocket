"""
Image Generator using Imagen 3 on Vertex AI

Generates timetable wallpaper images using Vertex AI's Imagen 3 model.
"""

import base64
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel


# Configuration
PROJECT_ID = "modpocket-369"
# Use us-central1 for image generation as it has best model availability
LOCATION = "us-central1"

# Map phone resolutions to Imagen 3 supported aspect ratios
# Imagen 3 supports: 1:1, 9:16, 16:9, 4:3, 3:4
RESOLUTION_TO_ASPECT = {
    "1179x2556": "9:16",   # iPhone 14/15 Pro (portrait)
    "1290x2796": "9:16",   # iPhone Pro Max (portrait)
    "750x1334": "9:16",    # iPhone SE (portrait)
    "1080x2400": "9:16",   # Android 1080p (portrait)
}


def generate_timetable_image(prompt: str, resolution: str = "1179x2556") -> bytes:
    """
    Generate a timetable wallpaper image using Imagen 3.
    
    Args:
        prompt: The full prompt for image generation
        resolution: Target resolution (e.g., "1179x2556")
    
    Returns:
        Image bytes (PNG format)
    """
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    # Load Imagen 3 model
    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-002")
    
    # Map resolution to Imagen 3 aspect ratio
    aspect_ratio = RESOLUTION_TO_ASPECT.get(resolution, "9:16")
    
    # Generate image
    response = model.generate_images(
        prompt=prompt,
        number_of_images=1,
        aspect_ratio=aspect_ratio,
        safety_filter_level="block_few",
        person_generation="dont_allow",
    )
    
    if not response.images:
        raise RuntimeError("No image was generated in the response")
    
    # Return image bytes
    return response.images[0]._image_bytes


def generate_image_base64(prompt: str, resolution: str = "1179x2556") -> str:
    """
    Generate image and return as base64-encoded string.
    
    Args:
        prompt: The full prompt for image generation
        resolution: Target resolution (e.g., "1179x2556")
    
    Returns:
        Base64-encoded PNG image string
    """
    image_bytes = generate_timetable_image(prompt, resolution)
    return base64.b64encode(image_bytes).decode("utf-8")
