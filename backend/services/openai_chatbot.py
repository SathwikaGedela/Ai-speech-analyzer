"""
OpenAI-powered Interview Chatbot Service
Enhanced chatbot using OpenAI's GPT model for more intelligent responses
"""

import os
import json
from typing import Dict, List, Optional
import openai
from .interview_chatbot import interview_chatbot as fallback_chatbot

class OpenAIChatbot:
    def __init__(self):
        # Initialize OpenAI client
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
            self.openai_available = True
        else:
            self.openai_available = False
            print("Warning: OPENAI_API_KEY not found. Using fallback chatbot.")
        
        self.conversation_history = []
        self.user_context = {
            'selected_category': None,
            'selected_question': None,
            'analysis_results': None,
            'session_stage': 'initial'
        }
        
        # System prompt for interview coaching
        self.system_prompt = """You are an expert interview coach and career advisor. Your role is to help users prepare for job interviews by providing:

1. DIRECT, ACTIONABLE ADVICE - Always give specific, helpful guidance instead of asking questions back
2. STRUCTURED RESPONSES - Use bullet points, numbered lists, and clear formatting
3. PRACTICAL EXAMPLES - Include real scripts, templates, and specific examples
4. ENCOURAGING TONE - Be supportive and confidence-building while remaining professional
5. COMPREHENSIVE GUIDANCE - Cover all aspects of interview preparation and performance

Key areas of expertise:
- STAR method for behavioral questions
- Interview anxiety and confidence building
- Salary negotiation strategies
- Questions to ask interviewers
- "Tell me about yourself" structure
- Handling weakness questions
- Technical interview preparation
- Body language and presentation

Always provide immediate value with specific, actionable steps the user can implement right away. Be concise but comprehensive, and maintain a professional coaching tone."""

    def update_context(self, **kwargs):
        """Update the chatbot's context about the user's session"""
        self.user_context.update(kwargs)

    def get_response(self, user_message: str) -> str:
        """Generate an intelligent response using OpenAI or fallback"""
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': 'now'
        })
        
        # Try OpenAI first, fallback to local chatbot if unavailable
        if self.openai_available:
            try:
                response = self._get_openai_response(user_message)
                self.conversation_history.append({
                    'role': 'assistant',
                    'content': response,
                    'timestamp': 'now'
                })
                return response
            except Exception as e:
                print(f"OpenAI API error: {e}")
                # Fall back to local chatbot
                return fallback_chatbot.get_response(user_message)
        else:
            # Use fallback chatbot
            return fallback_chatbot.get_response(user_message)

    def _get_openai_response(self, user_message: str) -> str:
        """Get response from OpenAI GPT model"""
        
        # Build context-aware prompt
        context_info = self._build_context_prompt()
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt + context_info}
        ]
        
        # Add recent conversation history (last 6 messages to stay within token limits)
        recent_history = self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
        for msg in recent_history:
            if msg['role'] in ['user', 'assistant']:
                messages.append({
                    "role": msg['role'],
                    "content": msg['content']
                })
        
        # Add current user message
        messages.append({"role": "user", "content": user_message})
        
        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # or "gpt-4" if available
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.1
        )
        
        return response.choices[0].message.content.strip()

    def _build_context_prompt(self) -> str:
        """Build context-aware prompt based on current session state"""
        context_parts = []
        
        if self.user_context.get('selected_category'):
            context_parts.append(f"Current interview category: {self.user_context['selected_category']}")
        
        if self.user_context.get('selected_question'):
            context_parts.append(f"Current question: {self.user_context['selected_question']}")
        
        stage = self.user_context.get('session_stage', 'initial')
        if stage == 'practicing':
            context_parts.append("User is currently practicing their interview answer")
        elif stage == 'completed':
            context_parts.append("User has completed their practice and received analysis")
        
        if self.user_context.get('analysis_results'):
            analysis = self.user_context['analysis_results']
            if 'relevance_score' in analysis:
                context_parts.append(f"Recent performance: {analysis['relevance_score']}% relevance score")
        
        if context_parts:
            return f"\n\nCurrent session context:\n" + "\n".join(f"- {part}" for part in context_parts)
        
        return ""

    def get_stage_response(self, stage: str, **kwargs) -> str:
        """Get a response based on the current interview stage"""
        
        # Build stage-specific prompt
        stage_prompts = {
            'question_selected': f"The user has selected a {kwargs.get('category', 'general')} interview question. Provide encouraging tips specific to this question type.",
            'recording_started': "The user just started recording their interview answer. Give brief, encouraging guidance.",
            'recording_long': "The user has been recording for a while. Gently suggest they wrap up their answer soon.",
            'analysis_complete': f"The user completed their practice with a {kwargs.get('relevance_score', 0)}% relevance score. Provide specific feedback and encouragement."
        }
        
        prompt = stage_prompts.get(stage, "Provide helpful interview coaching advice.")
        
        if self.openai_available:
            try:
                messages = [
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ]
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=200,
                    temperature=0.7
                )
                
                return response.choices[0].message.content.strip()
            except Exception as e:
                print(f"OpenAI stage response error: {e}")
                return fallback_chatbot.get_stage_response(stage, **kwargs)
        else:
            return fallback_chatbot.get_stage_response(stage, **kwargs)

# Global OpenAI chatbot instance
openai_chatbot = OpenAIChatbot()