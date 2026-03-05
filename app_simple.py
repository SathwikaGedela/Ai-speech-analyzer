from flask import Flask, request, render_template, jsonify
import os
import speech_recognition as sr
from textblob import TextBlob
import re
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'wav', 'mp3'}

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
                try:
                    # Import pydub and set FFmpeg path explicitly
                    from pydub import AudioSegment
                    
                    # Set FFmpeg path explicitly for this session
                    ffmpeg_dir = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
                    if os.path.exists(ffmpeg_dir):
                        AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                        AudioSegment.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                        AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")
                    
                    # Load MP3 and convert to WAV
                    audio_segment = AudioSegment.from_mp3(audio_file_path)
                    
                    # Create temporary WAV file in the uploads directory
                    temp_wav_path = audio_file_path.replace('.mp3', '_temp.wav')
                    
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
                            
                except Exception as mp3_error:
                    # If MP3 processing fails, provide helpful error message
                    error_msg = f"MP3 processing failed: {str(mp3_error)}. "
                    error_msg += "Please try converting your MP3 to WAV format using an online converter like cloudconvert.com"
                    raise Exception(error_msg)
            
            else:
                raise Exception("Unsupported audio format. Please use WAV or MP3 files.")
                
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            raise Exception(f"Speech recognition error: {e}")
        except Exception as e:
            raise Exception(f"Audio processing error: {e}")
    
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
    
    def generate_feedback(self, analysis_results):
        """Generate personalized feedback based on analysis"""
        feedback = []
        
        # Speaking speed feedback
        wpm = analysis_results['speaking_speed']
        if wpm < 120:
            feedback.append("Consider speaking a bit faster. Aim for 120-160 words per minute for optimal clarity.")
        elif wpm > 180:
            feedback.append("You're speaking quite fast. Try slowing down to 120-160 words per minute for better comprehension.")
        else:
            feedback.append("Great speaking pace! You're within the optimal range of 120-160 words per minute.")
        
        # Filler words feedback
        total_fillers = analysis_results['total_filler_words']
        word_count = len(analysis_results['transcript'].split())
        filler_percentage = (total_fillers / word_count) * 100 if word_count > 0 else 0
        
        if filler_percentage > 5:
            feedback.append(f"Try to reduce filler words. You used {total_fillers} filler words ({filler_percentage:.1f}% of your speech).")
        elif filler_percentage > 2:
            feedback.append("Good job keeping filler words to a minimum. A few less would make your speech even more polished.")
        else:
            feedback.append("Excellent! You kept filler words to a minimum, making your speech clear and professional.")
        
        # Sentiment feedback
        sentiment_data = analysis_results['sentiment']
        if sentiment_data['sentiment'] == 'Positive':
            feedback.append("Your speech has a positive tone, which helps engage your audience.")
        elif sentiment_data['sentiment'] == 'Negative':
            feedback.append("Consider adding more positive language to create a more engaging atmosphere.")
        else:
            feedback.append("Your speech maintains a neutral tone. Consider adding more emotional expression where appropriate.")
        
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
        return jsonify({'error': 'Invalid file format. Please upload WAV or MP3 files.'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Convert audio to text
        transcript = analyzer.audio_to_text(file_path)
        if not transcript:
            return jsonify({'error': 'Could not transcribe audio. Please ensure clear speech and good audio quality.'}), 400
        
        # Get audio duration using pydub
        try:
            from pydub import AudioSegment
            
            # Set FFmpeg path for duration calculation too
            ffmpeg_dir = r"C:\Users\USER\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.0.1-full_build\bin"
            if os.path.exists(ffmpeg_dir):
                AudioSegment.converter = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffmpeg = os.path.join(ffmpeg_dir, "ffmpeg.exe")
                AudioSegment.ffprobe = os.path.join(ffmpeg_dir, "ffprobe.exe")
            
            audio_segment = AudioSegment.from_file(file_path)
            audio_duration = len(audio_segment) / 1000.0  # Convert to seconds
        except:
            # Fallback if pydub fails
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
    app.run(debug=True)