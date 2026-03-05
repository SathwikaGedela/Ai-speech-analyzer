from flask import Flask, request, render_template, jsonify
import os
import speech_recognition as sr
from textblob import TextBlob
import re
from werkzeug.utils import secure_filename
import subprocess
import sys

# Add FFmpeg to PATH at the very beginning
def setup_ffmpeg():
    """Setup FFmpeg path for the entire application"""
    ffmpeg_paths = [
        r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin",
        r"C:\ffmpeg\bin",
        r"C:\Program Files\ffmpeg\bin"
    ]
    
    for path in ffmpeg_paths:
        if os.path.exists(os.path.join(path, "ffmpeg.exe")):
            # Add to system PATH
            if path not in os.environ.get("PATH", ""):
                os.environ["PATH"] = os.environ.get("PATH", "") + os.pathsep + path
            
            # Set for pydub specifically
            try:
                from pydub import AudioSegment
                AudioSegment.converter = os.path.join(path, "ffmpeg.exe")
                AudioSegment.ffmpeg = os.path.join(path, "ffmpeg.exe")
                AudioSegment.ffprobe = os.path.join(path, "ffprobe.exe")
                print(f"✅ FFmpeg configured: {path}")
                return True
            except ImportError:
                pass
            break
    
    print("⚠️ FFmpeg not found - MP3 support may not work")
    return False

