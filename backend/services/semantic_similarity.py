"""
Semantic Similarity Engine for Question Relevance Analysis

This module provides semantic similarity calculation between questions and answers
using sentence transformers and cosine similarity.
"""

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple, Optional
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SemanticOverlap:
    """Represents semantic overlap between question and answer"""
    shared_topics: List[str]
    question_only_topics: List[str]
    answer_only_topics: List[str]
    overlap_percentage: float

class SemanticSimilarityEngine:
    """
    Engine for calculating semantic similarity between text pairs using
    sentence transformers and cosine similarity.
    """
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize the semantic similarity engine.
        
        Args:
            model_name: Name of the sentence transformer model to use
        """
        self.model_name = model_name
        self._model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the sentence transformer model"""
        try:
            logger.info(f"Loading sentence transformer model: {self.model_name}")
            self._model = SentenceTransformer(self.model_name)
            logger.info("Sentence transformer model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer model: {e}")
            raise
    
    def get_sentence_embeddings(self, text: str) -> np.ndarray:
        """
        Generate sentence embeddings for the given text.
        
        Args:
            text: Input text to generate embeddings for
            
        Returns:
            numpy array containing the sentence embeddings
        """
        if not self._model:
            raise RuntimeError("Sentence transformer model not initialized")
        
        try:
            # Clean and prepare text
            cleaned_text = self._clean_text(text)
            if not cleaned_text.strip():
                # Return zero vector for empty text
                return np.zeros(self._model.get_sentence_embedding_dimension())
            
            # Generate embeddings
            embeddings = self._model.encode([cleaned_text])
            return embeddings[0]
        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            # Return zero vector as fallback
            return np.zeros(self._model.get_sentence_embedding_dimension())
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate cosine similarity between two text strings.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            Cosine similarity score between 0 and 1
        """
        try:
            # Generate embeddings for both texts
            embedding1 = self.get_sentence_embeddings(text1)
            embedding2 = self.get_sentence_embeddings(text2)
            
            # Calculate cosine similarity
            similarity = cosine_similarity([embedding1], [embedding2])[0][0]
            
            # Ensure similarity is between 0 and 1
            similarity = max(0.0, min(1.0, similarity))
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Failed to calculate similarity: {e}")
            return 0.0
    
    def find_semantic_overlap(self, question: str, answer: str) -> SemanticOverlap:
        """
        Find semantic overlap between question and answer by analyzing
        key topics and concepts.
        
        Args:
            question: The interview question
            answer: The user's answer
            
        Returns:
            SemanticOverlap object containing overlap analysis
        """
        try:
            # Extract key topics from both texts
            question_topics = self._extract_key_topics(question)
            answer_topics = self._extract_key_topics(answer)
            
            # Find overlapping topics using semantic similarity
            shared_topics = []
            question_only_topics = []
            answer_only_topics = list(answer_topics)
            
            for q_topic in question_topics:
                best_match = None
                best_similarity = 0.0
                
                for a_topic in answer_topics:
                    similarity = self.calculate_similarity(q_topic, a_topic)
                    if similarity > best_similarity:
                        best_similarity = similarity
                        best_match = a_topic
                
                # Consider topics similar if similarity > 0.6
                if best_similarity > 0.6 and best_match:
                    shared_topics.append(q_topic)
                    if best_match in answer_only_topics:
                        answer_only_topics.remove(best_match)
                else:
                    question_only_topics.append(q_topic)
            
            # Calculate overlap percentage
            total_topics = len(question_topics) + len(answer_topics)
            if total_topics > 0:
                overlap_percentage = (len(shared_topics) * 2) / total_topics * 100
            else:
                overlap_percentage = 0.0
            
            return SemanticOverlap(
                shared_topics=shared_topics,
                question_only_topics=question_only_topics,
                answer_only_topics=answer_only_topics,
                overlap_percentage=overlap_percentage
            )
        except Exception as e:
            logger.error(f"Failed to find semantic overlap: {e}")
            return SemanticOverlap([], [], [], 0.0)
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text for processing"""
        if not text:
            return ""
        
        # Basic text cleaning
        cleaned = text.strip()
        # Remove excessive whitespace
        cleaned = ' '.join(cleaned.split())
        
        return cleaned
    
    def _extract_key_topics(self, text: str) -> List[str]:
        """
        Extract key topics from text using improved keyword extraction.
        """
        if not text:
            return []
        
        # Clean text
        cleaned_text = self._clean_text(text.lower())
        
        # Split into sentences and words
        sentences = [s.strip() for s in cleaned_text.split('.') if s.strip()]
        words = cleaned_text.split()
        
        # Extract meaningful phrases and keywords
        topics = []
        
        # Add important keywords
        important_keywords = [
            'experience', 'skills', 'background', 'work', 'project', 'team', 'leadership',
            'challenge', 'problem', 'solution', 'result', 'achievement', 'goal', 'career',
            'strength', 'weakness', 'learn', 'develop', 'manage', 'technical', 'software',
            'development', 'programming', 'design', 'implement', 'analyze', 'improve'
        ]
        
        for keyword in important_keywords:
            if keyword in words:
                topics.append(keyword)
        
        # Add meaningful phrases (2-3 word combinations)
        for i in range(len(words) - 1):
            phrase = f"{words[i]} {words[i+1]}"
            if len(phrase) > 6 and any(keyword in phrase for keyword in important_keywords):
                topics.append(phrase)
        
        # Add sentences as topics if they're substantial
        for sentence in sentences:
            if len(sentence.split()) >= 4 and len(sentence.split()) <= 15:
                topics.append(sentence)
        
        # Remove duplicates and return top topics
        unique_topics = list(dict.fromkeys(topics))  # Preserve order while removing duplicates
        return unique_topics[:8]  # Return top 8 topics