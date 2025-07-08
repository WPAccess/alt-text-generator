import os
import requests
import base64
import tempfile
from PIL import Image
import logging
from openai import OpenAI

logger = logging.getLogger(__name__)

class ImageAnalyzer:
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    
    def generate_alt_text(self, image_url):
        """Generate SEO-friendly alt text for an image URL"""
        try:
            # Download image
            image_data = self._download_image(image_url)
            if not image_data:
                raise ValueError("Failed to download image")
            
            # Convert to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Generate alt text using OpenAI Vision API
            alt_text = self._generate_with_openai(base64_image)
            
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
                raise ValueError(f"Invalid content type: {content_type}")
            
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
                    
                    # Resize if too large (OpenAI has limits)
                    max_size = 2048
                    if img.width > max_size or img.height > max_size:
                        img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                    
                    # Save as JPEG for OpenAI
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
    
    def _generate_with_openai(self, base64_image):
        """Generate alt text using OpenAI Vision API"""
        try:
            # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            # do not change this unless explicitly requested by the user
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert at creating SEO-friendly alt text for images. 
                        Your alt text should be:
                        - Descriptive and specific
                        - Concise (under 125 characters)
                        - SEO-friendly with relevant keywords
                        - Accessible for screen readers
                        - Professional and natural sounding
                        
                        Focus on the main subject, important details, context, and any text visible in the image.
                        Do not start with "Image of" or "Picture of" - just describe what you see directly."""
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Generate SEO-friendly alt text for this image:"
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )
            
            alt_text = response.choices[0].message.content.strip()
            
            # Ensure alt text is not too long
            if len(alt_text) > 125:
                alt_text = alt_text[:122] + "..."
            
            return alt_text
            
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise ValueError(f"Failed to generate alt text: {str(e)}")
