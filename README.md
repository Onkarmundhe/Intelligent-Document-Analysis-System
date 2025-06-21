# 🚀 Intelligent Document Analysis System

A powerful RAG-based application that allows users to upload documents (PDFs, DOCX, TXT) and ask intelligent questions about their content using Google's Gemini AI.

## 🌟 Features

- **Multi-format Document Support**: PDF, DOCX, TXT, and more
- **Intelligent Q&A**: Ask questions about document content using Gemini AI
- **Document Summarization**: Get AI-powered summaries of uploaded documents
- **Citation Tracking**: Get exact page/section references for answers
- **Multi-document Comparison**: Compare content across multiple documents
- **Semantic Search**: Find relevant sections using vector similarity
- **Chat History**: Maintain conversation context
- **Document Management**: Upload, view, and delete documents

## 🏗️ Architecture

```
Frontend (React) ←→ Backend (FastAPI) ←→ Vector DB (ChromaDB) ←→ Gemini API
                           ↓
                    Document Processing
                    (PyPDF2, python-docx)
```

## 📁 Project Structure

```
intelligent-doc-analyzer/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI application
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── document.py         # Document models
│   │   │   └── chat.py             # Chat models
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── document_processor.py  # Document parsing
│   │   │   ├── vector_store.py     # ChromaDB operations
│   │   │   ├── gemini_service.py   # Gemini AI integration
│   │   │   └── rag_service.py      # RAG pipeline
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── documents.py        # Document endpoints
│   │   │   └── chat.py             # Chat endpoints
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   ├── config.py           # Configuration
│   │   │   └── dependencies.py     # Dependencies
│   │   └── utils/
│   │       ├── __init__.py
│   │       └── helpers.py          # Helper functions
│   ├── uploads/                    # Document storage
│   ├── chroma_db/                  # ChromaDB storage
│   ├── requirements.txt
│   ├── .env.example
│   └── Dockerfile
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── DocumentUpload.jsx
│   │   │   ├── DocumentList.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── DocumentViewer.jsx
│   │   │   └── Summary.jsx
│   │   ├── services/
│   │   │   └── api.js              # API calls
│   │   ├── hooks/
│   │   │   └── useDocuments.js     # Custom hooks
│   │   ├── styles/
│   │   │   └── globals.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **ChromaDB** - Free vector database
- **Google Gemini API** - Free AI model (15 requests/minute)
- **PyPDF2** - PDF processing
- **python-docx** - DOCX processing
- **sentence-transformers** - Text embeddings
- **Uvicorn** - ASGI server

### Frontend
- **React** - Modern UI framework
- **Vite** - Fast build tool
- **Tailwind CSS** - Utility-first CSS
- **Axios** - HTTP client
- **React Query** - Data fetching

### Free Deployment Options
- **Backend**: Railway, Render, or fly.io
- **Frontend**: Vercel, Netlify
- **Database**: ChromaDB (embedded, no separate hosting needed)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Google AI Studio API key (free)

### Backend Setup

1. Clone and navigate to backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set up environment:
```bash
cp .env.example .env
# Add your Gemini API key to .env
```

3. Run backend:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

1. Navigate to frontend:
```bash
cd frontend
npm install
```

2. Run frontend:
```bash
npm run dev
```

## 🔧 Environment Variables

```env
# Backend (.env)
GEMINI_API_KEY=your_gemini_api_key_here
UPLOAD_DIR=uploads
CHROMA_PERSIST_DIR=chroma_db
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=pdf,docx,txt,md

# Frontend (.env.local)
VITE_API_URL=http://localhost:8000
```

## 📋 API Endpoints

### Documents
- `POST /api/documents/upload` - Upload document
- `GET /api/documents/` - List documents
- `DELETE /api/documents/{doc_id}` - Delete document
- `POST /api/documents/{doc_id}/summarize` - Generate summary

### Chat
- `POST /api/chat/ask` - Ask question about documents
- `GET /api/chat/history/{doc_id}` - Get chat history
- `DELETE /api/chat/history/{doc_id}` - Clear chat history

## 🎯 Key Features Implementation

### 1. Document Processing
- Extract text from multiple formats
- Chunk text for optimal vector storage
- Generate embeddings using sentence-transformers

### 2. RAG Pipeline
- Store document chunks in ChromaDB
- Perform semantic search for relevant context
- Generate responses using Gemini with context

### 3. Citation Tracking
- Map chunks to original document sections
- Return page numbers and exact text locations

### 4. Multi-document Comparison
- Cross-document semantic search
- Identify similar content across files
- Generate comparative analysis

## 🚀 Deployment

### Using Docker Compose
```bash
docker-compose up --build
```

### Individual Deployment
- **Backend**: Deploy to Railway/Render
- **Frontend**: Deploy to Vercel/Netlify

## 📊 Performance Considerations

- **File Size Limit**: 10MB per document
- **Concurrent Users**: Optimized for 10-50 users
- **Response Time**: < 3 seconds for queries
- **Storage**: ChromaDB handles 100k+ document chunks

## 🔮 Future Enhancements

- [ ] OCR for scanned PDFs
- [ ] PowerPoint support
- [ ] Real-time collaboration
- [ ] Advanced analytics dashboard
- [ ] Integration with cloud storage (Google Drive, Dropbox)
- [ ] Mobile app
- [ ] Multi-language support

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

For issues and questions:
- Create GitHub issue
- Check documentation
- Review API endpoints at `http://localhost:8000/docs` 