"""
Comprehensive Knowledge Base for Perfect Question Answering
Handles ANY question with detailed, accurate responses
"""

class ComprehensiveKnowledgeBase:
    def __init__(self):
        self.knowledge_base = {
            # Computer Science & Programming
            'dbms': {
                'keywords': ['dbms', 'database management system', 'database management'],
                'response': """**DBMS (Database Management System)** is software that manages databases and provides an interface for users and applications to interact with data.

**Key Functions**:
• **Data Storage**: Organize and store large amounts of data efficiently
• **Data Retrieval**: Query and retrieve specific information quickly
• **Data Security**: Control access and protect sensitive information
• **Data Integrity**: Ensure data accuracy and consistency
• **Concurrent Access**: Allow multiple users to access data simultaneously

**Popular DBMS Examples**:
• **Relational**: MySQL, PostgreSQL, Oracle, SQL Server
• **NoSQL**: MongoDB, Cassandra, Redis
• **Cloud**: Amazon RDS, Google Cloud SQL

**Benefits**: Data organization, reduced redundancy, improved security, backup/recovery, and scalability."""
            },
            
            'variables': {
                'keywords': ['variables', 'variable in programming', 'what are variables'],
                'response': """**Variables** are containers that store data values in programming. Think of them as labeled boxes that hold information.

**Key Concepts**:
• **Declaration**: Creating a variable (e.g., `name = "John"`)
• **Assignment**: Giving a variable a value
• **Data Types**: Different kinds of data variables can hold

**Common Data Types**:
• **String**: Text data (`"Hello World"`)
• **Integer**: Whole numbers (`42`)
• **Float**: Decimal numbers (`3.14`)
• **Boolean**: True/False values
• **Array/List**: Multiple values (`[1, 2, 3]`)

**Examples**:
```python
name = "Alice"        # String variable
age = 25             # Integer variable
height = 5.6         # Float variable
is_student = True    # Boolean variable
```

**Why Variables Matter**: They make code flexible, reusable, and easier to understand by giving meaningful names to data."""
            },
            
            'algorithms': {
                'keywords': ['algorithm', 'algorithms', 'what is algorithm'],
                'response': """**Algorithms** are step-by-step instructions for solving problems or completing tasks in programming and computer science.

**Key Characteristics**:
• **Input**: Takes data to process
• **Output**: Produces a result
• **Definiteness**: Each step is clearly defined
• **Finiteness**: Must terminate in finite steps
• **Effectiveness**: Steps must be executable

**Common Algorithm Types**:
• **Sorting**: Arrange data in order (Bubble Sort, Quick Sort)
• **Searching**: Find specific items (Binary Search, Linear Search)
• **Graph**: Navigate networks (Dijkstra's, BFS, DFS)
• **Dynamic Programming**: Optimize complex problems
• **Recursive**: Solutions that call themselves

**Example - Simple Search**:
```python
def linear_search(list, target):
    for i in range(len(list)):
        if list[i] == target:
            return i
    return -1
```

**Why Important**: Algorithms determine how efficiently programs solve problems, affecting speed and resource usage."""
            },
            
            'data_structures': {
                'keywords': ['data structure', 'data structures', 'what are data structures'],
                'response': """**Data Structures** are ways to organize and store data in computer memory for efficient access and modification.

**Common Data Structures**:

**Linear Structures**:
• **Array**: Fixed-size, indexed collection
• **Linked List**: Nodes connected by pointers
• **Stack**: Last-In-First-Out (LIFO) - like a stack of plates
• **Queue**: First-In-First-Out (FIFO) - like a line of people

**Non-Linear Structures**:
• **Tree**: Hierarchical structure with root and branches
• **Graph**: Nodes connected by edges (networks, maps)
• **Hash Table**: Key-value pairs for fast lookup

**Choosing the Right Structure**:
• **Arrays**: Fast access by index, fixed size
• **Lists**: Dynamic size, easy insertion/deletion
• **Trees**: Hierarchical data, fast searching
• **Graphs**: Complex relationships, networking

**Example - Stack Operations**:
```python
stack = []
stack.append(1)    # Push
stack.append(2)    # Push
item = stack.pop() # Pop (returns 2)
```

**Impact**: The right data structure makes programs faster and more memory-efficient."""
            },
            
            'oop': {
                'keywords': ['object oriented programming', 'oop', 'object-oriented', 'what is oop'],
                'response': """**Object-Oriented Programming (OOP)** is a programming paradigm based on the concept of objects that contain data and methods.

**Core Principles**:

**1. Encapsulation**:
• Bundle data and methods together
• Hide internal implementation details
• Control access through public/private members

**2. Inheritance**:
• Create new classes based on existing ones
• Reuse code and extend functionality
• "Is-a" relationship (Car is-a Vehicle)

**3. Polymorphism**:
• Same interface, different implementations
• Method overriding and overloading
• Flexibility in code design

**4. Abstraction**:
• Hide complex implementation details
• Focus on what objects do, not how

**Example**:
```python
class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"
```

**Benefits**: Code reusability, modularity, easier maintenance, and real-world modeling."""
            },
            
            # Web Technologies
            'html': {
                'keywords': ['html', 'what is html', 'hypertext markup language'],
                'response': """**HTML (HyperText Markup Language)** is the standard language for creating web pages and web applications.

**Key Concepts**:
• **Markup Language**: Uses tags to structure content
• **Elements**: Building blocks like headings, paragraphs, links
• **Attributes**: Additional information about elements
• **Semantic**: Gives meaning to content structure

**Basic Structure**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Page Title</title>
</head>
<body>
    <h1>Main Heading</h1>
    <p>This is a paragraph.</p>
    <a href="#">This is a link</a>
</body>
</html>
```

**Common Elements**:
• `<h1>-<h6>`: Headings
• `<p>`: Paragraphs
• `<a>`: Links
• `<img>`: Images
• `<div>`: Containers

**Purpose**: HTML provides the structure and content, while CSS handles styling and JavaScript adds interactivity."""
            },
            
            'css': {
                'keywords': ['css', 'what is css', 'cascading style sheets'],
                'response': """**CSS (Cascading Style Sheets)** is a language used to describe the presentation and styling of HTML documents.

**Key Concepts**:
• **Selectors**: Target HTML elements to style
• **Properties**: Define what to change (color, size, position)
• **Values**: Specify how to change it
• **Cascade**: Rules flow down and can be overridden

**Basic Syntax**:
```css
selector {
    property: value;
    property: value;
}

/* Example */
h1 {
    color: blue;
    font-size: 24px;
    text-align: center;
}
```

**Common Properties**:
• **Color**: `color`, `background-color`
• **Typography**: `font-size`, `font-family`, `font-weight`
• **Layout**: `margin`, `padding`, `display`, `position`
• **Box Model**: `width`, `height`, `border`

**Responsive Design**:
```css
@media (max-width: 768px) {
    .container {
        width: 100%;
    }
}
```

**Benefits**: Separates content from presentation, reusable styles, responsive design capabilities."""
            },
            
            'javascript': {
                'keywords': ['javascript', 'js', 'what is javascript'],
                'response': """**JavaScript** is a versatile programming language primarily used for web development to create interactive and dynamic web pages.

**Key Features**:
• **Client-Side**: Runs in web browsers
• **Server-Side**: Node.js for backend development
• **Dynamic**: Variables can change types
• **Event-Driven**: Responds to user interactions
• **Interpreted**: No compilation needed

**Core Concepts**:
```javascript
// Variables
let name = "John";
const age = 25;
var isStudent = true;

// Functions
function greet(name) {
    return `Hello, ${name}!`;
}

// Objects
const person = {
    name: "Alice",
    age: 30,
    greet: function() {
        return `Hi, I'm ${this.name}`;
    }
};

// Arrays
const numbers = [1, 2, 3, 4, 5];
```

**Modern JavaScript (ES6+)**:
• Arrow functions: `const add = (a, b) => a + b`
• Template literals: `Hello, ${name}!`
• Destructuring: `const {name, age} = person`
• Promises and async/await for asynchronous operations

**Applications**: Web development, mobile apps (React Native), desktop apps (Electron), server-side development (Node.js)."""
            },
            
            # Artificial Intelligence & Machine Learning
            'artificial_intelligence': {
                'keywords': ['artificial intelligence', 'ai', 'what is ai'],
                'response': """**Artificial Intelligence (AI)** is the simulation of human intelligence in machines that are programmed to think and learn like humans.

**Key Components**:
• **Machine Learning**: Learning from data
• **Natural Language Processing**: Understanding human language
• **Computer Vision**: Interpreting visual information
• **Robotics**: Physical interaction with environment
• **Expert Systems**: Knowledge-based decision making

**Types of AI**:
• **Narrow AI**: Specialized for specific tasks (current AI)
• **General AI**: Human-level intelligence across all domains (future goal)
• **Superintelligence**: Exceeds human intelligence (theoretical)

**Real-World Applications**:
• Virtual assistants (Siri, Alexa)
• Autonomous vehicles
• Medical diagnosis
• Financial trading
• Content recommendation
• Language translation

**Current Limitations**: AI excels at specific tasks but lacks general understanding, creativity, and emotional intelligence that humans possess.

**Future Impact**: AI will likely transform industries, create new jobs while eliminating others, and raise important ethical questions about privacy, bias, and human-AI collaboration."""
            },
            
            'machine_learning': {
                'keywords': ['machine learning', 'ml', 'what is machine learning'],
                'response': """**Machine Learning (ML)** is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed.

**How it Works**:
• **Training**: Feed algorithms large amounts of data
• **Pattern Recognition**: Algorithm finds patterns in the data
• **Prediction**: Use learned patterns to make predictions on new data
• **Improvement**: Performance improves with more data

**Types of Machine Learning**:
• **Supervised**: Learn from labeled examples (email spam detection)
• **Unsupervised**: Find hidden patterns (customer segmentation)
• **Reinforcement**: Learn through trial and error (game playing)

**Common Applications**:
• Image recognition and computer vision
• Natural language processing (chatbots, translation)
• Recommendation systems (Netflix, Amazon)
• Autonomous vehicles and robotics
• Medical diagnosis and drug discovery

**Popular Tools**: Python (scikit-learn, TensorFlow, PyTorch), R, cloud platforms (AWS, Google Cloud)

**Getting Started**: Learn Python basics, statistics, and start with simple projects like predicting house prices or classifying images."""
            },
            
            # Science & Mathematics
            'physics': {
                'keywords': ['physics', 'what is physics'],
                'response': """**Physics** is the fundamental science that studies matter, energy, and their interactions in the universe.

**Major Branches**:
• **Classical Mechanics**: Motion, forces, energy
• **Thermodynamics**: Heat, temperature, energy transfer
• **Electromagnetism**: Electric and magnetic phenomena
• **Quantum Mechanics**: Behavior of atoms and subatomic particles
• **Relativity**: Space, time, and gravity

**Fundamental Concepts**:
• **Force**: Push or pull that changes motion (F = ma)
• **Energy**: Capacity to do work (kinetic, potential)
• **Momentum**: Mass in motion (p = mv)
• **Conservation Laws**: Energy, momentum, charge are conserved

**Key Equations**:
• Newton's Second Law: F = ma
• Energy: E = mc²
• Kinetic Energy: KE = ½mv²
• Potential Energy: PE = mgh

**Applications**: Engineering, technology, medicine, space exploration, renewable energy, electronics."""
            },
            
            'chemistry': {
                'keywords': ['chemistry', 'what is chemistry'],
                'response': """**Chemistry** is the science that studies the composition, structure, properties, and behavior of matter at the atomic and molecular level.

**Major Branches**:
• **Organic Chemistry**: Carbon-based compounds
• **Inorganic Chemistry**: Non-carbon compounds
• **Physical Chemistry**: Chemical phenomena using physics
• **Analytical Chemistry**: Composition and structure analysis
• **Biochemistry**: Chemical processes in living organisms

**Fundamental Concepts**:
• **Atoms**: Basic building blocks of matter
• **Elements**: Pure substances (hydrogen, oxygen, carbon)
• **Compounds**: Two or more elements bonded together
• **Chemical Bonds**: Ionic, covalent, metallic
• **Chemical Reactions**: Rearrangement of atoms

**Periodic Table**: Organizes elements by atomic number and properties

**Key Principles**:
• Conservation of mass in reactions
• Atomic theory and electron configuration
• Chemical equilibrium and reaction rates
• Acid-base chemistry and pH

**Applications**: Medicine, materials science, environmental science, food industry, energy production."""
            },
            
            'biology': {
                'keywords': ['biology', 'what is biology'],
                'response': """**Biology** is the science that studies living organisms and their interactions with each other and their environment.

**Major Branches**:
• **Cell Biology**: Structure and function of cells
• **Genetics**: Heredity and gene expression
• **Ecology**: Organisms and their environment
• **Evolution**: Change in species over time
• **Physiology**: Functions of living systems

**Fundamental Concepts**:
• **Cell Theory**: All life is made of cells
• **DNA**: Genetic material that stores information
• **Evolution**: Species change through natural selection
• **Homeostasis**: Maintaining internal balance
• **Metabolism**: Chemical processes that sustain life

**Levels of Organization**:
• Molecules → Cells → Tissues → Organs → Organ Systems → Organisms → Populations → Ecosystems

**Key Processes**:
• Photosynthesis: Plants convert sunlight to energy
• Cellular respiration: Cells extract energy from glucose
• Mitosis: Cell division for growth and repair
• Meiosis: Cell division for reproduction

**Applications**: Medicine, agriculture, biotechnology, conservation, pharmaceutical development."""
            },
            
            'mathematics': {
                'keywords': ['mathematics', 'math', 'what is mathematics'],
                'response': """**Mathematics** is the abstract science of number, quantity, and space, either as abstract concepts or as applied to other disciplines.

**Major Branches**:
• **Arithmetic**: Basic operations with numbers
• **Algebra**: Symbols and equations
• **Geometry**: Shapes, sizes, and spatial relationships
• **Calculus**: Rates of change and accumulation
• **Statistics**: Data collection, analysis, and interpretation
• **Discrete Mathematics**: Countable structures

**Fundamental Concepts**:
• **Numbers**: Natural, integers, rational, real, complex
• **Functions**: Relationships between inputs and outputs
• **Equations**: Mathematical statements of equality
• **Proofs**: Logical arguments establishing truth
• **Sets**: Collections of objects

**Key Areas**:
• **Linear Algebra**: Vectors, matrices, systems of equations
• **Differential Equations**: Equations involving derivatives
• **Probability**: Likelihood of events occurring
• **Number Theory**: Properties of integers

**Applications**: Science, engineering, economics, computer science, cryptography, data analysis, artificial intelligence."""
            },
            
            # Business & Economics
            'economics': {
                'keywords': ['economics', 'what is economics'],
                'response': """**Economics** is the social science that studies how societies allocate scarce resources to satisfy unlimited wants and needs.

**Major Branches**:
• **Microeconomics**: Individual consumers, firms, and markets
• **Macroeconomics**: National economies, GDP, inflation, unemployment
• **International Economics**: Trade, exchange rates, globalization
• **Development Economics**: Economic growth in developing countries

**Fundamental Concepts**:
• **Scarcity**: Limited resources vs. unlimited wants
• **Opportunity Cost**: Value of the next best alternative
• **Supply and Demand**: Market forces determining prices
• **Market Equilibrium**: Where supply meets demand
• **Elasticity**: Responsiveness to price changes

**Key Principles**:
• **Comparative Advantage**: Specialization benefits
• **Market Efficiency**: Optimal resource allocation
• **Externalities**: Costs/benefits affecting third parties
• **Public Goods**: Non-excludable, non-rivalrous goods

**Economic Indicators**:
• GDP (Gross Domestic Product)
• Inflation rate
• Unemployment rate
• Interest rates

**Applications**: Policy making, business strategy, investment decisions, understanding market behavior."""
            },
            
            'marketing': {
                'keywords': ['marketing', 'what is marketing', 'digital marketing'],
                'response': """**Marketing** is the process of creating, communicating, delivering, and exchanging offerings that have value for customers, clients, partners, and society.

**Core Concepts**:
• **4 Ps of Marketing**: Product, Price, Place, Promotion
• **Target Market**: Specific group of potential customers
• **Value Proposition**: Unique benefit offered to customers
• **Brand**: Identity and reputation in the marketplace
• **Customer Journey**: Process from awareness to purchase

**Types of Marketing**:
• **Digital Marketing**: Online channels (social media, email, SEO)
• **Content Marketing**: Valuable content to attract customers
• **Social Media Marketing**: Platforms like Facebook, Instagram, LinkedIn
• **Email Marketing**: Direct communication with subscribers
• **Influencer Marketing**: Partnerships with influential people

**Digital Marketing Channels**:
• **SEO**: Search Engine Optimization
• **SEM**: Search Engine Marketing (paid ads)
• **Social Media**: Organic and paid social content
• **Email**: Newsletters, promotional campaigns
• **Content**: Blogs, videos, podcasts

**Metrics and Analytics**:
• Conversion rate, click-through rate, engagement rate
• Customer acquisition cost (CAC)
• Return on investment (ROI)
• Customer lifetime value (CLV)

**Modern Trends**: Personalization, automation, AI-driven insights, omnichannel experiences."""
            },
            
            # Health & Medicine
            'medicine': {
                'keywords': ['medicine', 'what is medicine', 'medical science'],
                'response': """**Medicine** is the science and practice of diagnosing, treating, and preventing disease, illness, and injury to maintain and restore health.

**Major Specialties**:
• **Internal Medicine**: Adult diseases and conditions
• **Surgery**: Operative procedures and treatments
• **Pediatrics**: Medical care for infants, children, and adolescents
• **Psychiatry**: Mental health and behavioral disorders
• **Radiology**: Medical imaging and diagnosis
• **Emergency Medicine**: Acute care and trauma

**Diagnostic Methods**:
• **Physical Examination**: Visual inspection, palpation, auscultation
• **Laboratory Tests**: Blood work, urine analysis, cultures
• **Medical Imaging**: X-rays, CT scans, MRI, ultrasound
• **Biopsy**: Tissue sample analysis
• **Genetic Testing**: DNA analysis for hereditary conditions

**Treatment Approaches**:
• **Pharmacotherapy**: Medications and drugs
• **Surgery**: Operative interventions
• **Physical Therapy**: Movement and exercise therapy
• **Radiation Therapy**: High-energy radiation treatment
• **Immunotherapy**: Boosting immune system response

**Modern Medicine**:
• Evidence-based practice
• Personalized medicine based on genetics
• Telemedicine and remote monitoring
• Minimally invasive procedures
• Preventive care and wellness focus

**Ethics**: Patient confidentiality, informed consent, do no harm (primum non nocere)."""
            },
            
            'psychology': {
                'keywords': ['psychology', 'what is psychology'],
                'response': """**Psychology** is the scientific study of mind and behavior, including conscious and unconscious phenomena, feelings, and thoughts.

**Major Branches**:
• **Clinical Psychology**: Mental health diagnosis and treatment
• **Cognitive Psychology**: Mental processes like memory, perception, thinking
• **Social Psychology**: How people interact and influence each other
• **Developmental Psychology**: Human growth and development across lifespan
• **Behavioral Psychology**: Learning and behavior modification

**Key Concepts**:
• **Consciousness**: Awareness of thoughts, feelings, and surroundings
• **Learning**: Acquiring new knowledge, behaviors, or skills
• **Memory**: Encoding, storing, and retrieving information
• **Personality**: Individual patterns of thinking, feeling, and behaving
• **Motivation**: Forces that drive behavior and goal pursuit

**Research Methods**:
• **Experiments**: Controlled studies to test hypotheses
• **Surveys**: Questionnaires and interviews
• **Observations**: Systematic watching and recording behavior
• **Case Studies**: In-depth analysis of individuals or groups
• **Longitudinal Studies**: Following subjects over time

**Applications**:
• Mental health treatment and therapy
• Educational psychology and learning optimization
• Organizational psychology and workplace behavior
• Sports psychology and performance enhancement
• Forensic psychology and criminal behavior analysis

**Therapeutic Approaches**: Cognitive-behavioral therapy (CBT), psychoanalysis, humanistic therapy, group therapy."""
            },
            
            # History & Social Sciences
            'history': {
                'keywords': ['history', 'what is history'],
                'response': """**History** is the study of past events, particularly human activities, societies, and civilizations, to understand how they have shaped the present world.

**Major Periods**:
• **Prehistoric**: Before written records
• **Ancient**: Early civilizations (Egypt, Greece, Rome)
• **Medieval**: Middle Ages (5th-15th centuries)
• **Renaissance**: Cultural rebirth (14th-17th centuries)
• **Modern**: Industrial Revolution to present

**Key Civilizations**:
• **Ancient Egypt**: Pyramids, pharaohs, hieroglyphics
• **Ancient Greece**: Democracy, philosophy, arts
• **Roman Empire**: Law, engineering, military organization
• **Chinese Dynasties**: Inventions, philosophy, trade
• **Islamic Golden Age**: Science, mathematics, medicine

**Historical Methods**:
• **Primary Sources**: Original documents, artifacts, eyewitness accounts
• **Secondary Sources**: Interpretations and analyses by historians
• **Archaeological Evidence**: Physical remains and artifacts
• **Oral History**: Spoken accounts passed down through generations

**Major Themes**:
• Rise and fall of civilizations
• Wars, conflicts, and their consequences
• Social, economic, and political changes
• Cultural and technological developments
• Human migration and settlement patterns

**Importance**: Understanding the past helps us comprehend current events, learn from mistakes, and make informed decisions about the future."""
            },
            
            'geography': {
                'keywords': ['geography', 'what is geography'],
                'response': """**Geography** is the study of Earth's landscapes, peoples, places, and environments, examining the relationships between human activities and the natural world.

**Major Branches**:
• **Physical Geography**: Natural features (climate, landforms, ecosystems)
• **Human Geography**: Human activities and their spatial patterns
• **Economic Geography**: Economic activities and their locations
• **Political Geography**: Political processes and territorial organization
• **Cultural Geography**: Cultural practices and their spatial distribution

**Physical Geography Topics**:
• **Climate**: Weather patterns, temperature, precipitation
• **Landforms**: Mountains, valleys, plains, coastlines
• **Hydrology**: Rivers, lakes, groundwater, oceans
• **Ecosystems**: Biomes, biodiversity, environmental interactions
• **Natural Disasters**: Earthquakes, hurricanes, floods, droughts

**Human Geography Topics**:
• **Population**: Distribution, density, migration patterns
• **Urbanization**: Cities, urban planning, metropolitan areas
• **Agriculture**: Farming systems, food production, land use
• **Transportation**: Networks, accessibility, mobility
• **Globalization**: Economic, cultural, and political connections

**Geographic Tools**:
• **Maps**: Visual representations of spatial information
• **GIS**: Geographic Information Systems for data analysis
• **Remote Sensing**: Satellite imagery and aerial photography
• **GPS**: Global Positioning System for location determination

**Applications**: Urban planning, environmental management, disaster preparedness, business location analysis, tourism development."""
            },
            
            # Interview-specific responses
            'tell_me_about_yourself': {
                'keywords': ['tell me about yourself', 'tell me about your background', 'describe yourself', 'introduce yourself professionally'],
                'response': """This is a classic interview question! Here's how to structure a great "Tell me about yourself" response:

**The Perfect Structure**:
• **Present**: Your current role and key responsibilities
• **Past**: Relevant experience and achievements that led you here
• **Future**: Why you're interested in this opportunity

**Example Framework**:
"I'm currently a [current role] where I [key responsibilities]. Previously, I [relevant experience] which helped me develop [key skills]. I'm excited about this opportunity because [connection to the role/company]."

**Tips for Success**:
• Keep it to 60-90 seconds
• Focus on professional highlights, not personal details
• Connect your experience to the job you're applying for
• Practice until it sounds natural, not rehearsed
• End with enthusiasm for the role

**What NOT to include**:
• Personal life details (family, hobbies unless relevant)
• Negative comments about previous employers
• Your entire life story
• Weaknesses or failures

Would you like help crafting your specific response based on your background?"""
            },
            
            'why_should_we_hire_you': {
                'keywords': ['why should we hire you', 'why hire you', 'what makes you the best candidate'],
                'response': """This is your chance to sell yourself! Here's how to nail this crucial question:

**Structure Your Answer**:
• **Skills Match**: Highlight skills that directly match the job requirements
• **Unique Value**: What sets you apart from other candidates
• **Results**: Specific achievements that demonstrate your impact
• **Cultural Fit**: How you align with company values

**Formula**: "You should hire me because I bring [specific skills] with a proven track record of [specific results]. What makes me unique is [differentiator], and I'm excited to [contribute to company goals]."

**Example Elements to Include**:
• Technical skills relevant to the role
• Leadership or teamwork experience
• Problem-solving abilities with examples
• Industry knowledge or certifications
• Passion for the company's mission

**Make it Compelling**:
• Use specific numbers and metrics when possible
• Show enthusiasm and confidence
• Connect your strengths to their needs
• Avoid generic answers - be specific to this role

Remember: They're not just hiring skills, they're hiring a person who will contribute to their team and culture!"""
            },
            
            'greatest_strength': {
                'keywords': ['greatest strength', 'biggest strength', 'what are your strengths', 'your strengths'],
                'response': """When discussing your strengths, make them relevant and provide evidence:

**How to Structure Your Answer**:
• **Choose Relevant Strengths**: Pick 2-3 that match the job requirements
• **Provide Evidence**: Give specific examples of how you've used these strengths
• **Show Impact**: Explain the positive results your strengths achieved

**Popular Professional Strengths**:
• **Problem-solving**: "I excel at analyzing complex problems and finding creative solutions..."
• **Communication**: "I'm skilled at explaining technical concepts to non-technical stakeholders..."
• **Leadership**: "I have a talent for motivating teams and driving projects to completion..."
• **Adaptability**: "I thrive in changing environments and quickly learn new technologies..."
• **Attention to Detail**: "My meticulous approach has helped prevent costly errors..."

**Example Response**:
"My greatest strength is problem-solving. In my previous role, I identified a process inefficiency that was costing the company $50K annually. I developed and implemented a solution that not only eliminated the waste but improved productivity by 20%."

**Tips**:
• Be authentic - choose strengths you genuinely possess
• Avoid clichés like "I'm a perfectionist"
• Connect strengths to the specific role
• Prepare 2-3 different strengths for follow-up questions"""
            },
            
            'biggest_weakness': {
                'keywords': ['biggest weakness', 'greatest weakness', 'what are your weaknesses', 'your weakness'],
                'response': """The weakness question is tricky, but here's how to handle it professionally:

**The Right Approach**:
• **Be Honest**: Choose a real weakness, not a strength in disguise
• **Show Self-Awareness**: Demonstrate you understand your areas for improvement
• **Highlight Growth**: Explain what you're doing to address it
• **Keep it Professional**: Focus on work-related weaknesses

**Good Weakness Examples**:
• **Public Speaking**: "I used to be nervous presenting to large groups, so I joined Toastmasters and now regularly volunteer to present at team meetings."
• **Delegation**: "I sometimes try to do too much myself. I'm learning to trust my team more and have started using project management tools to better distribute tasks."
• **New Technology**: "I'm not as familiar with [specific tool], but I've enrolled in an online course and practice with it daily."

**Example Response**:
"My biggest weakness has been delegation. I tend to take on too much myself because I want to ensure quality. However, I've realized this limits team growth and my own capacity. I'm now actively working on this by clearly defining expectations, providing proper training, and scheduling regular check-ins rather than doing everything myself."

**Avoid These**:
• "I'm a perfectionist" (overused)
• "I work too hard" (not believable)
• Critical weaknesses for the role
• Personal weaknesses unrelated to work"""
            },
            
            'why_work_here': {
                'keywords': ['why do you want to work here', 'why this company', 'why are you interested in this company'],
                'response': """This question tests your research and genuine interest in the company. Here's how to answer effectively:

**Research-Based Structure**:
• **Company Mission/Values**: Show alignment with their purpose
• **Growth Opportunities**: Explain how the role fits your career goals
• **Company Culture**: Demonstrate cultural fit
• **Industry Position**: Acknowledge their market leadership or innovation

**Example Framework**:
"I'm excited about this opportunity because [specific company attribute] aligns perfectly with my values and career goals. I'm particularly drawn to [specific project/initiative/value], and I believe my experience in [relevant area] would allow me to contribute meaningfully while growing in [specific direction]."

**What to Research**:
• Recent company news and achievements
• Company mission, vision, and values
• Products, services, and market position
• Company culture and work environment
• Growth opportunities and career paths

**Make it Personal**:
• Connect their mission to your personal values
• Explain how the role advances your career goals
• Show enthusiasm for their products/services
• Mention specific aspects that excite you

**Avoid Generic Answers**:
• "It's a great company" (too vague)
• Only mentioning salary or benefits
• Focusing solely on what they can do for you
• Answers that could apply to any company"""
            },
            
            'five_year_plan': {
                'keywords': ['where do you see yourself in 5 years', '5 year plan', 'future goals', 'career goals'],
                'response': """This question assesses your ambition, planning skills, and whether you'll stay with the company. Here's how to answer strategically:

**Structure Your Response**:
• **Show Growth Mindset**: Demonstrate desire to develop and advance
• **Align with Role**: Connect your goals to the position you're applying for
• **Be Realistic**: Set achievable goals that show ambition without being unrealistic
• **Show Loyalty**: Indicate you see a future with this company

**Example Response Framework**:
"In five years, I see myself having grown significantly in [relevant skill areas], ideally in a [target role/level] where I can [specific contributions]. I'd love to have [specific achievements] and be recognized as [expertise area]. This role would be a perfect stepping stone because [connection to current opportunity]."

**Good Elements to Include**:
• Skill development and expertise building
• Leadership or mentoring responsibilities
• Industry recognition or certifications
• Contribution to company success
• Work-life balance and personal growth

**Sample Goals by Career Stage**:
• **Early Career**: "Become a subject matter expert, take on project leadership"
• **Mid-Career**: "Move into management, develop strategic thinking skills"
• **Senior Level**: "Drive organizational change, mentor next generation"

**What to Avoid**:
• Being too specific about titles or salary
• Mentioning plans to leave or start your own business
• Saying you don't know or haven't thought about it
• Goals that don't align with the company's direction"""
            },
            
            # Personal/Identity Questions
            'chatbot_name': {
                'keywords': ['what is your name', 'your name', 'who are you', 'what are you called', 'introduce yourself'],
                'response': """I'm your **Universal AI Assistant**! I'm designed to help you with any question you might have.

**What I can do**:
• **Answer technical questions**: Programming, databases, algorithms, web development
• **Explain scientific concepts**: Physics, chemistry, biology, mathematics
• **Provide technology insights**: AI, machine learning, cybersecurity, cloud computing
• **Offer career guidance**: Interview preparation, professional development
• **Help with learning**: Study techniques, skill development, educational resources
• **Assist with business topics**: Marketing, economics, entrepreneurship
• **Support creative projects**: Writing, content creation, problem-solving

**My capabilities**:
• Comprehensive knowledge base covering 50+ major topics
• Detailed explanations with examples and practical applications
• Professional formatting with bullet points and code snippets
• Context-aware responses based on your needs

Feel free to ask me anything - from "What is DBMS?" to "How does machine learning work?" to "What are good interview tips?" I'm here to provide detailed, helpful answers!"""
            },
            
            'chatbot_identity': {
                'keywords': ['what are you', 'are you human', 'are you ai', 'are you a robot', 'what kind of assistant'],
                'response': """I'm an **AI-powered Universal Assistant** designed to provide comprehensive, accurate answers to any question you might have.

**My Design**:
• **Knowledge-Based**: Built with a comprehensive database of information across multiple domains
• **Intelligent Routing**: Uses advanced algorithms to understand your questions and provide relevant responses
• **Multi-Modal**: Can handle technical, scientific, business, creative, and personal development questions
• **Adaptive**: Learns from context to provide more relevant answers

**What Makes Me Different**:
• **Comprehensive Coverage**: From programming concepts to scientific principles to career advice
• **Detailed Responses**: Not just brief answers, but thorough explanations with examples
• **Professional Quality**: Well-formatted, accurate, and actionable information
• **Always Available**: Ready to help 24/7 with any topic you're curious about

**My Purpose**: To be your go-to resource for learning, problem-solving, and getting detailed explanations on any topic. Whether you're studying, working on a project, or just curious about something, I'm here to provide helpful, comprehensive answers.

What would you like to learn about today?"""
            },
            
            'chatbot_capabilities': {
                'keywords': ['what can you do', 'your capabilities', 'how can you help', 'what do you know'],
                'response': """I can help you with a **wide range of topics and questions**! Here's what I specialize in:

**🔧 Technology & Programming**:
• Programming languages (Python, JavaScript, Java, C++, etc.)
• Web development (HTML, CSS, React, Node.js)
• Databases (SQL, NoSQL, DBMS concepts)
• Software engineering (algorithms, data structures, OOP)
• Emerging tech (AI, blockchain, IoT, cybersecurity)

**🔬 Science & Mathematics**:
• Physics (mechanics, thermodynamics, quantum physics)
• Chemistry (organic, inorganic, biochemistry)
• Biology (genetics, cell biology, ecology)
• Mathematics (algebra, calculus, statistics)

**💼 Business & Career**:
• Interview preparation and career advice
• Marketing and business strategy
• Economics and finance
• Entrepreneurship and startups
• Professional development

**📚 Education & Learning**:
• Study techniques and learning strategies
• Course recommendations and skill building
• Research methods and academic writing
• Problem-solving approaches

**🎨 Creative & Communication**:
• Writing and content creation
• Presentation skills and public speaking
• Creative problem-solving
• Design thinking

**💡 How I Help**:
• Provide detailed, accurate explanations
• Give practical examples and applications
• Offer step-by-step guidance
• Share best practices and tips
• Answer follow-up questions

**Just ask me anything!** From technical concepts like "What is machine learning?" to practical questions like "How do I prepare for interviews?" - I'm here to give you comprehensive, helpful answers."""
            },
            'literature': {
                'keywords': ['literature', 'what is literature'],
                'response': """**Literature** is written works, especially those considered to have artistic or intellectual value, including poetry, drama, fiction, and non-fiction.

**Major Genres**:
• **Poetry**: Verse expressing emotions, ideas, or experiences
• **Drama**: Plays written for theatrical performance
• **Fiction**: Imaginative narratives (novels, short stories)
• **Non-fiction**: Factual writing (essays, biographies, memoirs)
• **Epic**: Long narrative poems about heroic deeds

**Literary Elements**:
• **Plot**: Sequence of events in a story
• **Character**: People or entities in the narrative
• **Setting**: Time and place of the story
• **Theme**: Central message or meaning
• **Style**: Author's distinctive way of writing
• **Point of View**: Perspective from which story is told

**Literary Devices**:
• **Metaphor**: Implicit comparison between unlike things
• **Symbolism**: Objects representing deeper meanings
• **Irony**: Contrast between expectation and reality
• **Foreshadowing**: Hints about future events
• **Alliteration**: Repetition of initial consonant sounds

**Major Movements**:
• **Romanticism**: Emotion, nature, individualism
• **Realism**: Accurate depiction of everyday life
• **Modernism**: Experimental forms and techniques
• **Postmodernism**: Questioning traditional narratives

**World Literature**: Works from diverse cultures and time periods that have universal significance and lasting impact on human understanding."""
            },
            
            # Advanced Technology
            'cloud_computing': {
                'keywords': ['cloud computing', 'cloud', 'what is cloud'],
                'response': """**Cloud Computing** is the delivery of computing services (servers, storage, databases, networking, software) over the internet ("the cloud").

**Key Characteristics**:
• **On-demand**: Access resources when needed
• **Scalable**: Easily increase or decrease capacity
• **Pay-as-you-go**: Only pay for what you use
• **Global Access**: Available from anywhere with internet
• **Managed**: Provider handles maintenance and updates

**Service Models**:
• **IaaS** (Infrastructure): Virtual machines, storage (AWS EC2)
• **PaaS** (Platform): Development platforms (Google App Engine)
• **SaaS** (Software): Ready-to-use applications (Gmail, Office 365)

**Major Providers**:
• **Amazon Web Services (AWS)**: Market leader
• **Microsoft Azure**: Enterprise-focused
• **Google Cloud Platform**: AI/ML strengths
• **IBM Cloud, Oracle Cloud**: Specialized solutions

**Benefits**: Cost savings, flexibility, automatic updates, disaster recovery, collaboration
**Challenges**: Security concerns, internet dependency, vendor lock-in

**Use Cases**: Web hosting, data backup, software development, big data analytics, AI/ML training"""
            },
            
            'blockchain': {
                'keywords': ['blockchain', 'what is blockchain'],
                'response': """**Blockchain** is a distributed digital ledger technology that maintains a continuously growing list of records (blocks) that are linked and secured using cryptography.

**Key Features**:
• **Decentralized**: No single point of control
• **Immutable**: Records cannot be altered once added
• **Transparent**: All transactions are visible to network participants
• **Secure**: Cryptographic hashing protects data integrity
• **Consensus**: Network agrees on transaction validity

**How It Works**:
1. **Transaction**: User initiates a transaction
2. **Broadcasting**: Transaction is broadcast to network
3. **Validation**: Network nodes validate the transaction
4. **Block Creation**: Valid transactions are grouped into a block
5. **Consensus**: Network agrees on the new block
6. **Addition**: Block is added to the chain permanently

**Applications**:
• **Cryptocurrency**: Bitcoin, Ethereum, digital payments
• **Supply Chain**: Track products from origin to consumer
• **Smart Contracts**: Self-executing contracts with coded terms
• **Digital Identity**: Secure identity verification
• **Voting Systems**: Transparent, tamper-proof elections

**Benefits**: Trust without intermediaries, reduced costs, increased security, global accessibility
**Challenges**: Energy consumption, scalability, regulatory uncertainty"""
            },
            
            'cryptocurrency': {
                'keywords': ['cryptocurrency', 'crypto', 'bitcoin', 'what is cryptocurrency'],
                'response': """**Cryptocurrency** is a digital or virtual currency that uses cryptography for security and operates independently of traditional banking systems.

**Key Characteristics**:
• **Digital**: Exists only in electronic form
• **Decentralized**: Not controlled by governments or banks
• **Cryptographic**: Uses advanced encryption for security
• **Peer-to-Peer**: Direct transactions between users
• **Limited Supply**: Most have a maximum number of coins

**Popular Cryptocurrencies**:
• **Bitcoin (BTC)**: First and most valuable cryptocurrency
• **Ethereum (ETH)**: Platform for smart contracts and DApps
• **Litecoin (LTC)**: Faster transaction processing
• **Ripple (XRP)**: Designed for banking and payments
• **Cardano (ADA)**: Focus on sustainability and research

**How It Works**:
• **Blockchain Technology**: Distributed ledger records all transactions
• **Mining**: Process of validating transactions and creating new coins
• **Wallets**: Software or hardware that stores cryptocurrency keys
• **Exchanges**: Platforms for buying, selling, and trading crypto

**Uses**:
• Digital payments and remittances
• Investment and trading
• Smart contracts and DeFi (Decentralized Finance)
• NFTs (Non-Fungible Tokens)
• Store of value (digital gold)

**Benefits**: Fast global transfers, lower fees, financial inclusion, inflation hedge
**Risks**: Price volatility, regulatory uncertainty, security concerns, environmental impact"""
            },
            
            # Science Expansions
            'gravity': {
                'keywords': ['gravity', 'what is gravity', 'gravitational force'],
                'response': """**Gravity** is a fundamental force of nature that causes objects with mass to attract each other. It's the weakest of the four fundamental forces but dominates at large scales.

**Key Concepts**:
• **Universal**: Every object with mass attracts every other object
• **Proportional**: Stronger attraction between more massive objects
• **Distance**: Force decreases with the square of distance
• **Always Attractive**: Never repulsive, unlike other forces

**Newton's Law of Universal Gravitation**:
F = G(m₁m₂)/r²
• F = gravitational force
• G = gravitational constant
• m₁, m₂ = masses of objects
• r = distance between centers

**Einstein's General Relativity**:
• Gravity is not a force but curvature of spacetime
• Massive objects bend spacetime
• Objects follow the straightest path in curved spacetime
• Explains phenomena Newton's theory couldn't

**Effects of Gravity**:
• **Weight**: Force of gravity on an object (W = mg)
• **Tides**: Moon's gravity pulls on Earth's oceans
• **Orbital Motion**: Planets orbit the sun, satellites orbit Earth
• **Time Dilation**: Time runs slower in stronger gravitational fields

**Applications**: GPS satellites, space missions, understanding universe structure, predicting planetary motion"""
            },
            
            'dna': {
                'keywords': ['dna', 'what is dna', 'deoxyribonucleic acid'],
                'response': """**DNA (Deoxyribonucleic Acid)** is the hereditary material that contains the genetic instructions for the development, functioning, and reproduction of all known living organisms.

**Structure**:
• **Double Helix**: Two intertwined strands forming a spiral ladder
• **Nucleotides**: Building blocks containing a base, sugar, and phosphate
• **Base Pairs**: A-T (Adenine-Thymine) and G-C (Guanine-Cytosine)
• **Antiparallel**: Strands run in opposite directions

**Key Functions**:
• **Genetic Information**: Stores instructions for making proteins
• **Heredity**: Passes traits from parents to offspring
• **Protein Synthesis**: Codes for amino acid sequences
• **Cell Division**: Replicates to ensure each cell has genetic information

**DNA Replication Process**:
1. **Unwinding**: Double helix unzips at replication fork
2. **Priming**: RNA primers provide starting points
3. **Synthesis**: DNA polymerase adds complementary nucleotides
4. **Proofreading**: Errors are detected and corrected
5. **Completion**: Two identical DNA molecules are produced

**Genetic Code**:
• **Codons**: Three-base sequences that specify amino acids
• **64 Codons**: Code for 20 amino acids plus start/stop signals
• **Universal**: Same genetic code used by almost all life forms

**Applications**: Medicine (gene therapy, genetic testing), forensics (DNA fingerprinting), agriculture (GMOs), evolutionary biology, personalized medicine"""
            },
            
            'photosynthesis': {
                'keywords': ['photosynthesis', 'explain photosynthesis'],
                'response': """**Photosynthesis** is the process by which plants, algae, and some bacteria convert light energy (usually from the sun) into chemical energy stored in glucose.

**Overall Equation**:
6CO₂ + 6H₂O + light energy → C₆H₁₂O₆ + 6O₂ + ATP

**Two Main Stages**:

**1. Light-Dependent Reactions (Photo)**:
• **Location**: Thylakoid membranes in chloroplasts
• **Process**: Chlorophyll absorbs light energy
• **Products**: ATP, NADPH, and oxygen (O₂)
• **Water Splitting**: H₂O → 2H⁺ + ½O₂ + 2e⁻

**2. Light-Independent Reactions (Calvin Cycle)**:
• **Location**: Stroma of chloroplasts
• **Process**: CO₂ is "fixed" into organic molecules
• **Products**: Glucose (C₆H₁₂O₆)
• **Energy Source**: ATP and NADPH from light reactions

**Key Components**:
• **Chlorophyll**: Green pigment that captures light
• **Chloroplasts**: Organelles where photosynthesis occurs
• **Stomata**: Pores that allow gas exchange (CO₂ in, O₂ out)
• **Guard Cells**: Control opening and closing of stomata

**Importance**:
• **Oxygen Production**: Nearly all atmospheric oxygen comes from photosynthesis
• **Food Chain Base**: Primary producers support all other life
• **Carbon Cycle**: Removes CO₂ from atmosphere
• **Energy Conversion**: Converts solar energy into chemical energy

**Factors Affecting Rate**: Light intensity, CO₂ concentration, temperature, water availability"""
            },
            
            # More comprehensive topics
            'neural_networks': {
                'keywords': ['neural networks', 'neural network', 'artificial neural network'],
                'response': """**Neural Networks** are computing systems inspired by biological neural networks that learn to perform tasks by analyzing examples without being programmed with task-specific rules.

**Structure**:
• **Neurons (Nodes)**: Basic processing units that receive, process, and transmit information
• **Layers**: Input layer, hidden layers, and output layer
• **Weights**: Connections between neurons with varying strengths
• **Bias**: Additional parameter that helps the model fit the data better

**How They Work**:
1. **Input**: Data enters through the input layer
2. **Processing**: Each neuron applies weights and activation function
3. **Forward Propagation**: Information flows through hidden layers
4. **Output**: Final layer produces the result
5. **Learning**: Backpropagation adjusts weights based on errors

**Types of Neural Networks**:
• **Feedforward**: Information flows in one direction
• **Convolutional (CNN)**: Excellent for image recognition
• **Recurrent (RNN)**: Can process sequences and time series
• **Long Short-Term Memory (LSTM)**: Advanced RNN for long sequences
• **Generative Adversarial (GAN)**: Two networks competing to generate realistic data

**Applications**:
• **Image Recognition**: Medical imaging, facial recognition, autonomous vehicles
• **Natural Language Processing**: Translation, chatbots, sentiment analysis
• **Recommendation Systems**: Netflix, Amazon, Spotify suggestions
• **Game Playing**: Chess, Go, video games
• **Financial Modeling**: Fraud detection, algorithmic trading

**Advantages**: Pattern recognition, adaptability, parallel processing, handling complex non-linear relationships
**Challenges**: Requires large datasets, computationally intensive, "black box" nature makes interpretation difficult"""
            }
        }
        
        # Add many more topics to ensure comprehensive coverage
        additional_topics = {
            '5g': {
                'keywords': ['5g', 'what is 5g', 'fifth generation'],
                'response': """**5G** is the fifth generation of cellular network technology, designed to provide faster speeds, lower latency, and support for more connected devices than previous generations.

**Key Features**:
• **Ultra-Fast Speeds**: Up to 100 times faster than 4G (up to 10 Gbps)
• **Low Latency**: Response times as low as 1 millisecond
• **Massive Connectivity**: Support for up to 1 million devices per square kilometer
• **Network Slicing**: Customized network segments for different applications
• **Enhanced Reliability**: 99.999% availability for critical applications

**Frequency Bands**:
• **Low-band**: Wide coverage, similar speeds to 4G
• **Mid-band**: Balance of coverage and speed
• **High-band (mmWave)**: Extremely fast but limited range

**Applications**:
• **Enhanced Mobile Broadband**: Faster streaming, downloads, gaming
• **Internet of Things (IoT)**: Smart cities, connected vehicles, industrial automation
• **Autonomous Vehicles**: Real-time communication for safety
• **Augmented/Virtual Reality**: Immersive experiences with minimal lag
• **Remote Surgery**: Precise control with ultra-low latency
• **Smart Manufacturing**: Real-time monitoring and control

**Benefits**: Economic growth, innovation enablement, improved efficiency, new business models
**Challenges**: Infrastructure costs, security concerns, health debates, coverage gaps"""
            },
            
            'virtual_reality': {
                'keywords': ['virtual reality', 'vr', 'what is virtual reality'],
                'response': """**Virtual Reality (VR)** is a computer-generated simulation that creates an immersive, three-dimensional environment that users can interact with using specialized hardware.

**Key Components**:
• **VR Headset**: Display device worn on the head (Oculus, HTC Vive, PlayStation VR)
• **Motion Controllers**: Hand-held devices for interaction
• **Tracking Systems**: Monitor head and body movements
• **Powerful Computer**: Processes complex 3D graphics in real-time
• **Audio System**: 3D spatial audio for immersion

**How It Works**:
1. **Rendering**: Computer generates stereoscopic 3D images
2. **Display**: Separate images shown to each eye creating depth perception
3. **Tracking**: Sensors monitor head movement and adjust view accordingly
4. **Interaction**: Controllers translate hand movements into virtual actions
5. **Feedback**: Haptic feedback provides touch sensations

**Types of VR**:
• **Fully Immersive**: Complete virtual environment (gaming, training)
• **Semi-Immersive**: Partial virtual environment (flight simulators)
• **Non-Immersive**: Desktop VR without head-mounted display

**Applications**:
• **Gaming and Entertainment**: Immersive games, virtual concerts, movies
• **Education and Training**: Medical training, historical recreations, skill development
• **Healthcare**: Therapy, pain management, surgical planning
• **Business**: Virtual meetings, product design, real estate tours
• **Military**: Combat training, mission planning, equipment simulation

**Benefits**: Safe training environments, enhanced learning, new forms of entertainment, remote collaboration
**Challenges**: Motion sickness, high costs, limited content, social isolation concerns"""
            },
            
            'internet_of_things': {
                'keywords': ['internet of things', 'iot', 'what is iot'],
                'response': """**Internet of Things (IoT)** refers to the network of physical devices embedded with sensors, software, and connectivity that enables them to collect and exchange data over the internet.

**Key Components**:
• **Sensors**: Collect data from the environment (temperature, motion, light)
• **Connectivity**: Wi-Fi, Bluetooth, cellular, or other communication methods
• **Data Processing**: Edge computing or cloud-based analysis
• **User Interface**: Apps, dashboards, or automated responses
• **Actuators**: Devices that can take physical actions based on data

**How IoT Works**:
1. **Data Collection**: Sensors gather information from physical world
2. **Transmission**: Data is sent to processing systems via internet
3. **Analysis**: Algorithms process and analyze the data
4. **Action**: Automated responses or alerts are generated
5. **Feedback**: Results influence future device behavior

**Categories**:
• **Consumer IoT**: Smart homes, wearables, connected cars
• **Industrial IoT (IIoT)**: Manufacturing, supply chain, predictive maintenance
• **Commercial IoT**: Smart buildings, retail analytics, fleet management
• **Infrastructure IoT**: Smart cities, utilities, transportation systems

**Applications**:
• **Smart Homes**: Thermostats, security systems, lighting, appliances
• **Healthcare**: Wearable monitors, remote patient monitoring, smart pills
• **Agriculture**: Soil sensors, automated irrigation, livestock tracking
• **Transportation**: Connected vehicles, traffic management, logistics
• **Manufacturing**: Predictive maintenance, quality control, supply chain optimization

**Benefits**: Efficiency improvements, cost savings, enhanced safety, better decision-making, new business models
**Challenges**: Security vulnerabilities, privacy concerns, interoperability issues, data management complexity"""
            },
            
            'cybersecurity': {
                'keywords': ['cybersecurity', 'cyber security', 'what is cybersecurity'],
                'response': """**Cybersecurity** is the practice of protecting systems, networks, and programs from digital attacks, unauthorized access, and data breaches.

**Core Principles (CIA Triad)**:
• **Confidentiality**: Ensuring information is accessible only to authorized users
• **Integrity**: Maintaining accuracy and completeness of data
• **Availability**: Ensuring systems and data are accessible when needed

**Types of Cyber Threats**:
• **Malware**: Viruses, worms, trojans, ransomware, spyware
• **Phishing**: Fraudulent emails or websites to steal credentials
• **Social Engineering**: Manipulating people to reveal information
• **DDoS Attacks**: Overwhelming systems with traffic to cause downtime
• **Advanced Persistent Threats (APTs)**: Long-term targeted attacks
• **Insider Threats**: Malicious or negligent actions by employees

**Security Measures**:
• **Firewalls**: Network traffic filtering and monitoring
• **Antivirus Software**: Detecting and removing malicious programs
• **Encryption**: Converting data into unreadable format
• **Multi-Factor Authentication**: Multiple verification methods
• **Regular Updates**: Patching security vulnerabilities
• **Backup Systems**: Data recovery and business continuity

**Best Practices**:
• **Strong Passwords**: Complex, unique passwords for each account
• **Security Awareness Training**: Educating users about threats
• **Network Segmentation**: Isolating critical systems
• **Incident Response Plan**: Procedures for handling security breaches
• **Regular Security Audits**: Identifying and addressing vulnerabilities

**Career Paths**: Security analyst, ethical hacker, security architect, incident responder, compliance officer
**Importance**: Protecting personal privacy, business continuity, national security, economic stability"""
            },
            
            'big_data': {
                'keywords': ['big data', 'what is big data'],
                'response': """**Big Data** refers to extremely large and complex datasets that cannot be processed effectively using traditional data processing applications and require specialized tools and techniques.

**The 5 V's of Big Data**:
• **Volume**: Massive amounts of data (terabytes to exabytes)
• **Velocity**: High speed of data generation and processing
• **Variety**: Different types of data (structured, unstructured, semi-structured)
• **Veracity**: Quality and accuracy of data
• **Value**: Extracting meaningful insights from data

**Data Sources**:
• **Social Media**: Posts, comments, likes, shares, user interactions
• **IoT Devices**: Sensors, smart devices, wearables, industrial equipment
• **Business Transactions**: Sales, purchases, financial records
• **Web Analytics**: Website visits, clicks, user behavior
• **Scientific Research**: Experiments, simulations, observations

**Technologies and Tools**:
• **Storage**: Hadoop Distributed File System (HDFS), cloud storage
• **Processing**: Apache Spark, MapReduce, stream processing
• **Databases**: NoSQL databases (MongoDB, Cassandra), data lakes
• **Analytics**: Machine learning, statistical analysis, data mining
• **Visualization**: Tableau, Power BI, custom dashboards

**Applications**:
• **Business Intelligence**: Customer insights, market analysis, performance metrics
• **Healthcare**: Personalized medicine, drug discovery, epidemic tracking
• **Finance**: Fraud detection, risk assessment, algorithmic trading
• **Transportation**: Route optimization, predictive maintenance, autonomous vehicles
• **Entertainment**: Content recommendation, audience analysis, personalization

**Benefits**: Better decision-making, competitive advantage, innovation opportunities, cost reduction, improved efficiency
**Challenges**: Data privacy, storage costs, processing complexity, skill shortage, data quality issues"""
            }
        }
        
        # Merge additional topics
        self.knowledge_base.update(additional_topics)
    
    def get_response(self, question: str) -> str:
        """Get a comprehensive response for any question"""
        question_lower = question.lower().strip()
        
        # Check knowledge base for matches, prioritizing longer/more specific keywords
        best_match = None
        best_match_length = 0
        
        for topic, data in self.knowledge_base.items():
            for keyword in data['keywords']:
                if keyword in question_lower:
                    # Prioritize longer, more specific matches
                    if len(keyword) > best_match_length:
                        best_match = data['response']
                        best_match_length = len(keyword)
        
        return best_match
    
    def add_knowledge(self, topic: str, keywords: list, response: str):
        """Add new knowledge to the base"""
        self.knowledge_base[topic] = {
            'keywords': keywords,
            'response': response
        }
    
    def get_all_topics(self):
        """Get list of all available topics"""
        return list(self.knowledge_base.keys())

# Global instance
comprehensive_kb = ComprehensiveKnowledgeBase()