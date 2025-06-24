import React, { useState } from 'react'
import { FileText, MessageSquare, BarChart3, Settings } from 'lucide-react'
import DocumentUpload from './components/DocumentUpload'
import DocumentList from './components/DocumentList'
import ChatInterface from './components/ChatInterface'
import Summary from './components/Summary'

function App() {
  const [activeTab, setActiveTab] = useState('documents')
  const [selectedDocuments, setSelectedDocuments] = useState([])

  const tabs = [
    { id: 'documents', label: 'Documents', icon: FileText },
    { id: 'chat', label: 'Chat', icon: MessageSquare },
    { id: 'summary', label: 'Summary', icon: BarChart3 },
  ]

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-3">
              
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  Document Analyzer
                </h1>
                <p className="text-sm text-gray-500">
                  AI-powered document analysis with RAG
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">
                {selectedDocuments.length} document(s) selected
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center space-x-2 py-4 px-1 border-b-2 font-medium text-sm transition-colors duration-200 ${
                    activeTab === tab.id
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon className="h-4 w-4" />
                  <span>{tab.label}</span>
                </button>
              )
            })}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="flex-grow py-8 h-full">
        {activeTab === 'documents' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-full">
            <div className="lg:col-span-1">
              <DocumentList 
                selectedDocuments={selectedDocuments}
                onSelectionChange={setSelectedDocuments}
              />
            </div>
            <div className="lg:col-span-3">
              <DocumentUpload />
            </div>
          </div>
        )}

        {activeTab === 'chat' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-full">
            <div className="lg:col-span-1">
              <DocumentList 
                selectedDocuments={selectedDocuments}
                onSelectionChange={setSelectedDocuments}
              />
            </div>
            <div className="lg:col-span-3">
              <ChatInterface selectedDocuments={selectedDocuments} />
            </div>
          </div>
        )}

        {activeTab === 'summary' && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8 h-full">
            <div className="lg:col-span-1">
              <DocumentList 
                selectedDocuments={selectedDocuments}
                onSelectionChange={setSelectedDocuments}
              />
            </div>
            <div className="lg:col-span-3">
              <Summary selectedDocuments={selectedDocuments} />
            </div>
          </div>
        )}
      </main>
    </div>
  )
}

export default App 