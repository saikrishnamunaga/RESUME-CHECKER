import { useState } from 'react'
import { useGoogleLogout } from '@react-oauth/google'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'

const Dashboard = ({ user }) => {
  const [jobDesc, setJobDesc] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const logout = useGoogleLogout()

  const onDrop = async (acceptedFiles) => {
    if (acceptedFiles.length === 0 || !jobDesc.trim()) return

    setLoading(true)
    const formData = new FormData()
    acceptedFiles.forEach(file => formData.append('resumes', file))
    formData.append('job_description', jobDesc)

    try {
      const token = localStorage.getItem('token')
      const res = await fetch('/api/v1/screening/', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${token}`
        }
      })
      const data = await res.json()
      setResults(data)
    } catch (error) {
      alert('Screening failed: ' + error.message)
    }
    setLoading(false)
  }

  const { getRootProps, getInputProps } = useDropzone({ onDrop, accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'] } })

  const sortedResults = results.sort((a, b) => b.score - a.score)

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-3xl font-bold text-gray-900">Dashboard</h2>
        <div className="flex items-center space-x-4">
          <span className="px-4 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
            {user.plan.toUpperCase()} Plan
          </span>
          <button 
            onClick={() => {
              localStorage.clear()
              logout()
              navigate('/')
            }}
            className="px-6 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white p-8 rounded-2xl shadow-xl">
          <h3 className="text-2xl font-bold mb-6">Job Description</h3>
          <textarea
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            className="w-full h-48 p-4 border-2 border-gray-200 rounded-xl resize-none focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
            placeholder="Paste the full job description here..."
          />
        </div>

        <div {...getRootProps()} className="bg-gradient-to-r from-purple-50 to-blue-50 border-3 border-dashed border-purple-300 rounded-2xl p-12 hover:border-purple-400 transition-all cursor-pointer group">
          <input {...getInputProps()} />
          <div className="text-center">
            <div className="w-20 h-20 bg-purple-200 rounded-2xl mx-auto mb-4 flex items-center justify-center group-hover:bg-purple-300 transition">
              <svg className="w-10 h-10 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h4 className="text-2xl font-bold text-gray-900 mb-2">Drop Resumes</h4>
            <p className="text-gray-600 mb-4">PDF or DOCX files (max 2MB each)</p>
            <p className="text-sm text-purple-600 font-medium">Click or drag & drop up to 10 resumes</p>
          </div>
        </div>
      </div>

      {loading && (
        <div className="flex justify-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
        </div>
      )}

      {sortedResults.length > 0 && (
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          <div className="px-8 py-6 bg-gradient-to-r from-blue-600 to-indigo-600">
            <h3 className="text-2xl font-bold text-white">Ranking Results ({sortedResults.length} candidates)</h3>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-8 py-4 text-left text-sm font-bold text-gray-900">Candidate</th>
                  <th className="px-8 py-4 text-left text-sm font-bold text-gray-900">Domain</th>
                  <th className="px-8 py-4 text-left text-sm font-bold text-gray-900">Score</th>
                  <th className="px-8 py-4 text-left text-sm font-bold text-gray-900">Strengths</th>
                  <th className="px-8 py-4 text-left text-sm font-bold text-gray-900">Missing</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {sortedResults.map((result, i) => (
                  <tr key={i} className="hover:bg-gray-50">
                    <td className="px-8 py-6 font-medium text-gray-900">Resume {i+1}</td>
                    <td className="px-8 py-6">
                      <span className="px-3 py-1 bg-green-100 text-green-800 text-sm font-medium rounded-full">
                        {result.domain}
                      </span>
                    </td>
                    <td className="px-8 py-6">
                      <div className="flex items-center">
                        <div className="w-24 bg-gradient-to-r from-green-400 to-blue-500 rounded-full h-3 mr-3"></div>
                        <span className="font-bold text-2xl text-gray-900">{result.score}%</span>
                      </div>
                    </td>
                    <td className="px-8 py-6 text-sm text-gray-600 max-w-xs">
                      {result.strengths.slice(0,3).join(', ') || 'N/A'}
                    </td>
                    <td className="px-8 py-6 text-sm text-red-600">
                      {result.missing.slice(0,3).join(', ') || 'None'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      <div className="text-center">
        <button className="px-8 py-4 bg-gradient-to-r from-purple-500 to-pink-500 text-white text-lg font-bold rounded-2xl shadow-xl hover:shadow-2xl transform hover:-translate-y-1 transition-all duration-200">
          Upgrade to Pro - ₹299/mo (300 resumes)
        </button>
      </div>
    </div>
  )
}

export default Dashboard