# Setup FFmpeg before anything else
setup_ffmpeg()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class SpeechAnalyzer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.filler_words = ['um', 'uh', 'like', 'you know', 'so', 'actually', 'basically', 'literally']
    
    def audio_to_text(self, audio_file_path):
        """Convert audio file to text using speech recognition"""
        try:
            # Handle WAV files directly
            if audio_file_path.lower().endswith('.wav'):
                with sr.AudioFile(audio_file_path) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
                    return text
            
            # Handle MP3 files by converting to WAV first
            elif audio_file_path.lower().endswith('.mp3'):
                return self._process_mp3_file(audio_file_path)
            
            # Handle WebM files (from browser recording)
            elif audio_file_path.lower().endswith('.webm'):
                return self._process_webm_file(audio_file_path)
            
            else:
                raise Exception("Unsupported audio format. Please use WAV or MP3 files.")
                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise Exception(f"Speech recognition error: {e}")
        except Exception as e:
            raise Exception(f"Audio processing error: {e}")
    
    def _process_mp3_file(self, audio_file_path):
        """Process MP3 file with multiple fallback methods"""
        
        # Method 1: Try with pydub and explicit FFmpeg path
        try:
            from pydub import AudioSegment
            
            # Ensure FFmpeg is set for pydub
            ffmpeg_dir = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
            if os.path.exists(ffmpeg_dir):
                AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")
            
            # Load MP3 and convert to WAV
            audio_segment = AudioSegment.from_mp3(audio_file_path)
            
            # Create temporary WAV file in uploads directory
            temp_wav_path = os.path.join('uploads', 'temp_' + os.path.basename(audio_file_path).replace('.mp3', '.wav'))
            
            try:
                audio_segment.export(temp_wav_path, format="wav")
                
                with sr.AudioFile(temp_wav_path) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
                    return text
            finally:
                # Clean up temporary file
                if os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)
                    
        except Exception as pydub_error:
            # Method 2: Try using FFmpeg directly via subprocess
            try:
                return self._convert_mp3_with_subprocess(audio_file_path)
            except Exception as subprocess_error:
                # Method 3: Provide helpful error message
                error_msg = f"MP3 processing failed with multiple methods:\n"
                error_msg += f"1. pydub error: {pydub_error}\n"
                error_msg += f"2. subprocess error: {subprocess_error}\n"
                error_msg += "Please convert your MP3 to WAV format using an online converter like cloudconvert.com"
                raise Exception(error_msg)
    
    def _convert_mp3_with_subprocess(self, audio_file_path):
        """Convert MP3 to WAV using FFmpeg subprocess"""
        
        ffmpeg_exe = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
        
        if not os.path.exists(ffmpeg_exe):
            raise Exception("FFmpeg executable not found")
        
        temp_wav_path = os.path.join('uploads', 'temp_' + os.path.basename(audio_file_path).replace('.mp3', '.wav'))
        
        try:
            # Use FFmpeg to convert MP3 to WAV
            cmd = [ffmpeg_exe, '-i', audio_file_path, '-acodec', 'pcm_s16le', '-ar', '16000', temp_wav_path, '-y']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg conversion failed: {result.stderr}")
            
            # Process the converted WAV file
            with sr.AudioFile(temp_wav_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
    
    def _process_webm_file(self, audio_file_path):
        """Process WebM file from browser recording"""
        
        # Method 1: Try with pydub and explicit FFmpeg path
        try:
            from pydub import AudioSegment
            
            # Ensure FFmpeg is set for pydub
            ffmpeg_dir = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
            if os.path.exists(ffmpeg_dir):
                AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")
            
            # Load WebM and convert to WAV
            audio_segment = AudioSegment.from_file(audio_file_path, format="webm")
            
            # Create temporary WAV file in uploads directory
            temp_wav_path = os.path.join('uploads', 'temp_' + os.path.basename(audio_file_path).replace('.webm', '.wav'))
            
            try:
                # Export as WAV with specific parameters for speech recognition
                audio_segment.export(temp_wav_path, format="wav", 
                                   parameters=["-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1"])
                
                with sr.AudioFile(temp_wav_path) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
                    return text
            finally:
                # Clean up temporary file
                if os.path.exists(temp_wav_path):
                    os.remove(temp_wav_path)
                    
        except Exception as pydub_error:
            # Method 2: Try using FFmpeg directly via subprocess
            try:
                return self._convert_webm_with_subprocess(audio_file_path)
            except Exception as subprocess_error:
                # Method 3: Provide helpful error message
                error_msg = f"WebM processing failed with multiple methods:\n"
                error_msg += f"1. pydub error: {pydub_error}\n"
                error_msg += f"2. subprocess error: {subprocess_error}\n"
                error_msg += "This may be due to browser recording format. Try using file upload instead."
                raise Exception(error_msg)
    
    def _convert_webm_with_subprocess(self, audio_file_path):
        """Convert WebM to WAV using FFmpeg subprocess"""
        
        ffmpeg_exe = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin\ffmpeg.exe"
        
        if not os.path.exists(ffmpeg_exe):
            raise Exception("FFmpeg executable not found")
        
        temp_wav_path = os.path.join('uploads', 'temp_' + os.path.basename(audio_file_path).replace('.webm', '.wav'))
        
        try:
            # Use FFmpeg to convert WebM to WAV with speech recognition compatible settings
            cmd = [ffmpeg_exe, '-i', audio_file_path, '-acodec', 'pcm_s16le', '-ar', '16000', '-ac', '1', temp_wav_path, '-y']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise Exception(f"FFmpeg conversion failed: {result.stderr}")
            
            # Process the converted WAV file
            with sr.AudioFile(temp_wav_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
                
        finally:
            # Clean up temporary file
            if os.path.exists(temp_wav_path):
                os.remove(temp_wav_path)
    
    def calculate_speaking_speed(self, text, audio_duration):
        """Calculate words per minute"""
        word_count = len(text.split())
        duration_minutes = audio_duration / 60
        wpm = word_count / duration_minutes if duration_minutes > 0 else 0
        return round(wpm, 2)
    
    def analyze_filler_words(self, text):
        """Count filler words in the speech"""
        text_lower = text.lower()
        filler_count = {}
        total_fillers = 0
        
        for filler in self.filler_words:
            count = len(re.findall(r'\b' + re.escape(filler) + r'\b', text_lower))
            if count > 0:
                filler_count[filler] = count
                total_fillers += count
        
        return filler_count, total_fillers
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the speech"""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        if polarity > 0.1:
            sentiment = "Positive"
        elif polarity < -0.1:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        
        return {
            'sentiment': sentiment,
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3)
        }
    
    def calculate_confidence_score(self, analysis_results):
        """Calculate overall confidence score based on multiple factors"""
        score = 100  # Start with perfect score
        
        # Speaking speed factor (optimal: 120-160 WPM)
        wpm = analysis_results['speaking_speed']
        if wpm < 100 or wpm > 200:
            score -= 25
        elif wpm < 120 or wpm > 180:
            score -= 15
        elif wpm < 130 or wpm > 170:
            score -= 5
        
        # Filler words factor
        word_count = len(analysis_results['transcript'].split())
        filler_percentage = (analysis_results['total_filler_words'] / word_count) * 100 if word_count > 0 else 0
        
        if filler_percentage > 8:
            score -= 30
        elif filler_percentage > 5:
            score -= 20
        elif filler_percentage > 3:
            score -= 10
        elif filler_percentage > 1:
            score -= 5
        
        # Sentiment factor
        polarity = analysis_results['sentiment']['polarity']
        if polarity < -0.3:
            score -= 15
        elif polarity < -0.1:
            score -= 10
        elif polarity > 0.3:
            score += 5
        
        # Speech length factor (too short or too long can indicate nervousness)
        if word_count < 20:
            score -= 10  # Too short
        elif word_count > 300:
            score -= 5   # Might be rambling
        
        # Ensure score is between 0 and 100
        score = max(0, min(100, score))
        
        return round(score, 1)
    
    def get_confidence_level(self, score):
        """Convert confidence score to descriptive level"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 55:
            return "Fair"
        elif score >= 40:
            return "Needs Improvement"
        else:
            return "Poor"
    
    def get_confidence_feedback(self, score, analysis_results):
        """Generate specific feedback based on confidence score"""
        level = self.get_confidence_level(score)
        feedback = []
        
        if score >= 85:
            feedback.append("🌟 Excellent confidence! Your speech demonstrates strong communication skills.")
        elif score >= 70:
            feedback.append("👍 Good confidence level. Minor improvements could make your speech even better.")
        elif score >= 55:
            feedback.append("📈 Fair confidence. Focus on the areas highlighted below for improvement.")
        elif score >= 40:
            feedback.append("⚠️ Your confidence needs improvement. Practice the suggested areas below.")
        else:
            feedback.append("🔄 Low confidence detected. Consider practicing more and focusing on the key areas.")
        
        # Add specific improvement suggestions based on score factors
        wpm = analysis_results['speaking_speed']
        filler_percentage = (analysis_results['total_filler_words'] / len(analysis_results['transcript'].split())) * 100
        
        if wpm < 120:
            feedback.append("💡 Tip: Practice speaking at a slightly faster pace to sound more confident.")
        elif wpm > 180:
            feedback.append("💡 Tip: Slow down your speech to appear more composed and confident.")
        
        if filler_percentage > 5:
            feedback.append("💡 Tip: Reduce filler words by pausing instead of saying 'um' or 'uh'.")
        
        if analysis_results['sentiment']['polarity'] < 0:
            feedback.append("💡 Tip: Use more positive language to boost your confident tone.")
        
        return feedback
    
    def generate_feedback(self, analysis_results):
        """Generate personalized feedback based on analysis"""
        feedback = []
        
        # Calculate confidence score first
        confidence_score = self.calculate_confidence_score(analysis_results)
        confidence_level = self.get_confidence_level(confidence_score)
        
        # Add confidence score to results
        analysis_results['confidence_score'] = confidence_score
        analysis_results['confidence_level'] = confidence_level
        
        # Add confidence feedback
        confidence_feedback = self.get_confidence_feedback(confidence_score, analysis_results)
        feedback.extend(confidence_feedback)
        
        # Overall confidence summary
        feedback.append(f"🎯 Overall Confidence Score: {confidence_score}/100 ({confidence_level})")
        
        # Speaking speed feedback
        wpm = analysis_results['speaking_speed']
        if wpm < 120:
            feedback.append("🐌 Consider speaking a bit faster. Aim for 120-160 words per minute for optimal clarity.")
        elif wpm > 180:
            feedback.append("🏃 You're speaking quite fast. Try slowing down to 120-160 words per minute for better comprehension.")
        else:
            feedback.append("✅ Great speaking pace! You're within the optimal range of 120-160 words per minute.")
        
        # Filler words feedback
        total_fillers = analysis_results['total_filler_words']
        word_count = len(analysis_results['transcript'].split())
        filler_percentage = (total_fillers / word_count) * 100 if word_count > 0 else 0
        
        if filler_percentage > 5:
            feedback.append(f"🚫 Try to reduce filler words. You used {total_fillers} filler words ({filler_percentage:.1f}% of your speech).")
        elif filler_percentage > 2:
            feedback.append("⚠️ Good job keeping filler words to a minimum. A few less would make your speech even more polished.")
        else:
            feedback.append("✅ Excellent! You kept filler words to a minimum, making your speech clear and professional.")
        
        # Sentiment feedback
        sentiment_data = analysis_results['sentiment']
        if sentiment_data['sentiment'] == 'Positive':
            feedback.append("😊 Your speech has a positive tone, which helps engage your audience.")
        elif sentiment_data['sentiment'] == 'Negative':
            feedback.append("😐 Consider adding more positive language to create a more engaging atmosphere.")
        else:
            feedback.append("😐 Your speech maintains a neutral tone. Consider adding more emotional expression where appropriate.")
        
        return feedback
        return feedback

analyzer = SpeechAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_speech():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    file = request.files['audio_file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file format. Please upload WAV, MP3, or WebM files.'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Convert audio to text
        transcript = analyzer.audio_to_text(file_path)
        if not transcript:
            return jsonify({'error': 'Could not transcribe audio. Please ensure clear speech and good audio quality.'}), 400
        
        # Get audio duration
        try:
            from pydub import AudioSegment
            
            # Set FFmpeg path for duration calculation
            ffmpeg_dir = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
            if os.path.exists(ffmpeg_dir):
                AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")
            
            if file_path.lower().endswith('.webm'):
                audio_segment = AudioSegment.from_file(file_path, format="webm")
            else:
                audio_segment = AudioSegment.from_file(file_path)
            audio_duration = len(audio_segment) / 1000.0  # Convert to seconds
        except:
            # Fallback duration estimation
            audio_duration = 60  # Default assumption
        
        # Perform analysis
        speaking_speed = analyzer.calculate_speaking_speed(transcript, audio_duration)
        filler_words, total_fillers = analyzer.analyze_filler_words(transcript)
        sentiment_analysis = analyzer.analyze_sentiment(transcript)
        
        analysis_results = {
            'transcript': transcript,
            'speaking_speed': speaking_speed,
            'filler_words': filler_words,
            'total_filler_words': total_fillers,
            'sentiment': sentiment_analysis
        }
        
        feedback = analyzer.generate_feedback(analysis_results)
        
        # Clean up uploaded file
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'analysis': analysis_results,
            'feedback': feedback
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting AI Public Speaking Feedback System")
    print("📁 Upload directory:", app.config['UPLOAD_FOLDER'])
    print("🎵 Supported formats: WAV, MP3")
    print("🌐 Access at: http://127.0.0.1:5000")
    app.run(debug=True)