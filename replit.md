# SEO Alt Text Generator

## Overview

This is a Flask-based web application that processes Excel files containing image URLs and generates SEO-friendly alt text using Google's Gemini AI Vision API. The application allows users to upload Excel files, automatically detect missing alt text, and generate descriptive alt text for images using AI.

## System Architecture

### Backend Architecture
- **Framework**: Flask (Python web framework)
- **File Processing**: Uses openpyxl for Excel file manipulation
- **Image Processing**: PIL (Python Imaging Library) for image validation and processing
- **AI Integration**: Google Gemini AI Vision API for alt text generation
- **File Storage**: Local filesystem for temporary file storage

### Frontend Architecture
- **Template Engine**: Jinja2 (Flask's default templating)
- **CSS Framework**: Bootstrap (dark theme)
- **Icons**: Font Awesome
- **JavaScript**: Vanilla JavaScript for client-side interactions

## Key Components

### 1. Application Core (`app.py`)
- Flask application initialization
- Configuration management (upload limits, folder paths)
- Session management with secret key
- Directory creation for uploads and temporary files

### 2. Excel Processing (`excel_processor.py`)
- **ExcelProcessor Class**: Handles reading and writing Excel files
- **Column Detection**: Automatically identifies image URL and alt text columns
- **Data Extraction**: Extracts image URLs and existing alt text from spreadsheets
- **File Formatting**: Applies styling to processed Excel files

### 3. Image Analysis (`image_analyzer.py`)
- **ImageAnalyzer Class**: Manages AI-powered alt text generation
- **Image Download**: Fetches images from URLs with proper headers
- **Format Validation**: Ensures downloaded content is valid image format
- **Gemini Integration**: Uses Google's Gemini AI Vision API to generate descriptive alt text

### 4. Web Routes (`routes.py`)
- **File Upload**: Handles Excel file uploads with validation
- **Processing Endpoints**: Manages alt text generation requests
- **Download**: Provides processed Excel files for download
- **Error Handling**: Comprehensive error management across all endpoints

### 5. Frontend Interface
- **Upload Interface**: Drag-and-drop file upload with progress tracking
- **Data Display**: Table view of processed data with individual row actions
- **Bulk Operations**: Generate alt text for all missing entries
- **Download Management**: Export processed Excel files

## Data Flow

1. **File Upload**: User uploads Excel file (.xlsx format)
2. **File Processing**: System reads Excel file and identifies image URL columns
3. **Data Extraction**: Extract image URLs and existing alt text data
4. **Image Analysis**: Download images and generate alt text using Google Gemini AI Vision API
5. **Data Update**: Update Excel file with generated alt text
6. **File Download**: Provide processed Excel file for download

## External Dependencies

### Core Libraries
- **Flask**: Web framework
- **openpyxl**: Excel file processing
- **PIL (Pillow)**: Image processing and validation
- **requests**: HTTP requests for image downloading
- **google-genai**: Google Gemini AI API integration

### Frontend Dependencies
- **Bootstrap**: CSS framework (via CDN)
- **Font Awesome**: Icon library (via CDN)

### Environment Variables
- **GEMINI_API_KEY**: Required for AI-powered alt text generation
- **SESSION_SECRET**: Optional, defaults to development key

## Deployment Strategy

### Local Development
- Uses Flask development server
- Debug mode enabled
- Hot reloading for code changes
- Local file storage for uploads

### Production Considerations
- File upload limits: 16MB maximum
- Temporary file cleanup required
- Environment variable management for API keys
- HTTPS recommended for production deployment

### File Structure
```
/uploads/     # Uploaded Excel files
/temp/        # Temporary processing files
/static/      # CSS and JavaScript assets
/templates/   # HTML templates
```

## Changelog
- July 08, 2025. Initial setup with OpenAI Vision API
- July 08, 2025. Switched from OpenAI to Google Gemini AI for alt text generation

## User Preferences

Preferred communication style: Simple, everyday language.