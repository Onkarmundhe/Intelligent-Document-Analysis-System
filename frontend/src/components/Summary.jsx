import React, { useState } from 'react'
import { BarChart3, FileText, Sparkles, Clock, TrendingUp } from 'lucide-react'
import { documentAPI } from '../services/api'
import { useMutation } from 'react-query'

const Summary = ({ selectedDocuments }) => {
  const [summaries, setSummaries] = useState({})

  const summaryMutation = useMutation(documentAPI.summarize, {
    onSuccess: (data, documentId) => {
      setSummaries(prev => ({
        ...prev,
        [documentId]: data
      }))
    }
  })

  const handleGenerateSummary = (documentId) => {
    summaryMutation.mutate(documentId)
  }

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString()
  }

  return (
    <div className="space-y-6 w-full">
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-gray-900">Document Summaries</h2>
          {selectedDocuments.length > 0 && (
            <span className="text-sm text-primary-600">
              {selectedDocuments.length} document{selectedDocuments.length !== 1 ? 's' : ''} selected
            </span>
          )}
        </div>

        {selectedDocuments.length === 0 && (
          <div className="text-center py-12">
            <BarChart3 className="mx-auto h-12 w-12 text-gray-300 mb-4" />
            <p className="text-gray-500 text-sm">Select documents to generate summaries</p>
            <p className="text-gray-400 text-xs mt-1">Choose documents from the sidebar</p>
          </div>
        )}

        {selectedDocuments.length > 0 && (
          <div className="space-y-6">
            {selectedDocuments.map((documentId) => {
              const summary = summaries[documentId]
              const isLoading = summaryMutation.isLoading && summaryMutation.variables === documentId

              return (
                <div key={documentId} className="border border-gray-200 rounded-lg p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <FileText className="h-5 w-5 text-primary-600" />
                      <h3 className="font-medium text-gray-900">
                        Document {documentId.slice(0, 8)}...
                      </h3>
                    </div>
                    
                    {!summary && !isLoading && (
                      <button
                        onClick={() => handleGenerateSummary(documentId)}
                        className="btn-primary flex items-center space-x-2"
                        disabled={isLoading}
                      >
                        <Sparkles className="h-4 w-4" />
                        <span>Generate Summary</span>
                      </button>
                    )}
                  </div>

                  {isLoading && (
                    <div className="bg-blue-50 rounded-lg p-4">
                      <div className="flex items-center space-x-3">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-primary-600"></div>
                        <span className="text-primary-700">Generating AI summary...</span>
                      </div>
                      <p className="text-primary-600 text-sm mt-2">
                        This may take a few moments depending on document length.
                      </p>
                    </div>
                  )}

                  {summary && (
                    <div className="space-y-4">
                      {/* Summary Text */}
                      <div>
                        <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                          <FileText className="h-4 w-4 mr-2" />
                          Summary
                        </h4>
                        <div className="bg-gray-50 rounded-lg p-4">
                          <p className="text-gray-700 leading-relaxed">
                            {summary.summary}
                          </p>
                        </div>
                      </div>

                      {/* Key Points */}
                      {summary.key_points && summary.key_points.length > 0 && (
                        <div>
                          <h4 className="font-medium text-gray-900 mb-2 flex items-center">
                            <TrendingUp className="h-4 w-4 mr-2" />
                            Key Points
                          </h4>
                          <ul className="space-y-2">
                            {summary.key_points.map((point, index) => (
                              <li key={index} className="flex items-start space-x-2">
                                <span className="flex-shrink-0 w-2 h-2 bg-primary-600 rounded-full mt-2"></span>
                                <span className="text-gray-700">{point}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* Metadata */}
                      <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-200">
                        <div className="flex items-center space-x-2 text-sm text-gray-500">
                          <FileText className="h-4 w-4" />
                          <span>{summary.word_count?.toLocaleString()} words</span>
                        </div>
                        <div className="flex items-center space-x-2 text-sm text-gray-500">
                          <Clock className="h-4 w-4" />
                          <span>{formatDate(summary.generated_at)}</span>
                        </div>
                      </div>

                      {/* Regenerate Button */}
                      <div className="pt-2">
                        <button
                          onClick={() => handleGenerateSummary(documentId)}
                          className="btn-secondary text-sm"
                          disabled={isLoading}
                        >
                          <Sparkles className="h-3 w-3 mr-1" />
                          Regenerate Summary
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}
      </div>

      {/* Tips */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="mb-3">
          <h3 className="font-medium text-blue-900 flex items-center">
            <Sparkles className="h-4 w-4 mr-2" />
            Summary Tips
          </h3>
        </div>
        <ul className="space-y-2 text-sm text-blue-800">
          <li className="flex items-start space-x-2">
            <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full mt-2"></span>
            <span>Summaries are generated using AI and highlight the most important information</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full mt-2"></span>
            <span>Key points extract the main takeaways and actionable insights</span>
          </li>
          <li className="flex items-start space-x-2">
            <span className="flex-shrink-0 w-1.5 h-1.5 bg-blue-600 rounded-full mt-2"></span>
            <span>You can regenerate summaries to get different perspectives</span>
          </li>
        </ul>
      </div>
    </div>
  )
}

export default Summary 