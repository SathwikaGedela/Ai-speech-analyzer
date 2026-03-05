from database import db
from datetime import datetime, timezone, timedelta

class SpeechSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    
    # Basic data
    transcript = db.Column(db.Text)
    wpm = db.Column(db.Float)
    fillers = db.Column(db.Integer)
    sentiment = db.Column(db.Float)
    confidence = db.Column(db.Integer)
    emotion = db.Column(db.String(50))
    
    # Extended analysis data
    word_count = db.Column(db.Integer)
    filler_percentage = db.Column(db.Float)
    grammar_score = db.Column(db.Float)
    vocabulary_diversity = db.Column(db.Float)
    unique_words = db.Column(db.Integer)
    pronunciation_clarity = db.Column(db.Float)
    engagement_level = db.Column(db.String(20))
    skill_level = db.Column(db.String(30))
    
    # Assessment text fields
    pace_assessment = db.Column(db.Text)
    filler_assessment = db.Column(db.Text)
    grammar_assessment = db.Column(db.Text)
    vocabulary_assessment = db.Column(db.Text)
    tone_assessment = db.Column(db.Text)
    general_impression = db.Column(db.Text)
    
    # JSON fields for complex data
    strengths = db.Column(db.Text)  # JSON string
    improvements = db.Column(db.Text)  # JSON string
    actionable_tips = db.Column(db.Text)  # JSON string
    grammar_errors = db.Column(db.Text)  # JSON string
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_local_time(self):
        """Convert UTC time to local timezone (simplified)"""
        if self.created_at:
            # For simplicity, we'll assume the user is in their local timezone
            # In a production app, you'd store user timezone preferences
            try:
                # Get local timezone offset
                import time
                local_offset = time.timezone if time.daylight == 0 else time.altzone
                local_offset_hours = -local_offset // 3600
                
                # Apply offset to UTC time
                local_time = self.created_at + timedelta(hours=local_offset_hours)
                return local_time
            except:
                # Fallback to original time if conversion fails
                return self.created_at
        return None
    
    def format_datetime(self, format_type='full'):
        """Format datetime for display"""
        if not self.created_at:
            return "Unknown"
        
        # Get local time (or fallback to UTC)
        display_time = self.get_local_time() or self.created_at
        
        if format_type == 'full':
            return display_time.strftime("%B %d, %Y at %I:%M %p")
        elif format_type == 'short':
            return display_time.strftime("%m/%d/%Y %H:%M")
        elif format_type == 'chart':
            return display_time.strftime("%m-%d %H:%M")
        elif format_type == 'friendly':
            return display_time.strftime("%d %b %Y, %H:%M")
        else:
            return display_time.strftime("%d-%m-%Y %H:%M")
    
    def get_strengths_list(self):
        """Parse strengths JSON string to list"""
        if self.strengths:
            try:
                import json
                return json.loads(self.strengths)
            except:
                return []
        return []
    
    def get_improvements_list(self):
        """Parse improvements JSON string to list"""
        if self.improvements:
            try:
                import json
                return json.loads(self.improvements)
            except:
                return []
        return []
    
    def get_actionable_tips_list(self):
        """Parse actionable tips JSON string to list"""
        if self.actionable_tips:
            try:
                import json
                return json.loads(self.actionable_tips)
            except:
                return []
        return []
    
    def get_grammar_errors_list(self):
        """Parse grammar errors JSON string to list"""
        if self.grammar_errors:
            try:
                import json
                return json.loads(self.grammar_errors)
            except:
                return []
        return []