# 🚀 Intelligent Document Analysis System - Setup Guide

This guide will help you set up the complete RAG-based document analysis system with React frontend, FastAPI backend, ChromaDB vector store, and Gemini AI.

## 📋 Prerequisites

- **Python 3.8+**
- **Node.js 16+**
- **Google AI Studio API Key** (free at https://makersuite.google.com/)
- **Git**
- **Docker & Docker Compose** (optional)

## 🔧 Setup Steps

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/)
2. Create a new API key
3. Copy the API key for later use

### 2. Clone and Setup Backend

```bash
# Navigate to your project directory
cd RAG

# Create backend virtual environment
cd backend
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy env.example .env  # On Windows
# cp env.example .env  # On macOS/Linux

# Edit .env file and add your Gemini API key
# GEMINI_API_KEY=your_api_key_here
```

### 3. Setup Frontend

```bash
# Navigate to frontend directory
cd ../frontend

# Install dependencies
npm install

# Create environment file
echo "VITE_API_URL=http://localhost:8000" > .env.local
```

### 4. Create Required Directories

```bash
# From project root
mkdir -p backend/uploads
mkdir -p backend/chroma_db
```

### 5. Start the Application

#### Option A: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
# Activate virtual environment if not already active
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate  # On Windows

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

#### Option B: Docker Compose

```bash
# From project root
# Create .env file with your API key
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Start entire stack
docker-compose up --build
```

## 🌐 Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📝 Testing the Setup

### 1. Upload a Document

1. Open http://localhost:3000
2. Click "Upload Document" in the sidebar
3. Select a PDF, DOCX, or TXT file
4. Wait for processing to complete

### 2. Ask Questions

1. Select your uploaded document
2. Go to "Chat" tab
3. Ask questions like:
   - "What is this document about?"
   - "Summarize the main points"
   - "What are the key findings?"

### 3. Generate Summary

1. Select your document
2. Go to "Summary" tab
3. Click "Generate Summary"

## 🔍 Troubleshooting

### Common Issues

**1. Gemini API Key Not Working**
- Verify your API key is correct
- Check if you have free quota remaining
- Ensure the key is properly set in .env file

**2. ChromaDB Issues**
- Delete `backend/chroma_db` folder and restart
- Check Python version (needs 3.8+)

**3. File Upload Errors**
- Check file size (max 10MB)
- Verify file format (PDF, DOCX, TXT, MD)
- Ensure backend is running

**4. CORS Errors**
- Verify frontend is running on correct port
- Check CORS_ORIGINS in backend/.env

**5. Dependencies Issues**
```bash
# Backend
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules package-lock.json
npm install
```

### Logs and Debugging

**Backend Logs:**
```bash
# Check backend terminal for errors
# API logs appear in the terminal running uvicorn
```

**Frontend Logs:**
```bash
# Check browser console (F12)
# Check frontend terminal for build errors
```

## 📊 System Requirements

### Minimum Requirements
- **RAM**: 4GB
- **Storage**: 2GB free space
- **CPU**: 2 cores
- **Network**: Stable internet for Gemini API

### Recommended Requirements
- **RAM**: 8GB+
- **Storage**: 5GB+ free space
- **CPU**: 4+ cores
- **Network**: High-speed internet

## 🛠️ Development Tips

### Backend Development
```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (if you add them)
pytest

# Format code
black app/
```

### Frontend Development
```bash
# Run with hot reload
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

### Adding New Features

1. **New API Endpoint**: Add to `backend/app/api/`
2. **New Component**: Add to `frontend/src/components/`
3. **New Service**: Add to `backend/app/services/`

## 🚀 Deployment Options

### Free Deployment Options

**Backend:**
- Railway.app
- Render.com
- fly.io

**Frontend:**
- Vercel
- Netlify
- GitHub Pages

**Database:**
- ChromaDB runs embedded (no separate hosting needed)

### Deployment Environment Variables

**Backend:**
```env
GEMINI_API_KEY=your_production_key
CORS_ORIGINS=https://your-frontend-domain.com
```

**Frontend:**
```env
VITE_API_URL=https://your-backend-domain.com
```

## 📈 Performance Optimization

### For Large Documents
- Increase chunk size in `backend/app/core/config.py`
- Consider using GPU-accelerated embeddings
- Implement document preprocessing

### For High Traffic
- Add Redis for caching
- Implement rate limiting
- Use load balancer

## 🔒 Security Considerations

1. **API Key Security**: Never commit API keys to version control
2. **File Upload**: Validate file types and sizes
3. **CORS**: Configure proper CORS origins
4. **Rate Limiting**: Implement API rate limiting

## 🎯 Next Steps

1. **Add Authentication**: Implement user login/signup
2. **Persistent Storage**: Add PostgreSQL for metadata
3. **Advanced Analytics**: Add document analytics dashboard
4. **Mobile Support**: Create mobile-responsive design
5. **Batch Processing**: Add bulk document upload
6. **Integration**: Connect with cloud storage (Google Drive, Dropbox)

## 📞 Support

If you encounter issues:

1. Check this guide first
2. Look at the error logs
3. Verify all dependencies are installed
4. Check API key and permissions
5. Review the README.md for additional information

## 🎉 Success!

If everything is working correctly, you should see:
- ✅ Backend running on http://localhost:8000
- ✅ Frontend running on http://localhost:3000
- ✅ Document upload working
- ✅ Chat responses from Gemini AI
- ✅ Summary generation working

**Congratulations! Your Intelligent Document Analysis System is ready to use!** 🎊 