import { useState, useEffect } from 'react'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line, Bar } from 'react-chartjs-2'

// Register Chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const ProgressCharts = ({ sessions }) => {
  const [activeChart, setActiveChart] = useState('overview')
  const [chartError, setChartError] = useState(null)

  useEffect(() => {
    // Reset error when sessions change
    setChartError(null)
  }, [sessions])

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

  try {
    // Prepare data for charts (reverse to show chronological order)
    const chartSessions = [...sessions].reverse()
    const labels = chartSessions.map((session, index) => `Session ${index + 1}`)

    // Ensure we have valid numeric data
    const confidenceData = chartSessions.map(s => Number(s.confidence) || 0)
    const wpmData = chartSessions.map(s => Number(s.wpm) || 0)
    const fillersData = chartSessions.map(s => Number(s.fillers) || 0)
    const grammarData = chartSessions.map(s => Number(s.grammar_score) || 0)

    // Chart options
    const commonOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'top',
          labels: {
            usePointStyle: true,
            padding: 20,
            font: {
              size: 12,
              weight: '500'
            }
          }
        },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: 'white',
          bodyColor: 'white',
          borderColor: 'rgba(255, 255, 255, 0.1)',
          borderWidth: 1,
          cornerRadius: 8,
          padding: 12
        }
      },
      scales: {
        x: {
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          ticks: {
            font: {
              size: 11
            }
          }
        },
        y: {
          grid: {
            color: 'rgba(0, 0, 0, 0.05)'
          },
          ticks: {
            font: {
              size: 11
            }
          }
        }
      }
    }

    // Overview Chart Data (Multiple metrics)
    const overviewData = {
      labels,
      datasets: [
        {
          label: 'Confidence Score',
          data: confidenceData,
          borderColor: 'rgb(99, 102, 241)',
          backgroundColor: 'rgba(99, 102, 241, 0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgb(99, 102, 241)',
          pointBorderColor: 'white',
          pointBorderWidth: 2,
          pointRadius: 5
        },
        {
          label: 'Grammar Score',
          data: grammarData,
          borderColor: 'rgb(34, 197, 94)',
          backgroundColor: 'rgba(34, 197, 94, 0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgb(34, 197, 94)',
          pointBorderColor: 'white',
          pointBorderWidth: 2,
          pointRadius: 5
        }
      ]
    }

    // Speaking Speed Chart Data
    const speedData = {
      labels,
      datasets: [
        {
          label: 'Words Per Minute',
          data: wpmData,
          borderColor: 'rgb(59, 130, 246)',
          backgroundColor: 'rgba(59, 130, 246, 0.1)',
          fill: true,
          tension: 0.4,
          pointBackgroundColor: 'rgb(59, 130, 246)',
          pointBorderColor: 'white',
          pointBorderWidth: 2,
          pointRadius: 5
        }
      ]
    }

    // Fillers Chart Data
    const fillersData = {
      labels,
      datasets: [
        {
          label: 'Filler Words Count',
          data: fillersData,
          backgroundColor: fillersData.map(count => {
            if (count <= 2) return 'rgba(34, 197, 94, 0.8)'
            if (count <= 5) return 'rgba(251, 191, 36, 0.8)'
            return 'rgba(239, 68, 68, 0.8)'
          }),
          borderColor: fillersData.map(count => {
            if (count <= 2) return 'rgb(34, 197, 94)'
            if (count <= 5) return 'rgb(251, 191, 36)'
            return 'rgb(239, 68, 68)'
          }),
          borderWidth: 2,
          borderRadius: 6
        }
      ]
    }

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

    const chartTabs = [
      { id: 'overview', label: 'Overview', icon: '📊' },
      { id: 'speed', label: 'Speaking Speed', icon: '⚡' },
      { id: 'fillers', label: 'Filler Words', icon: '🎯' }
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

        {/* Chart Tabs */}
        <div className="flex flex-wrap gap-2 mb-6">
          {chartTabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveChart(tab.id)}
              className={`px-4 py-2 rounded-xl font-medium transition-all duration-300 flex items-center gap-2 ${
                activeChart === tab.id
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
          <div style={{ height: '400px' }}>
            {activeChart === 'overview' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Performance Overview</h3>
                <Line data={overviewData} options={commonOptions} />
              </div>
            )}

            {activeChart === 'speed' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Speaking Speed Progress</h3>
                <Line data={speedData} options={commonOptions} />
              </div>
            )}

            {activeChart === 'fillers' && (
              <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-4">Filler Words Tracking</h3>
                <Bar data={fillersData} options={commonOptions} />
              </div>
            )}
          </div>
        </div>

        {/* Simple Progress Summary */}
        <div className="bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-6">
          <h3 className="text-lg font-semibold text-gray-800 mb-4">📈 Progress Summary</h3>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium text-gray-700 mb-2">Total Sessions</h4>
              <p className="text-2xl font-bold text-purple-600">{sessions.length}</p>
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

  } catch (error) {
    console.error('Chart rendering error:', error)
    return (
      <div className="bg-red-50 rounded-2xl p-8 text-center">
        <div className="text-4xl mb-4">⚠️</div>
        <h3 className="text-xl font-bold text-red-800 mb-2">Chart Error</h3>
        <p className="text-red-600 mb-4">
          There was an issue rendering the charts. Please try refreshing the page.
        </p>
        <button
          onClick={() => window.location.reload()}
          className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors"
        >
          Refresh Page
        </button>
      </div>
    )
  }
}

export default ProgressCharts