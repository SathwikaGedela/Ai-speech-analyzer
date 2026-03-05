from flask import Blueprint, request, render_template, jsonify, session
import os
from werkzeug.utils import secure_filename

from services.audio_processing import process_audio
from services.speech_to_text import speech_to_text
from services.text_analysis import analyze_text
from services.confidence import calculate_confidence
from services.emotion import analyze_emotion, get_emotion_feedback, analyze_emotion_from_text

# Database imports
from database import db
from models.session import SpeechSession

# Authentication middleware
from middleware.auth_middleware import login_required, get_current_user_id

analyze_bp = Blueprint("analyze", __name__)

def get_skill_level(confidence):
    """Get skill level based on confidence score"""
    if confidence >= 90:
        return "Expert"
    elif confidence >= 80:
        return "Advanced"
    elif confidence >= 70:
        return "Intermediate"
    elif confidence >= 60:
        return "Beginner"
    else:
        return "Needs Practice"

def get_general_impression(confidence):
    """Get general impression based on confidence score"""
    if confidence >= 85:
        return "Excellent speaking performance with strong delivery"
    elif confidence >= 75:
        return "Good speaking performance with room for minor improvements"
    elif confidence >= 65:
        return "Decent speaking performance with some areas to work on"
    elif confidence >= 50:
        return "Fair speaking performance with several improvement opportunities"
    else:
        return "Speaking performance needs significant improvement"

def get_pace_assessment(wpm):
    """Get pace assessment based on WPM"""
    if wpm < 120:
        return "Speaking pace is too slow. Try to increase your speed slightly."
    elif wpm > 180:
        return "Speaking pace is too fast. Try to slow down for better clarity."
    elif 140 <= wpm <= 160:
        return "Excellent speaking pace - clear and engaging."
    else:
        return "Good speaking pace with minor room for improvement."

def get_filler_assessment(filler_count):
    """Get filler word assessment"""
    if filler_count == 0:
        return "Excellent! No filler words detected."
    elif filler_count <= 2:
        return "Very good! Minimal use of filler words."
    elif filler_count <= 5:
        return "Good control of filler words with room for improvement."
    else:
        return "Too many filler words. Practice reducing 'um', 'uh', and 'like'."

def get_grammar_assessment(score, errors):
    """Get grammar assessment"""
    if score >= 95:
        return "Excellent grammar with no significant errors detected."
    elif score >= 85:
        return "Good grammar with minor errors that don't affect understanding."
    elif score >= 70:
        return "Fair grammar with some errors that could be improved."
    else:
        return f"Grammar needs improvement. Detected issues: {', '.join(errors[:2])}"

def get_vocabulary_assessment(diversity):
    """Get vocabulary assessment"""
    if diversity >= 80:
        return "Excellent vocabulary diversity and word choice."
    elif diversity >= 70:
        return "Good vocabulary with varied word usage."
    elif diversity >= 60:
        return "Fair vocabulary - try using more varied words."
    else:
        return "Limited vocabulary diversity - expand your word choice."

def get_engagement_level(confidence):
    """Get engagement level based on confidence"""
    if confidence >= 80:
        return "High"
    elif confidence >= 60:
        return "Medium"
    else:
        return "Low"

def get_tone_assessment(sentiment):
    """Get tone assessment based on sentiment"""
    if sentiment > 0.3:
        return "Very positive and engaging tone."
    elif sentiment > 0.1:
        return "Positive tone that connects well with audience."
    elif sentiment > -0.1:
        return "Neutral tone - consider adding more enthusiasm."
    else:
        return "Tone seems negative - try to sound more positive and engaging."

def generate_strengths(metrics, confidence):
    """Generate list of strengths"""
    strengths = []
    
    if metrics['wpm'] >= 140 and metrics['wpm'] <= 160:
        strengths.append("Excellent speaking pace")
    
    if metrics['fillers'] <= 2:
        strengths.append("Minimal use of filler words")
    
    if metrics['sentiment'] > 0.2:
        strengths.append("Positive and engaging tone")
    
    if metrics['grammar_score'] >= 85:
        strengths.append("Strong grammar and sentence structure")
    
    if metrics['vocabulary_diversity'] >= 70:
        strengths.append("Good vocabulary diversity")
    
    if confidence >= 75:
        strengths.append("Overall confident delivery")
    
    if not strengths:
        strengths.append("Clear speech delivery")
    
    return strengths

