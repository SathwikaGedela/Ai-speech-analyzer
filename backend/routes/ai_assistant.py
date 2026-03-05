"""
Smart AI Interview Assistant API Routes
Provides endpoints for the Smart AI Interview Assistant functionality
"""

from flask import Blueprint, request, jsonify, session
from services.universal_chatbot import universal_chatbot
from middleware.auth_middleware import login_required
import logging

# Create blueprint
ai_assistant_bp = Blueprint('ai_assistant', __name__)

@ai_assistant_bp.route('/ai-assistant/answer', methods=['POST'])
@login_required
def get_ai_answer():
    """Get Smart AI-generated interview answer"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                'success': False,
                'error': 'Question is required'
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                'success': False,
                'error': 'Question cannot be empty'
            }), 400
        
        # Get optional context
        job_role = data.get('job_role', '')
        company = data.get('company', '')
        
        # Generate AI response using Universal Chatbot
        if job_role or company:
            # Add context for job-specific responses
            context_message = f"This is for a {job_role} position at {company}. {question}"
            response = universal_chatbot.get_response(context_message)
        else:
            response = universal_chatbot.get_response(question)
        
        # Get model info for debugging
        model_info = {
            'model_loaded': True,
            'model_name': 'Universal Chatbot with Comprehensive Knowledge Base',
            'ai_powered': True,
            'fallback_available': True
        }
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': response,
            'ai_powered': model_info['ai_powered'],
            'model_info': model_info,
            'timestamp': 'now'
        })
        
    except Exception as e:
        logging.error(f"Smart AI Assistant error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to generate AI response'
        }), 500

@ai_assistant_bp.route('/ai-assistant/model-info', methods=['GET'])
@login_required
def get_model_info():
    """Get information about the loaded AI model"""
    try:
        model_info = {
            'model_loaded': True,
            'model_name': 'Universal Chatbot with Comprehensive Knowledge Base',
            'ai_powered': True,
            'fallback_available': True
        }
        
        return jsonify({
            'success': True,
            'model_info': model_info
        })
        
    except Exception as e:
        logging.error(f"Model info error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get model information'
        }), 500

@ai_assistant_bp.route('/ai-assistant/practice-questions', methods=['GET'])
@login_required
def get_practice_questions():
    """Get common interview questions for practice"""
    try:
        practice_questions = [
            {
                'category': 'General',
                'questions': [
                    'Tell me about yourself',
                    'Why do you want to work here?',
                    'What are your greatest strengths?',
                    'What is your biggest weakness?',
                    'Where do you see yourself in 5 years?',
                    'Why are you leaving your current job?',
                    'Do you have any questions for us?'
                ]
            },
            {
                'category': 'Behavioral',
                'questions': [
                    'Tell me about a time you showed leadership',
                    'Describe a challenging situation you faced at work',
                    'Give me an example of when you worked in a team',
                    'Tell me about a time you failed',
                    'Describe a time you had to learn something new quickly',
                    'Tell me about a conflict you had with a coworker',
                    'Give me an example of when you went above and beyond'
                ]
            },
            {
                'category': 'Technical',
                'questions': [
                    'What programming languages are you most comfortable with?',
                    'How do you approach debugging a complex problem?',
                    'Explain your experience with databases',
                    'What development methodologies have you used?',
                    'How do you ensure code quality?',
                    'Describe your experience with version control',
                    'What tools do you use for testing?'
                ]
            },
            {
                'category': 'Situational',
                'questions': [
                    'How would you handle a tight deadline?',
                    'What would you do if you disagreed with your manager?',
                    'How do you prioritize multiple tasks?',
                    'What would you do if you made a mistake?',
                    'How do you handle criticism?',
                    'What would you do if a project was falling behind?',
                    'How do you stay updated with new technologies?'
                ]
            }
        ]
        
        return jsonify({
            'success': True,
            'practice_questions': practice_questions
        })
        
    except Exception as e:
        logging.error(f"Practice questions error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get practice questions'
        }), 500

@ai_assistant_bp.route('/ai-assistant/tips', methods=['GET'])
@login_required
def get_interview_tips():
    """Get interview tips and best practices"""
    try:
        tips = {
            'preparation': [
                'Research the company thoroughly - mission, values, recent news',
                'Review the job description and match your skills to requirements',
                'Prepare 5-7 STAR method examples for behavioral questions',
                'Practice your answers out loud, not just in your head',
                'Prepare thoughtful questions to ask the interviewer'
            ],
            'during_interview': [
                'Arrive 10-15 minutes early',
                'Make eye contact and offer a firm handshake',
                'Listen carefully to questions before answering',
                'Use specific examples and quantify your achievements',
                'Ask clarifying questions if you need more information'
            ],
            'communication': [
                'Speak clearly and at a moderate pace',
                'Use the STAR method for behavioral questions',
                'Be concise but thorough in your responses',
                'Show enthusiasm and genuine interest',
                'Maintain professional body language'
            ],
            'follow_up': [
                'Send a thank-you email within 24 hours',
                'Reiterate your interest in the position',
                'Mention specific points from the conversation',
                'Include any additional information requested',
                'Be patient while waiting for a response'
            ]
        }
        
        return jsonify({
            'success': True,
            'tips': tips
        })
        
    except Exception as e:
        logging.error(f"Interview tips error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Failed to get interview tips'
        }), 500