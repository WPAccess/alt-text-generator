import os
import uuid
import json
from flask import render_template, request, jsonify, send_file, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app import app
from excel_processor import ExcelProcessor
from image_analyzer import ImageAnalyzer
import logging

logger = logging.getLogger(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download_sample')
def download_sample():
    """Download a sample Excel file to show users the expected format"""
    try:
        sample_file_path = 'sample_images.xlsx'
        if os.path.exists(sample_file_path):
            return send_file(
                sample_file_path,
                as_attachment=True,
                download_name='sample_excel_format.xlsx',
                mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        else:
            return jsonify({'error': 'Sample file not found'}), 404
    except Exception as e:
        logger.error(f"Sample download error: {str(e)}")
        return jsonify({'error': 'Failed to download sample file'}), 500

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not file.filename.lower().endswith('.xlsx'):
            return jsonify({'error': 'Please upload an Excel file (.xlsx)'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)
        
        # Process Excel file
        processor = ExcelProcessor(filepath)
        data = processor.read_excel()
        
        if not data:
            return jsonify({'error': 'No data found in Excel file'}), 400
        
        return jsonify({
            'success': True,
            'filename': unique_filename,
            'data': data,
            'message': f'File uploaded successfully. Found {len(data)} rows.'
        })
        
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/generate_alt_text', methods=['POST'])
def generate_alt_text():
    try:
        data = request.get_json()
        filename = data.get('filename')
        row_indices = data.get('row_indices', [])
        
        if not filename or not row_indices:
            return jsonify({'error': 'Missing filename or row indices'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Process each row
        processor = ExcelProcessor(filepath)
        analyzer = ImageAnalyzer()
        
        results = []
        for row_index in row_indices:
            try:
                # Get image URL from Excel
                image_url = processor.get_image_url(row_index)
                if not image_url:
                    results.append({
                        'row_index': row_index,
                        'success': False,
                        'error': 'No image URL found'
                    })
                    continue
                
                # Generate alt text
                alt_text = analyzer.generate_alt_text(image_url)
                
                results.append({
                    'row_index': row_index,
                    'success': True,
                    'alt_text': alt_text
                })
                
            except Exception as e:
                logger.error(f"Error processing row {row_index}: {str(e)}")
                results.append({
                    'row_index': row_index,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'success': True,
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Generate alt text error: {str(e)}")
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500

@app.route('/download', methods=['POST'])
def download_file():
    try:
        data = request.get_json()
        filename = data.get('filename')
        updated_data = data.get('data', [])
        
        if not filename or not updated_data:
            return jsonify({'error': 'Missing filename or data'}), 400
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Create updated Excel file
        processor = ExcelProcessor(filepath)
        output_filename = f"updated_{filename}"
        output_path = os.path.join(app.config['TEMP_FOLDER'], output_filename)
        
        processor.update_excel(updated_data, output_path)
        
        return send_file(
            output_path,
            as_attachment=True,
            download_name=output_filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        logger.error(f"Download error: {str(e)}")
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error occurred.'}), 500
