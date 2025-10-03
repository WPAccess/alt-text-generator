#!/usr/bin/env python3
"""
Simple SEO Alt Text Generator
A minimal implementation that does exactly what you need:
- Connects to Google Sheets
- Runs daily to find blank alt text cells
- Generates alt text using Gemini AI
- Updates sheets automatically
"""

import os
import json
import time
import schedule
import requests
import logging
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google import genai
from google.genai import types

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleAltTextGenerator:
    def __init__(self):
        """Initialize the simple generator"""
        self.gemini_api_key = os.environ.get('GEMINI_API_KEY')
        self.google_credentials = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
        
        # Initialize Gemini AI
        if self.gemini_api_key:
            self.gemini_client = genai.Client(api_key=self.gemini_api_key)
        
        # Initialize Google Sheets
        if self.google_credentials:
            self._init_google_sheets()
        
        # Store connected sheets
        self.connected_sheets = []
    
    def _init_google_sheets(self):
        """Initialize Google Sheets API"""
        try:
            credentials_info = json.loads(self.google_credentials)
            credentials = Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets']
            )
            self.sheets_service = build('sheets', 'v4', credentials=credentials)
            logger.info("✅ Google Sheets API initialized")
        except json.JSONDecodeError as e:
            logger.error(f"❌ Invalid JSON in GOOGLE_SHEETS_CREDENTIALS: {e}")
            logger.error("📋 Make sure the JSON is properly formatted in Railway variables")
            self.sheets_service = None
        except Exception as e:
            logger.error(f"❌ Google Sheets initialization failed: {e}")
            logger.error("📋 Check your GOOGLE_SHEETS_CREDENTIALS environment variable")
            self.sheets_service = None
    
    def add_sheet(self, sheet_id, sheet_name="Sheet1"):
        """Add a Google Sheet to monitor"""
        sheet_info = {
            'id': sheet_id,
            'name': sheet_name,
            'added_at': datetime.now().isoformat()
        }
        self.connected_sheets.append(sheet_info)
        logger.info(f"✅ Added sheet: {sheet_id} ({sheet_name})")
    
    def find_blank_cells(self, sheet_id, sheet_name="Sheet1"):
        """Find rows with image URLs but blank alt text"""
        try:
            # Get all data from sheet
            range_name = f'{sheet_name}!A:Z'
            result = self.sheets_service.spreadsheets().values().get(
                spreadsheetId=sheet_id,
                range=range_name
            ).execute()
            
            values = result.get('values', [])
            if not values:
                return []
            
            # Find header row
            header_row = 0
            for i, row in enumerate(values):
                if row and any('image' in cell.lower() or 'url' in cell.lower() for cell in row):
                    header_row = i
                    break
            
            if header_row >= len(values):
                return []
            
            headers = values[header_row]
            
            # Find column indices
            image_col = None
            alt_col = None
            
            for i, header in enumerate(headers):
                header_lower = header.lower()
                if any(term in header_lower for term in ['image', 'url', 'link']):
                    image_col = i
                elif any(term in header_lower for term in ['alt', 'description', 'alt_text']):
                    alt_col = i
            
            if image_col is None:
                logger.warning("No image URL column found")
                return []
            
            # If no alt column, we'll create one
            if alt_col is None:
                alt_col = len(headers)
            
            blank_cells = []
            
            # Check each row
            for row_idx in range(header_row + 1, len(values)):
                row = values[row_idx]
                
                # Ensure row has enough columns
                while len(row) <= max(image_col, alt_col):
                    row.append('')
                
                image_url = row[image_col].strip()
                alt_text = row[alt_col].strip() if alt_col < len(row) else ''
                
                # Skip if no image URL or already has alt text
                if not image_url or not image_url.startswith(('http://', 'https://')):
                    continue
                
                if alt_text:  # Skip if already has alt text
                    continue
                
                blank_cells.append({
                    'row': row_idx + 1,  # 1-based for Google Sheets
                    'image_url': image_url,
                    'alt_col': alt_col + 1,  # 1-based
                    'sheet_name': sheet_name
                })
            
            logger.info(f"Found {len(blank_cells)} blank cells in {sheet_id}")
            return blank_cells
            
        except Exception as e:
            logger.error(f"Error finding blank cells: {e}")
            return []
    
    def generate_alt_text(self, image_url):
        """Generate alt text using Gemini AI (using working approach from original)"""
        try:
            # Download image
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()
            
            # Generate alt text using the working approach
            system_instruction = """You are an expert at creating SEO-friendly alt text for images. 
            Your alt text should be:
            - Descriptive and specific
            - Concise (under 125 characters)
            - SEO-friendly with relevant keywords
            - Accessible for screen readers
            - Professional and natural sounding
            
            Focus on the main subject, important details, context, and any text visible in the image.
            Do not start with "Image of" or "Picture of" - just describe what you see directly."""
            
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    types.Part.from_bytes(
                        data=response.content,
                        mime_type="image/jpeg",
                    ),
                    "Generate concise, SEO-friendly alt text for this image. Requirements: Maximum 120 characters, focus on main subject and key features, use descriptive keywords, no 'Image of' prefix. Be specific but brief."
                ],
                config=types.GenerateContentConfig(
                    max_output_tokens=150,  # Reduced to encourage shorter responses
                    temperature=0.3
                )
            )
            
            alt_text = response.text.strip() if response.text else ""
            
            # Ensure alt text is not too long, but make it more natural
            if len(alt_text) > 125:
                # Try to cut at a word boundary instead of just truncating
                truncated = alt_text[:122]
                last_space = truncated.rfind(' ')
                if last_space > 100:  # If we can find a good word boundary
                    alt_text = alt_text[:last_space]
                else:
                    alt_text = alt_text[:122]
            
            logger.info(f"Generated alt text: {alt_text[:50]}...")
            return alt_text
            
        except Exception as e:
            logger.error(f"Error generating alt text for {image_url}: {e}")
            return None
    
    def update_sheet(self, sheet_id, updates):
        """Update sheet with generated alt text"""
        try:
            if not updates:
                logger.warning("No updates to apply")
                return True
            
            logger.info(f"🔄 Updating sheet {sheet_id} with {len(updates)} updates")
            
            batch_data = []
            for update in updates:
                cell_range = f"{update['sheet_name']}!{self._col_letter(update['alt_col'])}{update['row']}"
                batch_data.append({
                    'range': cell_range,
                    'values': [[update['alt_text']]]
                })
                logger.info(f"Update range: {cell_range} = {update['alt_text'][:30]}...")
            
            body = {
                'valueInputOption': 'RAW',
                'data': batch_data
            }
            
            logger.info(f"Sending batch update to Google Sheets...")
            self.sheets_service.spreadsheets().values().batchUpdate(
                spreadsheetId=sheet_id,
                body=body
            ).execute()
            
            logger.info(f"✅ Updated {len(updates)} cells in {sheet_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error updating sheet: {e}")
            return False
    
    def _col_letter(self, col_num):
        """Convert column number to letter (1-based)"""
        result = ""
        while col_num > 0:
            col_num -= 1
            result = chr(65 + col_num % 26) + result
            col_num //= 26
        return result
    
    def process_sheet(self, sheet_id, sheet_name="Sheet1"):
        """Process a single sheet - find blank cells and generate alt text"""
        logger.info(f"Processing sheet: {sheet_id}")
        
        # Find blank cells
        blank_cells = self.find_blank_cells(sheet_id, sheet_name)
        if not blank_cells:
            logger.info("No blank cells found")
            return 0
        
        # Generate alt text for each blank cell with rate limiting
        updates = []
        for i, cell in enumerate(blank_cells):
            # Add delay between requests to avoid rate limiting (2 seconds)
            if i > 0:
                logger.info(f"Waiting 2 seconds to avoid rate limiting...")
                time.sleep(2)
            
            alt_text = self.generate_alt_text(cell['image_url'])
            if alt_text:
                update_data = {
                    'row': cell['row'],
                    'alt_text': alt_text,
                    'alt_col': cell['alt_col'],
                    'sheet_name': cell['sheet_name']
                }
                updates.append(update_data)
                logger.info(f"Added update for row {cell['row']}: {alt_text[:50]}...")
            else:
                logger.warning(f"No alt text generated for row {cell['row']}")
        
        # Update sheet
        if updates:
            self.update_sheet(sheet_id, updates)
            logger.info(f"✅ Processed {len(updates)} images")
            return len(updates)
        
        return 0
    
    def run_daily_check(self):
        """Run daily check on all connected sheets"""
        logger.info("🕘 Starting daily check...")
        start_time = datetime.now()
        
        total_processed = 0
        for sheet_info in self.connected_sheets:
            try:
                processed = self.process_sheet(sheet_info['id'], sheet_info['name'])
                total_processed += processed
            except Exception as e:
                logger.error(f"Error processing sheet {sheet_info['id']}: {e}")
        
        duration = (datetime.now() - start_time).total_seconds()
        logger.info(f"✅ Daily check complete: {total_processed} images processed in {duration:.1f}s")
    
    def start_scheduler(self):
        """Start the daily scheduler"""
        # Check if we should run immediately for testing
        schedule_time = os.environ.get('SCHEDULE_TIME', '09:00')
        
        if schedule_time.lower() == 'now':
            logger.info("🧪 TESTING MODE: Running immediately")
            logger.info("🚀 Alt text generator starting...")
            self.run_daily_check()
            logger.info("✅ Test run completed!")
            return
        
        # Schedule daily check
        schedule.every().day.at(schedule_time).do(self.run_daily_check)
        
        logger.info(f"📅 Scheduled daily check at {schedule_time}")
        logger.info("🚀 Alt text generator running...")
        logger.info("🌐 Service is ready and monitoring sheets...")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("👋 Stopping scheduler...")
        except Exception as e:
            logger.error(f"❌ Scheduler error: {e}")
            logger.info("🔄 Restarting scheduler...")
            time.sleep(10)
            self.start_scheduler()  # Restart scheduler

