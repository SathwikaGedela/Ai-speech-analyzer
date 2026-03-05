#!/usr/bin/env python3
"""
Debug the backend to find the issue
"""

import sys
import os

# Add backend to path
sys.path.insert(0, 'backend')

try:
    from services.audio_processing import process_audio
    from services.speech_to_text import speech_to_text
    from services.text_analysis import analyze_text
    from services.confidence import calculate_confidence
    
    print("✅ All imports successful")
    
    # Test with a simple mock
    class MockFile:
        def __init__(self, filename):
            self.filename = filename
        
        def save(self, path):
            # Just create an empty file for testing
            with open(path, 'w') as f:
                f.write("test")
    
    # Test audio processing
    print("Testing audio processing...")
    try:
        mock_file = MockFile("test.wav")
        # This will fail but let's see the error
        result = process_audio(mock_file)
        print(f"Audio processing result: {result}")
    except Exception as e:
        print(f"Audio processing error: {e}")
    
    # Test text analysis
    print("Testing text analysis...")
    try:
        result = analyze_text("Hello world this is a test", 10.0)
        print(f"Text analysis result: {result}")
    except Exception as e:
        print(f"Text analysis error: {e}")
    
    # Test confidence calculation
    print("Testing confidence calculation...")
    try:
        metrics = {"wpm": 120, "fillers": 2, "sentiment": 0.1}
        result = calculate_confidence(metrics)
        print(f"Confidence result: {result}")
    except Exception as e:
        print(f"Confidence calculation error: {e}")

except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")