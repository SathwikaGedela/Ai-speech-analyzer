import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const InterviewChatbot = ({ 
  selectedCategory, 
  selectedQuestion, 
  isRecording, 
  recordingTime, 
  analysis, 
  loading 
}) => {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isTyping, setIsTyping] = useState(false)
  const messagesEndRef = useRef(null)

  // Initial welcome message
  useEffect(() => {
    const welcomeMessage = {
      id: Date.now(),
      text: "Hi! I'm your personal interview coach 🎯 I'm here to help you practice and improve your interview skills. Ask me anything about interviews or let me guide you through the process!",
      sender: 'bot',
      timestamp: new Date()
    }
    setMessages([welcomeMessage])
  }, [])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Contextual tips based on interview state
  useEffect(() => {
    if (selectedQuestion && messages.length === 1) {
      setTimeout(() => {
        addBotMessage(`Great choice! You've selected a ${selectedCategory} question. Here's a quick tip: Take a moment to structure your answer using the STAR method (Situation, Task, Action, Result) for behavioral questions, or be specific and concise for general questions.`)
      }, 2000)
    }
  }, [selectedQuestion, selectedCategory])

  useEffect(() => {
    if (isRecording && recordingTime === 5) {
      addBotMessage("You're doing great! Remember to speak clearly and at a steady pace. Take your time to think through your answer.")
    }
    if (isRecording && recordingTime === 30) {
      addBotMessage("Good progress! Try to wrap up your main points soon. Most interview answers should be 1-2 minutes long.")
    }
    if (isRecording && recordingTime === 60) {
      addBotMessage("Consider concluding your answer soon. You want to be thorough but concise!")
    }
  }, [isRecording, recordingTime])

  useEffect(() => {
    if (analysis) {
      setTimeout(() => {
        const relevanceScore = analysis.relevance_analysis?.score || 0
        let message = ""
        
        if (relevanceScore >= 80) {
          message = "Excellent work! 🎉 Your answer was highly relevant and well-structured. "
        } else if (relevanceScore >= 60) {
          message = "Good job! 👍 Your answer addressed the question well. "
        } else if (relevanceScore >= 40) {
          message = "Not bad! 🤔 Your answer partially addressed the question. "
        } else {
          message = "Let's work on this together! 💪 Your answer could be more focused on the question. "
        }

        if (analysis.confidence < 60) {
          message += "Try to speak with more confidence - you know more than you think!"
        }
        if (analysis.metrics?.fillers > 5) {
          message += " Also, try to reduce filler words like 'um' and 'uh' by pausing instead."
        }

        addBotMessage(message)
      }, 1000)
    }
  }, [analysis])

  const addBotMessage = (text) => {
    setIsTyping(true)
    setTimeout(() => {
      const newMessage = {
        id: Date.now(),
        text,
        sender: 'bot',
        timestamp: new Date()
      }
      setMessages(prev => [...prev, newMessage])
      setIsTyping(false)
    }, 1000)
  }

  const addUserMessage = (text) => {
    const newMessage = {
      id: Date.now(),
      text,
      sender: 'user',
      timestamp: new Date()
    }
    setMessages(prev => [...prev, newMessage])
  }

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return

    addUserMessage(inputMessage)
    const userMsg = inputMessage
    setInputMessage('')
    setIsTyping(true)

    try {
      // Send message to backend chatbot API
      const response = await fetch('http://localhost:5000/interview/chatbot', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          message: userMsg,
          context: {
            selected_category: selectedCategory,
            selected_question: selectedQuestion,
            session_stage: isRecording ? 'practicing' : (analysis ? 'completed' : 'initial')
          }
        })
      })

      const data = await response.json()
      
      if (data.success) {
        setTimeout(() => {
          const botMessage = {
            id: Date.now(),
            text: data.response,
            sender: 'bot',
            timestamp: new Date()
          }
          setMessages(prev => [...prev, botMessage])
          setIsTyping(false)
        }, 1000)
      } else {
        // Fallback to local responses if API fails
        setTimeout(() => {
          const fallbackResponse = getFallbackResponse(userMsg.toLowerCase())
          const botMessage = {
            id: Date.now(),
            text: fallbackResponse,
            sender: 'bot',
            timestamp: new Date()
          }
          setMessages(prev => [...prev, botMessage])
          setIsTyping(false)
        }, 1000)
      }
    } catch (error) {
      console.error('Chatbot API error:', error)
      // Fallback to local responses
      setTimeout(() => {
        const fallbackResponse = getFallbackResponse(userMsg.toLowerCase())
        const botMessage = {
          id: Date.now(),
          text: fallbackResponse,
          sender: 'bot',
          timestamp: new Date()
        }
        setMessages(prev => [...prev, botMessage])
        setIsTyping(false)
      }, 1000)
    }
  }

  const getFallbackResponse = (userMsg) => {
    // More direct, helpful fallback responses when API is unavailable
    if (userMsg.includes('nervous') || userMsg.includes('anxiety') || userMsg.includes('scared')) {
      return "Here are proven techniques to manage interview nerves:\n\n• **Deep breathing**: 4 counts in, hold for 4, out for 4\n• **Power posing**: Stand confidently for 2 minutes beforehand\n• **Positive visualization**: Imagine the interview going well\n• **Preparation**: Practice answers to reduce uncertainty\n• **Reframe nerves**: They show you care about the opportunity!\n\nRemember: The interviewer wants you to succeed!"
    } else if (userMsg.includes('star') || userMsg.includes('method')) {
      return "The STAR method for behavioral questions:\n\n**S**ituation: Set the context (2-3 sentences)\n**T**ask: What you needed to accomplish\n**A**ction: Specific steps YOU took (most important)\n**R**esult: Positive outcome and lessons learned\n\nKeep it to 90-120 seconds and focus on YOUR actions, not what the team did."
    } else if (userMsg.includes('confidence') || userMsg.includes('confident')) {
      return "Build interview confidence with these strategies:\n\n• **Prepare thoroughly**: Research company and practice answers\n• **Record yourself**: Listen back to improve delivery\n• **Use confident body language**: Sit up straight, make eye contact\n• **Speak slowly**: Shows thoughtfulness and control\n• **Prepare examples**: Have 5-7 STAR stories ready\n• **Remember your worth**: You earned this interview!"
    } else if (userMsg.includes('weakness') || userMsg.includes('weaknesses')) {
      return "How to handle the weakness question:\n\n• **Choose wisely**: Pick something real but not job-critical\n• **Show growth**: Explain how you're actively improving\n• **Give examples**: Share specific steps you've taken\n• **Stay positive**: Frame it as learning and development\n\n**Example**: 'I used to struggle with public speaking, so I joined Toastmasters and now regularly present to large groups.'"
    } else if (userMsg.includes('salary') || userMsg.includes('money') || userMsg.includes('pay')) {
      return "Salary negotiation strategy:\n\n• **Research first**: Know the market rate for your role\n• **Let them lead**: Try to let employer bring it up first\n• **Give a range**: Based on research, not current salary\n• **Consider total package**: Benefits, growth, work-life balance\n• **Stay flexible**: Show openness to discussion\n\n**Script**: 'Based on my research, I'm looking for $X-Y range, but I'm open to discussing the complete package.'"
    } else if (userMsg.includes('question') || userMsg.includes('ask')) {
      return "Great questions to ask interviewers:\n\n**About the role**:\n• What does success look like in this position?\n• What are the biggest challenges facing the team?\n• How would you describe the team dynamics?\n\n**About growth**:\n• What opportunities exist for professional development?\n• How do you support career advancement?\n\n**About culture**:\n• How would you describe the company culture?\n• What do you enjoy most about working here?"
    } else if (userMsg.includes('tell me about yourself') || userMsg.includes('introduce')) {
      return "Structure for 'Tell me about yourself':\n\n**Present** (30 seconds): Current role and key skills\n**Past** (30 seconds): Relevant experience that led you here\n**Future** (30 seconds): Why you're excited about this opportunity\n\n**Example**: 'I'm currently a [role] with [X years] experience in [field]. Previously, I [achievement]. I'm excited about this role because [connection to company].'\n\nKeep it to 90 seconds max!"
    } else if (userMsg.includes('help') || userMsg.includes('tip') || userMsg.includes('advice')) {
      return "Top interview success tips:\n\n• **Be specific**: Use concrete examples and numbers\n• **Show enthusiasm**: Let genuine interest shine through\n• **Listen actively**: Understand the question before answering\n• **Stay positive**: Even when discussing challenges\n• **Follow up**: Send thank-you email within 24 hours\n• **Be authentic**: Genuine personality beats perfection"
    } else {
      const directResponses = [
        "Here's my advice: Focus on preparing 5-7 strong examples using the STAR method. This gives you material for most behavioral questions.",
        "Key tip: Research the company thoroughly and prepare 3-5 thoughtful questions to ask them. This shows genuine interest.",
        "Remember: Practice your answers out loud, not just in your head. Speaking responses helps you sound natural and confident.",
        "Focus on being specific in your answers. Instead of 'I'm a good leader,' tell a story that demonstrates leadership with results.",
        "The interviewer wants you to succeed! They're evaluating fit, not trying to trick you. Be yourself and show your value."
      ]
      return directResponses[Math.floor(Math.random() * directResponses.length)]
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSendMessage()
    }
  }

  const quickTips = [
    "How to use the STAR method?",
    "Tips for managing nerves?",
    "How to discuss weaknesses?",
    "What questions should I ask?",
    "How to show confidence?",
    "Tell me about yourself structure?"
  ]

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <>
      {/* Chatbot Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 right-6 z-50 w-16 h-16 rounded-full shadow-lg flex items-center justify-center text-white font-bold text-xl transition-all duration-300 ${
          isOpen 
            ? 'bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700' 
            : 'bg-gradient-to-r from-purple-500 to-pink-600 hover:from-purple-600 hover:to-pink-700'
        }`}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        animate={{ 
          rotate: isOpen ? 45 : 0,
          scale: isOpen ? 1.1 : 1
        }}
      >
        {isOpen ? '×' : '🤖'}
      </motion.button>

      {/* Notification Badge */}
      {!isOpen && messages.length > 1 && (
        <motion.div
          className="fixed bottom-20 right-6 z-40 bg-red-500 text-white text-xs rounded-full w-6 h-6 flex items-center justify-center font-bold"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          exit={{ scale: 0 }}
        >
          {messages.filter(m => m.sender === 'bot').length}
        </motion.div>
      )}

      {/* Chatbot Window */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 right-6 z-40 w-96 h-96 bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden"
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-purple-500 to-pink-600 text-white p-4 flex items-center justify-between">
              <div className="flex items-center">
                <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center mr-3">
                  🎯
                </div>
                <div>
                  <h3 className="font-semibold">Interview Coach</h3>
                  <p className="text-xs opacity-90">Your personal AI assistant</p>
                </div>
              </div>
              <div className="w-3 h-3 bg-green-400 rounded-full animate-pulse"></div>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.map((message) => (
                <motion.div
                  key={message.id}
                  className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3 }}
                >
                  <div
                    className={`max-w-xs px-3 py-2 rounded-2xl text-sm ${
                      message.sender === 'user'
                        ? 'bg-purple-500 text-white rounded-br-md'
                        : 'bg-gray-100 text-gray-800 rounded-bl-md'
                    }`}
                  >
                    <p>{message.text}</p>
                    <p className={`text-xs mt-1 ${
                      message.sender === 'user' ? 'text-purple-200' : 'text-gray-500'
                    }`}>
                      {formatTime(message.timestamp)}
                    </p>
                  </div>
                </motion.div>
              ))}

              {/* Typing Indicator */}
              {isTyping && (
                <motion.div
                  className="flex justify-start"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                >
                  <div className="bg-gray-100 px-3 py-2 rounded-2xl rounded-bl-md">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                  </div>
                </motion.div>
              )}

              <div ref={messagesEndRef} />
            </div>

            {/* Quick Tips */}
            {messages.length <= 2 && (
              <div className="px-4 pb-2">
                <p className="text-xs text-gray-500 mb-2">Quick tips:</p>
                <div className="flex flex-wrap gap-1">
                  {quickTips.slice(0, 3).map((tip, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        setInputMessage(tip)
                        handleSendMessage()
                      }}
                      className="text-xs bg-purple-50 text-purple-600 px-2 py-1 rounded-full hover:bg-purple-100 transition-colors"
                    >
                      {tip}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input */}
            <div className="p-4 border-t border-gray-200">
              <div className="flex space-x-2">
                <input
                  type="text"
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask me anything about interviews..."
                  className="flex-1 px-3 py-2 border border-gray-300 rounded-full text-sm focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                />
                <button
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim()}
                  className="w-8 h-8 bg-purple-500 text-white rounded-full flex items-center justify-center hover:bg-purple-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

export default InterviewChatbot