"""
Universal Chatbot Service
Provides intelligent responses to any type of question, not just interview-related
"""

import os
import json
import re
import random
from typing import Dict, List, Optional
import openai
from .interview_chatbot import interview_chatbot as fallback_chatbot
from .comprehensive_knowledge_base import comprehensive_kb

class UniversalChatbot:
    def __init__(self):
        # Initialize OpenAI client
        self.api_key = os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
            self.openai_available = True
        else:
            self.openai_available = False
            print("Warning: OPENAI_API_KEY not found. Using enhanced fallback chatbot.")
        
        self.conversation_history = []
        self.user_context = {
            'selected_category': None,
            'selected_question': None,
            'analysis_results': None,
            'session_stage': 'initial'
        }
        
        # Universal system prompt that can handle any question
        self.system_prompt = """You are a helpful, knowledgeable, and friendly AI assistant. You can answer questions on any topic and provide useful information and guidance. Your responses should be:

1. ACCURATE and INFORMATIVE - Provide correct, helpful information
2. CLEAR and WELL-STRUCTURED - Use bullet points, examples, and clear explanations
3. CONVERSATIONAL and FRIENDLY - Be warm and engaging while remaining professional
4. COMPREHENSIVE but CONCISE - Cover the topic thoroughly but don't be overly verbose
5. PRACTICAL and ACTIONABLE - Give specific steps, tips, or advice when relevant

You have expertise in many areas including:
- Interview preparation and career advice
- Technology, programming, and software development
- General knowledge and education
- Problem-solving and decision-making
- Communication and interpersonal skills
- Business and professional development
- Science, mathematics, and research
- Creative writing and content creation
- Health, wellness, and lifestyle
- And many other topics

When someone asks about interviews specifically, provide detailed interview coaching. For other topics, provide helpful, accurate information. Always aim to be genuinely helpful and provide value in your responses."""

    def update_context(self, **kwargs):
        """Update the chatbot's context about the user's session"""
        self.user_context.update(kwargs)

    def get_response(self, user_message: str) -> str:
        """Generate an intelligent response using OpenAI or enhanced fallback"""
        
        # Add to conversation history
        self.conversation_history.append({
            'role': 'user',
            'content': user_message,
            'timestamp': 'now'
        })
        
        # Try OpenAI first, fallback to enhanced local chatbot if unavailable
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
                # Fall back to enhanced local chatbot
                return self._get_enhanced_fallback_response(user_message)
        else:
            # Use enhanced fallback chatbot
            return self._get_enhanced_fallback_response(user_message)

    def _get_openai_response(self, user_message: str) -> str:
        """Get response from OpenAI GPT model"""
        
        # Build context-aware prompt
        context_info = self._build_context_prompt()
        
        # Prepare messages for OpenAI
        messages = [
            {"role": "system", "content": self.system_prompt + context_info}
        ]
        
        # Add recent conversation history (last 8 messages to stay within token limits)
        recent_history = self.conversation_history[-8:] if len(self.conversation_history) > 8 else self.conversation_history
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
            max_tokens=800,  # Increased for more comprehensive responses
            temperature=0.7,
            top_p=1,
            frequency_penalty=0.2,
            presence_penalty=0.1
        )
        
        return response.choices[0].message.content.strip()

    def _get_enhanced_fallback_response(self, user_message: str) -> str:
        """Enhanced fallback response system that can handle any question"""
        
        user_message_lower = user_message.lower().strip()
        
        # First, check comprehensive knowledge base for perfect answers
        kb_response = comprehensive_kb.get_response(user_message)
        if kb_response:
            return kb_response
        
        # Check if it's interview-related first
        interview_keywords = [
            'interview', 'job', 'career', 'resume', 'cv', 'hiring', 'employer', 
            'star method', 'behavioral', 'weakness', 'strength', 'salary', 
            'tell me about yourself', 'why do you want', 'questions to ask'
        ]
        
        if any(keyword in user_message_lower for keyword in interview_keywords):
            # Use the specialized interview chatbot for interview questions
            return fallback_chatbot.get_response(user_message)
        
        # Handle general questions with comprehensive responses
        return self._handle_general_question(user_message_lower, user_message)
    
    def _handle_general_question(self, user_message_lower: str, original_message: str) -> str:
        """Handle general non-interview questions with helpful responses"""
        
        # Programming and Technology
        if any(word in user_message_lower for word in ['programming', 'code', 'coding', 'python', 'javascript', 'java', 'react', 'node', 'database', 'sql', 'api', 'web development', 'software']):
            return self._get_programming_response(user_message_lower, original_message)
        
        # Science and Mathematics
        elif any(word in user_message_lower for word in ['math', 'mathematics', 'science', 'physics', 'chemistry', 'biology', 'calculate', 'formula', 'equation']):
            return self._get_science_response(user_message_lower, original_message)
        
        # Business and Finance
        elif any(word in user_message_lower for word in ['business', 'marketing', 'finance', 'investment', 'startup', 'entrepreneur', 'money', 'budget', 'economics']):
            return self._get_business_response(user_message_lower, original_message)
        
        # Health and Wellness
        elif any(word in user_message_lower for word in ['health', 'fitness', 'exercise', 'diet', 'nutrition', 'wellness', 'mental health', 'stress']):
            return self._get_health_response(user_message_lower, original_message)
        
        # Education and Learning
        elif any(word in user_message_lower for word in ['learn', 'study', 'education', 'school', 'university', 'course', 'tutorial', 'skill']):
            return self._get_education_response(user_message_lower, original_message)
        
        # Creative and Writing
        elif any(word in user_message_lower for word in ['write', 'writing', 'creative', 'story', 'blog', 'content', 'design', 'art']):
            return self._get_creative_response(user_message_lower, original_message)
        
        # Communication and Social
        elif any(word in user_message_lower for word in ['communication', 'social', 'relationship', 'team', 'leadership', 'presentation', 'public speaking']):
            return self._get_communication_response(user_message_lower, original_message)
        
        # Problem-solving and Decision-making
        elif any(word in user_message_lower for word in ['problem', 'solve', 'decision', 'choose', 'help me', 'advice', 'what should i']):
            return self._get_problem_solving_response(user_message_lower, original_message)
        
        # Greetings and Social
        elif any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'how are you']):
            return "Hello! I'm here to help you with any questions you have. Whether it's about interviews, technology, learning, problem-solving, or any other topic, feel free to ask me anything. What would you like to know about today?"
        
        # Thanks and Appreciation
        elif any(word in user_message_lower for word in ['thank', 'thanks', 'appreciate']):
            return "You're very welcome! I'm glad I could help. If you have any other questions about anything - whether it's interviews, technology, learning, or any other topic - feel free to ask anytime!"
        
        # Default comprehensive response
        else:
            return self._get_comprehensive_default_response(original_message)
    
    def _get_programming_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle programming and technology questions"""
        
        # Database Management Systems
        if 'dbms' in user_message_lower or 'database management system' in user_message_lower:
            return "**DBMS (Database Management System)** is software that manages databases and provides an interface for users and applications to interact with data.\n\n**Key Functions**:\n• **Data Storage**: Organize and store large amounts of data efficiently\n• **Data Retrieval**: Query and retrieve specific information quickly\n• **Data Security**: Control access and protect sensitive information\n• **Data Integrity**: Ensure data accuracy and consistency\n• **Concurrent Access**: Allow multiple users to access data simultaneously\n\n**Popular DBMS Examples**:\n• **Relational**: MySQL, PostgreSQL, Oracle, SQL Server\n• **NoSQL**: MongoDB, Cassandra, Redis\n• **Cloud**: Amazon RDS, Google Cloud SQL\n\n**Benefits**: Data organization, reduced redundancy, improved security, backup/recovery, and scalability."
        
        # Variables in Programming
        elif 'variables' in user_message_lower and ('programming' in user_message_lower or 'code' in user_message_lower or original_message.endswith('?')):
            return "**Variables** are containers that store data values in programming. Think of them as labeled boxes that hold information.\n\n**Key Concepts**:\n• **Declaration**: Creating a variable (e.g., `name = \"John\"`)\n• **Assignment**: Giving a variable a value\n• **Data Types**: Different kinds of data variables can hold\n\n**Common Data Types**:\n• **String**: Text data (`\"Hello World\"`)\n• **Integer**: Whole numbers (`42`)\n• **Float**: Decimal numbers (`3.14`)\n• **Boolean**: True/False values\n• **Array/List**: Multiple values (`[1, 2, 3]`)\n\n**Examples**:\n```python\nname = \"Alice\"        # String variable\nage = 25             # Integer variable\nheight = 5.6         # Float variable\nis_student = True    # Boolean variable\n```\n\n**Why Variables Matter**: They make code flexible, reusable, and easier to understand by giving meaningful names to data."
        
        # SQL vs NoSQL
        elif 'sql' in user_message_lower and 'nosql' in user_message_lower:
            return "**SQL vs NoSQL Databases** - Two different approaches to data storage:\n\n**SQL (Relational) Databases**:\n• **Structure**: Tables with rows and columns\n• **Schema**: Fixed structure defined upfront\n• **Language**: SQL (Structured Query Language)\n• **ACID**: Strong consistency and transactions\n• **Examples**: MySQL, PostgreSQL, Oracle\n• **Best for**: Complex queries, financial data, structured data\n\n**NoSQL (Non-Relational) Databases**:\n• **Structure**: Flexible (documents, key-value, graphs)\n• **Schema**: Dynamic, can change over time\n• **Language**: Various query methods\n• **Scalability**: Horizontal scaling, high performance\n• **Examples**: MongoDB, Cassandra, Redis\n• **Best for**: Big data, real-time apps, unstructured data\n\n**Choose SQL when**: You need complex relationships, transactions, and consistency\n**Choose NoSQL when**: You need flexibility, scalability, and handle varied data types"
        
        # HTML
        elif 'html' in user_message_lower and ('what is' in user_message_lower or 'explain' in user_message_lower):
            return "**HTML (HyperText Markup Language)** is the standard language for creating web pages and web applications.\n\n**Key Concepts**:\n• **Markup Language**: Uses tags to structure content\n• **Elements**: Building blocks like headings, paragraphs, links\n• **Attributes**: Additional information about elements\n• **Semantic**: Gives meaning to content structure\n\n**Basic Structure**:\n```html\n<!DOCTYPE html>\n<html>\n<head>\n    <title>Page Title</title>\n</head>\n<body>\n    <h1>Main Heading</h1>\n    <p>This is a paragraph.</p>\n    <a href=\"#\">This is a link</a>\n</body>\n</html>\n```\n\n**Common Elements**:\n• `<h1>-<h6>`: Headings\n• `<p>`: Paragraphs\n• `<a>`: Links\n• `<img>`: Images\n• `<div>`: Containers\n\n**Purpose**: HTML provides the structure and content, while CSS handles styling and JavaScript adds interactivity."
        
        # Algorithms
        elif 'algorithm' in user_message_lower:
            return "**Algorithms** are step-by-step instructions for solving problems or completing tasks in programming and computer science.\n\n**Key Characteristics**:\n• **Input**: Takes data to process\n• **Output**: Produces a result\n• **Definiteness**: Each step is clearly defined\n• **Finiteness**: Must terminate in finite steps\n• **Effectiveness**: Steps must be executable\n\n**Common Algorithm Types**:\n• **Sorting**: Arrange data in order (Bubble Sort, Quick Sort)\n• **Searching**: Find specific items (Binary Search, Linear Search)\n• **Graph**: Navigate networks (Dijkstra's, BFS, DFS)\n• **Dynamic Programming**: Optimize complex problems\n• **Recursive**: Solutions that call themselves\n\n**Example - Simple Search**:\n```python\ndef linear_search(list, target):\n    for i in range(len(list)):\n        if list[i] == target:\n            return i\n    return -1\n```\n\n**Why Important**: Algorithms determine how efficiently programs solve problems, affecting speed and resource usage."
        
        # Data Structures
        elif 'data structure' in user_message_lower:
            return "**Data Structures** are ways to organize and store data in computer memory for efficient access and modification.\n\n**Common Data Structures**:\n\n**Linear Structures**:\n• **Array**: Fixed-size, indexed collection\n• **Linked List**: Nodes connected by pointers\n• **Stack**: Last-In-First-Out (LIFO) - like a stack of plates\n• **Queue**: First-In-First-Out (FIFO) - like a line of people\n\n**Non-Linear Structures**:\n• **Tree**: Hierarchical structure with root and branches\n• **Graph**: Nodes connected by edges (networks, maps)\n• **Hash Table**: Key-value pairs for fast lookup\n\n**Choosing the Right Structure**:\n• **Arrays**: Fast access by index, fixed size\n• **Lists**: Dynamic size, easy insertion/deletion\n• **Trees**: Hierarchical data, fast searching\n• **Graphs**: Complex relationships, networking\n\n**Example - Stack Operations**:\n```python\nstack = []\nstack.append(1)    # Push\nstack.append(2)    # Push\nitem = stack.pop() # Pop (returns 2)\n```\n\n**Impact**: The right data structure makes programs faster and more memory-efficient."
        
        # Object-Oriented Programming
        elif 'object' in user_message_lower and 'oriented' in user_message_lower:
            return "**Object-Oriented Programming (OOP)** is a programming paradigm based on the concept of objects that contain data and methods.\n\n**Core Principles**:\n\n**1. Encapsulation**:\n• Bundle data and methods together\n• Hide internal implementation details\n• Control access through public/private members\n\n**2. Inheritance**:\n• Create new classes based on existing ones\n• Reuse code and extend functionality\n• \"Is-a\" relationship (Car is-a Vehicle)\n\n**3. Polymorphism**:\n• Same interface, different implementations\n• Method overriding and overloading\n• Flexibility in code design\n\n**4. Abstraction**:\n• Hide complex implementation details\n• Focus on what objects do, not how\n\n**Example**:\n```python\nclass Animal:\n    def __init__(self, name):\n        self.name = name\n    \n    def speak(self):\n        pass\n\nclass Dog(Animal):\n    def speak(self):\n        return f\"{self.name} says Woof!\"\n```\n\n**Benefits**: Code reusability, modularity, easier maintenance, and real-world modeling."
        
        # Python specific
        elif 'python' in user_message_lower:
            return "Python is a versatile programming language! Here's what makes it great:\n\n• **Easy to learn**: Clean, readable syntax\n• **Versatile**: Web development, data science, AI, automation\n• **Great libraries**: NumPy, Pandas, Django, Flask, TensorFlow\n• **Strong community**: Extensive documentation and support\n\n**Getting started**:\n1. Install Python from python.org\n2. Try interactive tutorials (codecademy, freeCodeCamp)\n3. Practice with small projects\n4. Join Python communities (r/Python, Stack Overflow)\n\nWhat specific aspect of Python interests you most?"
        
        elif 'javascript' in user_message_lower or 'js' in user_message_lower:
            return "JavaScript is essential for modern web development! Here's why:\n\n• **Frontend**: Interactive web pages and user interfaces\n• **Backend**: Node.js for server-side development\n• **Mobile**: React Native for mobile apps\n• **Desktop**: Electron for desktop applications\n\n**Key concepts to learn**:\n• Variables, functions, and objects\n• DOM manipulation\n• Async programming (promises, async/await)\n• Modern frameworks (React, Vue, Angular)\n\n**Resources**: MDN Web Docs, freeCodeCamp, JavaScript.info\n\nAre you looking to learn frontend or backend JavaScript?"
        
        elif 'react' in user_message_lower:
            return "React is a powerful JavaScript library for building user interfaces! Here's what you need to know:\n\n**Key concepts**:\n• **Components**: Reusable UI pieces\n• **JSX**: HTML-like syntax in JavaScript\n• **State**: Managing component data\n• **Props**: Passing data between components\n• **Hooks**: useState, useEffect for modern React\n\n**Getting started**:\n1. Learn JavaScript fundamentals first\n2. Understand HTML/CSS basics\n3. Try Create React App for quick setup\n4. Build small projects (todo list, weather app)\n\n**Resources**: Official React docs, React tutorial, freeCodeCamp\n\nWhat type of React project are you planning to build?"
        
        else:
            return "I'd be happy to help with programming questions! Here are some areas I can assist with:\n\n• **Languages**: Python, JavaScript, Java, C++, and more\n• **Web Development**: Frontend (React, Vue) and Backend (Node.js, Django)\n• **Databases**: SQL, NoSQL, database design\n• **Best Practices**: Code quality, testing, version control\n• **Career Advice**: Learning paths, project ideas, interview prep\n\nWhat specific programming topic or challenge can I help you with?"
    
    def _get_science_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle science and mathematics questions"""
        
        # Machine Learning
        if 'machine learning' in user_message_lower or 'ml' in user_message_lower:
            return "**Machine Learning (ML)** is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.\n\n**How it Works**:\n• **Training**: Feed algorithms large amounts of data\n• **Pattern Recognition**: Algorithm finds patterns in the data\n• **Prediction**: Use learned patterns to make predictions on new data\n• **Improvement**: Performance improves with more data\n\n**Types of Machine Learning**:\n• **Supervised**: Learn from labeled examples (email spam detection)\n• **Unsupervised**: Find hidden patterns (customer segmentation)\n• **Reinforcement**: Learn through trial and error (game playing)\n\n**Common Applications**:\n• Image recognition and computer vision\n• Natural language processing (chatbots, translation)\n• Recommendation systems (Netflix, Amazon)\n• Autonomous vehicles and robotics\n• Medical diagnosis and drug discovery\n\n**Popular Tools**: Python (scikit-learn, TensorFlow, PyTorch), R, cloud platforms (AWS, Google Cloud)\n\n**Getting Started**: Learn Python basics, statistics, and start with simple projects like predicting house prices or classifying images."
        
        # Artificial Intelligence
        elif 'artificial intelligence' in user_message_lower or user_message_lower.strip() == 'what is ai' or 'ai' in user_message_lower:
            return "**Artificial Intelligence (AI)** is the simulation of human intelligence in machines that are programmed to think and learn like humans.\n\n**Key Components**:\n• **Machine Learning**: Learning from data\n• **Natural Language Processing**: Understanding human language\n• **Computer Vision**: Interpreting visual information\n• **Robotics**: Physical interaction with environment\n• **Expert Systems**: Knowledge-based decision making\n\n**Types of AI**:\n• **Narrow AI**: Specialized for specific tasks (current AI)\n• **General AI**: Human-level intelligence across all domains (future goal)\n• **Superintelligence**: Exceeds human intelligence (theoretical)\n\n**Real-World Applications**:\n• Virtual assistants (Siri, Alexa)\n• Autonomous vehicles\n• Medical diagnosis\n• Financial trading\n• Content recommendation\n• Language translation\n\n**Current Limitations**: AI excels at specific tasks but lacks general understanding, creativity, and emotional intelligence that humans possess.\n\n**Future Impact**: AI will likely transform industries, create new jobs while eliminating others, and raise important ethical questions about privacy, bias, and human-AI collaboration."
        
        # Cloud Computing
        elif 'cloud computing' in user_message_lower or 'cloud' in user_message_lower:
            return "**Cloud Computing** is the delivery of computing services (servers, storage, databases, networking, software) over the internet (\"the cloud\").\n\n**Key Characteristics**:\n• **On-demand**: Access resources when needed\n• **Scalable**: Easily increase or decrease capacity\n• **Pay-as-you-go**: Only pay for what you use\n• **Global Access**: Available from anywhere with internet\n• **Managed**: Provider handles maintenance and updates\n\n**Service Models**:\n• **IaaS** (Infrastructure): Virtual machines, storage (AWS EC2)\n• **PaaS** (Platform): Development platforms (Google App Engine)\n• **SaaS** (Software): Ready-to-use applications (Gmail, Office 365)\n\n**Major Providers**:\n• **Amazon Web Services (AWS)**: Market leader\n• **Microsoft Azure**: Enterprise-focused\n• **Google Cloud Platform**: AI/ML strengths\n• **IBM Cloud, Oracle Cloud**: Specialized solutions\n\n**Benefits**: Cost savings, flexibility, automatic updates, disaster recovery, collaboration\n**Challenges**: Security concerns, internet dependency, vendor lock-in\n\n**Use Cases**: Web hosting, data backup, software development, big data analytics, AI/ML training"
        
        return "I'd love to help with science and math questions! Here's how I can assist:\n\n**Mathematics**:\n• Algebra, calculus, statistics\n• Problem-solving strategies\n• Mathematical concepts and applications\n\n**Sciences**:\n• Physics: mechanics, thermodynamics, electromagnetism\n• Chemistry: reactions, molecular structure, lab techniques\n• Biology: cell biology, genetics, ecology\n\n**Learning tips**:\n• Break complex problems into smaller steps\n• Practice regularly with varied problems\n• Understand concepts before memorizing formulas\n• Use visual aids and real-world examples\n\nWhat specific math or science topic would you like help with? Feel free to share the exact question or concept you're working on!"
    
    def _get_business_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle business and finance questions"""
        return "I can help with various business and finance topics! Here are key areas:\n\n**Business Strategy**:\n• Market analysis and competitive research\n• Business planning and model development\n• Marketing and customer acquisition\n• Operations and process improvement\n\n**Finance**:\n• Personal budgeting and financial planning\n• Investment basics (stocks, bonds, diversification)\n• Business finance and cash flow management\n• Understanding financial statements\n\n**Entrepreneurship**:\n• Startup planning and validation\n• Funding options and investor relations\n• Building and managing teams\n• Scaling and growth strategies\n\nWhat specific business or finance challenge are you facing? I can provide more targeted advice!"
    
    def _get_health_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle health and wellness questions"""
        return "I can provide general health and wellness information! Here are key areas:\n\n**Physical Health**:\n• Exercise routines and fitness planning\n• Nutrition basics and healthy eating\n• Sleep hygiene and stress management\n• Preventive care and healthy habits\n\n**Mental Wellness**:\n• Stress reduction techniques\n• Mindfulness and meditation\n• Work-life balance strategies\n• Building resilience and coping skills\n\n**Important note**: For specific medical concerns, always consult healthcare professionals. I can provide general wellness information and lifestyle tips.\n\n**Quick tips**:\n• Regular exercise (150 min/week moderate activity)\n• Balanced diet with fruits, vegetables, whole grains\n• 7-9 hours of quality sleep\n• Stay hydrated and manage stress\n\nWhat aspect of health and wellness interests you most?"
    
    def _get_education_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle education and learning questions"""
        return "I'm here to help with learning and education! Here's how I can assist:\n\n**Learning Strategies**:\n• Effective study techniques (spaced repetition, active recall)\n• Time management and productivity\n• Note-taking and information organization\n• Test preparation and exam strategies\n\n**Skill Development**:\n• Identifying learning goals and creating plans\n• Finding quality resources and courses\n• Building practical projects and portfolios\n• Tracking progress and staying motivated\n\n**Educational Paths**:\n• Course recommendations for various fields\n• Career-focused learning roadmaps\n• Balancing formal and self-directed learning\n• Building expertise in specific domains\n\n**Learning tips**:\n• Set clear, specific goals\n• Practice regularly and consistently\n• Teach others to reinforce your knowledge\n• Apply learning through real projects\n\nWhat subject or skill are you looking to learn or improve?"
    
    def _get_creative_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle creative and writing questions"""
        return "I'd love to help with creative projects and writing! Here's what I can assist with:\n\n**Writing**:\n• Content planning and structure\n• Improving clarity and engagement\n• Different writing styles and formats\n• Overcoming writer's block\n• Editing and revision strategies\n\n**Creative Projects**:\n• Brainstorming and idea development\n• Project planning and execution\n• Design principles and aesthetics\n• Building creative habits and routines\n\n**Content Creation**:\n• Blog posts and articles\n• Social media content\n• Marketing copy and messaging\n• Storytelling techniques\n\n**Tips for creativity**:\n• Set aside dedicated creative time\n• Consume diverse content for inspiration\n• Don't judge your first drafts\n• Collaborate and get feedback\n• Practice regularly to build skills\n\nWhat type of creative project or writing are you working on? I can provide more specific guidance!"
    
    def _get_communication_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle communication and social questions"""
        return "Communication skills are crucial for success! Here's how I can help:\n\n**Professional Communication**:\n• Email writing and business correspondence\n• Meeting facilitation and participation\n• Presentation skills and public speaking\n• Networking and relationship building\n\n**Leadership and Teamwork**:\n• Leading effective meetings\n• Giving and receiving feedback\n• Conflict resolution strategies\n• Building team collaboration\n\n**Personal Communication**:\n• Active listening techniques\n• Assertiveness and boundary setting\n• Difficult conversations\n• Building rapport and trust\n\n**Key principles**:\n• Listen more than you speak\n• Be clear and concise\n• Show empathy and understanding\n• Adapt your style to your audience\n• Practice regularly in low-stakes situations\n\nWhat specific communication challenge or skill would you like to work on?"
    
    def _get_problem_solving_response(self, user_message_lower: str, original_message: str) -> str:
        """Handle problem-solving and decision-making questions"""
        return "I'm here to help you work through problems and decisions! Here's my approach:\n\n**Problem-Solving Framework**:\n1. **Define the problem clearly** - What exactly needs to be solved?\n2. **Gather information** - What facts and context do you have?\n3. **Generate options** - What are possible solutions or approaches?\n4. **Evaluate alternatives** - What are pros/cons of each option?\n5. **Make a decision** - Choose based on your priorities and values\n6. **Take action** - Implement your solution\n7. **Review results** - Learn from the outcome\n\n**Decision-Making Tips**:\n• Consider both short-term and long-term consequences\n• Identify your key priorities and values\n• Seek input from trusted advisors when appropriate\n• Don't let perfect be the enemy of good\n• Be prepared to adjust course if needed\n\nWhat specific problem or decision are you facing? I can help you work through it step by step!"
    
    def _get_comprehensive_default_response(self, original_message: str) -> str:
        """Provide a comprehensive default response for unmatched questions"""
        return f"I'd be happy to help you with that! While I may not have caught the specific topic of your question '{original_message}', I can assist with a wide range of subjects:\n\n**Popular topics I can help with**:\n• **Technology & Programming**: Coding, web development, software tools\n• **Career & Professional**: Interview prep, skill development, workplace advice\n• **Learning & Education**: Study strategies, course recommendations, skill building\n• **Business & Finance**: Strategy, marketing, personal finance, entrepreneurship\n• **Communication**: Writing, presentations, leadership, teamwork\n• **Problem-Solving**: Decision-making, planning, overcoming challenges\n• **Creative Projects**: Writing, content creation, design thinking\n• **Health & Wellness**: Fitness, nutrition, stress management, work-life balance\n\nCould you provide a bit more detail about what you're looking for? I'm here to give you practical, helpful information on almost any topic!"

    def _build_context_prompt(self) -> str:
        """Build context-aware prompt based on current session state"""
        context_parts = []
        
        if self.user_context.get('selected_category'):
            context_parts.append(f"User is currently in interview practice mode, category: {self.user_context['selected_category']}")
        
        if self.user_context.get('selected_question'):
            context_parts.append(f"Current interview question: {self.user_context['selected_question']}")
        
        stage = self.user_context.get('session_stage', 'initial')
        if stage == 'practicing':
            context_parts.append("User is currently practicing their interview answer")
        elif stage == 'completed':
            context_parts.append("User has completed their practice and received analysis")
        
        if context_parts:
            return f"\n\nCurrent context: {'; '.join(context_parts)}"
        
        return ""

    def get_stage_response(self, stage: str, **kwargs) -> str:
        """Get a response based on the current interview stage"""
        
        # For interview stages, use the specialized interview chatbot
        if stage in ['question_selected', 'recording_started', 'recording_long', 'analysis_complete']:
            return fallback_chatbot.get_stage_response(stage, **kwargs)
        
        # For other stages, provide general helpful response
        return "I'm here to help you with any questions you have! Whether it's about interviews, technology, learning, or any other topic, feel free to ask me anything."

# Global universal chatbot instance
universal_chatbot = UniversalChatbot()