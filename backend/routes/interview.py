from flask import Blueprint, render_template, request, jsonify, session
import os
from werkzeug.utils import secure_filename

from utils.interview_questions import INTERVIEW_QUESTIONS, get_questions_by_category, get_all_categories
from services.audio_processing import process_audio
from services.speech_to_text import speech_to_text
from services.text_analysis import analyze_text
from services.confidence import calculate_confidence
from services.emotion import analyze_emotion_from_text, get_emotion_feedback
from services.question_relevance_simple import QuestionRelevanceAnalyzer
from services.interview_chatbot import interview_chatbot
from services.universal_chatbot import universal_chatbot

# Database imports for storing interview sessions
from database import db
from models.session import SpeechSession

# Authentication middleware
from middleware.auth_middleware import login_required, get_current_user_id

interview_bp = Blueprint("interview", __name__)

def get_interview_specific_feedback(question, transcript, metrics, confidence):
    """Generate interview-specific feedback based on the question and answer"""
    
    feedback = {
        "question_relevance": "Good",
        "answer_structure": "Clear",
        "specific_tips": []
    }
    
    # Analyze answer relevance to question
    question_lower = question.lower()
    transcript_lower = transcript.lower()
    
    # Question-specific analysis
    if "tell me about yourself" in question_lower:
        if len(transcript.split()) < 30:
            feedback["specific_tips"].append("Your answer is quite brief. Aim for 60-90 seconds covering your background, skills, and career goals.")
        if "experience" not in transcript_lower and "background" not in transcript_lower:
            feedback["specific_tips"].append("Consider mentioning your relevant experience and background.")
    
    elif "strengths and weaknesses" in question_lower:
        if "strength" not in transcript_lower and "weakness" not in transcript_lower:
            feedback["specific_tips"].append("Make sure to clearly address both strengths and weaknesses.")
        if "improve" not in transcript_lower and "working on" not in transcript_lower:
            feedback["specific_tips"].append("When discussing weaknesses, mention how you're working to improve them.")
    
    elif "why should we hire you" in question_lower:
        if "value" not in transcript_lower and "contribute" not in transcript_lower:
            feedback["specific_tips"].append("Focus on the value you can bring to the company and role.")
        if len(transcript.split()) < 40:
            feedback["specific_tips"].append("This is a key question - provide more detailed examples of your qualifications.")
    
    elif "challenging situation" in question_lower or "difficult" in question_lower:
        if "situation" not in transcript_lower and "challenge" not in transcript_lower:
            feedback["specific_tips"].append("Clearly describe the challenging situation you faced.")
        if "result" not in transcript_lower and "outcome" not in transcript_lower:
            feedback["specific_tips"].append("Don't forget to mention the positive outcome or what you learned.")
    
    # General interview feedback
    if metrics['fillers'] > 5:
        feedback["specific_tips"].append("Reduce filler words (um, uh, like) - practice pausing instead.")
    
    if metrics['wpm'] < 120:
        feedback["specific_tips"].append("Speak a bit faster - aim for 140-160 words per minute in interviews.")
    elif metrics['wpm'] > 180:
        feedback["specific_tips"].append("Slow down slightly - you want to sound confident, not rushed.")
    
    if confidence < 70:
        feedback["specific_tips"].append("Work on sounding more confident - practice your answers beforehand.")
    
    if not feedback["specific_tips"]:
        feedback["specific_tips"].append("Great answer! Keep practicing to maintain this level of performance.")
    
    return feedback

@interview_bp.route("/interview")
@login_required
def interview_home():
    """Interview mode home page"""
    return render_template(
        "interview.html",
        questions=INTERVIEW_QUESTIONS,
        categories=get_all_categories()
    )

