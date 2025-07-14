import React, { useEffect, useState, useRef } from 'react';
import AddEmployeeModal from '../components/AddEmployeeModal';
import SendBotMessageButton from '../components/SendBotMessageButton';

export default function Dashboard() {
  const [feedbackData, setFeedbackData] = useState(null);
  const wsRef = useRef(null);

  // Fetch feedback data from backend
  const fetchFeedbackData = async () => {
    try {
      const res = await fetch('/api/feedback-data/');
      const data = await res.json();
      setFeedbackData(data);
    } catch (err) {
      console.error('Error fetching feedback data:', err);
    }
  };

  useEffect(() => {
    fetchFeedbackData(); // initial fetch
    wsRef.current = new window.WebSocket('ws://localhost:8000/ws/feedback/');
    wsRef.current.onmessage = (event) => {
      // On new feedback, refetch data
      fetchFeedbackData();
    };
    wsRef.current.onerror = (e) => {
      console.error('WebSocket error:', e);
    };
    return () => {
      wsRef.current && wsRef.current.close();
    };
  }, []);

  const [showAddModal, setShowAddModal] = useState(false);

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f6d6ff]/30 via-[#d1f5f0]/30 to-[#e6e4ff]/30 p-6 font-[Poppins] text-gray-800">
      <AddEmployeeModal open={showAddModal} onClose={() => setShowAddModal(false)} onEmployeeAdded={fetchFeedbackData} />
      {/* Solid Header */}
      <header className="fixed top-0 left-0 w-full bg-[#90acc6] shadow-sm z-50 p-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <img src="/logo.png" alt="PulseTracker" className="w-8 h-8 rounded" />
          <h1 className="text-xl font-bold tracking-tight text-white">PulseTracker</h1>
        </div>
        <div className="flex items-center gap-4">
          <button
            className="bg-white/20 border border-white/30 hover:bg-white/40 text-white px-4 py-2 rounded-lg font-medium shadow transition"
            onClick={() => setShowAddModal(true)}
          >
            + Add Employee
          </button>
          <div className="text-sm text-white/90">Welcome, HR Department</div>
        </div>
      </header>
      <div className="mt-24">
        <SendBotMessageButton onSent={fetchFeedbackData} />
        <div className="space-y-8">
        {/* Emotional Summary Card */}
        <div className="bg-white/80 backdrop-blur-lg rounded-xl shadow-md p-6 animate-float">
          <h2 className="text-lg font-semibold mb-2 text-gray-700">Emotional Summary</h2>
          <div className="flex justify-around">
            <div className="text-center">
              <p className="text-2xl font-bold text-green-500">43%</p>
              <p className="text-sm">😊 Positive</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-yellow-500">31%</p>
              <p className="text-sm">😐 Neutral</p>
            </div>
            <div className="text-center">
              <p className="text-2xl font-bold text-red-500">26%</p>
              <p className="text-sm">😟 Negative</p>
            </div>
          </div>
        </div>
        {/* Employee Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white/80 backdrop-blur-lg p-4 rounded-lg shadow animate-float">
            <h3 className="font-medium text-gray-700 mb-1">Total Employees</h3>
            <div className="flex items-center space-x-3">
              <span className="text-3xl">👥</span>
              <p className="text-xl font-semibold">102</p>
            </div>
          </div>

          <div className="bg-white/80 backdrop-blur-lg p-4 rounded-lg shadow animate-float">
            <h3 className="font-medium text-gray-700 mb-1">Engaged with Bot</h3>
            <div className="flex items-center space-x-3">
              <span className="text-3xl animate-pulse">🤖</span>
              <p className="text-xl font-semibold">87</p>
            </div>
          </div>
        </div>

        {/* Mood Trend Chart - Real Line Graph */}
        <div className="bg-white/90 backdrop-blur-lg rounded-xl shadow-md p-6">
          <h2 className="text-lg font-semibold mb-4 text-gray-700">Mood Trend (Last 7 Days)</h2>
          <div className="relative">
            <svg viewBox="0 0 350 120" className="w-full h-32">
              {/* Grid lines */}
              <defs>
                <pattern id="grid" width="50" height="20" patternUnits="userSpaceOnUse">
                  <path d="M 50 0 L 0 0 0 20" fill="none" stroke="#e5e7eb" strokeWidth="1"/>
                </pattern>
              </defs>
              <rect width="350" height="120" fill="url(#grid)" />
              
              {/* Y-axis labels */}
              <text x="10" y="25" className="text-xs fill-gray-500">High</text>
              <text x="10" y="65" className="text-xs fill-gray-500">Med</text>
              <text x="10" y="105" className="text-xs fill-gray-500">Low</text>
              
              {/* Data points and line */}
              <polyline
                points="50,80 100,60 150,70 200,45 250,50 300,35 350,40"
                fill="none"
                stroke="#90acc6"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
              
              {/* Data point dots */}
              <circle cx="50" cy="80" r="4" fill="#90acc6" />
              <circle cx="100" cy="60" r="4" fill="#90acc6" />
              <circle cx="150" cy="70" r="4" fill="#90acc6" />
              <circle cx="200" cy="45" r="4" fill="#90acc6" />
              <circle cx="250" cy="50" r="4" fill="#90acc6" />
              <circle cx="300" cy="35" r="4" fill="#90acc6" />
              <circle cx="350" cy="40" r="4" fill="#90acc6" />
              
              {/* X-axis labels */}
              <text x="45" y="115" className="text-xs fill-gray-500">Mon</text>
              <text x="95" y="115" className="text-xs fill-gray-500">Tue</text>
              <text x="145" y="115" className="text-xs fill-gray-500">Wed</text>
              <text x="195" y="115" className="text-xs fill-gray-500">Thu</text>
              <text x="245" y="115" className="text-xs fill-gray-500">Fri</text>
              <text x="295" y="115" className="text-xs fill-gray-500">Sat</text>
              <text x="345" y="115" className="text-xs fill-gray-500">Sun</text>
            </svg>
          </div>
        </div>
        
        {/* Department Breakdown Table */}
        <div className="bg-white/80 backdrop-blur-lg p-6 rounded-xl shadow-md">
          <h2 className="text-lg font-semibold mb-2 text-gray-700">Department Mood</h2>
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b text-gray-500">
                <th className="py-2">Department</th>
                <th>Mood</th>
                <th>Feedback Count</th>
              </tr>
            </thead>
            <tbody>
              {feedbackData && feedbackData.departments && feedbackData.departments.length > 0 ? (
                feedbackData.departments.map((dept) => {
                  let emoji = '😐';
                  if (dept.avg_sentiment > 0.3) emoji = '😄';
                  else if (dept.avg_sentiment < -0.3) emoji = '😟';
                  return (
                    <tr className="border-b" key={dept.department}>
                      <td className="py-2 font-medium">{dept.department}</td>
                      <td>{emoji} <span className="ml-1 text-xs text-gray-500">{dept.avg_sentiment.toFixed(2)}</span></td>
                      <td>{dept.feedback_count}</td>
                    </tr>
                  );
                })
              ) : (
                <tr><td colSpan={3} className="py-2 text-gray-400 text-center">No department data yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>

        {/* Top Phrases & Suggestions */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white/80 backdrop-blur-lg p-4 rounded-lg shadow-md">
            <h3 className="font-semibold text-gray-700 mb-2">Top Feedback Phrases</h3>
            <ul className="list-disc ml-5 text-sm text-gray-600">
              <li>"I'm overwhelmed"</li>
              <li>"Deadlines too tight"</li>
              <li>"Great teamwork this week"</li>
            </ul>
          </div>

          <div className="bg-white/80 backdrop-blur-lg p-4 rounded-lg shadow-md">
            <h3 className="font-semibold text-gray-700 mb-2">Suggested Actions</h3>
            <ul className="list-disc ml-5 text-sm text-gray-600">
              <li>Check in with Sales</li>
              <li>Encourage time-off for HR</li>
              <li>Acknowledge Tech performance</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  );
}