"""
Smart AI Interview Assistant with Optional Real AI
Falls back gracefully when AI dependencies are not available
"""

import os
import json
import logging
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings("ignore")

class SmartAIInterviewAssistant:
    def __init__(self):
        self.ai_available = False
        self.model = None
        self.tokenizer = None
        self.generator = None
        self.conversation_history = []
        
        # Try to initialize AI model
        self._try_initialize_ai()
        
        # Enhanced fallback responses
        self._initialize_fallback_responses()

    def _try_initialize_ai(self):
        """Try to initialize AI model, fall back gracefully if not available"""
        try:
            print("🤖 Attempting to load Real AI model...")
            
            # Try importing AI libraries
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
            
            print("✅ AI libraries available")
            
            # Try loading a lightweight model
            model_name = "distilgpt2"  # Smaller, more compatible model
            
            print(f"Loading {model_name}...")
            
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if needed
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Create pipeline
            self.generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1  # Force CPU to avoid CUDA issues
            )
            
            self.ai_available = True
            print("✅ Real AI model loaded successfully!")
            
        except ImportError as e:
            print(f"ℹ️  AI libraries not available: {e}")
            print("Using enhanced fallback responses")
            self.ai_available = False
        except Exception as e:
            print(f"⚠️  AI model loading failed: {e}")
            print("Using enhanced fallback responses")
            self.ai_available = False

    def _initialize_fallback_responses(self):
        """Initialize enhanced fallback response system"""
        
        self.enhanced_responses = {
            'introduction': [
                "I'm a software developer with 5+ years of experience building scalable web applications and leading cross-functional teams. I specialize in full-stack development with expertise in Python, JavaScript, and cloud technologies. I'm passionate about creating user-focused solutions and have successfully delivered projects that improved system performance by 40% and user engagement by 30%.",
                "I'm a results-driven software engineer with extensive experience in both frontend and backend development. I've led multiple successful projects, including a speech analysis platform that serves thousands of users. I excel at problem-solving, team collaboration, and translating business requirements into technical solutions.",
                "I bring 5+ years of software development experience with a strong track record in web applications, API design, and system optimization. I've worked with diverse teams to deliver high-quality products and am particularly skilled at mentoring junior developers and driving technical innovation."
            ],
            'strengths': [
                "My greatest strengths are analytical problem-solving and technical leadership. I excel at breaking down complex challenges into manageable solutions and communicating effectively with both technical and non-technical stakeholders. I'm also highly adaptable and consistently deliver results under pressure.",
                "I'm particularly strong in system design and cross-functional collaboration. I have a proven ability to architect scalable solutions while working closely with product, design, and QA teams. My attention to detail and commitment to code quality have consistently resulted in robust, maintainable applications.",
                "My key strengths include rapid learning and technical mentorship. I quickly master new technologies and frameworks, and I'm passionate about sharing knowledge with team members. I also excel at optimizing performance and have improved system efficiency by 50% in my previous roles."
            ],
            'weaknesses': [
                "I sometimes spend too much time perfecting technical details when a simpler solution would meet business needs. I've been working on balancing technical excellence with practical deadlines by setting clear milestones and regularly checking in with stakeholders about priorities.",
                "Early in my career, I was hesitant to delegate tasks because I wanted to ensure quality. I've learned that effective delegation and clear communication actually improve outcomes. Now I focus on providing clear requirements and regular feedback rather than doing everything myself.",
                "I used to struggle with presenting technical concepts to non-technical audiences. I've actively improved this by practicing with colleagues, using visual aids, and focusing on business impact rather than technical details. I now regularly present to executive teams and have received positive feedback."
            ],
            'motivation': [
                "I'm excited about this opportunity because it aligns perfectly with my technical expertise and career goals. The company's focus on innovation and the role's emphasis on both technical challenges and team leadership make it an ideal fit for my skills and interests. I'm particularly drawn to the opportunity to work on products that have meaningful user impact.",
                "I'm motivated by the chance to work with cutting-edge technologies while solving real-world problems. This role offers the perfect combination of technical depth and collaborative teamwork that I thrive in. I'm also excited about the company's commitment to professional development and the opportunity to grow my leadership skills.",
                "What attracts me most is the opportunity to contribute to a product that makes a genuine difference for users. I'm passionate about building scalable, efficient systems, and this role would allow me to apply my experience while learning from a talented team. The company's culture of innovation and continuous learning strongly resonates with my values."
            ],
            'challenges': [
                "I once inherited a critical project that was significantly behind schedule with unclear requirements. I conducted stakeholder interviews to clarify expectations, broke down the work into manageable sprints, and implemented daily standups for better communication. We delivered the project on time and it became one of our most successful releases.",
                "When our main database started experiencing performance issues during peak traffic, I led the optimization effort. I analyzed query patterns, implemented caching strategies, and redesigned the database schema. The result was a 60% improvement in response times and eliminated the bottlenecks that were affecting user experience.",
                "I faced a situation where two team members had conflicting approaches to a technical solution, which was delaying the project. I facilitated a technical discussion where we evaluated both approaches objectively, considering factors like maintainability, performance, and timeline. We found a hybrid solution that incorporated the best aspects of both approaches."
            ],
            'leadership': [
                "I led a cross-functional team of 8 people to deliver a complex integration project under a tight deadline. I established clear communication channels, created detailed project timelines, and held regular check-ins to track progress. By delegating tasks based on team members' strengths and maintaining open communication, we delivered the project two days early.",
                "When our team lead unexpectedly left during a critical sprint, I stepped up to coordinate the deliverables. I quickly assessed the remaining work, redistributed tasks, and maintained team morale during the transition. I also took on mentoring responsibilities for junior developers, ensuring knowledge transfer and maintaining code quality standards.",
                "I initiated and led a process improvement project that reduced our deployment time from 4 hours to 45 minutes. I gathered input from all stakeholders, researched automation tools, and presented a comprehensive proposal to management. After getting approval, I led the implementation across three teams and trained everyone on the new processes."
            ]
        }

    def get_response(self, question: str, context: Dict = None) -> str:
        """Get AI response - real AI if available, enhanced fallback otherwise"""
        
        # Add to conversation history
        self.conversation_history.append({
            'question': question,
            'context': context,
            'timestamp': 'now'
        })
        
        if self.ai_available:
            try:
                return self._generate_ai_response(question, context)
            except Exception as e:
                print(f"AI generation error: {e}")
                return self._get_enhanced_fallback_response(question, context)
        else:
            return self._get_enhanced_fallback_response(question, context)

    def _generate_ai_response(self, question: str, context: Dict = None) -> str:
        """Generate response using real AI model"""
        
        # Build prompt
        prompt = self._build_ai_prompt(question, context)
        
        # Generate response
        response = self.generator(
            prompt,
            max_length=len(prompt.split()) + 80,
            min_length=len(prompt.split()) + 20,
            num_return_sequences=1,
            temperature=0.7,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            repetition_penalty=1.2
        )
        
        # Clean and return response
        generated_text = response[0]['generated_text']
        answer = self._clean_ai_response(generated_text, prompt)
        
        return self._validate_response(answer, question)

    def _build_ai_prompt(self, question: str, context: Dict = None) -> str:
        """Build prompt for AI generation"""
        
        context_info = ""
        if context:
            if context.get('job_role'):
                context_info += f"Job Role: {context['job_role']}. "
            if context.get('company'):
                context_info += f"Company: {context['company']}. "
        
        prompt = f"""You are a professional software developer in a job interview. {context_info}
Give a direct, confident answer to this interview question. Use specific examples from your experience. Keep it professional and concise (2-3 sentences).

Interviewer: {question}
Professional Answer:"""
        
        return prompt

    def _clean_ai_response(self, generated_text: str, prompt: str) -> str:
        """Clean AI-generated response"""
        
        # Remove prompt
        if prompt in generated_text:
            response = generated_text.replace(prompt, "").strip()
        else:
            response = generated_text.strip()
        
        # Clean up common artifacts
        response = response.replace('Professional Answer:', '').strip()
        response = response.replace('Answer:', '').strip()
        
        # Split by lines and take first meaningful line
        lines = response.split('\n')
        response = lines[0].strip()
        
        # Take first 2-3 sentences
        sentences = response.split('.')
        if len(sentences) > 3:
            response = '.'.join(sentences[:3]) + '.'
        elif not response.endswith('.'):
            response = response + '.'
        
        return response

    def _validate_response(self, response: str, question: str) -> str:
        """Validate and fix response quality"""
        
        if not response or len(response) < 20:
            return self._get_enhanced_fallback_response(question)
        
        # Check if response seems inappropriate for interview
        inappropriate_indicators = [
            'i don\'t know', 'not sure', 'maybe', 'i think', 'probably',
            'what is the point', 'how do you feel', 'your focus is on'
        ]
        
        response_lower = response.lower()
        if any(indicator in response_lower for indicator in inappropriate_indicators):
            return self._get_enhanced_fallback_response(question)
        
        if response.strip().endswith('?'):
            return self._get_enhanced_fallback_response(question)
        
        if not response.strip().endswith('.'):
            response = response.strip() + '.'
        
        # Ensure reasonable length for interview
        if len(response) > 400:
            sentences = response.split('.')
            response = '.'.join(sentences[:2]) + '.'
        
        return response

    def _get_enhanced_fallback_response(self, question: str, context: Dict = None) -> str:
        """Get enhanced fallback response based on question analysis"""
        
        question_lower = question.lower().strip()
        
        # Analyze question type and return appropriate response
        if any(phrase in question_lower for phrase in [
            'tell me about yourself', 'introduce yourself', 'walk me through your background'
        ]):
            return self._get_random_response('introduction')
        
        elif any(phrase in question_lower for phrase in [
            'strength', 'good at', 'best qualities', 'what makes you'
        ]):
            return self._get_random_response('strengths')
        
        elif any(phrase in question_lower for phrase in [
            'weakness', 'improve', 'struggle with', 'not good at'
        ]):
            return self._get_random_response('weaknesses')
        
        elif any(phrase in question_lower for phrase in [
            'why', 'interested', 'company', 'role', 'position'
        ]):
            return self._get_random_response('motivation')
        
        elif any(phrase in question_lower for phrase in [
            'challenge', 'difficult', 'problem', 'tough situation'
        ]):
            return self._get_random_response('challenges')
        
        elif any(phrase in question_lower for phrase in [
            'led', 'leadership', 'manage', 'team', 'project'
        ]):
            return self._get_random_response('leadership')
        
        else:
            # Generic professional response
            return "I believe my combination of technical expertise, problem-solving skills, and collaborative approach makes me well-suited for this role. I'm committed to delivering high-quality work while contributing positively to team goals and driving successful outcomes."

    def _get_random_response(self, category: str) -> str:
        """Get a random response from the specified category"""
        import random
        responses = self.enhanced_responses.get(category, [])
        if responses:
            return random.choice(responses)
        return "I'm excited about the opportunity to contribute my skills and experience to this role."

    def get_contextual_response(self, question: str, job_role: str = None, company: str = None) -> str:
        """Generate contextual response"""
        
        context = {}
        if job_role:
            context['job_role'] = job_role
        if company:
            context['company'] = company
        
        base_response = self.get_response(question, context)
        
        # Add contextual enhancement
        if job_role and 'senior' in job_role.lower():
            base_response += " My experience in technical leadership and mentoring junior developers has prepared me well for senior-level responsibilities."
        
        return base_response

    def get_model_info(self) -> Dict:
        """Get model information"""
        
        if self.ai_available:
            return {
                'model_loaded': True,
                'model_name': 'distilgpt2',
                'device': 'cpu',
                'ai_powered': True,
                'parameters': '82M'
            }
        else:
            return {
                'model_loaded': False,
                'model_name': 'Enhanced Fallback System',
                'device': 'cpu',
                'ai_powered': False,
                'parameters': 'Rule-based with smart selection'
            }

# Global instance
smart_ai_assistant = SmartAIInterviewAssistant()