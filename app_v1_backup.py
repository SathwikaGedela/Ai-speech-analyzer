from flask import Flask, request, render_template, jsonify
import os
from enhanced_analyzer import EnhancedSpeechAnalyzer
from werkzeug.utils import secure_filename
from error_handler import ErrorHandler, get_user_friendly_error
from audio_quality_checker import AudioQualityChecker

# Set FFmpeg path for pydub
ffmpeg_path = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
if os.path.exists(ffmpeg_path):
    os.environ["PATH"] += os.pathsep + ffmpeg_path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm', 'flac', 'm4a'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

analyzer = EnhancedSpeechAnalyzer()
error_handler = ErrorHandler()
quality_checker = AudioQualityChecker()

@app.route('/')
def index():
    return render_template('enhanced_index.html')

@app.route('/analyze', methods=['POST'])
def analyze_speech():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Please upload supported audio files (WAV, MP3, M4A, FLAC, WebM).'}), 400
    
    file_path = None
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Assess audio quality
        quality_assessment = quality_checker.assess_audio_quality(file_path)
        quality_score = quality_checker.get_quality_score(quality_assessment)
        
        # Warn about quality issues but don't block processing
        quality_warnings = []
        if quality_assessment['overall_quality'] == 'poor':
            quality_warnings.append("Audio quality is poor. Results may be less accurate.")
        elif quality_assessment['overall_quality'] == 'fair':
            quality_warnings.append("Audio quality could be better for optimal results.")
        
        # Add specific recommendations
        if quality_assessment['recommendations']:
            quality_warnings.extend(quality_assessment['recommendations'][:2])  # Top 2 recommendations
        
        # Convert audio to text with enhanced error handling
        try:
            transcript = analyzer.audio_to_text(file_path)
            if not transcript:
                return jsonify({
                    'error': 'Could not transcribe audio. Please ensure clear speech and good audio quality.',
                    'suggestion': 'Try recording in a quiet environment with clear pronunciation.'
                }), 400
        except Exception as e:
            error_info = error_handler.handle_transcription_error(e)
            return jsonify(error_handler.create_error_response(error_info)), 400
        
        # Get audio duration with enhanced error handling
        try:
            audio_duration = analyzer._get_audio_duration(file_path)
        except Exception as e:
            error_info = error_handler.handle_audio_error(e, file_path)
            # Use fallback duration but log the error
            error_handler.log_error('DURATION_FALLBACK', str(e), file_path)
            audio_duration = 60  # Fallback duration
        
        # Perform comprehensive analysis with enhanced error handling
        try:
            analysis = analyzer.comprehensive_analysis(transcript, audio_duration)
        except Exception as e:
            error_info = error_handler.handle_analysis_error(e)
            return jsonify(error_handler.create_error_response(error_info)), 500
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'audio_quality': {
                'score': quality_score,
                'assessment': quality_assessment['overall_quality'],
                'warnings': quality_warnings
            }
        })
    
    except Exception as e:
        # Catch-all error handling
        user_friendly_error = get_user_friendly_error(e)
        error_handler.log_error('UNEXPECTED_ERROR', str(e), request.endpoint)
        
        return jsonify({
            'error': user_friendly_error,
            'suggestion': 'Please try again with a different audio file or contact support if the problem persists.'
        }), 500
    
    finally:
        # Clean up uploaded file
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Don't fail if cleanup fails

if __name__ == '__main__':
    print("🚀 Starting Enhanced AI Public Speaking Feedback System")
    print("📁 Upload directory:", app.config['UPLOAD_FOLDER'])
    print("🎵 Supported formats: WAV, MP3, WebM, FLAC, M4A")
    print("🌐 Access at: http://127.0.0.1:5000")
    print("✨ Now with comprehensive professional analysis!")
    app.run(debug=True)