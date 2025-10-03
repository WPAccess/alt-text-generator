# 🚀 Simple SEO Alt Text Generator

A minimal, automated system that connects to Google Sheets and generates SEO-friendly alt text for images using Google's Gemini AI.

## 🎯 What It Does

- ✅ **Connects to Google Sheets** automatically
- ✅ **Runs daily at 9:00 AM** to check for new images
- ✅ **Finds blank alt text cells** in your sheets
- ✅ **Generates SEO-friendly alt text** using Gemini AI
- ✅ **Updates sheets automatically** with generated content
- ✅ **Runs as background process** - no manual intervention needed

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Environment
```bash
python simple_setup.py
```
This will ask for:
- Your Gemini API key
- Your Google Sheets service account credentials

### 3. Add Your Sheets
Edit `simple_config.json` and add your Google Sheet IDs:
```json
{
  "sheets": [
    {
      "id": "YOUR_GOOGLE_SHEET_ID_HERE",
      "name": "Sheet1"
    }
  ]
}
```

### 4. Run the Generator
```bash
python simple_alt_generator.py
```

That's it! The system will:
- Run daily at 9:00 AM
- Process all your connected sheets
- Generate alt text for images automatically
- Update your sheets with the generated content

## 📊 Your Sheet Structure

Your Google Sheets should have these columns:

| Image URL | Alt Text | Title | Product Name |
|-----------|----------|-------|--------------|
| https://example.com/image1.jpg | | | Product 1 |
| https://example.com/image2.jpg | | | Product 2 |

**Supported column names:**
- **Image URL**: `image_url`, `image`, `url`, `image_link`
- **Alt Text**: `alt_text`, `alt`, `description`, `alt_description`

## 🔧 Configuration

### Environment Variables (.env file)
```bash
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_SHEETS_CREDENTIALS='{"type":"service_account",...}'
SCHEDULE_TIME=09:00
```

### Sheet Configuration (simple_config.json)
```json
{
  "sheets": [
    {
      "id": "sheet_id_1",
      "name": "Sheet1"
    },
    {
      "id": "sheet_id_2", 
      "name": "Products"
    }
  ],
  "settings": {
    "schedule_time": "09:00",
    "max_alt_length": 125
  }
}
```

## 📁 Project Structure

```
ImageTextGenerator/
├── simple_alt_generator.py    # Main application (one file!)
├── simple_setup.py           # Setup helper
├── simple_config.json        # Configuration
├── requirements.txt          # Dependencies
├── README.md                 # This file
└── .env                      # Environment variables (created during setup)
```

## 🎯 How It Works

1. **Daily Check**: System wakes up at 9:00 AM
2. **Scan Sheets**: Checks all connected Google Sheets
3. **Find Images**: Looks for rows with image URLs but empty alt text
4. **Generate Content**: Uses Gemini AI to create SEO-friendly alt text
5. **Update Sheets**: Automatically updates your sheets
6. **Log Activity**: Records all processing in logs

## 🔑 Getting API Keys

### Gemini API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key

### Google Sheets Credentials
1. Go to: https://console.cloud.google.com/
2. Create a project and enable Google Sheets API
3. Create service account credentials
4. Download the JSON file
5. Share your Google Sheets with the service account email

## 📝 Logs

The system creates logs showing:
- Daily processing results
- Number of images processed
- Any errors encountered
- Processing time

## 🛠️ Troubleshooting

### "No valid Google Sheets credentials found"
- Check your `.env` file has the correct credentials
- Ensure service account has access to your sheets

### "Gemini API error"
- Verify your Gemini API key is correct
- Check you have sufficient API quota

### "Sheet not found"
- Verify the sheet ID in `simple_config.json`
- Ensure the sheet is shared with your service account

## 🎉 Benefits

- **✅ Simple**: One Python file does everything
- **✅ Automated**: Runs daily without intervention
- **✅ Efficient**: Only processes new images
- **✅ SEO-Optimized**: AI-generated alt text
- **✅ Reliable**: Robust error handling
- **✅ Scalable**: Can handle multiple sheets

## 📞 Support

For issues:
1. Check the logs for error messages
2. Verify your API keys are correct
3. Ensure your sheets are properly configured
4. Make sure service account has sheet access

---

**Ready to automate your alt text generation!** 🚀
