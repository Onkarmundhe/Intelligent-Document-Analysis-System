import React, { useState } from 'react'
import { Send, MessageSquare, Bot, User, ExternalLink } from 'lucide-react'
import { chatAPI } from '../services/api'
import { useMutation } from 'react-query'

const ChatInterface = ({ selectedDocuments }) => {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])

  const chatMutation = useMutation(chatAPI.ask, {
    onSuccess: (response) => {
      setMessages(prev => [...prev, {
        type: 'assistant',
        content: response.answer,
        sources: response.sources,
        timestamp: new Date()
      }])
    },
    onError: (error) => {
      setMessages(prev => [...prev, {
        type: 'error',
        content: error.response?.data?.detail || 'Failed to get response',
        timestamp: new Date()
      }])
    }
  })

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!question.trim() || chatMutation.isLoading) return

    // Add user message
    const userMessage = {
      type: 'user',
      content: question,
      timestamp: new Date()
    }
    setMessages(prev => [...prev, userMessage])

    // Make API call
    chatMutation.mutate(question, selectedDocuments.length > 0 ? selectedDocuments : null)
    
    // Clear input
    setQuestion('')
  }

  const formatTime = (timestamp) => {
    return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }

  return (
    <div className="card flex flex-col w-full">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Chat with Documents</h2>
        {selectedDocuments.length > 0 && (
          <span className="text-sm text-primary-600">
            {selectedDocuments.length} document{selectedDocuments.length !== 1 ? 's' : ''} selected
          </span>
        )}
      </div>

      {selectedDocuments.length === 0 && (
        <div className="flex-1 flex items-center justify-center">
          <div className="text-center">
            <MessageSquare className="mx-auto h-12 w-12 text-gray-300 mb-4" />
            <p className="text-gray-500 text-sm">Select documents to start chatting</p>
            <p className="text-gray-400 text-xs mt-1">Choose documents from the sidebar</p>
          </div>
        </div>
      )}

      {selectedDocuments.length > 0 && (
        <>
          {/* Messages */}
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 min-h-0">
            {messages.length === 0 && (
              <div className="text-center py-8">
                <Bot className="mx-auto h-12 w-12 text-gray-300 mb-4" />
                <p className="text-gray-500 text-sm">Ask me anything about your documents!</p>
                <p className="text-gray-400 text-xs mt-1">
                  Try: "What is this document about?" or "Summarize the main points"
                </p>
              </div>
            )}

            {messages.map((message, index) => (
              <div key={index} className="flex items-start space-x-3">
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.type === 'user' 
                    ? 'bg-primary-600' 
                    : message.type === 'error'
                    ? 'bg-red-500'
                    : 'bg-gray-600'
                }`}>
                  {message.type === 'user' ? (
                    <User className="h-4 w-4 text-white" />
                  ) : (
                    <Bot className="h-4 w-4 text-white" />
                  )}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-sm font-medium text-gray-900">
                      {message.type === 'user' ? 'You' : message.type === 'error' ? 'Error' : 'AI Assistant'}
                    </span>
                    <span className="text-xs text-gray-500">
                      {formatTime(message.timestamp)}
                    </span>
                  </div>
                  
                  <div className={`text-sm ${
                    message.type === 'error' ? 'text-red-600' : 'text-gray-700'
                  }`}>
                    {message.content}
                  </div>
                </div>
              </div>
            ))}

            {chatMutation.isLoading && (
              <div className="flex items-start space-x-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-white" />
                </div>
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1">
                    <span className="text-sm font-medium text-gray-900">AI Assistant</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600"></div>
                    <span className="text-sm text-gray-500">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="flex space-x-2">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask a question about your documents..."
              className="input flex-1"
              disabled={chatMutation.isLoading}
            />
            <button
              type="submit"
              disabled={!question.trim() || chatMutation.isLoading}
              className="btn-primary px-4 py-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="h-4 w-4" />
            </button>
          </form>
        </>
      )}
    </div>
  )
}

export default ChatInterface 