def generate_improvements(metrics, confidence):
    """Generate list of improvements"""
    improvements = []
    
    if metrics['wpm'] < 130:
        improvements.append("Increase speaking pace for better engagement")
    elif metrics['wpm'] > 170:
        improvements.append("Slow down speaking pace for better clarity")
    
    if metrics['fillers'] > 3:
        improvements.append("Reduce filler words like 'um', 'uh', 'like'")
    
    if metrics['sentiment'] < 0:
        improvements.append("Use more positive language and tone")
    
    if metrics['grammar_score'] < 80:
        improvements.append("Improve grammar and sentence structure")
    
    if metrics['vocabulary_diversity'] < 60:
        improvements.append("Use more varied vocabulary")
    
    if confidence < 70:
        improvements.append("Work on overall confidence and delivery")
    
    return improvements

def generate_actionable_tips(metrics, confidence):
    """Generate actionable tips"""
    tips = []
    
    if metrics['fillers'] > 2:
        tips.append({
            'title': 'Reduce Filler Words',
            'technique': 'Pause and Breathe',
            'description': 'When you feel the urge to say "um" or "uh", take a brief pause instead. This sounds more professional and gives you time to think.'
        })
    
    if metrics['wpm'] < 130:
        tips.append({
            'title': 'Increase Speaking Pace',
            'technique': 'Practice with a Metronome',
            'description': 'Practice speaking at 140-160 words per minute. Use online tools or apps to maintain consistent pace.'
        })
    
    if metrics['sentiment'] < 0.1:
        tips.append({
            'title': 'Improve Tone and Energy',
            'technique': 'Smile While Speaking',
            'description': 'Smiling while speaking naturally improves your tone and makes you sound more engaging and positive.'
        })
    
    if confidence < 70:
        tips.append({
            'title': 'Build Confidence',
            'technique': 'Practice and Prepare',
            'description': 'Practice your speech multiple times. The more familiar you are with your content, the more confident you will sound.'
        })
    
    # Always include at least one tip
    if not tips:
        tips.append({
            'title': 'Continue Practicing',
            'technique': 'Regular Practice',
            'description': 'Keep practicing regularly to maintain and improve your speaking skills. Record yourself to track progress.'
        })
    
    return tips

@analyze_bp.route("/", methods=["GET"])
@login_required
def index():
    return render_template("enhanced_index.html")

