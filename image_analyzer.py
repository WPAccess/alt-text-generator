import os
import requests
import base64
import tempfile
from PIL import Image
import logging
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    def __init__(self):
        self.gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
    
    def generate_alt_text(self, image_url):
        """Generate SEO-friendly alt text for an image URL"""
        try:
            # Download image
            image_data = self._download_image(image_url)
            if not image_data:
                raise ValueError("Failed to download image")
            
            # Generate alt text using Gemini Vision API
            alt_text = self._generate_with_gemini(image_data)
            
            return alt_text
            
        except Exception as e:
            logger.error(f"Error generating alt text for {image_url}: {str(e)}")
            raise
    
    def _download_image(self, image_url):
        """Download image from URL and return image data"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Validate image format
            content_type = response.headers.get('content-type', '')
            if not content_type.startswith('image/'):
                if 'text/html' in content_type:
                    raise ValueError(f"URL points to a webpage, not an image. Please use direct image URLs (e.g., https://images.unsplash.com/photo-xxx)")
                else:
                    raise ValueError(f"Invalid content type: {content_type}. Expected image, got {content_type}")
            
            # Process image with PIL to ensure it's valid
            image_data = response.content
            with tempfile.NamedTemporaryFile() as temp_file:
                temp_file.write(image_data)
                temp_file.flush()
                
                # Open with PIL to validate and potentially resize
                with Image.open(temp_file.name) as img:
                    # Convert to RGB if necessary
                    if img.mode not in ('RGB', 'RGBA'):
                        img = img.convert('RGB')
                    
                    # Resize if too large (Gemini has limits)
                    max_size = 2048
                    if img.width > max_size or img.height > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
                    # Save as JPEG for Gemini
                    with tempfile.NamedTemporaryFile(suffix='.jpg') as output_file:
                        img.save(output_file.name, 'JPEG', quality=85)
                        output_file.seek(0)
                        return output_file.read()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error downloading image: {str(e)}")
            raise ValueError(f"Failed to download image: {str(e)}")
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            raise ValueError(f"Failed to process image: {str(e)}")
    
    def _generate_with_gemini(self, image_data):
        """Generate alt text using Gemini Vision API"""
        try:
            # Create system instruction for SEO-friendly alt text
            system_instruction = """You are an expert at creating SEO-friendly alt text for images. 
            Your alt text should be:
            - Descriptive and specific
            - Concise (under 125 characters)
            - SEO-friendly with relevant keywords
            - Accessible for screen readers
            - Professional and natural sounding
            
            Focus on the main subject, important details, context, and any text visible in the image.
            Do not start with "Image of" or "Picture of" - just describe what you see directly."""
            
            # Note that the newest Gemini model series is "gemini-2.5-flash" or "gemini-2.5-pro"
            # do not change this unless explicitly requested by the user
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=image_data,
                        mime_type="image/jpeg",
                    ),
                    "You are an expert at creating SEO-friendly alt text. Generate descriptive, professional alt text for this image. Keep it under 125 characters, focus on main subject and important details. Don't start with 'Image of' or 'Picture of' - describe directly what you see."
                ],
                config=types.GenerateContentConfig(
                    max_output_tokens=500,
                    temperature=0.3
                )
            )
            
            alt_text = response.text.strip() if response.text else ""
            
            # Ensure alt text is not too long
            if len(alt_text) > 125:
                alt_text = alt_text[:122] + "..."
            
            return alt_text
            
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise ValueError(f"Failed to generate alt text: {str(e)}")
