"""
Question Relevance Analyzer for Interview Mode

This module provides the core functionality for analyzing whether interview answers
are relevant to the questions asked, providing scores, classifications, and feedback.
"""

import time
from enum import Enum
from typing import List, Dict, Optional
from dataclasses import dataclass
import logging

from .semantic_similarity import SemanticSimilarityEngine, SemanticOverlap
from .question_patterns import QuestionPatternMatcher, QuestionType, QuestionPattern, StructureValidation

logger = logging.getLogger(__name__)

class RelevanceClassification(Enum):
    """Classification levels for answer relevance"""
    HIGHLY_RELEVANT = "Highly Relevant"      # 80-100%
    MOSTLY_RELEVANT = "Mostly Relevant"      # 60-79%
    PARTIALLY_RELEVANT = "Partially Relevant" # 40-59%
    MINIMALLY_RELEVANT = "Minimally Relevant" # 20-39%
    OFF_TOPIC = "Off-Topic"                  # 0-19%

class FeedbackPriority(Enum):
    """Priority levels for feedback intensity"""
    LOW = "low"      # Brief positive reinforcement
    MEDIUM = "medium"  # Moderate feedback
    HIGH = "high"    # Detailed guidance

@dataclass
class TopicDrift:
    """Information about topic drift in an answer"""
    detected: bool
    off_topic_content: List[str]
    suggested_topics: List[str]
    drift_severity: float  # 0-1, higher means more drift

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
    topic_overlap: SemanticOverlap
    topic_drift: Optional[TopicDrift]
    structure_validation: StructureValidation
    feedback: RelevanceFeedback
    processing_time: float

