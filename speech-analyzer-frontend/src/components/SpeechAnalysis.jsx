import { useState, useRef } from 'react'
import { useAuth } from '../contexts/AuthContext'
import Navigation from './Navigation'
import LoadingSpinner from './LoadingSpinner'
import PageWrapper from './PageWrapper'
import SectionWrapper from './SectionWrapper'
import { AnalysisHeader } from './HeaderVariants'

const SpeechAnalysis = () => {
  const { analyzeAudio } = useAuth()
  const [audioFile, setAudioFile] = useState(null)
  const [imageFile, setImageFile] = useState(null)
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
        const file = new File([blob], 'recorded-audio.webm', { type: 'audio/webm' })
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

  const handleAudioChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setAudioFile(file)
      setError('')
    }
  }

  const handleImageChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      setImageFile(file)
    }
  }

  const handleAnalyze = async () => {
    if (!audioFile) {
      setError('Please select an audio file')
      return
    }

    setLoading(true)
    setError('')
    setAnalysis(null)

    const formData = new FormData()
    formData.append('audio_file', audioFile)
    if (imageFile) {
      formData.append('image_file', imageFile)
    }

    const result = await analyzeAudio(formData)
    
    if (result.success) {
      setAnalysis(result.data.analysis)
    } else {
      setError(result.error || 'Analysis failed')
    }
    
    setLoading(false)
  }

  const resetForm = () => {
    setAudioFile(null)
    setImageFile(null)
    setAnalysis(null)
    setError('')
    setRecordedBlob(null)
    setRecordingTime(0)
    
    // Stop recording if active
    if (isRecording) {
      stopRecording()
    }
    
    // Reset file inputs
    const audioInput = document.getElementById('audio-input')
    const imageInput = document.getElementById('image-input')
    if (audioInput) audioInput.value = ''
    if (imageInput) imageInput.value = ''
  }

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBg = (score) => {
    if (score >= 80) return 'bg-green-100'
    if (score >= 60) return 'bg-yellow-100'
    return 'bg-red-100'
  }

  return (
    <PageWrapper className="min-h-screen">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Enhanced Header */}
        <SectionWrapper index={0}>
          <AnalysisHeader className="mb-6" />
        </SectionWrapper>

        {/* Upload Form */}
        <SectionWrapper index={1}>
          <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
          <h2 className="text-xl font-semibold text-gray-800 mb-6">Record or Upload Audio</h2>
          
          <div className="space-y-6">
            {/* Recording Section */}
            <div className="p-6 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border-2 border-dashed border-purple-300">
              <h3 className="text-lg font-semibold text-purple-800 mb-4">🎤 Record Audio</h3>
              
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-4">
                  {!isRecording ? (
                    <button
                      onClick={startRecording}
                      className="flex items-center px-6 py-3 bg-gradient-to-r from-red-500 to-pink-600 text-white rounded-xl font-semibold hover:from-red-600 hover:to-pink-700 transition-all duration-300"
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
                    ✅ Recording saved ({formatTime(recordingTime)})
                  </div>
                )}
              </div>
              
              <p className="text-sm text-purple-600">
                Click "Start Recording" to record your speech directly from your microphone.
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
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Supported formats: WAV, MP3, M4A, FLAC, WebM
              </p>
            </div>

            {/* Image File Input (Optional) */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Image File (Optional - for emotion detection)
              </label>
              <input
                id="image-input"
                type="file"
                accept="image/*"
                onChange={handleImageChange}
                className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-purple-50 file:text-purple-700 hover:file:bg-purple-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Upload a photo for enhanced emotion analysis
              </p>
            </div>

            {/* Action Buttons */}
            <div className="flex gap-4">
              <button
                onClick={handleAnalyze}
                disabled={loading || !audioFile}
                className="px-6 py-3 bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-xl font-semibold hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300"
              >
                {loading ? 'Analyzing...' : 'Analyze Speech'}
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
          <SectionWrapper index={2}>
            <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
            <LoadingSpinner />
            <p className="text-center text-gray-600 mt-4">
              Analyzing your speech... This may take a few moments.
            </p>
            </div>
          </SectionWrapper>
        )}

        {/* Analysis Results */}
        {analysis && (
          <SectionWrapper index={2}>
            <div className="space-y-6">
            {/* Overall Score */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Overall Analysis</h2>
              
              <div className="grid md:grid-cols-3 gap-6">
                <div className={`p-6 rounded-xl ${getScoreBg(analysis.overall_score.score)} hover:shadow-md hover:-translate-y-0.5 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer`}>
                  <div className="text-center">
                    <div className={`text-4xl font-bold ${getScoreColor(analysis.overall_score.score)} group-hover:scale-105 transition-transform duration-200`}>
                      {analysis.overall_score.score}%
                    </div>
                    <div className="text-sm text-gray-600 mt-2">Confidence Score</div>
                  </div>
                </div>
                
                <div className="p-6 bg-blue-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-blue-25 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-blue-600 group-hover:scale-105 transition-transform duration-200">
                      {analysis.overall_score.skill_level}
                    </div>
                    <div className="text-sm text-gray-600 mt-2">Skill Level</div>
                  </div>
                </div>
                
                <div className="p-6 bg-purple-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-purple-25 hover:scale-[1.01] transition-all duration-250 ease-out group cursor-pointer">
                  <div className="text-center">
                    <div className="text-lg font-semibold text-purple-600 group-hover:scale-105 transition-transform duration-200">
                      {analysis.emotion_analysis.detected_emotion}
                    </div>
                    <div className="text-sm text-gray-600 mt-2">Detected Emotion</div>
                  </div>
                </div>
              </div>
              
              <div className="mt-6 p-4 bg-gray-50 rounded-xl">
                <p className="text-gray-700 font-medium">General Impression:</p>
                <p className="text-gray-600 mt-1">{analysis.overall_score.general_impression}</p>
              </div>
            </div>

            {/* Transcript */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h3 className="text-xl font-bold text-gray-800 mb-4">Transcript</h3>
              <div className="p-4 bg-gray-50 rounded-xl">
                <p className="text-gray-700 leading-relaxed">{analysis.transcript}</p>
              </div>
            </div>

            {/* Detailed Metrics */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h3 className="text-xl font-bold text-gray-800 mb-6">Detailed Analysis</h3>
              
              <div className="grid md:grid-cols-2 gap-6">
                {/* Vocal Delivery */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-800">Vocal Delivery</h4>
                  
                  <div className="p-4 bg-blue-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-blue-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium group-hover:text-blue-800 transition-colors">Speaking Pace</span>
                      <span className="font-bold text-blue-600 group-hover:scale-105 transition-transform duration-200">{analysis.vocal_delivery.speaking_pace.wpm} WPM</span>
                    </div>
                    <p className="text-sm text-gray-600">{analysis.vocal_delivery.speaking_pace.assessment}</p>
                  </div>
                  
                  <div className="p-4 bg-yellow-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-yellow-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium group-hover:text-yellow-800 transition-colors">Filler Words</span>
                      <span className="font-bold text-yellow-600 group-hover:scale-105 transition-transform duration-200">{analysis.vocal_delivery.filler_words.total_count}</span>
                    </div>
                    <p className="text-sm text-gray-600">{analysis.vocal_delivery.filler_words.assessment}</p>
                  </div>
                  
                  <div className="p-4 bg-green-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-green-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium group-hover:text-green-800 transition-colors">Pronunciation</span>
                      <span className="font-bold text-green-600 group-hover:scale-105 transition-transform duration-200">{analysis.vocal_delivery.pronunciation.clarity_percentage}%</span>
                    </div>
                    <p className="text-sm text-gray-600">{analysis.vocal_delivery.pronunciation.assessment}</p>
                  </div>
                </div>

                {/* Language Content */}
                <div className="space-y-4">
                  <h4 className="font-semibold text-gray-800">Language Content</h4>
                  
                  <div className="p-4 bg-purple-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-purple-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium group-hover:text-purple-800 transition-colors">Grammar</span>
                      <span className="font-bold text-purple-600 group-hover:scale-105 transition-transform duration-200">{analysis.language_content.grammar.score}%</span>
                    </div>
                    <p className="text-sm text-gray-600">{analysis.language_content.grammar.assessment}</p>
                  </div>
                  
                  <div className="p-4 bg-indigo-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-indigo-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium group-hover:text-indigo-800 transition-colors">Vocabulary</span>
                      <span className="font-bold text-indigo-600 group-hover:scale-105 transition-transform duration-200">{analysis.language_content.vocabulary.diversity_score}%</span>
                    </div>
                    <p className="text-sm text-gray-600">{analysis.language_content.vocabulary.quality}</p>
                  </div>
                  
                  <div className="p-4 bg-pink-50 rounded-xl hover:shadow-md hover:-translate-y-0.5 hover:bg-pink-25 hover:scale-[1.01] transition-all duration-250 ease-out group">
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium group-hover:text-pink-800 transition-colors">Engagement</span>
                      <span className="font-bold text-pink-600 group-hover:scale-105 transition-transform duration-200">{analysis.emotional_engagement.engagement_level}</span>
                    </div>
                    <p className="text-sm text-gray-600">{analysis.emotional_engagement.tone_assessment}</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Strengths and Improvements */}
            <div className="grid md:grid-cols-2 gap-6">
              {/* Strengths */}
              <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
                <h3 className="text-xl font-bold text-green-600 mb-4">✅ Strengths</h3>
                <ul className="space-y-2">
                  {analysis.strengths.map((strength, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-green-500 mr-2">•</span>
                      <span className="text-gray-700">{strength}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* Improvements */}
              <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
                <h3 className="text-xl font-bold text-orange-600 mb-4">🎯 Areas for Improvement</h3>
                <ul className="space-y-2">
                  {analysis.improvements.map((improvement, index) => (
                    <li key={index} className="flex items-start">
                      <span className="text-orange-500 mr-2">•</span>
                      <span className="text-gray-700">{improvement}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Actionable Tips */}
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h3 className="text-xl font-bold text-indigo-600 mb-6">💡 Actionable Tips</h3>
              <div className="grid gap-4">
                {analysis.actionable_tips.map((tip, index) => (
                  <div key={index} className="p-4 bg-indigo-50 rounded-xl border-l-4 border-indigo-500">
                    <h4 className="font-semibold text-indigo-800 mb-2">{tip.title}</h4>
                    <p className="text-sm text-indigo-600 font-medium mb-1">Technique: {tip.technique}</p>
                    <p className="text-gray-700">{tip.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Emotion Analysis */}
            {analysis.emotion_analysis && (
              <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
                <h3 className="text-xl font-bold text-purple-600 mb-4">😊 Emotion Analysis</h3>
                <div className="p-4 bg-purple-50 rounded-xl">
                  <p className="text-purple-800 font-medium mb-2">
                    Detected Emotion: {analysis.emotion_analysis.detected_emotion}
                  </p>
                  <p className="text-gray-700">{analysis.emotion_analysis.emotion_feedback}</p>
                </div>
              </div>
            )}
            </div>
          </SectionWrapper>
        )}
      </div>
    </PageWrapper>
  )
}

export default SpeechAnalysis