import React, { useState } from 'react'
import { Upload, File, AlertCircle } from 'lucide-react'
import { documentAPI } from '../services/api'
import { useMutation, useQueryClient } from 'react-query'

const DocumentUpload = () => {
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError] = useState('')
  const queryClient = useQueryClient()

  const uploadMutation = useMutation(documentAPI.upload, {
    onSuccess: () => {
      queryClient.invalidateQueries('documents')
      setError('')
    },
    onError: (error) => {
      setError(error.response?.data?.detail || 'Upload failed')
    }
  })

  const handleFileUpload = async (file) => {
    if (!file) return
    
    // Validate file type
    const allowedTypes = ['pdf', 'docx', 'txt', 'md']
    const fileExtension = file.name.split('.').pop().toLowerCase()
    
    if (!allowedTypes.includes(fileExtension)) {
      setError(`File type .${fileExtension} not supported. Allowed types: ${allowedTypes.join(', ')}`)
      return
    }
    
    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
      setError('File size must be less than 10MB')
      return
    }
    
    uploadMutation.mutate(file)
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    handleFileUpload(file)
  }

  const handleFileInput = (e) => {
    const file = e.target.files[0]
    handleFileUpload(file)
  }

  return (
    <div className="card">
      <h3 className="font-semibold text-gray-900 mb-4">Upload Document</h3>
      
      <div
        className={`border-2 border-dashed rounded-lg p-6 text-center transition-colors ${
          isDragging
            ? 'border-primary-500 bg-primary-50'
            : 'border-gray-300 hover:border-gray-400'
        }`}
        onDragOver={(e) => {
          e.preventDefault()
          setIsDragging(true)
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
      >
        <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
        <p className="text-sm text-gray-600 mb-2">
          Drag and drop your document here, or
        </p>
        <label className="btn-primary cursor-pointer">
          Choose File
          <input
            type="file"
            className="hidden"
            accept=".pdf,.docx,.txt,.md"
            onChange={handleFileInput}
            disabled={uploadMutation.isLoading}
          />
        </label>
        <p className="text-xs text-gray-500 mt-2">
          Supports PDF, DOCX, TXT, MD (max 10MB)
        </p>
      </div>

      {uploadMutation.isLoading && (
        <div className="mt-4 p-3 bg-blue-50 rounded-lg">
          <div className="flex items-center">
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-primary-600 mr-2"></div>
            <span className="text-sm text-primary-700">Processing document...</span>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 p-3 bg-red-50 rounded-lg">
          <div className="flex items-center">
            <AlertCircle className="h-4 w-4 text-red-500 mr-2" />
            <span className="text-sm text-red-700">{error}</span>
          </div>
        </div>
      )}

      {uploadMutation.isSuccess && (
        <div className="mt-4 p-3 bg-green-50 rounded-lg">
          <span className="text-sm text-green-700">Document uploaded successfully!</span>
        </div>
      )}
    </div>
  )
}

export default DocumentUpload 