class QuestionRelevanceAnalyzer:
    """
    Core analyzer for question-answer relevance in interview mode
    """
    
    def __init__(self):
        """Initialize the relevance analyzer with required components"""
        self.semantic_engine = SemanticSimilarityEngine()
        self.pattern_matcher = QuestionPatternMatcher()
        self.feedback_generator = FeedbackGenerator()
    
    def analyze_relevance(self, question: str, answer: str) -> RelevanceResult:
        """
        Analyze the relevance between a question and answer.
        
        Args:
            question: The interview question
            answer: The user's answer
            
        Returns:
            RelevanceResult with comprehensive analysis
        """
        start_time = time.time()
        
        try:
            # Step 1: Classify question type
            question_pattern = self.pattern_matcher.match_pattern(question)
            question_type = question_pattern.question_type
            
            # Step 2: Calculate semantic similarity
            semantic_similarity = self.semantic_engine.calculate_similarity(question, answer)
            
            # Step 3: Analyze topic overlap
            topic_overlap = self.semantic_engine.find_semantic_overlap(question, answer)
            
            # Step 4: Validate answer structure
            structure_validation = self.pattern_matcher.validate_answer_structure(answer, question_pattern)
            
            # Step 5: Detect topic drift
            topic_drift = self.detect_topic_drift(question, answer, topic_overlap)
            
            # Step 6: Calculate overall relevance score
            relevance_score = self._calculate_relevance_score(
                semantic_similarity, topic_overlap, structure_validation, topic_drift
            )
            
            # Step 7: Classify relevance level
            classification = self._classify_relevance(relevance_score)
            
            # Step 8: Generate feedback
            feedback = self.feedback_generator.generate_relevance_feedback(
                question, answer, question_type, relevance_score, classification,
                topic_overlap, structure_validation, topic_drift
            )
            
            processing_time = time.time() - start_time
            
            return RelevanceResult(
                relevance_score=relevance_score,
                classification=classification,
                question_type=question_type,
                semantic_similarity=semantic_similarity,
                topic_overlap=topic_overlap,
                topic_drift=topic_drift,
                structure_validation=structure_validation,
                feedback=feedback,
                processing_time=processing_time
            )
            
        except Exception as e:
            logger.error(f"Error in relevance analysis: {e}")
            processing_time = time.time() - start_time
            
            # Return fallback result
            return self._create_fallback_result(question, answer, processing_time)
    
    def classify_question_type(self, question: str) -> QuestionType:
        """Classify the type of interview question"""
        pattern = self.pattern_matcher.match_pattern(question)
        return pattern.question_type
    
    def extract_topics(self, text: str) -> List[str]:
        """Extract key topics from text"""
        return self.semantic_engine._extract_key_topics(text)
    
    def detect_topic_drift(self, question: str, answer: str, topic_overlap: SemanticOverlap) -> TopicDrift:
        """
        Detect if the answer drifts away from the question topic.
        
        Args:
            question: The interview question
            answer: The user's answer
            topic_overlap: Topic overlap analysis
            
        Returns:
            TopicDrift information
        """
        try:
            # Calculate drift based on topic overlap
            drift_detected = topic_overlap.overlap_percentage < 30.0
            
            # Identify off-topic content (topics only in answer)
            off_topic_content = topic_overlap.answer_only_topics
            
            # Suggest topics that should have been covered
            suggested_topics = topic_overlap.question_only_topics
            
            # Calculate drift severity
            if topic_overlap.overlap_percentage >= 70:
                drift_severity = 0.0  # No drift
            elif topic_overlap.overlap_percentage >= 50:
                drift_severity = 0.3  # Mild drift
            elif topic_overlap.overlap_percentage >= 30:
                drift_severity = 0.6  # Moderate drift
            else:
                drift_severity = 1.0  # Severe drift
            
            return TopicDrift(
                detected=drift_detected,
                off_topic_content=off_topic_content[:3],  # Limit to top 3
                suggested_topics=suggested_topics[:3],    # Limit to top 3
                drift_severity=drift_severity
            )
            
        except Exception as e:
            logger.error(f"Error detecting topic drift: {e}")
            return TopicDrift(False, [], [], 0.0)
    
    def _calculate_relevance_score(self, semantic_similarity: float, topic_overlap: SemanticOverlap,
                                 structure_validation: StructureValidation, topic_drift: TopicDrift) -> float:
        """
        Calculate overall relevance score from multiple factors.
        
        Args:
            semantic_similarity: Semantic similarity score (0-1)
            topic_overlap: Topic overlap analysis
            structure_validation: Answer structure validation
            topic_drift: Topic drift analysis
            
        Returns:
            Relevance score (0-100)
        """
        try:
            # Adjust weights to be more generous for good answers
            semantic_weight = 0.3
            topic_weight = 0.2
            structure_weight = 0.3
            base_score_weight = 0.2  # Base score for any reasonable answer
            
            # Semantic similarity component (0-30 points)
            # Apply a curve to make moderate similarity more valuable
            adjusted_semantic = min(1.0, semantic_similarity * 2.0)  # Boost semantic scores
            semantic_component = adjusted_semantic * 100 * semantic_weight
            
            # Topic overlap component (0-20 points)
            # Be more generous with topic overlap
            adjusted_overlap = min(100.0, topic_overlap.overlap_percentage * 1.5)
            topic_component = (adjusted_overlap / 100) * 100 * topic_weight
            
            # Structure component (0-30 points)
            structure_component = structure_validation.structure_score * 100 * structure_weight
            
            # Base score for reasonable length answers (0-20 points)
            # Give credit for providing a substantial answer
            base_score = 20 * base_score_weight  # Default base score
            
            # Topic drift penalty (reduce by drift severity)
            drift_penalty = topic_drift.drift_severity * 15  # Max 15 point penalty
            
            # Calculate final score
            relevance_score = semantic_component + topic_component + structure_component + base_score - drift_penalty
            
            # Apply minimum score for answers that show some effort
            if structure_validation.structure_score > 0.3:  # If answer has some structure
                relevance_score = max(relevance_score, 25.0)  # Minimum 25% for structured answers
            
            # Ensure score is between 0 and 100
            relevance_score = max(0.0, min(100.0, relevance_score))
            
            return round(relevance_score, 1)
            
        except Exception as e:
            logger.error(f"Error calculating relevance score: {e}")
            return 0.0
    
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
    
    def _create_fallback_result(self, question: str, answer: str, processing_time: float) -> RelevanceResult:
        """Create a fallback result when analysis fails"""
        from .semantic_similarity import SemanticOverlap
        from .question_patterns import StructureValidation
        
        return RelevanceResult(
            relevance_score=0.0,
            classification=RelevanceClassification.OFF_TOPIC,
            question_type=QuestionType.GENERAL,
            semantic_similarity=0.0,
            topic_overlap=SemanticOverlap([], [], [], 0.0),
            topic_drift=TopicDrift(True, [], [], 1.0),
            structure_validation=StructureValidation([], [], 0.0, ["Analysis failed"]),
            feedback=RelevanceFeedback(
                summary="Analysis failed. Please try again.",
                strengths=[],
                improvements=["Please ensure your answer addresses the question"],
                specific_suggestions=[],
                example_elements=[],
                priority_level=FeedbackPriority.HIGH
            ),
            processing_time=processing_time
        )

