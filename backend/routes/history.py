from flask import Blueprint, render_template, jsonify, session
from models.session import SpeechSession
from middleware.auth_middleware import login_required, get_current_user_id
import json

history_bp = Blueprint("history", __name__)

def serialize_sessions(sessions):
    return {
        "labels": [s.format_datetime('chart') for s in sessions],
        "confidence": [s.confidence for s in sessions],
        "wpm": [s.wpm for s in sessions],
        "fillers": [s.fillers for s in sessions],
    }

@history_bp.route("/history")
@login_required
def history():
    # Get current user ID
    current_user_id = get_current_user_id()
    
    # Get sessions in ascending order for charts (natural progression) - filtered by user
    sessions_for_charts = SpeechSession.query.filter_by(user_id=current_user_id).order_by(
        SpeechSession.created_at.asc()
    ).all()
    
    # Get sessions in descending order for table (newest first) - filtered by user
    sessions_for_table = SpeechSession.query.filter_by(user_id=current_user_id).order_by(
        SpeechSession.created_at.desc()
    ).all()
    
    chart_data = serialize_sessions(sessions_for_charts)
    
    return render_template(
        "history.html",
        sessions=sessions_for_table,  # Table shows newest first
        chart_data=chart_data         # Charts show natural progression
    )

@history_bp.route("/api/history")
@login_required
def api_history():
    """Get history data as JSON for React frontend"""
    # Get current user ID
    current_user_id = get_current_user_id()
    
    # Get sessions in ascending order for charts (natural progression) - filtered by user
    sessions_for_charts = SpeechSession.query.filter_by(user_id=current_user_id).order_by(
        SpeechSession.created_at.asc()
    ).all()
    
    # Get sessions in descending order for table (newest first) - filtered by user
    sessions_for_table = SpeechSession.query.filter_by(user_id=current_user_id).order_by(
        SpeechSession.created_at.desc()
    ).all()
    
    # Serialize sessions for table
    sessions_data = []
    for session in sessions_for_table:
        session_data = {
            'id': session.id,
            'transcript': session.transcript,
            'wpm': session.wpm,
            'fillers': session.fillers,
            'sentiment': session.sentiment,
            'confidence': session.confidence,
            'emotion': session.emotion,
            'word_count': session.word_count,
            'filler_percentage': session.filler_percentage,
            'grammar_score': session.grammar_score,
            'vocabulary_diversity': session.vocabulary_diversity,
            'unique_words': session.unique_words,
            'pronunciation_clarity': session.pronunciation_clarity,
            'engagement_level': session.engagement_level,
            'skill_level': session.skill_level,
            'pace_assessment': session.pace_assessment,
            'filler_assessment': session.filler_assessment,
            'grammar_assessment': session.grammar_assessment,
            'vocabulary_assessment': session.vocabulary_assessment,
            'tone_assessment': session.tone_assessment,
            'general_impression': session.general_impression,
            'created_at': session.format_datetime('friendly'),
            'created_at_chart': session.format_datetime('chart')
        }
        
        # Parse JSON fields safely
        try:
            session_data['strengths'] = json.loads(session.strengths) if session.strengths else []
        except:
            session_data['strengths'] = []
            
        try:
            session_data['improvements'] = json.loads(session.improvements) if session.improvements else []
        except:
            session_data['improvements'] = []
            
        try:
            session_data['actionable_tips'] = json.loads(session.actionable_tips) if session.actionable_tips else []
        except:
            session_data['actionable_tips'] = []
            
        try:
            session_data['grammar_errors'] = json.loads(session.grammar_errors) if session.grammar_errors else []
        except:
            session_data['grammar_errors'] = []
        
        sessions_data.append(session_data)
    
    # Chart data
    chart_data = serialize_sessions(sessions_for_charts)
    
    return jsonify({
        'success': True,
        'sessions': sessions_data,
        'chart_data': chart_data,
        'total_sessions': len(sessions_data)
    })

@history_bp.route("/session/<int:session_id>")
@login_required
def get_session(session_id):
    """Get individual session data as JSON"""
    # Get current user ID
    current_user_id = get_current_user_id()
    
    # Get session only if it belongs to the current user
    session_obj = SpeechSession.query.filter_by(id=session_id, user_id=current_user_id).first()
    
    if not session_obj:
        return jsonify({'error': 'Session not found or access denied'}), 404
    
    # Convert session to dictionary
    session_data = {
        'id': session_obj.id,
        'transcript': session_obj.transcript,
        'wpm': session_obj.wpm,
        'fillers': session_obj.fillers,
        'sentiment': session_obj.sentiment,
        'confidence': session_obj.confidence,
        'emotion': session_obj.emotion,
        'word_count': session_obj.word_count,
        'filler_percentage': session_obj.filler_percentage,
        'grammar_score': session_obj.grammar_score,
        'vocabulary_diversity': session_obj.vocabulary_diversity,
        'unique_words': session_obj.unique_words,
        'pronunciation_clarity': session_obj.pronunciation_clarity,
        'engagement_level': session_obj.engagement_level,
        'skill_level': session_obj.skill_level,
        'pace_assessment': session_obj.pace_assessment,
        'filler_assessment': session_obj.filler_assessment,
        'grammar_assessment': session_obj.grammar_assessment,
        'vocabulary_assessment': session_obj.vocabulary_assessment,
        'tone_assessment': session_obj.tone_assessment,
        'general_impression': session_obj.general_impression,
        'strengths': session_obj.strengths,
        'improvements': session_obj.improvements,
        'actionable_tips': session_obj.actionable_tips,
        'grammar_errors': session_obj.grammar_errors,
        'created_at': session_obj.format_datetime('friendly')
    }
    
    return jsonify(session_data)