#!/usr/bin/env python3
"""
Enhanced Error Handling & Recovery Module
Provides comprehensive error handling for all system components
"""

import os
import logging
from functools import wraps

class SpeechAnalysisError(Exception):
    """Base exception for speech analysis errors"""
    pass

class AudioProcessingError(SpeechAnalysisError):
    """Errors related to audio file processing"""
    pass

class TranscriptionError(SpeechAnalysisError):
    """Errors related to speech-to-text conversion"""
    pass

class AnalysisError(SpeechAnalysisError):
    """Errors related to speech analysis"""
    pass

class ErrorHandler:
    """Comprehensive error handling and recovery system"""
    
    def __init__(self):
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging for error tracking"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('speech_analysis.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def handle_audio_error(self, error, file_path):
        """Handle audio processing errors with specific guidance"""
        error_msg = str(error).lower()
        
        if "no such file" in error_msg or "file not found" in error_msg:
            return {
                'error_type': 'FILE_NOT_FOUND',
                'user_message': f'Audio file not found: {os.path.basename(file_path)}',
                'suggestion': 'Please check that the file exists and try uploading again.',
                'technical_details': str(error)
            }
        
        elif "unsupported format" in error_msg or "codec" in error_msg:
            return {
                'error_type': 'UNSUPPORTED_FORMAT',
                'user_message': 'Audio format not supported or corrupted',
                'suggestion': 'Please use WAV, MP3, M4A, FLAC, or WebM format. Try converting your file to WAV.',
                'technical_details': str(error)
            }
        
        elif "ffmpeg" in error_msg:
            return {
                'error_type': 'FFMPEG_ERROR',
                'user_message': 'Audio conversion failed',
                'suggestion': 'FFmpeg may not be properly installed. Try using WAV format instead.',
                'technical_details': str(error)
            }
        
        elif "permission" in error_msg or "access" in error_msg:
            return {
                'error_type': 'PERMISSION_ERROR',
                'user_message': 'Cannot access audio file',
                'suggestion': 'Check file permissions or try saving the file to a different location.',
                'technical_details': str(error)
            }
        
        else:
            return {
                'error_type': 'AUDIO_PROCESSING_ERROR',
                'user_message': 'Failed to process audio file',
                'suggestion': 'Try using a different audio file or convert to WAV format.',
                'technical_details': str(error)
            }
    
    def handle_transcription_error(self, error):
        """Handle speech-to-text errors with specific guidance"""
        error_msg = str(error).lower()
        
        if "unknown value" in error_msg or "could not understand" in error_msg:
            return {
                'error_type': 'SPEECH_NOT_RECOGNIZED',
                'user_message': 'Could not understand the speech in the audio',
                'suggestion': 'Please ensure clear speech with minimal background noise. Try recording in a quiet environment.',
                'technical_details': str(error)
            }
        
        elif "request error" in error_msg or "network" in error_msg:
            return {
                'error_type': 'NETWORK_ERROR',
                'user_message': 'Speech recognition service unavailable',
                'suggestion': 'Check your internet connection and try again.',
                'technical_details': str(error)
            }
        
        elif "quota" in error_msg or "limit" in error_msg:
            return {
                'error_type': 'SERVICE_LIMIT',
                'user_message': 'Speech recognition service limit reached',
                'suggestion': 'Please try again later or use a shorter audio file.',
                'technical_details': str(error)
            }
        
        else:
            return {
                'error_type': 'TRANSCRIPTION_ERROR',
                'user_message': 'Speech-to-text conversion failed',
                'suggestion': 'Try with a clearer audio recording or different file format.',
                'technical_details': str(error)
            }
    
    def handle_analysis_error(self, error):
        """Handle analysis errors with specific guidance"""
        error_msg = str(error).lower()
        
        if "empty" in error_msg or "no text" in error_msg:
            return {
                'error_type': 'EMPTY_TRANSCRIPT',
                'user_message': 'No speech content found for analysis',
                'suggestion': 'Ensure your audio contains clear speech and try again.',
                'technical_details': str(error)
            }
        
        elif "duration" in error_msg:
            return {
                'error_type': 'DURATION_ERROR',
                'user_message': 'Could not determine audio duration',
                'suggestion': 'Try using a different audio format or check if the file is corrupted.',
                'technical_details': str(error)
            }
        
        else:
            return {
                'error_type': 'ANALYSIS_ERROR',
                'user_message': 'Speech analysis failed',
                'suggestion': 'Please try again with a different audio file.',
                'technical_details': str(error)
            }
    
    def create_error_response(self, error_info):
        """Create a standardized error response"""
        return {
            'success': False,
            'error': error_info['user_message'],
            'error_type': error_info['error_type'],
            'suggestion': error_info['suggestion'],
            'technical_details': error_info.get('technical_details', '')
        }
    
    def log_error(self, error_type, error_message, context=None):
        """Log error for debugging and monitoring"""
        log_message = f"{error_type}: {error_message}"
        if context:
            log_message += f" | Context: {context}"
        
        self.logger.error(log_message)

