import { useState } from 'react'

const SimpleProgressCharts = ({ sessions }) => {
  const [activeView, setActiveView] = useState('overview')

  if (!sessions || sessions.length === 0) {
    return (
      <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl p-8 text-center">
        <div className="text-4xl mb-4">📊</div>
        <h3 className="text-xl font-bold text-gray-800 mb-2">No Data Available</h3>
        <p className="text-gray-600">
          Complete some speech analyses to see your progress charts.
        </p>
      </div>
    )
  }

  // Prepare data for charts (reverse to show chronological order)
  const chartSessions = [...sessions].reverse()

  // Calculate statistics
  const getStatistics = () => {
    if (chartSessions.length < 2) return null

    const latest = chartSessions[chartSessions.length - 1]
    const previous = chartSessions[chartSessions.length - 2]
    
    return {
      confidence: {
        current: latest.confidence,
        change: latest.confidence - previous.confidence,
        trend: latest.confidence > previous.confidence ? 'up' : latest.confidence < previous.confidence ? 'down' : 'stable'
      },
      wpm: {
        current: latest.wpm,
        change: latest.wpm - previous.wpm,
        trend: latest.wpm > previous.wpm ? 'up' : latest.wpm < previous.wpm ? 'down' : 'stable'
      },
      fillers: {
        current: latest.fillers,
        change: latest.fillers - previous.fillers,
        trend: latest.fillers < previous.fillers ? 'up' : latest.fillers > previous.fillers ? 'down' : 'stable'
      },
      grammar: {
        current: latest.grammar_score || 0,
        change: (latest.grammar_score || 0) - (previous.grammar_score || 0),
        trend: (latest.grammar_score || 0) > (previous.grammar_score || 0) ? 'up' : (latest.grammar_score || 0) < (previous.grammar_score || 0) ? 'down' : 'stable'
      }
    }
  }

  const stats = getStatistics()

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up': return '📈'
      case 'down': return '📉'
      default: return '➡️'
    }
  }

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'up': return 'text-green-600'
      case 'down': return 'text-red-600'
      default: return 'text-gray-600'
    }
  }

  // Calculate averages
  const calculateAverages = () => {
    const totals = chartSessions.reduce((acc, session) => ({
      confidence: acc.confidence + session.confidence,
      wpm: acc.wpm + session.wpm,
      fillers: acc.fillers + session.fillers,
      grammar: acc.grammar + (session.grammar_score || 0)
    }), { confidence: 0, wpm: 0, fillers: 0, grammar: 0 })
    
    return {
      confidence: Math.round(totals.confidence / chartSessions.length),
      wpm: Math.round(totals.wpm / chartSessions.length),
      fillers: Math.round(totals.fillers / chartSessions.length),
      grammar: Math.round(totals.grammar / chartSessions.length)
    }
  }

  const averages = calculateAverages()

  // Simple bar chart component
  const SimpleBarChart = ({ data, label, color, maxValue }) => (
    <div className="space-y-3">
      <h4 className="font-medium text-gray-700">{label}</h4>
      <div className="space-y-2">
        {data.map((value, index) => (
          <div key={index} className="flex items-center gap-3">
            <span className="text-xs text-gray-500 w-16">Session {index + 1}</span>
            <div className="flex-1 bg-gray-200 rounded-full h-3">
              <div
                className={`h-3 rounded-full ${color}`}
                style={{ width: `${(value / maxValue) * 100}%` }}
              />
            </div>
            <span className="text-xs font-medium text-gray-700 w-8">{value}</span>
          </div>
        ))}
      </div>
    </div>
  )

  // Line chart component (simplified)
  const SimpleLineChart = ({ data, label, color }) => (
    <div className="space-y-3">
      <h4 className="font-medium text-gray-700">{label}</h4>
      <div className="relative h-32 bg-gray-50 rounded-lg p-4">
        <svg className="w-full h-full" viewBox="0 0 400 100">
          {/* Grid lines */}
          {[0, 25, 50, 75, 100].map(y => (
            <line
              key={y}
              x1="0"
              y1={y}
              x2="400"
              y2={y}
              stroke="#e5e7eb"
              strokeWidth="1"
            />
          ))}
          
          {/* Data line */}
          {data.length > 1 && (
            <polyline
              points={data.map((value, index) => {
                const x = (index / (data.length - 1)) * 400
                const y = 100 - (value / Math.max(...data)) * 100
                return `${x},${y}`
              }).join(' ')}
              fill="none"
              stroke={color}
              strokeWidth="3"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          )}
          
          {/* Data points */}
          {data.map((value, index) => {
            const x = (index / Math.max(data.length - 1, 1)) * 400
            const y = 100 - (value / Math.max(...data)) * 100
            return (
              <circle
                key={index}
                cx={x}
                cy={y}
                r="4"
                fill={color}
                stroke="white"
                strokeWidth="2"
              />
            )
          })}
        </svg>
      </div>
    </div>
  )

  const viewTabs = [
    { id: 'overview', label: 'Overview', icon: '📊' },
    { id: 'trends', label: 'Trends', icon: '📈' },
    { id: 'details', label: 'Details', icon: '📋' }
  ]

  return (
    <div className="space-y-6">
      {/* Progress Statistics */}
      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-gradient-to-br from-indigo-50 to-indigo-100 p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-indigo-600 font-medium">Confidence</p>
                <p className="text-2xl font-bold text-indigo-800">{stats.confidence.current}%</p>
              </div>
              <div className={`text-right ${getTrendColor(stats.confidence.trend)}`}>
                <div className="text-lg">{getTrendIcon(stats.confidence.trend)}</div>
                <div className="text-xs font-medium">
                  {stats.confidence.change > 0 ? '+' : ''}{stats.confidence.change}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-blue-600 font-medium">Speaking Speed</p>
                <p className="text-2xl font-bold text-blue-800">{stats.wpm.current} WPM</p>
              </div>
              <div className={`text-right ${getTrendColor(stats.wpm.trend)}`}>
                <div className="text-lg">{getTrendIcon(stats.wpm.trend)}</div>
                <div className="text-xs font-medium">
                  {stats.wpm.change > 0 ? '+' : ''}{stats.wpm.change}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-yellow-50 to-yellow-100 p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-yellow-600 font-medium">Filler Words</p>
                <p className="text-2xl font-bold text-yellow-800">{stats.fillers.current}</p>
              </div>
              <div className={`text-right ${getTrendColor(stats.fillers.trend)}`}>
                <div className="text-lg">{getTrendIcon(stats.fillers.trend)}</div>
                <div className="text-xs font-medium">
                  {stats.fillers.change > 0 ? '+' : ''}{stats.fillers.change}
                </div>
              </div>
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-green-600 font-medium">Grammar</p>
                <p className="text-2xl font-bold text-green-800">{stats.grammar.current}%</p>
              </div>
              <div className={`text-right ${getTrendColor(stats.grammar.trend)}`}>
                <div className="text-lg">{getTrendIcon(stats.grammar.trend)}</div>
                <div className="text-xs font-medium">
                  {stats.grammar.change > 0 ? '+' : ''}{stats.grammar.change}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* View Tabs */}
      <div className="flex flex-wrap gap-2 mb-6">
        {viewTabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveView(tab.id)}
            className={`px-4 py-2 rounded-xl font-medium transition-all duration-300 flex items-center gap-2 ${
              activeView === tab.id
                ? 'bg-indigo-500 text-white shadow-lg'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <span>{tab.icon}</span>
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Chart Container */}
      <div className="bg-white rounded-2xl p-6 shadow-sm border border-gray-100">
        {activeView === 'overview' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-800">Performance Overview</h3>
            
            {/* Average Performance */}
            <div className="grid md:grid-cols-4 gap-4">
              <div className="text-center p-4 bg-indigo-50 rounded-xl">
                <div className="text-2xl font-bold text-indigo-600">{averages.confidence}%</div>
                <div className="text-sm text-gray-600">Avg Confidence</div>
              </div>
              <div className="text-center p-4 bg-blue-50 rounded-xl">
                <div className="text-2xl font-bold text-blue-600">{averages.wpm}</div>
                <div className="text-sm text-gray-600">Avg WPM</div>
              </div>
              <div className="text-center p-4 bg-yellow-50 rounded-xl">
                <div className="text-2xl font-bold text-yellow-600">{averages.fillers}</div>
                <div className="text-sm text-gray-600">Avg Fillers</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-xl">
                <div className="text-2xl font-bold text-green-600">{averages.grammar}%</div>
                <div className="text-sm text-gray-600">Avg Grammar</div>
              </div>
            </div>

            {/* Session Progress */}
            <div className="space-y-4">
              <h4 className="font-medium text-gray-700">Session Progress</h4>
              <div className="space-y-3">
                {chartSessions.slice(-5).map((session, index) => (
                  <div key={session.id} className="flex items-center gap-4 p-3 bg-gray-50 rounded-lg">
                    <div className="text-sm font-medium text-gray-600 w-20">
                      Session {chartSessions.length - 4 + index}
                    </div>
                    <div className="flex-1 grid grid-cols-4 gap-4 text-sm">
                      <div className="text-center">
                        <span className="font-medium text-indigo-600">{session.confidence}%</span>
                        <div className="text-xs text-gray-500">Confidence</div>
                      </div>
                      <div className="text-center">
                        <span className="font-medium text-blue-600">{session.wpm}</span>
                        <div className="text-xs text-gray-500">WPM</div>
                      </div>
                      <div className="text-center">
                        <span className="font-medium text-yellow-600">{session.fillers}</span>
                        <div className="text-xs text-gray-500">Fillers</div>
                      </div>
                      <div className="text-center">
                        <span className="font-medium text-green-600">{session.grammar_score || 0}%</span>
                        <div className="text-xs text-gray-500">Grammar</div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeView === 'trends' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-800">Progress Trends</h3>
            
            <div className="grid md:grid-cols-2 gap-6">
              <SimpleLineChart
                data={chartSessions.map(s => s.confidence)}
                label="Confidence Score Trend"
                color="#6366f1"
              />
              <SimpleLineChart
                data={chartSessions.map(s => s.wpm)}
                label="Speaking Speed Trend"
                color="#3b82f6"
              />
            </div>
          </div>
        )}

        {activeView === 'details' && (
          <div className="space-y-6">
            <h3 className="text-lg font-semibold text-gray-800">Detailed Analysis</h3>
            
            <div className="grid md:grid-cols-2 gap-6">
              <SimpleBarChart
                data={chartSessions.map(s => s.confidence)}
                label="Confidence by Session"
                color="bg-indigo-500"
                maxValue={100}
              />
              <SimpleBarChart
                data={chartSessions.map(s => s.fillers)}
                label="Filler Words by Session"
                color="bg-yellow-500"
                maxValue={Math.max(...chartSessions.map(s => s.fillers), 10)}
              />
            </div>
          </div>
        )}
      </div>

      {/* Progress Summary */}
      <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">📈 Progress Summary</h3>
        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <h4 className="font-medium text-gray-700 mb-2">Total Sessions</h4>
            <p className="text-2xl font-bold text-purple-600">{sessions.length}</p>
          </div>
          <div>
            <h4 className="font-medium text-gray-700 mb-2">Best Performance</h4>
            <div className="space-y-1">
              <p className="text-sm text-gray-600">
                Confidence: <span className="font-semibold">{Math.max(...chartSessions.map(s => s.confidence))}%</span>
              </p>
              <p className="text-sm text-gray-600">
                Speed: <span className="font-semibold">{Math.max(...chartSessions.map(s => s.wpm))} WPM</span>
              </p>
            </div>
          </div>
          <div>
            <h4 className="font-medium text-gray-700 mb-2">Latest Performance</h4>
            <div className="space-y-1">
              <p className="text-sm text-gray-600">
                Confidence: <span className="font-semibold">{sessions[0]?.confidence}%</span>
              </p>
              <p className="text-sm text-gray-600">
                Speed: <span className="font-semibold">{sessions[0]?.wpm} WPM</span>
              </p>
              <p className="text-sm text-gray-600">
                Fillers: <span className="font-semibold">{sessions[0]?.fillers}</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SimpleProgressCharts