#!/usr/bin/env python3
"""
Simple server to test frontend issues
"""

from flask import Flask, send_file, request, jsonify
import os

app = Flask(__name__)

@app.route('/')
def serve_test_page():
    """Serve the test HTML page"""
    return send_file('test_frontend.html')

@app.route('/analyze', methods=['POST'])
def test_analyze():
    """Simple test analyze endpoint"""
    print("📡 Received analyze request")
    print(f"Files: {list(request.files.keys())}")
    print(f"Form data: {list(request.form.keys())}")
    
    if 'audio_file' not in request.files:
        print("❌ No audio file in request")
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    print(f"📁 Audio file: {audio_file.filename}")
    print(f"📏 File size: {len(audio_file.read())} bytes")
    audio_file.seek(0)  # Reset file pointer
    
    # Simple success response
    return jsonify({
        'success': True,
        'message': 'Test successful!',
        'filename': audio_file.filename
    })

if __name__ == '__main__':
    print("🧪 FRONTEND TEST SERVER")
    print("=" * 30)
    print("🌐 Open browser to: http://127.0.0.1:5001")
    print("📝 This will help debug the 'Network error' issue")
    print("=" * 30)
    
    app.run(debug=True, port=5001)