import { useState, useEffect, useRef } from 'react'
import { useAuth } from '../contexts/AuthContext'
import Navigation from './Navigation'
import LoadingSpinner from './LoadingSpinner'
import PageWrapper from './PageWrapper'
import SectionWrapper from './SectionWrapper'
import { InterviewHeader } from './HeaderVariants'
import InterviewChatbot from './InterviewChatbot'
import AIInterviewAssistant from './AIInterviewAssistant'

const InterviewMode = () => {
  const { analyzeInterview } = useAuth()
  const [questions, setQuestions] = useState([])
  const [categories, setCategories] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('general')
  const [selectedQuestion, setSelectedQuestion] = useState('')
  const [audioFile, setAudioFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState(null)
  const [error, setError] = useState('')
  
  // Recording state
  const [isRecording, setIsRecording] = useState(false)
  const [recordedBlob, setRecordedBlob] = useState(null)
  const [recordingTime, setRecordingTime] = useState(0)
  const mediaRecorderRef = useRef(null)
  const streamRef = useRef(null)
  const timerRef = useRef(null)

  // Interview questions data
  const interviewQuestions = {
    general: [
      "Tell me about yourself.",
      "Why are you interested in this position?",
      "What are your greatest strengths and weaknesses?",
      "Where do you see yourself in 5 years?",
      "Why should we hire you?"
    ],
    behavioral: [
      "Describe a challenging situation you faced and how you handled it.",
      "Tell me about a time when you had to work with a difficult team member.",
      "Give me an example of a goal you reached and tell me how you achieved it.",
      "Describe a time when you had to learn something new quickly.",
      "Tell me about a mistake you made and how you handled it."
    ],
    technical: [
      "Walk me through your problem-solving process.",
      "How do you stay updated with industry trends?",
      "Describe a complex project you worked on.",
      "How do you handle tight deadlines?",
      "What tools and technologies are you most comfortable with?"
    ],
    situational: [
      "How would you handle a disagreement with your supervisor?",
      "What would you do if you were assigned a task you've never done before?",
      "How would you prioritize multiple urgent tasks?",
      "What would you do if you noticed a colleague making a mistake?",
      "How would you handle receiving constructive criticism?"
    ]
  }

  useEffect(() => {
    setCategories(Object.keys(interviewQuestions))
    setQuestions(interviewQuestions[selectedCategory])
    setSelectedQuestion(interviewQuestions[selectedCategory][0])
  }, [selectedCategory])

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      streamRef.current = stream
      
      const mediaRecorder = new MediaRecorder(stream)
      mediaRecorderRef.current = mediaRecorder
      
      const chunks = []
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data)
        }
      }
      
      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: 'audio/webm' })
        setRecordedBlob(blob)
        
        // Create a file from the blob
        const file = new File([blob], 'interview-answer.webm', { type: 'audio/webm' })
        setAudioFile(file)
        
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
      }
      
      mediaRecorder.start()
      setIsRecording(true)
      setRecordingTime(0)
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1)
      }, 1000)
      
    } catch (error) {
      setError('Could not access microphone. Please check permissions.')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      
      if (timerRef.current) {
        clearInterval(timerRef.current)
      }
    }
  }

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleCategoryChange = (category) => {
    setSelectedCategory(category)
    setQuestions(interviewQuestions[category])
    setSelectedQuestion(interviewQuestions[category][0])
    resetAnalysis()
  }

  const handleQuestionChange = (question) => {
    setSelectedQuestion(question)
    resetAnalysis()
  }

  const handleAudioChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setAudioFile(file)
      setError('')
    }
  }

  const resetAnalysis = () => {
    setAnalysis(null)
    setError('')
  }

  const resetForm = () => {
    setAudioFile(null)
    setAnalysis(null)
    setError('')
    setRecordedBlob(null)
    setRecordingTime(0)
    
    // Stop recording if active
    if (isRecording) {
      stopRecording()
    }
    
    const audioInput = document.getElementById('audio-input')
    if (audioInput) audioInput.value = ''
  }

  const handleAnalyze = async () => {
    if (!audioFile) {
      setError('Please select an audio file')
      return
    }

    if (!selectedQuestion) {
      setError('Please select a question')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis(null)

    const formData = new FormData()
    formData.append('audio_file', audioFile)
    formData.append('question', selectedQuestion)
    formData.append('category', selectedCategory)

    const result = await analyzeInterview(formData)
    
    if (result.success) {
      setAnalysis(result.data.analysis)
    } else {
      setError(result.error || 'Analysis failed')
    }
    
    setLoading(false)
  }

  const getRelevanceColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    if (score >= 40) return 'text-orange-600'
    return 'text-red-600'
  }

  const getRelevanceBg = (score) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    if (score >= 40) return 'bg-orange-100'
    return 'bg-red-100'
  }

  const getClassificationColor = (classification) => {
    switch (classification) {
      case 'highly_relevant': return 'text-green-600'
      case 'relevant': return 'text-blue-600'
      case 'partially_relevant': return 'text-yellow-600'
      case 'somewhat_relevant': return 'text-orange-600'
      case 'not_relevant': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  return (
    <PageWrapper className="min-h-screen">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Enhanced Header */}
        <SectionWrapper index={0}>
          <InterviewHeader selectedCategory={selectedCategory} className="mb-6" />
        </SectionWrapper>

        {/* Question Selection */}
        <SectionWrapper index={1}>
          <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Select Interview Question</h2>
          
          <div className="space-y-6">
            {/* Category Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Question Category</label>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => handleCategoryChange(category)}
                    className={`p-3 rounded-xl font-medium transition-all duration-300 hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.02] active:scale-[0.98] active:translate-y-0 ${
                      selectedCategory === category
                        ? 'bg-indigo-500 text-white shadow-lg'
                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                    }`}
                  >
                    {category.charAt(0).toUpperCase() + category.slice(1)}
                  </button>
                ))}
              </div>
            </div>

            {/* Question Selection */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-3">Interview Question</label>
              <select
                value={selectedQuestion}
                onChange={(e) => handleQuestionChange(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              >
                {questions.map((question, index) => (
                  <option key={index} value={question}>
                    {question}
                  </option>
                ))}
              </select>
            </div>

            {/* Selected Question Display */}
            <div className="p-4 bg-indigo-50 rounded-xl border-l-4 border-indigo-500">
              <h3 className="font-semibold text-indigo-800 mb-2">Selected Question:</h3>
              <p className="text-indigo-700">{selectedQuestion}</p>
            </div>
          </div>
          </div>
        </SectionWrapper>

        {/* Audio Upload */}
        <SectionWrapper index={2}>
          <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Record Your Answer</h2>
          
          <div className="space-y-6">
            {/* Recording Section */}
            <div className="p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border-2 border-dashed border-purple-300">
              <h3 className="text-lg font-semibold text-purple-800 mb-4">🎤 Record Your Answer</h3>
              
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-4">
                  {!isRecording ? (
                    <button
                      onClick={startRecording}
                      disabled={!selectedQuestion}
                      className="flex items-center px-6 py-3 bg-gradient-to-r from-red-500 to-pink-600 text-white rounded-xl font-semibold hover:from-red-600 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
                    >
                      <span className="w-3 h-3 bg-white rounded-full mr-2"></span>
                      Start Recording
                    </button>
                  ) : (
                    <button
                      onClick={stopRecording}
                      className="flex items-center px-6 py-3 bg-gradient-to-r from-gray-500 to-gray-600 text-white rounded-xl font-semibold hover:from-gray-600 hover:to-gray-700 transition-all duration-300"
                    >
                      <span className="w-3 h-3 bg-white rounded-sm mr-2"></span>
                      Stop Recording
                    </button>
                  )}
                  
                  {isRecording && (
                    <div className="flex items-center text-red-600">
                      <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse mr-2"></div>
                      <span className="font-mono text-lg">{formatTime(recordingTime)}</span>
                    </div>
                  )}
                </div>
                
                {recordedBlob && !isRecording && (
                  <div className="text-green-600 font-medium">
                    ✅ Answer recorded ({formatTime(recordingTime)})
                  </div>
                )}
              </div>
              
              <p className="text-sm text-purple-600">
                Think about your answer to the question above, then click "Start Recording" to record your response.
              </p>
            </div>

            {/* Divider */}
            <div className="flex items-center">
              <div className="flex-1 border-t border-gray-300"></div>
              <span className="px-4 text-gray-500 font-medium">OR</span>
              <div className="flex-1 border-t border-gray-300"></div>
            </div>

            {/* Audio File Input */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Upload Audio File
              </label>
              <input
                id="audio-input"
                type="file"
                accept="audio/*"
                onChange={handleAudioChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Supported formats: WAV, MP3, M4A, FLAC, WebM
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleAnalyze}
                disabled={loading || !audioFile || !selectedQuestion}
                className="px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-600 text-white rounded-xl font-semibold hover:from-purple-600 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
              >
                {loading ? 'Analyzing...' : 'Analyze Answer'}
              </button>
              
              <button
                onClick={resetForm}
                className="px-6 py-3 bg-gray-200 text-gray-700 rounded-xl font-semibold hover:bg-gray-300 transition-all duration-300"
              >
                Reset
              </button>
            </div>
          </div>

          {/* Error Display */}
          {error && (
            <div className="mt-6 p-4 bg-red-50 border border-red-200 rounded-xl">
              <p className="text-red-700">{error}</p>
            </div>
          )}
          </div>
        </SectionWrapper>

        {/* Loading */}
        {loading && (
          <SectionWrapper index={3}>
            <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
            <LoadingSpinner />
            <p className="text-center text-gray-600 mt-4">
              Analyzing your interview answer... This includes relevance analysis and speech metrics.
            </p>
            </div>
          </SectionWrapper>
        )}

        {/* Analysis Results */}
        {analysis && (
          <SectionWrapper index={3}>
            <div className="space-y-6">
            {/* Question and Answer Overview */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Interview Analysis</h2>
              
              <div className="grid md:grid-cols-2 gap-6 mb-6">
                <div className="p-4 bg-purple-50 rounded-xl">
                  <h3 className="font-semibold text-purple-800 mb-2">Question Asked:</h3>
                  <p className="text-gray-700">{analysis.question}</p>
                  <p className="text-sm text-purple-600 mt-2">Category: {analysis.category}</p>
                </div>
                
                <div className="p-4 bg-blue-50 rounded-xl">
                  <h3 className="font-semibold text-blue-800 mb-2">Your Answer:</h3>
                  <p className="text-gray-700 text-sm leading-relaxed">{analysis.transcript}</p>
                  <p className="text-sm text-blue-600 mt-2">Duration: {analysis.duration?.toFixed(1)}s</p>
                </div>
              </div>
            </div>

            {/* Relevance Analysis - Most Important */}
            {analysis.relevance_analysis && (
              <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
                <h2 className="text-2xl font-bold text-purple-600 mb-6">🎯 Answer Relevance Analysis</h2>
                
                <div className="grid md:grid-cols-3 gap-6 mb-6">
                  <div className={`p-6 rounded-xl ${getRelevanceBg(analysis.relevance_analysis.score)} hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-250 ease-out group`}>
                    <div className="text-center">
                      <div className={`text-4xl font-bold ${getRelevanceColor(analysis.relevance_analysis.score)} group-hover:scale-105 transition-transform duration-200`}>
                        {analysis.relevance_analysis.score.toFixed(1)}%
                      </div>
                      <div className="text-sm text-gray-600 mt-2">Relevance Score</div>
                    </div>
                  </div>
                  
                  <div className="p-6 bg-indigo-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-indigo-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="text-center">
                      <div className={`text-lg font-bold ${getClassificationColor(analysis.relevance_analysis.classification)} group-hover:scale-105 transition-transform duration-200`}>
                        {analysis.relevance_analysis.classification.replace('_', ' ').toUpperCase()}
                      </div>
                      <div className="text-sm text-gray-600 mt-2">Classification</div>
                    </div>
                  </div>
                  
                  <div className="p-6 bg-green-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-green-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="text-center">
                      <div className="text-lg font-bold text-green-600 group-hover:scale-105 transition-transform duration-200">
                        {analysis.relevance_analysis.question_type.replace('_', ' ').toUpperCase()}
                      </div>
                      <div className="text-sm text-gray-600 mt-2">Question Type</div>
                    </div>
                  </div>
                </div>

                {/* Relevance Feedback */}
                <div className="space-y-4">
                  <div className="p-4 bg-blue-50 rounded-xl">
                    <h4 className="font-semibold text-blue-800 mb-2">Summary:</h4>
                    <p className="text-gray-700">{analysis.relevance_analysis.feedback.summary}</p>
                  </div>

                  {analysis.relevance_analysis.feedback.strengths.length > 0 && (
                    <div className="p-4 bg-green-50 rounded-xl">
                      <h4 className="font-semibold text-green-800 mb-2">✅ Relevance Strengths:</h4>
                      <ul className="space-y-1">
                        {analysis.relevance_analysis.feedback.strengths.map((strength, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-green-500 mr-2">•</span>
                            <span className="text-gray-700">{strength}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {analysis.relevance_analysis.feedback.improvements.length > 0 && (
                    <div className="p-4 bg-orange-50 rounded-xl">
                      <h4 className="font-semibold text-orange-800 mb-2">🎯 Relevance Improvements:</h4>
                      <ul className="space-y-1">
                        {analysis.relevance_analysis.feedback.improvements.map((improvement, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-orange-500 mr-2">•</span>
                            <span className="text-gray-700">{improvement}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {analysis.relevance_analysis.feedback.suggestions.length > 0 && (
                    <div className="p-4 bg-purple-50 rounded-xl">
                      <h4 className="font-semibold text-purple-800 mb-2">💡 Specific Suggestions:</h4>
                      <ul className="space-y-1">
                        {analysis.relevance_analysis.feedback.suggestions.map((suggestion, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-purple-500 mr-2">•</span>
                            <span className="text-gray-700">{suggestion}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Speech Metrics */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">📊 Speech Metrics</h2>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="p-4 bg-blue-50 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:bg-blue-25 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer">
                  <div className="text-2xl font-bold text-blue-600 group-hover:scale-105 transition-transform duration-200">{analysis.metrics.wpm}</div>
                  <div className="text-sm text-gray-600">Words/Min</div>
                </div>
                
                <div className="p-4 bg-yellow-50 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:bg-yellow-25 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer">
                  <div className="text-2xl font-bold text-yellow-600 group-hover:scale-105 transition-transform duration-200">{analysis.metrics.fillers}</div>
                  <div className="text-sm text-gray-600">Filler Words</div>
                </div>
                
                <div className="p-4 bg-green-50 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:bg-green-25 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer">
                  <div className="text-2xl font-bold text-green-600 group-hover:scale-105 transition-transform duration-200">{analysis.confidence}%</div>
                  <div className="text-sm text-gray-600">Confidence</div>
                </div>
                
                <div className="p-4 bg-purple-50 rounded-xl text-center hover:shadow-md hover:-translate-y-0.5 hover:bg-purple-25 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer">
                  <div className="text-2xl font-bold text-purple-600 group-hover:scale-105 transition-transform duration-200">{analysis.emotion}</div>
                  <div className="text-sm text-gray-600">Emotion</div>
                </div>
              </div>
            </div>

            {/* Interview-Specific Feedback */}
            {analysis.interview_feedback && (
              <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
                <h2 className="text-2xl font-bold text-indigo-600 mb-6">💼 Interview Feedback</h2>
                
                {analysis.interview_feedback.specific_tips && analysis.interview_feedback.specific_tips.length > 0 && (
                  <div className="p-4 bg-indigo-50 rounded-xl">
                    <h4 className="font-semibold text-indigo-800 mb-3">Interview Tips:</h4>
                    <ul className="space-y-2">
                      {analysis.interview_feedback.specific_tips.map((tip, index) => (
                        <li key={index} className="flex items-start">
                          <span className="text-indigo-500 mr-2">•</span>
                          <span className="text-gray-700">{tip}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}

            {/* Emotion Analysis */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h2 className="text-2xl font-bold text-pink-600 mb-6">😊 Emotional Analysis</h2>
              <div className="p-4 bg-pink-50 rounded-xl">
                <div className="flex items-center justify-between mb-2">
                  <span className="font-semibold text-pink-800">Detected Emotion:</span>
                  <span className="font-bold text-pink-600">{analysis.emotion}</span>
                </div>
                <p className="text-gray-700">{analysis.emotion_feedback}</p>
              </div>
            </div>
            </div>
          </SectionWrapper>
        )}
      </div>

      {/* Personal Interview Chatbot */}
      <InterviewChatbot
        selectedCategory={selectedCategory}
        selectedQuestion={selectedQuestion}
        isRecording={isRecording}
        recordingTime={recordingTime}
        analysis={analysis}
        loading={loading}
      />

      {/* AI Interview Assistant */}
      <AIInterviewAssistant />
    </PageWrapper>
  )
}

export default InterviewMode