def with_error_handling(error_handler):
    """Decorator for adding comprehensive error handling to functions"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Determine error type and handle appropriately
                if "audio" in func.__name__.lower() or "process" in func.__name__.lower():
                    error_info = error_handler.handle_audio_error(e, kwargs.get('file_path', 'unknown'))
                elif "transcr" in func.__name__.lower() or "speech" in func.__name__.lower():
                    error_info = error_handler.handle_transcription_error(e)
                else:
                    error_info = error_handler.handle_analysis_error(e)
                
                # Log the error
                error_handler.log_error(error_info['error_type'], str(e), func.__name__)
                
                # Re-raise with enhanced error info
                raise SpeechAnalysisError(error_info['user_message']) from e
        
        return wrapper
    return decorator

# Global error handler instance
error_handler = ErrorHandler()

def get_user_friendly_error(error):
    """Convert any error to user-friendly message"""
    if isinstance(error, SpeechAnalysisError):
        return str(error)
    
    error_msg = str(error).lower()
    
    # Common error patterns
    if any(pattern in error_msg for pattern in ['file not found', 'no such file']):
        return "Audio file not found. Please check the file and try again."
    
    elif any(pattern in error_msg for pattern in ['permission', 'access denied']):
        return "Cannot access the audio file. Please check file permissions."
    
    elif any(pattern in error_msg for pattern in ['format', 'codec', 'unsupported']):
        return "Audio format not supported. Please use WAV, MP3, M4A, FLAC, or WebM format."
    
    elif any(pattern in error_msg for pattern in ['network', 'connection', 'timeout']):
        return "Network error. Please check your internet connection and try again."
    
    elif any(pattern in error_msg for pattern in ['ffmpeg', 'conversion']):
        return "Audio conversion failed. Try using WAV format or check FFmpeg installation."
    
    else:
        return "An unexpected error occurred. Please try again with a different audio file."

if __name__ == "__main__":
    # Test error handling
    handler = ErrorHandler()
    
    # Test different error types
    test_errors = [
        FileNotFoundError("No such file: test.mp3"),
        Exception("Unsupported codec"),
        Exception("Network timeout"),
        Exception("FFmpeg not found"),
        Exception("Unknown value error")
    ]
    
    print("🧪 TESTING ERROR HANDLING")
    print("=" * 40)
    
    for i, error in enumerate(test_errors, 1):
        print(f"\n{i}. Testing: {error}")
        
        if "file" in str(error).lower():
            error_info = handler.handle_audio_error(error, "test.mp3")
        elif "network" in str(error).lower():
            error_info = handler.handle_transcription_error(error)
        else:
            error_info = handler.handle_analysis_error(error)
        
        print(f"   Error Type: {error_info['error_type']}")
        print(f"   User Message: {error_info['user_message']}")
        print(f"   Suggestion: {error_info['suggestion']}")
    
    print("\n✅ Error handling system ready!")