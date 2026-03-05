"""
Question Pattern Matching System for Interview Analysis

This module provides question type classification and expected answer structure
validation for different types of interview questions.
"""

import re
from enum import Enum
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

class QuestionType(Enum):
    """Types of interview questions"""
    BEHAVIORAL = "behavioral"
    TECHNICAL = "technical"
    PERSONAL = "personal"
    VALUE_PROPOSITION = "value_proposition"
    STRENGTHS_WEAKNESSES = "strengths_weaknesses"
    SITUATIONAL = "situational"
    GENERAL = "general"

@dataclass
class ExpectedElement:
    """Expected element in an answer"""
    element_type: str
    description: str
    keywords: List[str]
    required: bool = False

@dataclass
class QuestionPattern:
    """Pattern for a specific question type"""
    question_type: QuestionType
    keywords: List[str]
    expected_elements: List[ExpectedElement]
    description: str

@dataclass
class StructureValidation:
    """Result of answer structure validation"""
    found_elements: List[str]
    missing_elements: List[str]
    structure_score: float
    feedback: List[str]

class QuestionPatternMatcher:
    """
    Matches interview questions to patterns and validates answer structures
    """
    
    def __init__(self):
        """Initialize the question pattern matcher with predefined patterns"""
        self.patterns = self._initialize_patterns()
    
    def _initialize_patterns(self) -> Dict[QuestionType, QuestionPattern]:
        """Initialize predefined question patterns"""
        patterns = {}
        
        # Behavioral Questions (STAR method)
        patterns[QuestionType.BEHAVIORAL] = QuestionPattern(
            question_type=QuestionType.BEHAVIORAL,
            keywords=[
                "tell me about a time", "describe a situation", "give me an example",
                "challenging situation", "difficult situation", "conflict", "mistake",
                "achievement", "leadership", "teamwork", "problem solving"
            ],
            expected_elements=[
                ExpectedElement("situation", "Context and background", 
                              ["situation", "context", "background", "company", "project"], True),
                ExpectedElement("task", "Specific task or challenge", 
                              ["task", "challenge", "responsibility", "goal", "objective"], True),
                ExpectedElement("action", "Actions taken", 
                              ["action", "did", "implemented", "decided", "approached"], True),
                ExpectedElement("result", "Outcome and impact", 
                              ["result", "outcome", "impact", "achieved", "learned"], True)
            ],
            description="Behavioral questions expect STAR method responses"
        )
        
        # Technical Questions
        patterns[QuestionType.TECHNICAL] = QuestionPattern(
            question_type=QuestionType.TECHNICAL,
            keywords=[
                "how would you", "explain", "implement", "design", "algorithm",
                "database", "programming", "code", "technical", "system", "architecture",
                "framework", "language", "technology", "api", "performance"
            ],
            expected_elements=[
                ExpectedElement("concept", "Technical concept explanation", 
                              ["concept", "definition", "means", "is"], True),
                ExpectedElement("methodology", "Approach or methodology", 
                              ["approach", "method", "process", "steps", "way"]),
                ExpectedElement("example", "Specific example or implementation", 
                              ["example", "instance", "case", "implemented", "used"]),
                ExpectedElement("considerations", "Trade-offs and considerations", 
                              ["consider", "trade-off", "advantage", "disadvantage", "limitation"])
            ],
            description="Technical questions expect concept explanation with examples"
        )
        
        # Personal Questions
        patterns[QuestionType.PERSONAL] = QuestionPattern(
            question_type=QuestionType.PERSONAL,
            keywords=[
                "tell me about yourself", "background", "experience", "career",
                "journey", "interests", "passion", "motivation", "goals"
            ],
            expected_elements=[
                ExpectedElement("background", "Professional background", 
                              ["background", "experience", "worked", "career"], True),
                ExpectedElement("skills", "Key skills and expertise", 
                              ["skills", "expertise", "good at", "experienced"]),
                ExpectedElement("goals", "Career goals and aspirations", 
                              ["goals", "future", "want", "aspire", "looking"])
            ],
            description="Personal questions expect background, skills, and goals"
        )
        
        # Value Proposition Questions
        patterns[QuestionType.VALUE_PROPOSITION] = QuestionPattern(
            question_type=QuestionType.VALUE_PROPOSITION,
            keywords=[
                "why should we hire you", "what makes you", "unique", "value",
                "bring to", "contribute", "best candidate", "stand out"
            ],
            expected_elements=[
                ExpectedElement("skills", "Relevant skills and expertise", 
                              ["skills", "expertise", "experience", "knowledge"], True),
                ExpectedElement("achievements", "Notable achievements", 
                              ["achieved", "accomplished", "success", "results"]),
                ExpectedElement("fit", "Company/role fit", 
                              ["fit", "match", "align", "company", "role", "culture"])
            ],
            description="Value proposition questions expect skills, achievements, and fit"
        )
        
        # Strengths and Weaknesses
        patterns[QuestionType.STRENGTHS_WEAKNESSES] = QuestionPattern(
            question_type=QuestionType.STRENGTHS_WEAKNESSES,
            keywords=[
                "strengths", "weaknesses", "greatest strength", "biggest weakness",
                "areas for improvement", "what are you good at", "struggle with"
            ],
            expected_elements=[
                ExpectedElement("strength", "Specific strength with example", 
                              ["strength", "good at", "excel", "strong"]),
                ExpectedElement("weakness", "Weakness with improvement plan", 
                              ["weakness", "struggle", "challenge", "improve"]),
                ExpectedElement("improvement", "Steps for improvement", 
                              ["working on", "learning", "developing", "plan"])
            ],
            description="Strengths/weaknesses questions expect both aspects with examples"
        )
        
        # Situational Questions
        patterns[QuestionType.SITUATIONAL] = QuestionPattern(
            question_type=QuestionType.SITUATIONAL,
            keywords=[
                "what would you do", "how would you handle", "if you were",
                "hypothetical", "scenario", "situation", "imagine"
            ],
            expected_elements=[
                ExpectedElement("understanding", "Understanding of the situation", 
                              ["understand", "situation", "challenge", "issue"]),
                ExpectedElement("approach", "Planned approach", 
                              ["would", "approach", "plan", "strategy", "steps"]),
                ExpectedElement("rationale", "Reasoning behind approach", 
                              ["because", "reason", "important", "ensure"])
            ],
            description="Situational questions expect understanding and planned approach"
        )
        
        # General Questions (fallback)
        patterns[QuestionType.GENERAL] = QuestionPattern(
            question_type=QuestionType.GENERAL,
            keywords=[],
            expected_elements=[
                ExpectedElement("content", "Relevant content addressing the question", 
                              ["answer", "response", "information"], True)
            ],
            description="General interview questions expect relevant answers"
        )
        
        return patterns
    
    def match_pattern(self, question: str) -> QuestionPattern:
        """
        Match a question to the most appropriate pattern.
        
        Args:
            question: The interview question to analyze
            
        Returns:
            QuestionPattern that best matches the question
        """
        if not question:
            return self.patterns[QuestionType.GENERAL]
        
        question_lower = question.lower()
        best_match = QuestionType.GENERAL
        best_score = 0
        
        for question_type, pattern in self.patterns.items():
            score = 0
            for keyword in pattern.keywords:
                if keyword in question_lower:
                    score += 1
            
            if score > best_score:
                best_score = score
                best_match = question_type
        
        return self.patterns.get(best_match, self.patterns[QuestionType.GENERAL])
    
    def get_expected_elements(self, pattern: QuestionPattern) -> List[ExpectedElement]:
        """
        Get expected elements for a question pattern.
        
        Args:
            pattern: The question pattern
            
        Returns:
            List of expected elements for the pattern
        """
        return pattern.expected_elements
    
    def validate_answer_structure(self, answer: str, pattern: QuestionPattern) -> StructureValidation:
        """
        Validate if an answer contains expected structural elements.
        
        Args:
            answer: The user's answer
            pattern: The question pattern to validate against
            
        Returns:
            StructureValidation with found/missing elements and score
        """
        if not answer:
            return StructureValidation([], [], 0.0, ["Answer is empty"])
        
        answer_lower = answer.lower()
        found_elements = []
        missing_elements = []
        feedback = []
        
        for element in pattern.expected_elements:
            element_found = False
            
            # Check if any keywords for this element are present
            for keyword in element.keywords:
                if keyword in answer_lower:
                    element_found = True
                    break
            
            if element_found:
                found_elements.append(element.element_type)
            else:
                missing_elements.append(element.element_type)
                if element.required:
                    feedback.append(f"Missing {element.element_type}: {element.description}")
        
        # Calculate structure score
        total_elements = len(pattern.expected_elements)
        if total_elements > 0:
            structure_score = len(found_elements) / total_elements
        else:
            structure_score = 1.0
        
        # Add positive feedback for found elements
        if found_elements:
            feedback.append(f"Good coverage of: {', '.join(found_elements)}")
        
        return StructureValidation(
            found_elements=found_elements,
            missing_elements=missing_elements,
            structure_score=structure_score,
            feedback=feedback
        )
    
    def get_question_type_description(self, question_type: QuestionType) -> str:
        """Get description for a question type"""
        pattern = self.patterns.get(question_type)
        return pattern.description if pattern else "General interview question"