#!/usr/bin/env python3
"""
Simple Setup Script
This script helps you set up the simple alt text generator
"""

import os
import json

def create_env_file():
    """Create .env file with required variables"""
    print("🔧 Setting up environment variables...")
    
    # Get Gemini API key
    gemini_key = input("Enter your Gemini API key: ").strip()
    if not gemini_key:
        print("❌ Gemini API key is required")
        return False
    
    # Get Google Sheets credentials
    print("\n📊 Google Sheets Setup:")
    print("1. Go to: https://console.cloud.google.com/")
    print("2. Create service account and download JSON")
    print("3. Paste the entire JSON content below (end with empty line):")
    
    json_lines = []
    while True:
        line = input()
        if line == "":
            break
        json_lines.append(line)
    
    if not json_lines:
        print("❌ Google Sheets credentials are required")
        return False
    
    google_creds = "\n".join(json_lines)
    
    # Create .env file
    env_content = f"""# Simple Alt Text Generator Environment Variables
GEMINI_API_KEY={gemini_key}
GOOGLE_SHEETS_CREDENTIALS='{google_creds}'
SCHEDULE_TIME=09:00
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created successfully!")
    return True

def setup_sheets():
    """Setup sheets in config file"""
    print("\n📋 Setting up your Google Sheets...")
    
    sheets = []
    while True:
        sheet_id = input("Enter Google Sheet ID (or press Enter to finish): ").strip()
        if not sheet_id:
            break
        
        sheet_name = input("Enter sheet name (default: Sheet1): ").strip() or "Sheet1"
        
        sheets.append({
            "id": sheet_id,
            "name": sheet_name,
            "description": f"Auto-generated alt text for {sheet_name}"
        })
        
        print(f"✅ Added sheet: {sheet_id}")
    
    # Update config file
    with open('simple_config.json', 'r') as f:
        config = json.load(f)
    
    config['sheets'] = sheets
    
    with open('simple_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Added {len(sheets)} sheets to config")
    return len(sheets) > 0

def main():
    """Main setup function"""
    print("🚀 Simple Alt Text Generator Setup")
    print("=" * 40)
    
    # Setup environment
    if not create_env_file():
        return
    
    # Setup sheets
    if not setup_sheets():
        print("⚠️ No sheets configured. You can add them later by editing simple_config.json")
    
    print("\n🎉 Setup Complete!")
    print("=" * 20)
    print("✅ Environment variables configured")
    print("✅ Sheets configured")
    print("\n🚀 Ready to run:")
    print("   python simple_alt_generator.py")
    print("\n📝 To add more sheets later, edit simple_config.json")

if __name__ == "__main__":
    main()