@interview_bp.route("/interview/analyze", methods=["POST"])
@login_required
def analyze_interview():
    """Analyze interview answer"""
    
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    audio_file = request.files['audio_file']
    question = request.form.get('question', '')
    category = request.form.get('category', 'general')
    
    if audio_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    
    file_path = None
    
    try:
        # Process audio file
        try:
            audio_path, duration = process_audio(audio_file)
            file_path = audio_path
        except Exception as e:
            error_msg = str(e)
            if "corrupted" in error_msg.lower() or "invalid" in error_msg.lower():
                return jsonify({'error': f'{error_msg} Please try recording again with better audio quality.'}), 400
            elif "webm" in error_msg.lower() and "recording" in error_msg.lower():
                return jsonify({'error': f'{error_msg} You can also try using the file upload option instead.'}), 400
            elif "ffmpeg" in error_msg.lower():
                return jsonify({'error': 'Audio processing failed. FFmpeg is required for this format. Please try uploading a WAV file or ensure FFmpeg is properly installed.'}), 400
            elif "format" in error_msg.lower() or "codec" in error_msg.lower():
                return jsonify({'error': f'Unsupported audio format. Please try converting to WAV, MP3, M4A, or FLAC format. Error: {error_msg}'}), 400
            else:
                return jsonify({'error': f'Audio processing failed: {error_msg}. Please try a different audio file or format.'}), 400
        
        # Convert to text
        try:
            transcript = speech_to_text(audio_path)
            if not transcript or transcript.strip() == "":
                return jsonify({'error': 'Could not detect speech in the audio file. Please ensure the audio contains clear speech and try again. Tips: Speak clearly, reduce background noise, and ensure good audio quality.'}), 400
        except Exception as e:
            error_msg = str(e)
            if "speech_recognition" in error_msg.lower() or "recognition" in error_msg.lower():
                return jsonify({'error': 'Speech recognition failed. Please try: 1) Speaking more clearly, 2) Reducing background noise, 3) Using a different audio file, or 4) Checking your internet connection.'}), 400
            else:
                return jsonify({'error': f'Speech recognition error: {error_msg}'}), 400
        
        # Analyze text
        try:
            metrics = analyze_text(transcript, duration)
        except Exception as e:
            return jsonify({'error': f'Text analysis failed: {str(e)}'}), 400
        
        # Calculate confidence
        try:
            confidence = calculate_confidence(metrics)
        except Exception as e:
            return jsonify({'error': f'Confidence calculation failed: {str(e)}'}), 400
        
        # Emotion detection from text
        try:
            emotion = analyze_emotion_from_text(transcript)
            emotion_feedback = get_emotion_feedback(emotion)
        except Exception as e:
            emotion = "neutral"
            emotion_feedback = "Emotion analysis completed."
        
        # Question relevance analysis
        try:
            relevance_analyzer = QuestionRelevanceAnalyzer()
            relevance_result = relevance_analyzer.analyze_relevance(question, transcript)
        except Exception as e:
            print(f"Relevance analysis failed: {e}")
            # Create fallback relevance result
            from services.question_relevance_simple import RelevanceResult, RelevanceClassification, RelevanceFeedback, FeedbackPriority, QuestionType
            
            relevance_result = RelevanceResult(
                relevance_score=50.0,
                classification=RelevanceClassification.PARTIALLY_RELEVANT,
                question_type=QuestionType.GENERAL,
                semantic_similarity=0.5,
                topic_overlap_percentage=50.0,
                feedback=RelevanceFeedback(
                    summary="Relevance analysis unavailable",
                    strengths=[],
                    improvements=[],
                    specific_suggestions=[],
                    example_elements=[],
                    priority_level=FeedbackPriority.MEDIUM
                ),
                processing_time=0.0
            )
        
        # Get interview-specific feedback (legacy)
        interview_feedback = get_interview_specific_feedback(question, transcript, metrics, confidence)
        
        # Save to database as interview session (optional - can be separated later)
        try:
            import json
            
            session_obj = SpeechSession(
                user_id=get_current_user_id(),  # Associate with current user
                transcript=transcript,
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
                engagement_level="Interview Mode",
                skill_level=f"Interview - {category.title()}",
                
                # Store interview-specific data in assessment fields
                pace_assessment=f"Interview Question: {question}",
                filler_assessment=f"Category: {category}",
                grammar_assessment=json.dumps(interview_feedback),
                vocabulary_assessment=emotion_feedback,
                tone_assessment=f"Interview practice session",
                general_impression=f"Interview answer analysis",
                
                # JSON fields for complex data
                strengths=json.dumps(interview_feedback.get("specific_tips", [])),
                improvements=json.dumps([]),
                actionable_tips=json.dumps([]),
                grammar_errors=json.dumps(metrics.get('grammar_errors', []))
            )
            
            db.session.add(session_obj)
            db.session.commit()
            print(f"Interview session saved to database (ID: {session_obj.id})")
            
        except Exception as e:
            db.session.rollback()
            print(f"Interview DB save failed: {e}")
            # Continue normally - DB failure doesn't break the app
        
        return jsonify({
            'success': True,
            'analysis': {
                'question': question,
                'category': category,
                'transcript': transcript,
                'duration': duration,
                'metrics': {
                    'wpm': metrics['wpm'],
                    'word_count': metrics.get('word_count', 0),
                    'fillers': metrics['fillers'],
                    'filler_percentage': metrics.get('filler_percentage', 0),
                    'grammar_score': metrics.get('grammar_score', 0),
                    'vocabulary_diversity': metrics.get('vocabulary_diversity', 0),
                    'sentiment': metrics['sentiment']
                },
                'confidence': confidence,
                'emotion': emotion,
                'emotion_feedback': emotion_feedback,
                'interview_feedback': interview_feedback,
                'relevance_analysis': {
                    'score': relevance_result.relevance_score,
                    'classification': relevance_result.classification.value,
                    'question_type': relevance_result.question_type.value,
                    'semantic_similarity': relevance_result.semantic_similarity,
                    'topic_overlap_percentage': relevance_result.topic_overlap_percentage,
                    'feedback': {
                        'summary': relevance_result.feedback.summary,
                        'strengths': relevance_result.feedback.strengths,
                        'improvements': relevance_result.feedback.improvements,
                        'suggestions': relevance_result.feedback.specific_suggestions,
                        'examples': relevance_result.feedback.example_elements
                    },
                    'processing_time': relevance_result.processing_time
                }
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

@interview_bp.route("/interview/question/<category>")
@login_required
def get_category_questions(category):
    """Get questions for a specific category"""
    questions = get_questions_by_category(category)
    return jsonify({
        'category': category,
        'questions': questions
    })

@interview_bp.route("/interview/chatbot", methods=["POST"])
@login_required
def interview_chatbot_endpoint():
    """Handle chatbot conversations during interview practice"""
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        context = data.get('context', {})
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Update chatbot context if provided
        if context:
            universal_chatbot.update_context(**context)
        
        # Get intelligent response from Universal Chatbot (with OpenAI and enhanced fallback)
        response = universal_chatbot.get_response(user_message)
        
        return jsonify({
            'success': True,
            'response': response,
            'timestamp': 'now'  # In production, use actual timestamp
        })
    
    except Exception as e:
        return jsonify({'error': f'Chatbot error: {str(e)}'}), 500

@interview_bp.route("/interview/chatbot/stage", methods=["POST"])
@login_required
def interview_chatbot_stage():
    """Get contextual chatbot response based on interview stage"""
    
    try:
        data = request.get_json()
        stage = data.get('stage', '')
        context = data.get('context', {})
        
        if not stage:
            return jsonify({'error': 'No stage provided'}), 400
        
        # Get stage-specific response from Universal Chatbot (with OpenAI and enhanced fallback)
        response = universal_chatbot.get_stage_response(stage, **context)
        
        return jsonify({
            'success': True,
            'response': response,
            'stage': stage,
            'timestamp': 'now'
        })
    
    except Exception as e:
        return jsonify({'error': f'Stage response error: {str(e)}'}), 500