class FeedbackGenerator:
    """Generates specific feedback based on relevance analysis results"""
    
    def generate_relevance_feedback(self, question: str, answer: str, question_type: QuestionType,
                                  relevance_score: float, classification: RelevanceClassification,
                                  topic_overlap: SemanticOverlap, structure_validation: StructureValidation,
                                  topic_drift: TopicDrift) -> RelevanceFeedback:
        """Generate comprehensive feedback for the relevance analysis"""
        
        # Determine feedback priority based on score
        if relevance_score >= 80:
            priority = FeedbackPriority.LOW
        elif relevance_score >= 60:
            priority = FeedbackPriority.MEDIUM
        else:
            priority = FeedbackPriority.HIGH
        
        # Generate summary
        summary = self._generate_summary(classification, relevance_score)
        
        # Generate strengths
        strengths = self._generate_strengths(topic_overlap, structure_validation, relevance_score)
        
        # Generate improvements
        improvements = self._generate_improvements(topic_drift, structure_validation, relevance_score)
        
        # Generate specific suggestions
        suggestions = self._generate_suggestions(question_type, topic_drift, structure_validation)
        
        # Generate example elements
        examples = self._generate_examples(question_type, structure_validation)
        
        return RelevanceFeedback(
            summary=summary,
            strengths=strengths,
            improvements=improvements,
            specific_suggestions=suggestions,
            example_elements=examples,
            priority_level=priority
        )
    
    def _generate_summary(self, classification: RelevanceClassification, score: float) -> str:
        """Generate summary based on classification and score"""
        summaries = {
            RelevanceClassification.HIGHLY_RELEVANT: f"Excellent! Your answer directly addresses the question ({score}% relevance).",
            RelevanceClassification.MOSTLY_RELEVANT: f"Good job! Your answer mostly addresses the question ({score}% relevance).",
            RelevanceClassification.PARTIALLY_RELEVANT: f"Your answer partially addresses the question ({score}% relevance). Consider focusing more on the specific question asked.",
            RelevanceClassification.MINIMALLY_RELEVANT: f"Your answer has minimal relevance to the question ({score}% relevance). Try to address the question more directly.",
            RelevanceClassification.OFF_TOPIC: f"Your answer appears to be off-topic ({score}% relevance). Please focus on answering the specific question asked."
        }
        return summaries.get(classification, f"Relevance score: {score}%")
    
    def _generate_strengths(self, topic_overlap: SemanticOverlap, structure_validation: StructureValidation, score: float) -> List[str]:
        """Generate list of strengths in the answer"""
        strengths = []
        
        if topic_overlap.shared_topics:
            strengths.append(f"You covered relevant topics: {', '.join(topic_overlap.shared_topics[:2])}")
        
        if structure_validation.found_elements:
            strengths.append(f"Good structure with: {', '.join(structure_validation.found_elements)}")
        
        if score >= 60:
            strengths.append("Your answer demonstrates understanding of the question")
        
        return strengths
    
    def _generate_improvements(self, topic_drift: TopicDrift, structure_validation: StructureValidation, score: float) -> List[str]:
        """Generate list of improvements needed"""
        improvements = []
        
        if topic_drift.detected and topic_drift.off_topic_content:
            improvements.append("Avoid discussing unrelated topics")
        
        if structure_validation.missing_elements:
            improvements.append(f"Include missing elements: {', '.join(structure_validation.missing_elements)}")
        
        if score < 60:
            improvements.append("Focus more directly on answering the specific question asked")
        
        return improvements
    
    def _generate_suggestions(self, question_type: QuestionType, topic_drift: TopicDrift, structure_validation: StructureValidation) -> List[str]:
        """Generate specific suggestions based on question type"""
        suggestions = []
        
        if question_type == QuestionType.BEHAVIORAL:
            suggestions.append("Use the STAR method: Situation, Task, Action, Result")
        elif question_type == QuestionType.TECHNICAL:
            suggestions.append("Explain the concept, provide methodology, and give examples")
        elif question_type == QuestionType.PERSONAL:
            suggestions.append("Cover your background, key skills, and career goals")
        
        if topic_drift.suggested_topics:
            suggestions.append(f"Consider discussing: {', '.join(topic_drift.suggested_topics[:2])}")
        
        return suggestions
    
    def _generate_examples(self, question_type: QuestionType, structure_validation: StructureValidation) -> List[str]:
        """Generate example elements for the question type"""
        examples = {
            QuestionType.BEHAVIORAL: [
                "Start with the situation/context",
                "Describe your specific task or challenge",
                "Explain the actions you took",
                "Share the results and what you learned"
            ],
            QuestionType.TECHNICAL: [
                "Define the technical concept clearly",
                "Explain your approach or methodology",
                "Provide a specific example or use case",
                "Discuss trade-offs or considerations"
            ],
            QuestionType.PERSONAL: [
                "Share your professional background",
                "Highlight your key skills and expertise",
                "Mention your career goals and aspirations"
            ]
        }
        
        return examples.get(question_type, ["Focus on directly answering the question asked"])