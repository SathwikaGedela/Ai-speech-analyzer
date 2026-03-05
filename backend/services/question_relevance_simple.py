"""
Simplified Question Relevance Analysis for Demo
Uses lightweight keyword matching instead of heavy ML models
"""

import time
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass

class RelevanceClassification(Enum):
    """Classification levels for answer relevance"""
    HIGHLY_RELEVANT = "Highly Relevant"      # 80-100%
    MOSTLY_RELEVANT = "Mostly Relevant"      # 60-79%
    PARTIALLY_RELEVANT = "Partially Relevant" # 40-59%
    MINIMALLY_RELEVANT = "Minimally Relevant" # 20-39%
    OFF_TOPIC = "Off-Topic"                  # 0-19%

class QuestionType(Enum):
    """Types of interview questions"""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    PERSONAL = "personal"
    VALUE_PROPOSITION = "value_proposition"
    STRENGTHS_WEAKNESSES = "strengths_weaknesses"
    SITUATIONAL = "situational"
    GENERAL = "general"

class FeedbackPriority(Enum):
    """Priority levels for feedback intensity"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

@dataclass
class RelevanceFeedback:
    """Feedback for answer relevance"""
    summary: str
    strengths: List[str]
    improvements: List[str]
    specific_suggestions: List[str]
    example_elements: List[str]
    priority_level: FeedbackPriority

@dataclass
class RelevanceResult:
    """Complete result of relevance analysis"""
    relevance_score: float  # 0-100
    classification: RelevanceClassification
    question_type: QuestionType
    semantic_similarity: float
    topic_overlap_percentage: float
    feedback: RelevanceFeedback
    processing_time: float

class QuestionRelevanceAnalyzer:
    """
    Simplified analyzer for question-answer relevance in interview mode
    """
    
    def __init__(self):
        """Initialize the relevance analyzer"""
        self.question_patterns = self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize question patterns for classification"""
        return {
            QuestionType.PERSONAL: {
                "keywords": ["tell me about yourself", "background", "experience", "career", "journey"],
                "expected": ["experience", "background", "skills", "goal", "career"]
            },
            QuestionType.BEHAVIORAL: {
                "keywords": ["tell me about a time", "describe a situation", "challenging situation", "difficult"],
                "expected": ["situation", "challenge", "action", "result", "problem", "solution"]
            },
            QuestionType.VALUE_PROPOSITION: {
                "keywords": ["why should we hire you", "what makes you", "unique", "value", "contribute"],
                "expected": ["skills", "value", "contribute", "experience", "achieve", "bring"]
            },
            QuestionType.STRENGTHS_WEAKNESSES: {
                "keywords": ["strengths", "weaknesses", "greatest strength", "biggest weakness"],
                "expected": ["strength", "weakness", "good", "improve", "working"]
            },
            QuestionType.TECHNICAL: {
                "keywords": ["how would you", "explain", "implement", "design", "technical", "programming"],
                "expected": ["technical", "implement", "design", "code", "system", "approach"]
            }
        }
    
    def analyze_relevance(self, question: str, answer: str) -> RelevanceResult:
        """
        Analyze the relevance between a question and answer.
        """
        start_time = time.time()
        
        try:
            # Step 1: Classify question type
            question_type = self._classify_question(question)
            
            # Step 2: Calculate relevance score
            relevance_score = self._calculate_relevance_score(question, answer, question_type)
            
            # Step 3: Classify relevance level
            classification = self._classify_relevance(relevance_score)
            
            # Step 4: Generate feedback
            feedback = self._generate_feedback(question, answer, question_type, relevance_score, classification)
            
            processing_time = time.time() - start_time
            
            return RelevanceResult(
                relevance_score=relevance_score,
                classification=classification,
                question_type=question_type,
                semantic_similarity=relevance_score / 100.0,
                topic_overlap_percentage=relevance_score,
                feedback=feedback,
                processing_time=processing_time
            )
            
        except Exception as e:
            processing_time = time.time() - start_time
            return self._create_fallback_result(processing_time)
    
    def _classify_question(self, question: str) -> QuestionType:
        """Classify the type of interview question"""
        question_lower = question.lower()
        
        for q_type, pattern in self.question_patterns.items():
            for keyword in pattern["keywords"]:
                if keyword in question_lower:
                    return q_type
        
        return QuestionType.GENERAL
    
    def _calculate_relevance_score(self, question: str, answer: str, question_type: QuestionType) -> float:
        """Calculate relevance score based on keyword matching"""
        if not answer or not answer.strip():
            return 0.0
        
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        # Get expected keywords for this question type
        if question_type in self.question_patterns:
            expected_keywords = self.question_patterns[question_type]["expected"]
        else:
            expected_keywords = ["work", "experience", "skills"]
        
        # Count keyword matches with more generous matching
        matches = 0
        matched_keywords = []
        
        # Count keyword matches with more generous matching
        matches = 0
        matched_keywords = []
        
        # Expanded synonym dictionary for better matching
        synonyms = {
            "skills": ["skill", "ability", "abilities", "capable", "capabilities", "talents", "expertise", "competencies", "strengths", "good at", "excel", "proficient", "analytical", "thinking"],
            "experience": ["experienced", "background", "work", "history", "tenure", "years", "time", "decade", "developer", "engineer", "professional", "career", "worked"],
            "value": ["bring", "contribute", "offer", "provide", "add", "help", "assist", "drive", "forward", "addition", "asset", "benefit", "valuable"],
            "achieve": ["deliver", "accomplish", "complete", "quality", "success", "results", "outcome", "finish", "successful", "completed", "delivered", "accomplished", "met"],
            "situation": ["scenario", "circumstance", "case", "instance", "problem", "issue", "challenge", "encountered"],
            "action": ["steps", "took", "did", "implemented", "approached", "handled", "managed", "initiative", "stepped", "reorganized"],
            "challenge": ["challenging", "difficult", "tough", "complex", "demanding", "hard", "problem"],
            "team": ["teamwork", "collaboration", "group", "colleagues", "together", "cooperative"],
            "leadership": ["lead", "leading", "manage", "managing", "guide", "direct", "supervise", "leader"],
            "learning": ["learn", "grow", "development", "improve", "adapt", "education", "training"],
            "goal": ["goals", "vision", "future", "aspire", "aim", "objective", "plan", "direction"],
            "background": ["history", "past", "previous", "former", "education", "training"]
        }
        
        for keyword in expected_keywords:
            found_match = False
            
            # Check for exact match
            if keyword in answer_lower:
                matches += 1
                matched_keywords.append(keyword)
                found_match = True
            else:
                # Check for synonym matches
                if keyword in synonyms:
                    for synonym in synonyms[keyword]:
                        if synonym in answer_lower:
                            matches += 1
                            matched_keywords.append(keyword)
                            found_match = True
                            break
                
                # Additional specific checks for common variations
                if not found_match:
                    if keyword == "skills" and any(term in answer_lower for term in ["good at", "excel at", "talented", "proficient"]):
                        matches += 1
                        matched_keywords.append("skills")
                    elif keyword == "experience" and any(term in answer_lower for term in ["worked", "career", "professional", "developer", "engineer"]):
                        matches += 1
                        matched_keywords.append("experience")
                    elif keyword == "value" and any(term in answer_lower for term in ["benefit", "asset", "addition", "valuable"]):
                        matches += 1
                        matched_keywords.append("value")
                    elif keyword == "achieve" and any(term in answer_lower for term in ["successful", "completed", "delivered", "accomplished"]):
                        matches += 1
                        matched_keywords.append("achievements")
        
        # Calculate base score from keyword matches
        keyword_score = (matches / len(expected_keywords)) * 60  # Max 60 points from keywords
        
        # Add bonus points for comprehensive answers
        word_count = len(answer.split())
        if word_count >= 20:  # Substantial answer
            length_bonus = min(25, word_count * 0.5)  # Up to 25 bonus points
        else:
            length_bonus = word_count * 1.0  # Smaller bonus for shorter answers
        
        # Add bonus for question-specific content
        question_bonus = 0
        if question_type == QuestionType.VALUE_PROPOSITION:
            # Look for value proposition indicators
            value_indicators = ["hire", "because", "bring", "contribute", "deliver", "quality", "dedication", "responsibility", "enthusiasm"]
            value_matches = sum(1 for indicator in value_indicators if indicator in answer_lower)
            question_bonus = min(15, value_matches * 3)  # Up to 15 bonus points
        
        # Check for off-topic content (penalty)
        off_topic_words = ["pizza", "weather", "color", "movie", "dog", "cat", "food", "music", "sports", "hobby"]
        off_topic_count = sum(1 for word in off_topic_words if word in answer_lower)
        off_topic_penalty = off_topic_count * 20  # 20 point penalty per off-topic word
        
        # Calculate final score
        relevance_score = keyword_score + length_bonus + question_bonus - off_topic_penalty
        
        # Ensure minimum score for reasonable answers
        if matches > 0 and word_count >= 10 and off_topic_count == 0:
            relevance_score = max(relevance_score, 50)  # Minimum 50% for decent relevant answers
        
        # Cap at 100%
        relevance_score = min(100, max(0, relevance_score))
        
        return round(relevance_score, 1)
    
    def _classify_relevance(self, score: float) -> RelevanceClassification:
        """Classify relevance score into categories"""
        if score >= 80:
            return RelevanceClassification.HIGHLY_RELEVANT
        elif score >= 60:
            return RelevanceClassification.MOSTLY_RELEVANT
        elif score >= 40:
            return RelevanceClassification.PARTIALLY_RELEVANT
        elif score >= 20:
            return RelevanceClassification.MINIMALLY_RELEVANT
        else:
            return RelevanceClassification.OFF_TOPIC
    
    def _generate_feedback(self, question: str, answer: str, question_type: QuestionType,
                          relevance_score: float, classification: RelevanceClassification) -> RelevanceFeedback:
        """Generate comprehensive feedback"""
        
        # Determine priority
        if relevance_score >= 80:
            priority = FeedbackPriority.LOW
        elif relevance_score >= 60:
            priority = FeedbackPriority.MEDIUM
        else:
            priority = FeedbackPriority.HIGH
        
        # Generate summary
        if relevance_score >= 80:
            summary = f"Excellent! Your answer directly addresses the question ({relevance_score}% relevance)."
        elif relevance_score >= 60:
            summary = f"Good job! Your answer mostly addresses the question ({relevance_score}% relevance)."
        elif relevance_score >= 40:
            summary = f"Your answer partially addresses the question ({relevance_score}% relevance). Consider focusing more on the specific question asked."
        elif relevance_score >= 20:
            summary = f"Your answer has some relevance to the question ({relevance_score}% relevance). Try to address the question more directly."
        else:
            summary = f"Your answer appears to be off-topic ({relevance_score}% relevance). Please focus on answering the specific question asked."
        
        # Generate strengths and improvements
        strengths = []
        improvements = []
        suggestions = []
        examples = []
        
        answer_lower = answer.lower()
        
        # Check for relevant content
        if question_type in self.question_patterns:
            expected = self.question_patterns[question_type]["expected"]
            found_keywords = []
            
            for kw in expected:
                if kw in answer_lower:
                    found_keywords.append(kw)
                # Check for related terms
                elif kw == "skills" and any(term in answer_lower for term in ["skill", "ability", "abilities"]):
                    found_keywords.append("skills")
                elif kw == "value" and any(term in answer_lower for term in ["bring", "contribute", "offer"]):
                    found_keywords.append("value")
                elif kw == "achieve" and any(term in answer_lower for term in ["deliver", "quality", "dedication"]):
                    found_keywords.append("achievements")
            
            if found_keywords:
                strengths.append(f"You covered relevant topics: {', '.join(found_keywords[:3])}")
        
        # Check answer length and structure
        word_count = len(answer.split())
        if word_count >= 20:
            strengths.append("Good answer length with substantial content")
        elif word_count < 10:
            improvements.append("Consider providing more detailed examples and explanations")
        
        # Generate improvements based on score
        if relevance_score < 60:
            improvements.append("Focus more directly on answering the specific question asked")
        
        # Check for off-topic content
        off_topic_words = ["pizza", "weather", "color", "movie", "dog", "cat"]
        if any(word in answer_lower for word in off_topic_words):
            improvements.append("Avoid discussing unrelated topics")
        
        # Generate question-specific suggestions
        if question_type == QuestionType.BEHAVIORAL:
            suggestions.append("Use the STAR method: Situation, Task, Action, Result")
            examples = ["Describe the specific situation", "Explain your task or challenge", "Detail the actions you took", "Share the results achieved"]
        elif question_type == QuestionType.PERSONAL:
            suggestions.append("Cover your background, key skills, and career goals")
            examples = ["Share your professional background", "Highlight your key skills", "Mention your career aspirations"]
        elif question_type == QuestionType.VALUE_PROPOSITION:
            if relevance_score >= 60:
                suggestions.append("Great job highlighting your value! Consider adding specific examples of achievements")
            else:
                suggestions.append("Highlight your unique value and what you can contribute")
            examples = ["Mention specific skills and achievements", "Explain how you can add value to the company", "Show enthusiasm for the role and company"]
        
        # Add positive reinforcement for good answers
        if relevance_score >= 70:
            if not strengths:
                strengths.append("Your answer demonstrates good understanding of the question")
        
        return RelevanceFeedback(
            summary=summary,
            strengths=strengths,
            improvements=improvements,
            specific_suggestions=suggestions,
            example_elements=examples,
            priority_level=priority
        )
    
    def _create_fallback_result(self, processing_time: float) -> RelevanceResult:
        """Create a fallback result when analysis fails"""
        return RelevanceResult(
            relevance_score=50.0,
            classification=RelevanceClassification.PARTIALLY_RELEVANT,
            question_type=QuestionType.GENERAL,
            semantic_similarity=0.5,
            topic_overlap_percentage=50.0,
            feedback=RelevanceFeedback(
                summary="Relevance analysis completed with basic scoring.",
                strengths=[],
                improvements=["Consider providing more specific details"],
                specific_suggestions=["Focus on directly answering the question"],
                example_elements=[],
                priority_level=FeedbackPriority.MEDIUM
            ),
            processing_time=processing_time
        )