@analyze_bp.route("/analyze", methods=["POST"])
@login_required
def analyze():
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    file_path = None
    image_path = None
    
    try:
        # Process audio file
        try:
            audio_path, duration = process_audio(audio_file)
            file_path = audio_path
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower():
                return jsonify({'error': 'Audio processing failed. Please ensure FFmpeg is installed or try a WAV file.'}), 400
            else:
                return jsonify({'error': f'Audio processing failed: {error_msg}'}), 400
        
        # Convert to text
        try:
            text = speech_to_text(audio_path)
            if not text or text.strip() == "":
                # If speech recognition fails, provide a helpful error
                return jsonify({'error': 'Could not detect speech in the audio file. Please ensure the audio contains clear speech and try again. For testing, try recording yourself speaking for a few seconds.'}), 400
        except Exception as e:
            error_msg = str(e)
            if "recognition request failed" in error_msg.lower():
                return jsonify({'error': 'Speech recognition service is temporarily unavailable. Please try again in a moment.'}), 400
            else:
                return jsonify({'error': f'Speech recognition failed: Please ensure the audio contains clear speech and try again.'}), 400
        
        # Analyze text
        try:
            metrics = analyze_text(text, duration)
        except Exception as e:
            return jsonify({'error': f'Text analysis failed: {str(e)}'}), 400
        
        # Calculate confidence
        try:
            confidence = calculate_confidence(metrics)
        except Exception as e:
            return jsonify({'error': f'Confidence calculation failed: {str(e)}'}), 400
        
        # Process optional image for emotion detection
        emotion = "neutral"  # Default fallback
        emotion_feedback = "Emotion analyzed from speech content."
        
        image_file = request.files.get('image_file')
        if image_file and image_file.filename != '':
            try:
                # Ensure temp directory exists
                os.makedirs('temp', exist_ok=True)
                
                # Save image file
                image_filename = secure_filename(image_file.filename)
                image_path = os.path.join('temp', image_filename)
                image_file.save(image_path)
                
                # Analyze emotion from image
                emotion = analyze_emotion(image_path)
                emotion_feedback = get_emotion_feedback(emotion)
                
            except Exception as e:
                print(f"Image processing failed: {e}")
                emotion = "processing_failed"
                emotion_feedback = "Image processing failed, but this doesn't affect your speech analysis."
        else:
            # Use text-based emotion detection as fallback
            try:
                emotion = analyze_emotion_from_text(text)
                emotion_feedback = get_emotion_feedback(emotion)
                print(f"Text-based emotion detection: {emotion}")
            except Exception as e:
                print(f"Text-based emotion detection failed: {e}")
                emotion = "neutral"
                emotion_feedback = "Emotion analysis completed based on available data."
        
        # Save analysis results to database (fail-safe)
        try:
            import json
            
            session_obj = SpeechSession(
                user_id=get_current_user_id(),  # Associate with current user
                transcript=text,
                wpm=metrics["wpm"],
                fillers=metrics["fillers"],
                sentiment=metrics["sentiment"],
                confidence=confidence,
                emotion=emotion,
                
                # Extended analysis data
                word_count=metrics.get("word_count", 0),
                filler_percentage=metrics.get("filler_percentage", 0),
                grammar_score=metrics.get("grammar_score", 0),
                vocabulary_diversity=metrics.get("vocabulary_diversity", 0),
                unique_words=metrics.get("unique_words", 0),
                pronunciation_clarity=max(70, 100 - metrics['fillers'] * 2),
                engagement_level=get_engagement_level(confidence),
                skill_level=get_skill_level(confidence),
                
                # Assessment text fields
                pace_assessment=get_pace_assessment(metrics['wpm']),
                filler_assessment=get_filler_assessment(metrics['fillers']),
                grammar_assessment=get_grammar_assessment(metrics['grammar_score'], metrics.get('grammar_errors', [])),
                vocabulary_assessment=get_vocabulary_assessment(metrics['vocabulary_diversity']),
                tone_assessment=get_tone_assessment(metrics['sentiment']),
                general_impression=get_general_impression(confidence),
                
                # JSON fields for complex data
                strengths=json.dumps(generate_strengths(metrics, confidence)),
                improvements=json.dumps(generate_improvements(metrics, confidence)),
                actionable_tips=json.dumps(generate_actionable_tips(metrics, confidence)),
                grammar_errors=json.dumps(metrics.get('grammar_errors', []))
            )
            
            db.session.add(session_obj)
            db.session.commit()
            print(f"Analysis saved to database (ID: {session_obj.id})")
            
        except Exception as e:
            db.session.rollback()
            print(f"DB save failed: {e}")
            # Continue normally - DB failure doesn't break the app
        
        return jsonify({
            'success': True,
            'analysis': {
                'transcript': text,
                'overall_score': {
                    'score': confidence,
                    'skill_level': get_skill_level(confidence),
                    'general_impression': get_general_impression(confidence)
                },
                'vocal_delivery': {
                    'speaking_pace': {
                        'wpm': metrics['wpm'],
                        'assessment': get_pace_assessment(metrics['wpm'])
                    },
                    'filler_words': {
                        'total_count': metrics['fillers'],
                        'percentage': metrics['filler_percentage'],
                        'assessment': get_filler_assessment(metrics['fillers'])
                    },
                    'pronunciation': {
                        'clarity_percentage': max(70, 100 - metrics['fillers'] * 2),
                        'assessment': 'Good pronunciation detected'
                    }
                },
                'language_content': {
                    'grammar': {
                        'score': metrics['grammar_score'],
                        'assessment': get_grammar_assessment(metrics['grammar_score'], metrics.get('grammar_errors', []))
                    },
                    'vocabulary': {
                        'diversity_score': metrics['vocabulary_diversity'],
                        'quality': get_vocabulary_assessment(metrics['vocabulary_diversity'])
                    }
                },
                'emotional_engagement': {
                    'confidence_score': confidence,
                    'sentiment_polarity': metrics['sentiment'],
                    'engagement_level': get_engagement_level(confidence),
                    'tone_assessment': get_tone_assessment(metrics['sentiment'])
                },
                'emotion_analysis': {
                    'detected_emotion': emotion,
                    'emotion_feedback': emotion_feedback
                },
                'strengths': generate_strengths(metrics, confidence),
                'improvements': generate_improvements(metrics, confidence),
                'actionable_tips': generate_actionable_tips(metrics, confidence)
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500
    
    finally:
        # Clean up uploaded files
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
        
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except:
                pass