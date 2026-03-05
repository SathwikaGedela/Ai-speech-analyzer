import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'

const AIInterviewAssistant = () => {
  const [isOpen, setIsOpen] = useState(false)
  const [activeTab, setActiveTab] = useState('practice')
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [practiceQuestions, setPracticeQuestions] = useState([])
  const [tips, setTips] = useState({})
  const [jobRole, setJobRole] = useState('')
  const [company, setCompany] = useState('')
  const [modelInfo, setModelInfo] = useState(null)
  const answerRef = useRef(null)

  // Fetch practice questions and tips on component mount
  useEffect(() => {
    if (isOpen) {
      fetchPracticeQuestions()
      fetchTips()
      fetchModelInfo()
    }
  }, [isOpen])

  const fetchModelInfo = async () => {
    try {
      const response = await fetch('http://localhost:5000/ai-assistant/model-info', {
        credentials: 'include'
      })
      const data = await response.json()
      if (data.success) {
        setModelInfo(data.model_info)
      }
    } catch (error) {
      console.error('Error fetching model info:', error)
    }
  }

  const fetchPracticeQuestions = async () => {
    try {
      const response = await fetch('http://localhost:5000/ai-assistant/practice-questions', {
        credentials: 'include'
      })
      const data = await response.json()
      if (data.success) {
        setPracticeQuestions(data.practice_questions)
      }
    } catch (error) {
      console.error('Error fetching practice questions:', error)
    }
  }

  const fetchTips = async () => {
    try {
      const response = await fetch('http://localhost:5000/ai-assistant/tips', {
        credentials: 'include'
      })
      const data = await response.json()
      if (data.success) {
        setTips(data.tips)
      }
    } catch (error) {
      console.error('Error fetching tips:', error)
    }
  }

  const handleGetAnswer = async () => {
    if (!question.trim()) return

    setIsLoading(true)
    setAnswer('')

    try {
      const response = await fetch('http://localhost:5000/ai-assistant/answer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          question: question.trim(),
          job_role: jobRole.trim(),
          company: company.trim()
        })
      })

      const data = await response.json()
      
      if (data.success) {
        setAnswer(data.answer)
        setModelInfo(data.model_info) // Update model info from response
        // Scroll to answer
        setTimeout(() => {
          answerRef.current?.scrollIntoView({ behavior: 'smooth' })
        }, 100)
      } else {
        setAnswer('Sorry, I could not generate an answer at this time. Please try again.')
      }
    } catch (error) {
      console.error('Error getting AI answer:', error)
      setAnswer('Sorry, there was an error connecting to the AI assistant. Please try again.')
    } finally {
      setIsLoading(false)
    }
  }

  const handleQuestionSelect = (selectedQuestion) => {
    setQuestion(selectedQuestion)
    setActiveTab('practice')
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleGetAnswer()
    }
  }

  return (
    <>
      {/* Toggle Button */}
      <motion.button
        onClick={() => setIsOpen(!isOpen)}
        className={`fixed bottom-6 left-6 z-50 w-16 h-16 rounded-full shadow-lg flex items-center justify-center text-white font-bold text-xl transition-all duration-300 ${
          isOpen 
            ? 'bg-gradient-to-r from-red-500 to-pink-600 hover:from-red-600 hover:to-pink-700' 
            : modelInfo?.ai_powered 
              ? 'bg-gradient-to-r from-green-500 to-blue-600 hover:from-green-600 hover:to-blue-700'
              : 'bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700'
        }`}
        whileHover={{ scale: 1.1 }}
        whileTap={{ scale: 0.9 }}
        animate={{ 
          rotate: isOpen ? 45 : 0,
          scale: isOpen ? 1.1 : 1
        }}
        title={modelInfo?.ai_powered ? "Real AI Assistant" : "AI Assistant"}
      >
        {isOpen ? '×' : '🤖'}
      </motion.button>

      {/* AI Assistant Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 left-6 z-40 w-[500px] h-[600px] bg-white rounded-2xl shadow-2xl border border-gray-200 flex flex-col overflow-hidden"
            initial={{ opacity: 0, scale: 0.8, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.8, y: 20 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-blue-500 to-indigo-600 text-white p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <div className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center mr-3">
                    🤖
                  </div>
                  <div>
                    <h3 className="font-semibold">Real AI Interview Assistant</h3>
                    <p className="text-xs opacity-90">
                      {modelInfo?.ai_powered ? 
                        `Powered by ${modelInfo.model_name?.split('/').pop() || 'AI Model'}` : 
                        'AI-powered responses'
                      }
                    </p>
                  </div>
                </div>
                <div className={`w-3 h-3 rounded-full animate-pulse ${
                  modelInfo?.ai_powered ? 'bg-green-400' : 'bg-yellow-400'
                }`}></div>
              </div>
            </div>

            {/* Tabs */}
            <div className="flex border-b border-gray-200">
              <button
                onClick={() => setActiveTab('practice')}
                className={`flex-1 py-3 px-4 text-sm font-medium transition-colors ${
                  activeTab === 'practice'
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Practice
              </button>
              <button
                onClick={() => setActiveTab('questions')}
                className={`flex-1 py-3 px-4 text-sm font-medium transition-colors ${
                  activeTab === 'questions'
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Questions
              </button>
              <button
                onClick={() => setActiveTab('tips')}
                className={`flex-1 py-3 px-4 text-sm font-medium transition-colors ${
                  activeTab === 'tips'
                    ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Tips
              </button>
            </div>

            {/* Content */}
            <div className="flex-1 overflow-y-auto p-4">
              {/* Practice Tab */}
              {activeTab === 'practice' && (
                <div className="space-y-4">
                  {/* Context Inputs */}
                  <div className="grid grid-cols-2 gap-3">
                    <input
                      type="text"
                      placeholder="Job Role (optional)"
                      value={jobRole}
                      onChange={(e) => setJobRole(e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <input
                      type="text"
                      placeholder="Company (optional)"
                      value={company}
                      onChange={(e) => setCompany(e.target.value)}
                      className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>

                  {/* Question Input */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Interview Question
                    </label>
                    <textarea
                      value={question}
                      onChange={(e) => setQuestion(e.target.value)}
                      onKeyPress={handleKeyPress}
                      placeholder="Enter an interview question..."
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                      rows="3"
                    />
                  </div>

                  {/* Get Answer Button */}
                  <button
                    onClick={handleGetAnswer}
                    disabled={!question.trim() || isLoading}
                    className="w-full bg-blue-500 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center">
                        <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                        Generating Answer...
                      </div>
                    ) : (
                      'Get AI Answer'
                    )}
                  </button>

                  {/* Answer Display */}
                  {answer && (
                    <div ref={answerRef} className="mt-4">
                      <label className="block text-sm font-medium text-gray-700 mb-2">
                        AI-Generated Answer
                      </label>
                      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                        <p className="text-sm text-gray-800 leading-relaxed whitespace-pre-wrap">
                          {answer}
                        </p>
                        {modelInfo && (
                          <div className="mt-3 pt-3 border-t border-gray-200">
                            <div className="flex items-center justify-between text-xs text-gray-500">
                              <span>
                                {modelInfo.ai_powered ? 
                                  `🤖 Generated by ${modelInfo.model_name?.split('/').pop() || 'AI Model'}` : 
                                  '📝 Rule-based response'
                                }
                              </span>
                              <span>{modelInfo.device || 'CPU'}</span>
                            </div>
                          </div>
                        )}
                      </div>
                      <p className="text-xs text-gray-500 mt-2">
                        💡 Use this as inspiration for your own answer. Practice speaking it out loud!
                      </p>
                    </div>
                  )}
                </div>
              )}

              {/* Questions Tab */}
              {activeTab === 'questions' && (
                <div className="space-y-4">
                  {practiceQuestions.map((category, index) => (
                    <div key={index}>
                      <h4 className="font-semibold text-gray-800 mb-2">{category.category}</h4>
                      <div className="space-y-2">
                        {category.questions.map((q, qIndex) => (
                          <button
                            key={qIndex}
                            onClick={() => handleQuestionSelect(q)}
                            className="w-full text-left p-3 bg-gray-50 hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-lg text-sm transition-colors"
                          >
                            {q}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Tips Tab */}
              {activeTab === 'tips' && (
                <div className="space-y-4">
                  {Object.entries(tips).map(([category, tipList]) => (
                    <div key={category}>
                      <h4 className="font-semibold text-gray-800 mb-2 capitalize">
                        {category.replace('_', ' ')}
                      </h4>
                      <ul className="space-y-2">
                        {tipList.map((tip, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-blue-500 mr-2 mt-1">•</span>
                            <span className="text-sm text-gray-700">{tip}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

export default AIInterviewAssistant