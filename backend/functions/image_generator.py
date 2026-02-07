"""
Image Generator using Imagen 04 Ultra

Generates NUSMods timetable wallpapers using Google's Imagen text-to-image model.
"""

import base64
import io
import logging
from google import genai
from google.genai import types

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def stylize_timetable(source_image: bytes, prompt: str, aspect_ratio: str = "9:16") -> bytes:
    """
    Generate a timetable wallpaper using Imagen text-to-image model.
    
    Args:
        source_image: Source timetable image bytes (not used with Imagen, kept for API compatibility)
        prompt: Text prompt describing the timetable wallpaper to generate
        aspect_ratio: Target aspect ratio (e.g., "9:16", "9:19.5", "9:20", "9:21")
    
    Returns:
        Generated image bytes (PNG format)
    """
    try:
        logger.info("Initializing Imagen client")
        # Initialize client with Vertex AI
        client = genai.Client(
            vertexai=True,
            project="modpocket-369",
            location="us-central1"
        )
        
        logger.info(f"Generating image with Imagen from text prompt ({len(prompt)} characters)")
        
        # Try multiple Imagen model options
        models_to_try = [
            "imagen-4.0-ultra-generate-001",
            "imagen-3.0-generate-001",  # Imagen 3.0 fallback
        ]
        
        last_error = None
        for model_name in models_to_try:
            try:
                logger.info(f"Attempting to use model: {model_name}")
                
                # Generate image from text prompt
                response = client.models.generate_images(
                    model=model_name,
                    prompt=prompt,
                    config=types.GenerateImagesConfig(
                        number_of_images=1,
                        aspect_ratio=aspect_ratio,  # Use provided aspect ratio
                        safety_filter_level="block_some",
                        person_generation="allow_all",
                    )
                )
                
                logger.info(f"Successfully generated image with {model_name}")
                
                # Extract the generated image
                if response.generated_images and len(response.generated_images) > 0:
                    image_data = response.generated_images[0].image.image_bytes
                    logger.info(f"Image generated successfully: {len(image_data)} bytes")
                    return image_data
                
                # If we get here, no image was in the response
                logger.warning(f"Model {model_name} returned response but no image data")
                break  # Don't try other models if this one responded
                
            except Exception as model_error:
                logger.warning(f"Model {model_name} failed: {str(model_error)}")
                last_error = model_error
                continue
        
        # If we got here, either no image was generated or all models failed
        if last_error:
            raise ValueError(f"All Imagen models failed. Last error: {str(last_error)}")
        else:
            raise ValueError("Imagen did not generate an image. Please try again.")
            
    except Exception as e:
        logger.error(f"Error in stylize_timetable: {type(e).__name__}: {str(e)}")
        raise


def generate_image_base64(source_image: bytes, prompt: str, aspect_ratio: str = "9:16") -> str:
    """
    Transform image and return as base64-encoded string.
    
    Args:
        source_image: Source timetable image bytes
        prompt: Style editing prompt
        aspect_ratio: Target aspect ratio (e.g., "9:16", "9:19.5", "9:20", "9:21")
    
    Returns:
        Base64-encoded PNG image string
    """
    image_bytes = stylize_timetable(source_image, prompt, aspect_ratio)
    return base64.b64encode(image_bytes).decode("utf-8")
