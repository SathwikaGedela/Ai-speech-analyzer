"""
Real AI Interview Assistant using Transformers
Dynamic AI-powered interview responses using local language models
"""

import os
import json
import logging
from typing import Dict, List, Optional
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    GPT2LMHeadModel,
    GPT2Tokenizer
)
import warnings
warnings.filterwarnings("ignore")

class RealAIInterviewAssistant:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.conversation_history = []
        
        # Initialize the AI model
        self._initialize_model()
        
        # Interview context and prompts
        self.system_prompt = """You are an experienced professional being interviewed for a job. You should:
- Give direct, confident answers to interview questions
- Use specific examples from your experience
- Keep responses between 2-4 sentences
- Sound professional but personable
- Never ask questions back to the interviewer
- Focus on your skills, achievements, and value you bring

Background: You are a software developer with 5+ years experience in web development, team leadership, and problem-solving."""

    def _initialize_model(self):
        """Initialize the AI model for text generation"""
        try:
            print("🤖 Initializing Real AI Model...")
            
            # Try to use a lightweight but capable model
            model_name = "microsoft/DialoGPT-medium"
            
            # Alternative models to try if the first fails
            fallback_models = [
                "gpt2",
                "distilgpt2",
                "microsoft/DialoGPT-small"
            ]
            
            models_to_try = [model_name] + fallback_models
            
            for model_name in models_to_try:
                try:
                    print(f"Trying to load model: {model_name}")
                    
                    # Load tokenizer and model
                    self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                    self.model = AutoModelForCausalLM.from_pretrained(
                        model_name,
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                        device_map="auto" if self.device == "cuda" else None
                    )
                    
                    # Add padding token if it doesn't exist
                    if self.tokenizer.pad_token is None:
                        self.tokenizer.pad_token = self.tokenizer.eos_token
                    
                    # Create text generation pipeline
                    self.generator = pipeline(
                        "text-generation",
                        model=self.model,
                        tokenizer=self.tokenizer,
                        device=0 if self.device == "cuda" else -1,
                        torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
                    )
                    
                    print(f"✅ Successfully loaded model: {model_name}")
                    print(f"Device: {self.device}")
                    break
                    
                except Exception as e:
                    print(f"❌ Failed to load {model_name}: {e}")
                    continue
            
            if self.model is None:
                raise Exception("Failed to load any AI model")
                
        except Exception as e:
            print(f"❌ Error initializing AI model: {e}")
            print("Falling back to rule-based responses...")
            self.model = None
            self.tokenizer = None
            self.generator = None

    def generate_ai_response(self, question: str, context: Dict = None) -> str:
        """Generate AI response using the language model"""
        
        if self.generator is None:
            return self._get_fallback_response(question)
        
        try:
            # Prepare the prompt
            prompt = self._build_prompt(question, context)
            
            # Generate response
            response = self.generator(
                prompt,
                max_length=len(prompt.split()) + 100,  # Limit response length
                min_length=len(prompt.split()) + 20,   # Ensure minimum response
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                repetition_penalty=1.2,
                no_repeat_ngram_size=3
            )
            
            # Extract the generated text
            generated_text = response[0]['generated_text']
            
            # Clean up the response
            answer = self._clean_response(generated_text, prompt)
            
            # Validate and post-process
            final_answer = self._post_process_response(answer, question)
            
            return final_answer
            
        except Exception as e:
            print(f"AI generation error: {e}")
            return self._get_fallback_response(question)

    def _build_prompt(self, question: str, context: Dict = None) -> str:
        """Build a proper prompt for the AI model"""
        
        # Add context if provided
        context_info = ""
        if context:
            if context.get('job_role'):
                context_info += f"Job Role: {context['job_role']}. "
            if context.get('company'):
                context_info += f"Company: {context['company']}. "
        
        # Build the prompt
        prompt = f"""Interview Context: {context_info}
{self.system_prompt}

Interviewer: {question}
Candidate:"""
        
        return prompt

    def _clean_response(self, generated_text: str, prompt: str) -> str:
        """Clean and extract the response from generated text"""
        
        # Remove the prompt from the generated text
        if prompt in generated_text:
            response = generated_text.replace(prompt, "").strip()
        else:
            response = generated_text.strip()
        
        # Split by common delimiters and take the first part
        delimiters = ['\n\nInterviewer:', '\nInterviewer:', 'Interviewer:', '\n\n', '###']
        
        for delimiter in delimiters:
            if delimiter in response:
                response = response.split(delimiter)[0].strip()
                break
        
        # Remove any remaining artifacts
        response = response.replace('Candidate:', '').strip()
        response = response.replace('Answer:', '').strip()
        
        return response

    def _post_process_response(self, response: str, question: str) -> str:
        """Post-process the AI response for quality"""
        
        if not response or len(response) < 20:
            return self._get_fallback_response(question)
        
        # Ensure it doesn't end with a question
        if response.strip().endswith('?'):
            # Try to remove the question part
            sentences = response.split('.')
            if len(sentences) > 1:
                response = '.'.join(sentences[:-1]) + '.'
            else:
                return self._get_fallback_response(question)
        
        # Ensure reasonable length
        if len(response) > 500:
            sentences = response.split('.')
            response = '.'.join(sentences[:3]) + '.'
        
        # Ensure it ends properly
        if not response.strip().endswith('.'):
            response = response.strip() + '.'
        
        return response

    def _get_fallback_response(self, question: str) -> str:
        """Fallback responses when AI fails"""
        
        question_lower = question.lower()
        
        # Smart fallback based on question type
        if any(phrase in question_lower for phrase in ['tell me about yourself', 'introduce yourself']):
            return "I'm a software developer with over 5 years of experience building scalable web applications. I specialize in full-stack development and have led several successful projects that improved user engagement and system performance. I'm passionate about creating efficient solutions and collaborating with cross-functional teams."
        
        elif any(phrase in question_lower for phrase in ['strength', 'good at']):
            return "My key strengths are problem-solving and technical leadership. I excel at breaking down complex challenges into manageable solutions and communicating effectively with both technical and non-technical stakeholders. I also adapt quickly to new technologies and methodologies."
        
        elif any(phrase in question_lower for phrase in ['weakness', 'improve']):
            return "I sometimes focus too much on perfecting technical details when a simpler solution would suffice. I've been working on balancing technical excellence with business priorities and have improved significantly by setting clear deadlines and regularly checking in with stakeholders."
        
        elif any(phrase in question_lower for phrase in ['why', 'company', 'role']):
            return "I'm excited about this opportunity because it aligns perfectly with my technical skills and career goals. The company's focus on innovation and the role's emphasis on both technical challenges and team collaboration make it an ideal fit for my experience and interests."
        
        elif any(phrase in question_lower for phrase in ['challenge', 'difficult', 'problem']):
            return "I once inherited a project that was significantly behind schedule with unclear requirements. I conducted stakeholder interviews to clarify expectations, restructured the development approach, and implemented regular check-ins. We delivered the project on time and it became one of our most successful releases."
        
        else:
            return "I believe my combination of technical expertise, problem-solving skills, and collaborative approach makes me well-suited for this role. I'm committed to delivering high-quality work while contributing positively to team goals and company success."

    def get_response(self, question: str, context: Dict = None) -> str:
        """Main method to get AI response"""
        
        # Add to conversation history
        self.conversation_history.append({
            'question': question,
            'context': context,
            'timestamp': 'now'
        })
        
        # Generate AI response
        response = self.generate_ai_response(question, context)
        
        # Add response to history
        self.conversation_history.append({
            'response': response,
            'timestamp': 'now'
        })
        
        return response

    def get_contextual_response(self, question: str, job_role: str = None, company: str = None) -> str:
        """Generate contextual response with job role and company info"""
        
        context = {}
        if job_role:
            context['job_role'] = job_role
        if company:
            context['company'] = company
        
        return self.get_response(question, context)

    def get_model_info(self) -> Dict:
        """Get information about the loaded model"""
        
        if self.model is None:
            return {
                'model_loaded': False,
                'model_name': 'None (using fallback)',
                'device': 'CPU',
                'ai_powered': False
            }
        
        return {
            'model_loaded': True,
            'model_name': self.model.config.name_or_path if hasattr(self.model.config, 'name_or_path') else 'Unknown',
            'device': self.device,
            'ai_powered': True,
            'parameters': self.model.num_parameters() if hasattr(self.model, 'num_parameters') else 'Unknown'
        }

# Global instance
real_ai_assistant = RealAIInterviewAssistant()