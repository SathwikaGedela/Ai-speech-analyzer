import { useState, useEffect } from 'react'
import { useAuth } from '../contexts/AuthContext'
import Navigation from './Navigation'
import LoadingSpinner from './LoadingSpinner'
import SimpleProgressCharts from './SimpleProgressCharts'
import PageWrapper from './PageWrapper'
import SectionWrapper from './SectionWrapper'
import { HistoryHeader } from './HeaderVariants'
import EmptyState from './EmptyState'
import AnimatedModal from './AnimatedModal'
import MetricCard from './MetricCard'

const HistoryPage = () => {
  const { getHistory } = useAuth()
  const [historyData, setHistoryData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [selectedSession, setSelectedSession] = useState(null)
  const [showModal, setShowModal] = useState(false)

  useEffect(() => {
    loadHistory()
  }, [])

  const loadHistory = async () => {
    setLoading(true)
    const result = await getHistory()
    
    if (result.success) {
      setHistoryData(result.data)
    } else {
      setError(result.error || 'Failed to load history')
    }
    
    setLoading(false)
  }

  const openSessionModal = (session) => {
    setSelectedSession(session)
    setShowModal(true)
  }

  const closeModal = () => {
    setShowModal(false)
    setSelectedSession(null)
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

  const calculateAverages = (sessions) => {
    if (!sessions || sessions.length === 0) return null
    
    const totals = sessions.reduce((acc, session) => ({
      confidence: acc.confidence + session.confidence,
      wpm: acc.wpm + session.wpm,
      fillers: acc.fillers + session.fillers,
      grammar: acc.grammar + (session.grammar_score || 0)
    }), { confidence: 0, wpm: 0, fillers: 0, grammar: 0 })
    
    return {
      confidence: Math.round(totals.confidence / sessions.length),
      wpm: Math.round(totals.wpm / sessions.length),
      fillers: Math.round(totals.fillers / sessions.length),
      grammar: Math.round(totals.grammar / sessions.length)
    }
  }

  const getProgressTrend = (sessions, metric) => {
    if (!sessions || sessions.length < 2) return 'stable'
    
    const recent = sessions.slice(0, Math.min(3, sessions.length))
    const older = sessions.slice(-Math.min(3, sessions.length))
    
    const recentAvg = recent.reduce((sum, s) => sum + s[metric], 0) / recent.length
    const olderAvg = older.reduce((sum, s) => sum + s[metric], 0) / older.length
    
    const diff = recentAvg - olderAvg
    
    if (metric === 'fillers') {
      // For fillers, lower is better
      if (diff < -0.5) return 'improving'
      if (diff > 0.5) return 'declining'
    } else {
      // For other metrics, higher is better
      if (diff > 2) return 'improving'
      if (diff < -2) return 'declining'
    }
    
    return 'stable'
  }

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'improving': return '📈'
      case 'declining': return '📉'
      default: return '➡️'
    }
  }

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'improving': return 'text-green-600'
      case 'declining': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  if (loading) {
    return (
      <PageWrapper className="min-h-screen">
        <Navigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <SectionWrapper index={0}>
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <LoadingSpinner />
              <p className="text-center text-gray-600 mt-4">Loading your analysis history...</p>
            </div>
          </SectionWrapper>
        </div>
      </PageWrapper>
    )
  }

  if (error) {
    return (
      <PageWrapper className="min-h-screen">
        <Navigation />
        <div className="max-w-7xl mx-auto px-4 py-8">
          <SectionWrapper index={0}>
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <div className="text-center">
                <div className="text-6xl mb-4">📊</div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Unable to Load History</h2>
                <p className="text-gray-600 mb-6">{error}</p>
                <button
                  onClick={loadHistory}
                  className="px-6 py-3 bg-indigo-500 text-white rounded-xl font-semibold hover:bg-indigo-600 transition-all duration-300"
                >
                  Try Again
                </button>
              </div>
            </div>
          </SectionWrapper>
        </div>
      </PageWrapper>
    )
  }

  const sessions = historyData?.sessions || []
  const averages = calculateAverages(sessions)

  return (
    <PageWrapper className="min-h-screen">
      <Navigation />
      
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Enhanced Header */}
        <SectionWrapper index={0}>
          <HistoryHeader totalSessions={sessions.length} className="mb-6" />
        </SectionWrapper>

        {sessions.length === 0 ? (
          /* No Data State */
          <SectionWrapper index={1}>
            <div className="glass-card rounded-3xl p-8 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <EmptyState
                icon="📊"
                title="No Analysis History Yet"
                description="Start analyzing your speech to see your progress over time. Your journey to better communication begins with your first analysis."
                primaryAction={{
                  label: "Start Speech Analysis",
                  onClick: () => window.location.href = '/analysis'
                }}
                secondaryAction={{
                  label: "Try Interview Mode",
                  onClick: () => window.location.href = '/interview'
                }}
              />
            </div>
          </SectionWrapper>
        ) : (
          <>
            {/* Statistics Overview */}
            <SectionWrapper index={1}>
              <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Performance Overview</h2>
              
              <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
                <MetricCard
                  title="Total Sessions"
                  value={sessions.length}
                  icon="🎯"
                  color="indigo"
                  delay={0}
                />
                
                {averages && (
                  <>
                    <MetricCard
                      title="Avg Confidence"
                      value={averages.confidence}
                      unit="%"
                      icon="💪"
                      color={averages.confidence >= 80 ? 'green' : averages.confidence >= 60 ? 'yellow' : 'red'}
                      trend={{
                        direction: getProgressTrend(sessions, 'confidence'),
                        value: `${getProgressTrend(sessions, 'confidence')}`
                      }}
                      delay={0.1}
                    />
                    
                    <MetricCard
                      title="Avg WPM"
                      value={averages.wpm}
                      icon="⚡"
                      color="blue"
                      trend={{
                        direction: getProgressTrend(sessions, 'wpm'),
                        value: `${getProgressTrend(sessions, 'wpm')}`
                      }}
                      delay={0.2}
                    />
                    
                    <MetricCard
                      title="Avg Fillers"
                      value={averages.fillers}
                      icon="🎭"
                      color="yellow"
                      trend={{
                        direction: getProgressTrend(sessions, 'fillers'),
                        value: `${getProgressTrend(sessions, 'fillers')}`
                      }}
                      delay={0.3}
                    />
                  </>
                )}
              </div>
              </div>
            </SectionWrapper>

            {/* Progress Charts */}
            <SectionWrapper index={2}>
              <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Progress Charts</h2>
                <SimpleProgressCharts sessions={sessions} />
              </div>
            </SectionWrapper>

            {/* Recent Sessions */}
            <SectionWrapper index={3}>
              <div className="glass-card rounded-3xl p-8 mb-6 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 ease-out">
              <h2 className="text-2xl font-bold text-gray-800 mb-6">Recent Sessions</h2>
              
              <div className="space-y-4">
                {sessions.slice(0, 10).map((session) => (
                  <div
                    key={session.id}
                    className="p-4 bg-gray-50 rounded-xl hover:bg-white hover:shadow-lg hover:-translate-y-1 hover:scale-[1.01] transition-all duration-300 ease-out cursor-pointer active:scale-[0.99] active:translate-y-0 group"
                    onClick={() => openSessionModal(session)}
                  >
                    <div className="flex justify-between items-start">
                      <div className="flex-1">
                        <div className="flex items-center gap-4 mb-2">
                          <span className="text-sm text-gray-500 group-hover:text-gray-700 transition-colors">{session.created_at}</span>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${getScoreBg(session.confidence)} ${getScoreColor(session.confidence)} group-hover:scale-105 transition-all duration-200`}>
                            {session.confidence}% Confidence
                          </span>
                          <span className="px-2 py-1 bg-blue-100 text-blue-600 rounded-full text-xs font-medium group-hover:bg-blue-200 group-hover:scale-105 transition-all duration-200">
                            {session.wpm} WPM
                          </span>
                          <span className="px-2 py-1 bg-yellow-100 text-yellow-600 rounded-full text-xs font-medium group-hover:bg-yellow-200 group-hover:scale-105 transition-all duration-200">
                            {session.fillers} Fillers
                          </span>
                        </div>
                        <p className="text-gray-700 text-sm leading-relaxed group-hover:text-gray-900 transition-colors">
                          {session.transcript.length > 150 
                            ? `${session.transcript.substring(0, 150)}...` 
                            : session.transcript}
                        </p>
                      </div>
                      <div className="ml-4 text-gray-400 group-hover:text-gray-600 group-hover:translate-x-1 transition-all duration-200">
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                        </svg>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
              
              {sessions.length > 10 && (
                <div className="text-center mt-6">
                  <p className="text-gray-500">Showing 10 of {sessions.length} sessions</p>
                </div>
              )}
              </div>
            </SectionWrapper>
          </>
        )}
      </div>

      {/* Session Detail Modal */}
      <AnimatedModal
        isOpen={showModal}
        onClose={closeModal}
        title="Session Details"
        size="large"
      >
        {selectedSession && (
          <div className="p-8">
            {/* Session Info */}
            <div className="mb-6 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
              <p className="text-gray-600 text-sm">Session Date</p>
              <p className="text-lg font-semibold text-gray-800">{selectedSession.created_at}</p>
            </div>

            {/* Session Metrics */}
            <div className="grid md:grid-cols-4 gap-4 mb-6">
              <MetricCard
                title="Confidence"
                value={selectedSession.confidence}
                unit="%"
                icon="💪"
                color={selectedSession.confidence >= 80 ? 'green' : selectedSession.confidence >= 60 ? 'yellow' : 'red'}
                delay={0}
              />
              
              <MetricCard
                title="WPM"
                value={selectedSession.wpm}
                icon="⚡"
                color="blue"
                delay={0.1}
              />
              
              <MetricCard
                title="Fillers"
                value={selectedSession.fillers}
                icon="🎭"
                color="yellow"
                delay={0.2}
              />
              
              <MetricCard
                title="Emotion"
                value={selectedSession.emotion}
                icon="😊"
                color="purple"
                delay={0.3}
              />
            </div>

            {/* Transcript */}
            <div className="mb-6">
              <h3 className="text-lg font-semibold text-gray-800 mb-3">Transcript</h3>
              <div className="p-4 bg-gray-50 rounded-xl">
                <p className="text-gray-700 leading-relaxed">{selectedSession.transcript}</p>
              </div>
            </div>

            {/* Assessments */}
            <div className="grid md:grid-cols-2 gap-6 mb-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Performance Assessment</h3>
                <div className="space-y-3">
                  <div className="p-3 bg-blue-50 rounded-lg">
                    <p className="text-sm font-medium text-blue-800">Pace Assessment:</p>
                    <p className="text-gray-700 text-sm">{selectedSession.pace_assessment}</p>
                  </div>
                  <div className="p-3 bg-yellow-50 rounded-lg">
                    <p className="text-sm font-medium text-yellow-800">Filler Assessment:</p>
                    <p className="text-gray-700 text-sm">{selectedSession.filler_assessment}</p>
                  </div>
                  <div className="p-3 bg-green-50 rounded-lg">
                    <p className="text-sm font-medium text-green-800">Grammar Assessment:</p>
                    <p className="text-gray-700 text-sm">{selectedSession.grammar_assessment}</p>
                  </div>
                </div>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">Additional Metrics</h3>
                <div className="space-y-3">
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Word Count:</span>
                    <span className="text-gray-900">{selectedSession.word_count}</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Grammar Score:</span>
                    <span className="text-gray-900">{selectedSession.grammar_score}%</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Vocabulary Diversity:</span>
                    <span className="text-gray-900">{selectedSession.vocabulary_diversity}%</span>
                  </div>
                  <div className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm font-medium text-gray-700">Skill Level:</span>
                    <span className="text-gray-900">{selectedSession.skill_level}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* General Impression */}
            <div className="p-4 bg-indigo-50 rounded-xl">
              <h3 className="text-lg font-semibold text-indigo-800 mb-2">General Impression</h3>
              <p className="text-gray-700">{selectedSession.general_impression}</p>
            </div>
          </div>
        )}
      </AnimatedModal>
    </PageWrapper>
  )
}

export default HistoryPage