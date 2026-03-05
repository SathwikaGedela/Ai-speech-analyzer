"""
Interview Chatbot Service
Provides intelligent responses and guidance for interview practice
"""

import re
import random
from typing import Dict, List, Tuple

class InterviewChatbot:
    def __init__(self):
        self.conversation_history = []
        self.user_context = {
            'selected_category': None,
            'selected_question': None,
            'analysis_results': None,
            'session_stage': 'initial'  # initial, practicing, analyzing, completed
        }
        
        # Knowledge base for responses
        self.knowledge_base = {
            'star_method': {
                'keywords': ['star', 'method', 'structure', 'behavioral'],
                'response': "The STAR method is perfect for behavioral questions! 🌟\n\n**S**ituation: Set the context and background\n**T**ask: Explain what you needed to accomplish\n**A**ction: Describe the specific steps you took\n**R**esult: Share the outcome and what you learned\n\nThis structure helps you give complete, compelling answers that showcase your problem-solving skills!"
            },
            'nervousness': {
                'keywords': ['nervous', 'anxiety', 'scared', 'worried', 'stress'],
                'response': "It's completely normal to feel nervous! 😌 Here are proven techniques to manage interview anxiety:\n\n• **Deep breathing**: 4 counts in, hold for 4, out for 4\n• **Power posing**: Stand confidently for 2 minutes before\n• **Positive visualization**: Imagine the interview going well\n• **Preparation**: Practice answers to common questions\n• **Reframe nerves**: They show you care about the opportunity!\n\nRemember: The interviewer wants you to succeed!"
            },
            'confidence': {
                'keywords': ['confidence', 'confident', 'self-doubt', 'imposter'],
                'response': "Building confidence is a skill you can develop! 💪 Try these strategies:\n\n• **Prepare thoroughly**: Research the company and role\n• **Practice out loud**: Record yourself answering questions\n• **List your achievements**: Write down your accomplishments\n• **Use confident body language**: Sit up straight, make eye contact\n• **Speak slowly**: It shows thoughtfulness and control\n• **Remember your worth**: You earned this interview!\n\nConfidence comes from preparation and practice!"
            },
            'weaknesses': {
                'keywords': ['weakness', 'weaknesses', 'flaws', 'shortcoming'],
                'response': "The weakness question is actually an opportunity! 🎯 Here's how to handle it:\n\n**Choose wisely**: Pick a real weakness that's not critical to the job\n**Show growth**: Explain how you're actively working to improve\n**Give examples**: Share specific steps you've taken\n**Stay positive**: Frame it as a learning opportunity\n\n**Example**: 'I used to struggle with public speaking, so I joined Toastmasters and now regularly present to large groups. I've learned that facing challenges head-on helps me grow professionally.'"
            },
            'salary': {
                'keywords': ['salary', 'money', 'pay', 'compensation', 'benefits'],
                'response': "Salary discussions require strategy! 💰 Here's the approach:\n\n**Research first**: Know the market rate for your role and location\n**Let them lead**: Try to let the employer bring up compensation first\n**Give a range**: Based on your research, not your current salary\n**Consider total package**: Benefits, growth opportunities, work-life balance\n**Stay flexible**: Show you're open to negotiation\n\n**Script**: 'Based on my research and experience, I'm looking for something in the $X-Y range, but I'm open to discussing the complete compensation package.'"
            },
            'questions_to_ask': {
                'keywords': ['questions', 'ask interviewer', 'what to ask'],
                'response': "Great questions show genuine interest! 🤔 Here are some powerful ones:\n\n**About the role**:\n• What does success look like in this position?\n• What are the biggest challenges facing the team?\n• How would you describe the team dynamics?\n\n**About growth**:\n• What opportunities exist for professional development?\n• How do you support employee career advancement?\n\n**About culture**:\n• How would you describe the company culture?\n• What do you enjoy most about working here?\n\nAvoid asking about salary, benefits, or vacation time in the first interview!"
            },
            'tell_me_about_yourself': {
                'keywords': ['tell me about yourself', 'introduce yourself', 'elevator pitch'],
                'response': "This is your elevator pitch moment! 🚀 Structure it like this:\n\n**Present** (30 seconds): Your current role and key skills\n**Past** (30 seconds): Relevant experience that led you here\n**Future** (30 seconds): Why you're excited about this opportunity\n\n**Example structure**:\n'I'm currently a [role] with [X years] experience in [field]. I specialize in [key skills]. Previously, I [major achievement]. I'm excited about this role because [connection to company/role]. I'm particularly drawn to [specific aspect of the job].'\n\nKeep it to 90 seconds max and practice until it feels natural!"
            }
        }
        
        # Contextual responses based on interview stage
        self.stage_responses = {
            'question_selected': [
                "Great choice! That's a {category} question. {tip}",
                "Perfect! For {category} questions, remember to {advice}.",
                "Excellent selection! Here's a quick tip for this type of question: {tip}"
            ],
            'recording_started': [
                "You're doing great! Remember to speak clearly and take your time.",
                "Perfect! Take a deep breath and structure your thoughts before speaking.",
                "Excellent! Remember to be specific and give concrete examples."
            ],
            'recording_long': [
                "Good progress! Try to wrap up your main points soon - aim for 1-2 minutes total.",
                "You're being thorough! Consider concluding your answer to keep it concise.",
                "Great detail! Remember that concise, focused answers are often more impactful."
            ],
            'analysis_complete': {
                'high_relevance': "Excellent work! 🎉 Your answer was highly relevant and well-structured. You clearly understood the question and provided a comprehensive response.",
                'good_relevance': "Good job! 👍 Your answer addressed the question well. With a bit more focus on the specific details, you'll be even stronger.",
                'moderate_relevance': "Not bad! 🤔 Your answer partially addressed the question. Try to stay more focused on what the interviewer is specifically asking.",
                'low_relevance': "Let's work on this together! 💪 Your answer could be more directly focused on the question. Remember to listen carefully and address the core of what's being asked."
            }
        }
        
        # Tips by category
        self.category_tips = {
            'general': "be specific about your experiences and show enthusiasm for the role",
            'behavioral': "use the STAR method to structure your response with specific examples",
            'technical': "explain your thought process clearly and mention specific tools or methodologies",
            'situational': "think through the scenario step-by-step and explain your reasoning"
        }

    def update_context(self, **kwargs):
        """Update the chatbot's context about the user's session"""
        self.user_context.update(kwargs)

    def get_response(self, user_message: str) -> str:
        """Generate an intelligent response based on user input and context"""
        user_message_lower = user_message.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append({
            'user': user_message,
            'timestamp': 'now'  # In real implementation, use actual timestamp
        })
        
        # Check for knowledge base matches
        for topic, data in self.knowledge_base.items():
            if any(keyword in user_message_lower for keyword in data['keywords']):
                return data['response']
        
        # Context-aware responses
        if 'help' in user_message_lower or 'tip' in user_message_lower:
            return self._get_contextual_help()
        
        if any(word in user_message_lower for word in ['thank', 'thanks']):
            return "You're very welcome! 😊 I'm here to help you succeed. Remember, every interview is practice, and you're getting better each time! Is there anything specific you'd like to work on?"
        
        # Default responses with context
        return self._get_default_response(user_message_lower)

    def _get_contextual_help(self) -> str:
        """Provide help based on current context"""
        stage = self.user_context.get('session_stage', 'initial')
        category = self.user_context.get('selected_category')
        
        if stage == 'initial':
            return "Here's how I can help you succeed in interviews:\n\n• **STAR Method**: Structure for behavioral questions (Situation, Task, Action, Result)\n• **Confidence Building**: Techniques to reduce anxiety and speak with authority\n• **Common Questions**: How to answer 'Tell me about yourself,' weaknesses, etc.\n• **Salary Discussion**: When and how to negotiate compensation\n• **Questions to Ask**: Thoughtful questions that impress interviewers\n• **Body Language**: Non-verbal communication tips\n\nJust ask me about any of these topics and I'll give you specific, actionable advice!"
        
        elif stage == 'practicing' and category:
            if category == 'behavioral':
                return f"For behavioral questions, use the STAR method:\n\n**S**ituation: Set the scene (2-3 sentences)\n**T**ask: What you needed to accomplish\n**A**ction: Specific steps you took (most important part)\n**R**esult: Positive outcome and what you learned\n\nKeep your answer to 90-120 seconds and focus on YOUR actions, not what the team did."
            elif category == 'technical':
                return f"For technical questions:\n\n• **Think out loud**: Explain your problem-solving process\n• **Be specific**: Mention actual tools, languages, or methodologies\n• **Give examples**: Reference real projects or challenges you've solved\n• **Show learning**: Mention how you stay updated with industry trends\n• **Ask clarifying questions**: Make sure you understand what they're asking"
            elif category == 'situational':
                return f"For situational questions:\n\n• **Listen carefully**: Make sure you understand the scenario\n• **Think step-by-step**: Walk through your approach logically\n• **Consider stakeholders**: Think about who would be affected\n• **Show judgment**: Explain your reasoning and decision-making\n• **Be practical**: Give realistic, actionable solutions"
            else:
                return f"For {category} questions, remember to be specific with examples, show enthusiasm for the role, and keep your answers focused and concise (1-2 minutes max)."
        
        else:
            return "I'm here to give you specific, actionable interview advice! Whether you need help with the STAR method, managing nerves, salary discussions, or any other interview topic, just ask and I'll provide clear guidance to help you succeed."

    def _get_default_response(self, user_message: str) -> str:
        """Generate a default response when no specific match is found"""
        
        # Check for common interview topics that might not have been caught
        if any(word in user_message for word in ['prepare', 'preparation', 'ready']):
            return "Here's how to prepare effectively for interviews:\n\n• **Research the company**: Know their mission, values, and recent news\n• **Practice common questions**: Prepare 5-7 stories using the STAR method\n• **Prepare your questions**: Have 3-5 thoughtful questions ready\n• **Mock interviews**: Practice with friends or record yourself\n• **Plan your outfit**: Choose professional attire in advance\n• **Arrive early**: Plan to arrive 10-15 minutes before your interview\n\nFocus on these fundamentals and you'll feel much more confident!"
        
        if any(word in user_message for word in ['tips', 'advice', 'help']):
            return "Here are my top interview tips:\n\n• **Be specific**: Use concrete examples and numbers when possible\n• **Show enthusiasm**: Let your genuine interest in the role shine through\n• **Listen actively**: Make sure you understand the question before answering\n• **Stay positive**: Even when discussing challenges or failures\n• **Follow up**: Send a thank-you email within 24 hours\n• **Be yourself**: Authenticity is more valuable than trying to be perfect\n\nRemember: They already like your resume - now show them your personality!"
        
        if any(word in user_message for word in ['practice', 'practicing', 'rehearse']):
            return "Effective interview practice strategies:\n\n• **Record yourself**: Listen back to identify areas for improvement\n• **Time your answers**: Aim for 1-2 minutes for most responses\n• **Practice out loud**: Don't just think through answers - say them\n• **Use the mirror**: Practice eye contact and confident body language\n• **Mock interviews**: Ask friends to interview you with real questions\n• **Vary your examples**: Prepare different stories for different questions\n\nConsistent practice builds confidence and helps answers flow naturally!"
        
        # More direct, helpful responses instead of asking questions back
        responses = [
            "Here's what I recommend: Focus on preparing 5-7 strong examples from your experience using the STAR method. This will give you material to answer most behavioral questions confidently.",
            "My advice: Research the company thoroughly and prepare 3-5 thoughtful questions to ask them. This shows genuine interest and helps you evaluate if it's the right fit.",
            "Key tip: Practice your answers out loud, not just in your head. Speaking your responses helps you sound more natural and confident during the actual interview.",
            "Remember: The interviewer wants you to succeed! They're not trying to trick you - they want to see if you're a good fit for the role and team.",
            "Focus on being specific in your answers. Instead of saying 'I'm a good leader,' tell a story that demonstrates your leadership skills with concrete results."
        ]
        return random.choice(responses)

    def get_stage_response(self, stage: str, **kwargs) -> str:
        """Get a response based on the current interview stage"""
        if stage == 'question_selected':
            category = kwargs.get('category', 'general')
            tip = self.category_tips.get(category, "be specific and give examples")
            template = random.choice(self.stage_responses['question_selected'])
            return template.format(category=category, tip=tip, advice=tip)
        
        elif stage == 'recording_started':
            return random.choice(self.stage_responses['recording_started'])
        
        elif stage == 'recording_long':
            return random.choice(self.stage_responses['recording_long'])
        
        elif stage == 'analysis_complete':
            relevance_score = kwargs.get('relevance_score', 0)
            if relevance_score >= 80:
                return self.stage_responses['analysis_complete']['high_relevance']
            elif relevance_score >= 60:
                return self.stage_responses['analysis_complete']['good_relevance']
            elif relevance_score >= 40:
                return self.stage_responses['analysis_complete']['moderate_relevance']
            else:
                return self.stage_responses['analysis_complete']['low_relevance']
        
        return "I'm here to help you succeed in your interview preparation! 🎯"

# Global chatbot instance
interview_chatbot = InterviewChatbot()