def load_sheets_from_config():
    """Load sheets from config file"""
    try:
        with open('simple_config.json', 'r') as f:
            config = json.load(f)
        return config.get('sheets', [])
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return []

def main():
    """Main function"""
    print("🚀 Simple SEO Alt Text Generator")
    print("=" * 40)
    
    # Check required environment variables
    missing_vars = []
    
    if not os.environ.get('GEMINI_API_KEY'):
        missing_vars.append('GEMINI_API_KEY')
    
    if not os.environ.get('GOOGLE_SHEETS_CREDENTIALS'):
        missing_vars.append('GOOGLE_SHEETS_CREDENTIALS')
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📋 To fix this:")
        print("1. Add environment variables in Railway dashboard")
        print("2. Or run locally: python simple_setup.py")
        print("\n⏳ Service will wait for configuration...")
        
        # Wait for environment variables to be set
        print("🔄 Checking for environment variables every 60 seconds...")
        while missing_vars:
            time.sleep(60)  # Wait 1 minute
            missing_vars = []
            if not os.environ.get('GEMINI_API_KEY'):
                missing_vars.append('GEMINI_API_KEY')
            if not os.environ.get('GOOGLE_SHEETS_CREDENTIALS'):
                missing_vars.append('GOOGLE_SHEETS_CREDENTIALS')
            
            if missing_vars:
                print(f"⏳ Still missing: {', '.join(missing_vars)}")
            else:
                print("✅ All environment variables found!")
                break
    
    # Initialize generator
    generator = SimpleAltTextGenerator()
    
    # Load sheets from config file
    sheets = load_sheets_from_config()
    if not sheets:
        print("⚠️ No sheets configured in simple_config.json")
        print("Edit simple_config.json or run: python simple_setup.py")
        return
    
    # Add sheets to generator
    for sheet in sheets:
        generator.add_sheet(sheet['id'], sheet['name'])
    
    print(f"✅ Generator initialized with {len(sheets)} sheets")
    print("🔄 Starting scheduler...")
    
    # Start scheduler
    generator.start_scheduler()

if __name__ == "__main__":
    main()
