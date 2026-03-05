"""
Property Tests for Question Relevance Analysis

These tests validate universal properties that should hold across all
question-answer combinations for the relevance analysis system.
"""

import pytest
import random
import string
from typing import List, Tuple
import time

from backend.services.question_relevance import QuestionRelevanceAnalyzer, RelevanceClassification
from backend.services.semantic_similarity import SemanticSimilarityEngine
from backend.services.question_patterns import QuestionPatternMatcher, QuestionType

class TestQuestionRelevanceProperties:
    """Property tests for question relevance analysis"""
    
    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance for testing"""
        return QuestionRelevanceAnalyzer()
    
    @pytest.fixture
    def test_data_generator(self):
        """Generate test data for property tests"""
        return TestDataGenerator()
    
    def test_property_1_relevance_score_validity(self, analyzer, test_data_generator):
        """
        Property 1: Relevance Score Validity
        For any question and answer pair, the relevance score should always be between 0 and 100 inclusive
        Validates: Requirements 1.2
        """
        # Test with 100 random question-answer pairs
        for _ in range(100):
            question, answer = test_data_generator.generate_random_qa_pair()
            
            result = analyzer.analyze_relevance(question, answer)
            
            # Property: Score must be between 0 and 100 inclusive
            assert 0.0 <= result.relevance_score <= 100.0, \
                f"Relevance score {result.relevance_score} is outside valid range [0, 100]"
            
            # Property: Score should be a float
            assert isinstance(result.relevance_score, (int, float)), \
                f"Relevance score should be numeric, got {type(result.relevance_score)}"
    
    def test_property_2_classification_consistency(self, analyzer, test_data_generator):
        """
        Property 2: Classification Consistency
        For any relevance score, the classification should match the defined ranges
        Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5
        """
        # Test with various question-answer pairs
        for _ in range(100):
            question, answer = test_data_generator.generate_random_qa_pair()
            
            result = analyzer.analyze_relevance(question, answer)
            score = result.relevance_score
            classification = result.classification
            
            # Property: Classification must match score ranges
            if 80 <= score <= 100:
                assert classification == RelevanceClassification.HIGHLY_RELEVANT
            elif 60 <= score < 80:
                assert classification == RelevanceClassification.MOSTLY_RELEVANT
            elif 40 <= score < 60:
                assert classification == RelevanceClassification.PARTIALLY_RELEVANT
            elif 20 <= score < 40:
                assert classification == RelevanceClassification.MINIMALLY_RELEVANT
            elif 0 <= score < 20:
                assert classification == RelevanceClassification.OFF_TOPIC
            else:
                pytest.fail(f"Score {score} doesn't fit any classification range")

class TestDataGenerator:
    """Generates test data for property testing"""
    
    def __init__(self):
        self.sample_questions = [
            "Tell me about yourself",
            "Describe a challenging situation you faced",
            "What are your strengths and weaknesses?",
            "Why should we hire you?",
            "How would you handle a difficult team member?",
            "Explain object-oriented programming",
            "What motivates you in your career?"
        ]
        
        self.sample_answers = [
            "I have 5 years of experience in software development",
            "I worked on a project where we had tight deadlines",
            "My strength is problem-solving and attention to detail",
            "I bring strong technical skills and leadership experience",
            "I would communicate openly and find common ground",
            "OOP is a programming paradigm based on objects and classes",
            "I'm motivated by solving complex problems and learning new technologies"
        ]
    
    def generate_random_qa_pair(self) -> Tuple[str, str]:
        """Generate a random question-answer pair"""
        question = random.choice(self.sample_questions)
        answer = random.choice(self.sample_answers)
        
        # Sometimes generate completely random text
        if random.random() < 0.2:
            question = self._generate_random_text(10, 50)
        if random.random() < 0.2:
            answer = self._generate_random_text(20, 100)
        
        return question, answer
    
    def _generate_random_text(self, min_words: int, max_words: int) -> str:
        """Generate random text with specified word count range"""
        word_count = random.randint(min_words, max_words)
        words = []
        
        for _ in range(word_count):
            word_length = random.randint(3, 10)
            word = ''.join(random.choices(string.ascii_lowercase, k=word_length))
            words.append(word)
        
        return ' '.join(words)
    def test_property_3_semantic_analysis_completeness(self, analyzer, test_data_generator):
        """
        Property 3: Semantic Analysis Completeness
        For any question-answer pair, semantic analysis should identify topics in both question and answer,
        calculate similarity, and detect topic drift when present
        Validates: Requirements 1.1, 1.3, 1.4
        """
        for _ in range(50):
            question, answer = test_data_generator.generate_random_qa_pair()
            
            result = analyzer.analyze_relevance(question, answer)
            
            # Property: Semantic similarity should be between 0 and 1
            assert 0.0 <= result.semantic_similarity <= 1.0, \
                f"Semantic similarity {result.semantic_similarity} is outside valid range [0, 1]"
            
            # Property: Topic overlap should have valid percentage
            assert 0.0 <= result.topic_overlap.overlap_percentage <= 100.0, \
                f"Topic overlap percentage {result.topic_overlap.overlap_percentage} is outside valid range [0, 100]"
            
            # Property: Topic drift should be detected when overlap is low
            if result.topic_overlap.overlap_percentage < 30.0:
                assert result.topic_drift.detected, \
                    "Topic drift should be detected when overlap percentage is below 30%"
            
            # Property: All topic lists should be lists
            assert isinstance(result.topic_overlap.shared_topics, list)
            assert isinstance(result.topic_overlap.question_only_topics, list)
            assert isinstance(result.topic_overlap.answer_only_topics, list)
    
    def test_property_4_performance_constraint(self, analyzer, test_data_generator):
        """
        Property 4: Performance Constraint
        For any transcript input, relevance analysis should complete within 3 seconds
        Validates: Requirements 1.5
        """
        for _ in range(20):  # Fewer iterations for performance test
            question, answer = test_data_generator.generate_random_qa_pair()
            
            start_time = time.time()
            result = analyzer.analyze_relevance(question, answer)
            end_time = time.time()
            
            processing_time = end_time - start_time
            
            # Property: Analysis should complete within 3 seconds
            assert processing_time <= 3.0, \
                f"Analysis took {processing_time:.2f} seconds, exceeding 3-second limit"
            
            # Property: Processing time should match reported time (within tolerance)
            assert abs(processing_time - result.processing_time) <= 0.1, \
                f"Reported processing time {result.processing_time} doesn't match actual time {processing_time}"
    
    def test_property_5_question_type_analysis(self, analyzer, test_data_generator):
        """
        Property 5: Question Type Analysis
        For any interview question, the analyzer should correctly identify question type
        and look for appropriate elements
        Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 6.1, 6.2, 6.3, 6.4
        """
        # Test with known question types
        behavioral_questions = [
            "Tell me about a time when you faced a challenge",
            "Describe a situation where you had to work with a difficult person",
            "Give me an example of when you showed leadership"
        ]
        
        technical_questions = [
            "Explain how you would design a database",
            "What is object-oriented programming?",
            "How would you implement a sorting algorithm?"
        ]
        
        personal_questions = [
            "Tell me about yourself",
            "What are your career goals?",
            "Describe your background and experience"
        ]
        
        # Test behavioral questions
        for question in behavioral_questions:
            answer = "I worked on a project where we had challenges with deadlines. I took action by organizing the team and we achieved success."
            result = analyzer.analyze_relevance(question, answer)
            
            # Property: Behavioral questions should be classified correctly
            assert result.question_type == QuestionType.BEHAVIORAL, \
                f"Question '{question}' should be classified as BEHAVIORAL, got {result.question_type}"
        
        # Test technical questions
        for question in technical_questions:
            answer = "The concept involves using classes and objects to organize code with inheritance and polymorphism."
            result = analyzer.analyze_relevance(question, answer)
            
            # Property: Technical questions should be classified correctly
            assert result.question_type == QuestionType.TECHNICAL, \
                f"Question '{question}' should be classified as TECHNICAL, got {result.question_type}"
        
        # Test personal questions
        for question in personal_questions:
            answer = "I have a background in software engineering with experience in various technologies and my goal is to grow as a leader."
            result = analyzer.analyze_relevance(question, answer)
            
            # Property: Personal questions should be classified correctly
            assert result.question_type == QuestionType.PERSONAL, \
                f"Question '{question}' should be classified as PERSONAL, got {result.question_type}"
    
    def test_property_6_feedback_completeness(self, analyzer, test_data_generator):
        """
        Property 6: Feedback Completeness
        For any analysis result, the system should provide feedback that includes relevance score,
        classification, specific suggestions, and examples appropriate to the question type
        Validates: Requirements 2.6, 3.4, 3.5
        """
        for _ in range(50):
            question, answer = test_data_generator.generate_random_qa_pair()
            
            result = analyzer.analyze_relevance(question, answer)
            feedback = result.feedback
            
            # Property: Feedback should have all required components
            assert feedback.summary, "Feedback should include a summary"
            assert isinstance(feedback.strengths, list), "Feedback should include strengths list"
            assert isinstance(feedback.improvements, list), "Feedback should include improvements list"
            assert isinstance(feedback.specific_suggestions, list), "Feedback should include specific suggestions"
            assert isinstance(feedback.example_elements, list), "Feedback should include example elements"
            assert feedback.priority_level, "Feedback should have a priority level"
            
            # Property: Summary should mention the relevance score
            assert str(int(result.relevance_score)) in feedback.summary or f"{result.relevance_score}" in feedback.summary, \
                "Feedback summary should mention the relevance score"
    
    def test_property_7_adaptive_feedback_intensity(self, analyzer):
        """
        Property 7: Adaptive Feedback Intensity
        For any relevance score, feedback detail should increase as relevance decreases
        Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.5
        """
        # Create test cases with different relevance levels
        test_cases = [
            ("Tell me about yourself", "I have extensive experience in software development with strong leadership skills and clear career goals", "high_relevance"),
            ("Tell me about yourself", "I like programming and have some experience", "medium_relevance"),
            ("Tell me about yourself", "The weather is nice today and I enjoy cooking", "low_relevance")
        ]
        
        for question, answer, expected_level in test_cases:
            result = analyzer.analyze_relevance(question, answer)
            feedback = result.feedback
            
            # Property: Higher relevance should have lower priority feedback
            if result.relevance_score >= 80:
                # Brief feedback for high relevance
                assert len(feedback.improvements) <= 2, \
                    f"High relevance answers should have brief feedback, got {len(feedback.improvements)} improvements"
            elif result.relevance_score < 60:
                # Detailed feedback for low relevance
                assert len(feedback.specific_suggestions) >= 1, \
                    f"Low relevance answers should have detailed suggestions, got {len(feedback.specific_suggestions)}"
                assert len(feedback.example_elements) >= 1, \
                    f"Low relevance answers should have example elements, got {len(feedback.example_elements)}"

if __name__ == "__main__":
    # Run property tests
    pytest.main([__file__, "-v"])