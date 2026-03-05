"""
AI Interview Assistant Service
Provides direct, professional interview answers as if from a candidate
"""

import random
from typing import Dict, List, Optional

class AIInterviewAssistant:
    def __init__(self):
        self.conversation_history = []
        
        # Knowledge base for different types of questions
        self.behavioral_responses = {
            'leadership': [
                "I led a cross-functional team of 8 people to deliver a critical project under a tight deadline. I established clear communication channels, delegated tasks based on team strengths, and held daily check-ins to track progress. We delivered the project two days early and received recognition from senior management.",
                "When our team lead was unexpectedly absent, I stepped up to coordinate our sprint deliverables. I organized task priorities, facilitated team discussions, and ensured everyone had the resources they needed. The sprint was completed successfully with all objectives met.",
                "I initiated a process improvement project that reduced our deployment time by 40%. I gathered input from all stakeholders, presented the proposal to management, and led the implementation across three teams.",
                "I mentored three junior developers on a complex integration project. I created learning materials, conducted regular one-on-ones, and gradually increased their responsibilities. All three developers successfully completed their tasks and gained valuable experience.",
                "During a critical system outage, I took charge of the incident response team. I coordinated with multiple departments, communicated updates to stakeholders, and led the root cause analysis that prevented future occurrences."
            ],
            'challenge': [
                "I faced a situation where a critical system went down during peak business hours. I quickly assembled a response team, diagnosed the root cause within 30 minutes, and implemented a temporary fix while working on the permanent solution. I also established a communication plan to keep stakeholders informed throughout the process.",
                "When I inherited a project that was significantly behind schedule, I conducted a thorough analysis of the remaining work, identified bottlenecks, and restructured the timeline. I negotiated with stakeholders for additional resources and delivered the project within the revised timeline.",
                "I encountered resistance when proposing a new technology adoption. I addressed concerns by creating a detailed comparison analysis, organizing pilot demonstrations, and providing comprehensive training materials. The technology was successfully adopted and improved our efficiency by 25%.",
                "I had to learn a completely new programming language in two weeks to contribute to an urgent project. I created a structured learning plan, practiced with small projects, and sought mentorship from experienced team members. I successfully delivered my components on time and continued using the language in future projects.",
                "When our main client threatened to cancel their contract due to performance issues, I led a comprehensive optimization effort. I identified the bottlenecks, implemented caching strategies, and improved database queries. We achieved a 60% performance improvement and retained the client."
            ],
            'teamwork': [
                "I collaborated with the design team to resolve conflicting requirements between user experience and technical constraints. I facilitated joint sessions where we explored alternative solutions, ultimately finding an approach that satisfied both teams and improved the final product.",
                "When working on a multi-team project, I established regular sync meetings and shared documentation standards. I also created cross-team knowledge sharing sessions that helped everyone understand dependencies and improved our overall coordination.",
                "I partnered with a colleague who had complementary skills to tackle a complex problem. We divided responsibilities based on our strengths, maintained open communication, and regularly reviewed each other's work to ensure quality and consistency.",
                "During a product launch, I worked closely with QA, DevOps, and Product teams to ensure smooth deployment. I created detailed handoff documentation, participated in cross-functional testing, and was available for immediate support during the launch window.",
                "I collaborated with the sales team to create technical demonstrations for potential clients. I translated complex technical concepts into business benefits and helped close three major deals by effectively communicating our solution's value."
            ],
            'failure': [
                "I once underestimated the complexity of a database migration, which caused a delay in our release schedule. I took full responsibility, worked extra hours to resolve the issues, and implemented additional testing procedures to prevent similar problems. I also improved our estimation process for future migrations.",
                "Early in my career, I failed to communicate a critical dependency to another team, which impacted their timeline. I learned the importance of proactive communication and now maintain detailed stakeholder maps and regular update schedules for all my projects.",
                "I made an incorrect assumption about user requirements that led to rework. I took ownership of the mistake, gathered proper requirements through user interviews, and delivered the corrected solution. This experience taught me to always validate assumptions with stakeholders.",
                "I once deployed code without proper testing that caused a minor service disruption. I immediately rolled back the changes, conducted a thorough post-mortem, and implemented additional code review and testing procedures. This experience reinforced the importance of following established processes.",
                "I failed to anticipate scalability issues in a system I designed, which caused performance problems as usage grew. I redesigned the architecture to handle the load, implemented monitoring tools, and now always consider scalability from the initial design phase."
            ]
        }
        
        self.technical_responses = {
            'programming': [
                "I have extensive experience with Python, JavaScript, and Java. I'm particularly strong in Python for backend development and data processing, having used it for building REST APIs, implementing machine learning models, and automating workflows. I stay current with best practices and regularly contribute to code reviews.",
                "I work with both SQL and NoSQL databases. I've designed and optimized database schemas for high-traffic applications, implemented efficient indexing strategies, and have experience with PostgreSQL, MongoDB, and Redis for different use cases.",
                "I follow object-oriented design principles and have experience with design patterns like MVC, Observer, and Factory. I prioritize clean, maintainable code and use tools like ESLint and pytest to ensure code quality.",
                "My frontend experience includes React, Vue.js, and vanilla JavaScript. I'm comfortable with modern development tools like Webpack, npm, and Git. I also have experience with CSS frameworks like Tailwind and Bootstrap for responsive design.",
                "I have strong experience with cloud platforms, particularly AWS and Docker. I've deployed applications using containerization, set up CI/CD pipelines, and worked with microservices architecture for scalable applications."
            ],
            'problem_solving': [
                "I approach complex problems by breaking them down into smaller, manageable components. I start by understanding the requirements thoroughly, research existing solutions, and then design a step-by-step approach. I also consider edge cases and potential scalability issues from the beginning.",
                "When debugging, I use systematic approaches like logging, unit testing, and code review. I document my findings and solutions to help team members who might encounter similar issues in the future.",
                "I believe in iterative problem-solving. I create minimum viable solutions first, test them thoroughly, and then enhance based on feedback and requirements. This approach helps deliver value quickly while maintaining quality.",
                "My debugging process starts with reproducing the issue consistently, then I use debugging tools and logs to trace the problem. I also leverage version control to identify when issues were introduced and collaborate with team members who might have relevant expertise.",
                "I use data-driven approaches to solve performance problems. I profile applications to identify bottlenecks, analyze metrics to understand user behavior, and implement targeted optimizations based on actual usage patterns rather than assumptions."
            ]
        }
        
        self.general_responses = {
            'strengths': [
                "My key strengths are analytical thinking and effective communication. I excel at breaking down complex problems and explaining technical concepts to both technical and non-technical stakeholders. I'm also highly adaptable and learn new technologies quickly.",
                "I'm particularly strong in project coordination and technical problem-solving. I have a track record of delivering projects on time and helping teams work more efficiently through process improvements and clear communication.",
                "My strengths include attention to detail and collaborative leadership. I catch issues early in the development process and work well with cross-functional teams to achieve shared goals.",
                "I excel at system design and architecture planning. I can see the big picture while managing technical details, and I'm skilled at making technology decisions that balance current needs with future scalability.",
                "My communication skills are a major strength. I can translate complex technical concepts for business stakeholders and facilitate productive discussions between different teams with varying technical backgrounds."
            ],
            'weaknesses': [
                "I sometimes spend too much time perfecting details when good enough would suffice. I've been working on better time management and learning to prioritize impact over perfection, especially in fast-paced environments.",
                "I used to struggle with public speaking, but I've actively worked on this by joining presentation workshops and volunteering for team demos. I'm now comfortable presenting to large groups and have received positive feedback on my communication skills.",
                "I tend to take on too many responsibilities because I want to help wherever possible. I've learned to be more strategic about my commitments and better at delegating tasks to ensure quality doesn't suffer.",
                "Early in my career, I was hesitant to ask for help when stuck on problems. I've learned that collaboration and seeking input from colleagues often leads to better solutions faster than working in isolation.",
                "I used to focus too heavily on technical perfection without considering business constraints. I've learned to balance technical excellence with practical business needs and timeline requirements."
            ],
            'motivation': [
                "I'm motivated by solving complex problems and seeing the direct impact of my work. I enjoy the challenge of finding elegant solutions to difficult technical problems and working with talented teams to build something meaningful.",
                "I'm driven by continuous learning and growth. Technology evolves rapidly, and I find it exciting to stay current with new developments and apply them to create better solutions for users and businesses.",
                "I'm passionate about building products that make a real difference. I want to work on projects where I can contribute to meaningful outcomes and collaborate with people who share similar values about quality and innovation.",
                "I'm motivated by the opportunity to mentor others and share knowledge. I find it rewarding to help junior developers grow and to contribute to a positive team culture where everyone can succeed.",
                "I'm driven by the challenge of scaling systems and solving performance problems. There's something satisfying about optimizing code and architecture to handle millions of users efficiently."
            ]
        }

    def get_response(self, question: str, context: Dict = None) -> str:
        """Generate a professional interview response to the given question"""
        
        question_lower = question.lower().strip()
        
        # Enhanced question analysis with better keyword matching
        
        # Tell me about yourself variations
        if any(phrase in question_lower for phrase in [
            'tell me about yourself', 'introduce yourself', 'walk me through your background',
            'describe yourself', 'who are you', 'your background'
        ]):
            return "I'm a software developer with 5 years of experience building scalable web applications and data processing systems. I specialize in Python and JavaScript, with strong experience in both frontend and backend development. In my current role, I've led several successful projects including a speech analysis system that improved user engagement by 30%. I'm passionate about creating efficient, user-focused solutions and enjoy collaborating with cross-functional teams to deliver high-quality products."
        
        # Strengths questions
        elif any(phrase in question_lower for phrase in [
            'greatest strength', 'your strength', 'what are you good at', 'best qualities',
            'top skills', 'what makes you', 'your abilities'
        ]):
            return random.choice(self.general_responses['strengths'])
        
        # Weakness questions
        elif any(phrase in question_lower for phrase in [
            'weakness', 'areas for improvement', 'what would you improve', 'struggle with',
            'not good at', 'challenging for you', 'difficult aspect'
        ]):
            return random.choice(self.general_responses['weaknesses'])
        
        # Why this company/role questions
        elif any(phrase in question_lower for phrase in [
            'why do you want to work here', 'why this company', 'why us', 'why this role',
            'what interests you about', 'why are you interested', 'what attracts you'
        ]):
            return "I'm excited about this opportunity because it aligns perfectly with my technical skills and career goals. Your company's focus on innovation and user-centered design resonates with my values, and I'm particularly interested in contributing to projects that have meaningful impact. The role offers the right balance of technical challenges and collaborative work that I thrive in, and I believe my experience with similar technologies and project types would allow me to contribute effectively from day one."
        
        # Future/career goals questions
        elif any(phrase in question_lower for phrase in [
            'where do you see yourself', '5 years', 'career goals', 'future plans',
            'long term goals', 'career aspirations', 'where are you headed'
        ]):
            return "In five years, I see myself in a senior technical role where I can mentor other developers while continuing to work on challenging technical problems. I want to deepen my expertise in system architecture and potentially move into technical leadership, contributing to strategic technology decisions. I'm also interested in staying current with emerging technologies and finding ways to apply them to create better user experiences and more efficient systems."
        
        # Behavioral questions - Leadership
        elif any(phrase in question_lower for phrase in [
            'time you led', 'leadership experience', 'when you managed', 'led a team',
            'time you were a leader', 'leadership role', 'managed a project'
        ]):
            return random.choice(self.behavioral_responses['leadership'])
        
        # Behavioral questions - Challenges/Problems
        elif any(phrase in question_lower for phrase in [
            'challenging situation', 'difficult time', 'problem you solved', 'obstacle you faced',
            'time you overcame', 'difficult project', 'major challenge', 'tough situation'
        ]):
            return random.choice(self.behavioral_responses['challenge'])
        
        # Behavioral questions - Teamwork
        elif any(phrase in question_lower for phrase in [
            'worked in a team', 'team environment', 'collaborated with', 'team project',
            'working with others', 'team experience', 'group work'
        ]):
            return random.choice(self.behavioral_responses['teamwork'])
        
        # Behavioral questions - Failure/Mistakes
        elif any(phrase in question_lower for phrase in [
            'time you failed', 'mistake you made', 'something went wrong', 'failure',
            'time you were wrong', 'error you made', 'when you messed up'
        ]):
            return random.choice(self.behavioral_responses['failure'])
        
        # Technical skills questions
        elif any(phrase in question_lower for phrase in [
            'programming languages', 'technical skills', 'technologies you know', 'coding experience',
            'development experience', 'technical background', 'programming experience'
        ]):
            return random.choice(self.technical_responses['programming'])
        
        # Problem solving questions
        elif any(phrase in question_lower for phrase in [
            'problem solving', 'how do you debug', 'approach to problems', 'troubleshooting',
            'solve complex problems', 'analytical approach', 'debugging process'
        ]):
            return random.choice(self.technical_responses['problem_solving'])
        
        # Motivation questions
        elif any(phrase in question_lower for phrase in [
            'what motivates you', 'what drives you', 'passionate about', 'what excites you',
            'what inspires you', 'what energizes you'
        ]):
            return random.choice(self.general_responses['motivation'])
        
        # Questions for the interviewer
        elif any(phrase in question_lower for phrase in [
            'questions for us', 'questions for me', 'anything you want to ask',
            'questions about the role', 'questions about the company'
        ]):
            return "Yes, I'd like to know more about the team structure and how this role collaborates with other departments. I'm also curious about the company's approach to professional development and what opportunities exist for growth. Finally, what are the biggest technical challenges the team is currently facing, and how would this role contribute to solving them?"
        
        # Salary/compensation questions
        elif any(phrase in question_lower for phrase in [
            'salary expectations', 'compensation', 'how much do you want', 'pay expectations',
            'salary requirements', 'expected salary'
        ]):
            return "I'm looking for a compensation package that reflects the value I can bring to the role and is competitive with market standards. I'm open to discussing the complete package including benefits, growth opportunities, and work-life balance. I'm more interested in finding the right fit where I can contribute meaningfully and grow professionally."
        
        # Why leaving current job
        elif any(phrase in question_lower for phrase in [
            'why are you leaving', 'why do you want to leave', 'leaving your current job',
            'why change jobs', 'reason for leaving'
        ]):
            return "I'm looking for new challenges and opportunities to grow professionally. While I've learned a great deal in my current role, I'm ready to take on more responsibility and work on different types of projects. This position offers the perfect opportunity to expand my skills while contributing to meaningful work in an environment that values innovation and collaboration."
        
        # Work style questions
        elif any(phrase in question_lower for phrase in [
            'work style', 'how do you work', 'working style', 'approach to work',
            'work preferences', 'work best when'
        ]):
            return "I work best in collaborative environments where I can combine independent problem-solving with team input. I'm detail-oriented and like to plan my approach before diving into complex tasks, but I'm also adaptable when priorities change. I believe in clear communication, regular check-ins with stakeholders, and maintaining high quality standards while meeting deadlines."
        
        # Handling pressure/stress
        elif any(phrase in question_lower for phrase in [
            'handle pressure', 'work under pressure', 'stressful situations', 'tight deadlines',
            'handle stress', 'pressure situations'
        ]):
            return "I handle pressure well by staying organized and breaking complex tasks into manageable steps. When facing tight deadlines, I prioritize the most critical components first and communicate proactively with stakeholders about progress and any potential issues. I've found that maintaining clear priorities and regular communication helps reduce stress for both myself and my team."
        
        # Learning and development
        elif any(phrase in question_lower for phrase in [
            'how do you learn', 'stay updated', 'keep learning', 'professional development',
            'new technologies', 'continuous learning'
        ]):
            return "I stay current through a combination of hands-on practice, online courses, and industry resources. I regularly read technical blogs, participate in developer communities, and work on side projects to experiment with new technologies. I also believe in learning from colleagues through code reviews and knowledge sharing sessions. When I need to learn something new for work, I start with official documentation and then seek out practical tutorials and examples."
        
        # Default response for unrecognized questions - more intelligent fallback
        else:
            # Try to give a relevant response based on common question patterns
            if '?' in question_lower:
                return "I believe my combination of technical skills, problem-solving ability, and collaborative approach makes me well-suited for this role. I'm committed to delivering high-quality work, learning continuously, and contributing positively to team goals. I'm excited about the opportunity to bring my experience to your organization and help drive successful outcomes."
            else:
                return "That's an interesting point. In my experience, I've found that success comes from combining technical expertise with strong communication and collaboration skills. I'm always eager to take on new challenges and contribute to team success while continuing to grow professionally."

    def get_contextual_response(self, question: str, job_role: str = None, company: str = None) -> str:
        """Generate a response tailored to specific job role or company"""
        
        base_response = self.get_response(question)
        
        # Add role-specific context if provided
        if job_role:
            if 'senior' in job_role.lower():
                base_response += " My experience leading projects and mentoring junior developers has prepared me well for senior-level responsibilities."
            elif 'lead' in job_role.lower() or 'manager' in job_role.lower():
                base_response += " I'm ready to take on leadership responsibilities and help guide technical decisions while supporting team growth."
        
        return base_response

# Global instance
ai_interview_assistant = AIInterviewAssistant()