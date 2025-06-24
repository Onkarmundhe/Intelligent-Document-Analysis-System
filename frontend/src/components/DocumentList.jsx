import React from 'react'
import { FileText, Trash2, Check } from 'lucide-react'
import { documentAPI } from '../services/api'
import { useQuery, useMutation, useQueryClient } from 'react-query'

const DocumentList = ({ selectedDocuments, onSelectionChange }) => {
  const queryClient = useQueryClient()

  // Fetch documents
  const { data: documents = [], isLoading, error } = useQuery(
    'documents',
    documentAPI.list,
    {
      refetchOnWindowFocus: false,
    }
  )

  // Delete mutation
  const deleteMutation = useMutation(documentAPI.delete, {
    onSuccess: () => {
      queryClient.invalidateQueries('documents')
    }
  })

  const handleToggleSelection = (documentId) => {
    const isSelected = selectedDocuments.includes(documentId)
    if (isSelected) {
      onSelectionChange(selectedDocuments.filter(id => id !== documentId))
    } else {
      onSelectionChange([...selectedDocuments, documentId])
    }
  }

  const handleDelete = (documentId, e) => {
    e.stopPropagation()
    if (window.confirm('Are you sure you want to delete this document?')) {
      deleteMutation.mutate(documentId)
      // Remove from selection if selected
      onSelectionChange(selectedDocuments.filter(id => id !== documentId))
    }
  }

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
  }

  const getFileIcon = (filename) => {
    const extension = filename.split('.').pop().toLowerCase()
    const iconClass = "h-5 w-5"
    
    switch (extension) {
      case 'pdf':
        return <FileText className={`${iconClass} text-red-500`} />
      case 'docx':
        return <FileText className={`${iconClass} text-blue-500`} />
      case 'txt':
      case 'md':
        return <FileText className={`${iconClass} text-gray-500`} />
      default:
        return <FileText className={`${iconClass} text-gray-400`} />
    }
  }

  if (isLoading) {
    return (
      <div className="card">
        <h3 className="font-semibold text-gray-900 mb-4">Documents</h3>
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="h-16 bg-gray-200 rounded-lg"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="card">
        <h3 className="font-semibold text-gray-900 mb-4">Documents</h3>
        <div className="text-center py-8">
          <p className="text-red-500 text-sm">Error loading documents</p>
        </div>
      </div>
    )
  }

  return (
    <div className="card h-full">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-semibold text-gray-900">Documents</h3>
        <span className="text-sm text-gray-500">
          {documents.length} document{documents.length !== 1 ? 's' : ''}
        </span>
      </div>

      {documents.length === 0 ? (
        <div className="text-center py-8">
          <FileText className="mx-auto h-12 w-12 text-gray-300 mb-4" />
          <p className="text-gray-500 text-sm">No documents uploaded yet</p>
          <p className="text-gray-400 text-xs mt-1">Upload your first document to get started</p>
        </div>
      ) : (
        <div className="space-y-2">
          {documents.map((doc) => {
            const isSelected = selectedDocuments.includes(doc.id)
            return (
              <div
                key={doc.id}
                onClick={() => handleToggleSelection(doc.id)}
                className={`p-3 rounded-lg border cursor-pointer transition-all ${
                  isSelected
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-3 flex-1 min-w-0">
                    <div className="flex items-center space-x-2">
                      {getFileIcon(doc.filename)}
                      {isSelected && (
                        <Check className="h-4 w-4 text-primary-600" />
                      )}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {doc.filename}
                      </p>
                      <div className="flex items-center space-x-2 text-xs text-gray-500">
                        <span>{formatFileSize(doc.size)}</span>
                        {doc.word_count && (
                          <>
                            <span>•</span>
                            <span>{doc.word_count.toLocaleString()} words</span>
                          </>
                        )}
                      </div>
                    </div>
                  </div>
                  <button
                    onClick={(e) => handleDelete(doc.id, e)}
                    className="p-1 text-gray-400 hover:text-red-500 transition-colors"
                    disabled={deleteMutation.isLoading}
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {selectedDocuments.length > 0 && (
        <div className="mt-4 p-3 bg-primary-50 rounded-lg">
          <p className="text-sm text-primary-700">
            {selectedDocuments.length} document{selectedDocuments.length !== 1 ? 's' : ''} selected
          </p>
          <button
            onClick={() => onSelectionChange([])}
            className="text-xs text-primary-600 hover:text-primary-700 mt-1"
          >
            Clear selection
          </button>
        </div>
      )}
    </div>
  )
}

export default DocumentList 