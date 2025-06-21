import google.generativeai as genai
from typing import List, Dict, Any
import asyncio
import time
from app.core.config import settings

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    async def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using Gemini AI with optional context."""
        try:
            full_prompt = f"""
            Context: {context}
            
            Question: {prompt}
            
            Please provide a comprehensive answer based on the context provided. 
            If the context doesn't contain relevant information, say so clearly.
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, full_prompt
            )
            return response.text
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I apologize, but I encountered an error while processing your request."
    
    async def generate_summary(self, text: str, max_length: int = 500) -> Dict[str, Any]:
        """Generate document summary with key points."""
        try:
            prompt = f"""
            Please analyze the following document and provide:
            1. A concise summary (max {max_length} words)
            2. 5-7 key points from the document
            3. Main themes or topics covered
            
            Document text:
            {text[:8000]}  # Limit text to avoid token limits
            
            Format your response as:
            SUMMARY: [your summary here]
            KEY_POINTS:
            - [point 1]
            - [point 2]
            - [etc.]
            THEMES: [main themes separated by commas]
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            # Parse the response
            response_text = response.text
            summary = ""
            key_points = []
            themes = []
            
            lines = response_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('SUMMARY:'):
                    summary = line.replace('SUMMARY:', '').strip()
                    current_section = 'summary'
                elif line.startswith('KEY_POINTS:'):
                    current_section = 'key_points'
                elif line.startswith('THEMES:'):
                    themes = [t.strip() for t in line.replace('THEMES:', '').split(',')]
                    current_section = 'themes'
                elif line.startswith('- ') and current_section == 'key_points':
                    key_points.append(line.replace('- ', ''))
                elif current_section == 'summary' and line:
                    summary += ' ' + line
            
            return {
                "summary": summary.strip(),
                "key_points": key_points,
                "themes": themes
            }
            
        except Exception as e:
            print(f"Error generating summary: {e}")
            return {
                "summary": "Unable to generate summary at this time.",
                "key_points": [],
                "themes": []
            }
    
    async def compare_documents(self, doc_contents: List[str], doc_names: List[str]) -> Dict[str, Any]:
        """Compare multiple documents and find similarities/differences."""
        try:
            # Limit content length for each document
            limited_contents = [content[:3000] for content in doc_contents]
            
            prompt = f"""
            Compare the following documents and identify:
            1. Key similarities between them
            2. Major differences
            3. Common themes or topics
            4. Unique aspects of each document
            
            Documents:
            {chr(10).join([f"Document {i+1} ({doc_names[i]}): {content}" for i, content in enumerate(limited_contents)])}
            
            Format your response as:
            SIMILARITIES:
            - [similarity 1]
            - [similarity 2]
            
            DIFFERENCES:
            - [difference 1]
            - [difference 2]
            
            COMMON_THEMES: [themes separated by commas]
            """
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            # Parse response similar to summary
            response_text = response.text
            similarities = []
            differences = []
            common_themes = []
            
            lines = response_text.split('\n')
            current_section = None
            
            for line in lines:
                line = line.strip()
                if line.startswith('SIMILARITIES:'):
                    current_section = 'similarities'
                elif line.startswith('DIFFERENCES:'):
                    current_section = 'differences'
                elif line.startswith('COMMON_THEMES:'):
                    common_themes = [t.strip() for t in line.replace('COMMON_THEMES:', '').split(',')]
                elif line.startswith('- '):
                    if current_section == 'similarities':
                        similarities.append(line.replace('- ', ''))
                    elif current_section == 'differences':
                        differences.append(line.replace('- ', ''))
            
            return {
                "similarities": similarities,
                "differences": differences,
                "common_themes": common_themes
            }
            
        except Exception as e:
            print(f"Error comparing documents: {e}")
            return {
                "similarities": [],
                "differences": [],
                "common_themes": []
            }
    
    async def extract_key_information(self, text: str, query_type: str = "general") -> Dict[str, Any]:
        """Extract specific information based on query type."""
        try:
            if query_type == "names":
                prompt = f"Extract all person names, organization names, and location names from this text: {text[:4000]}"
            elif query_type == "dates":
                prompt = f"Extract all dates, time periods, and temporal references from this text: {text[:4000]}"
            elif query_type == "numbers":
                prompt = f"Extract all important numbers, statistics, and quantitative data from this text: {text[:4000]}"
            else:
                prompt = f"Extract the most important information and facts from this text: {text[:4000]}"
            
            response = await asyncio.to_thread(
                self.model.generate_content, prompt
            )
            
            return {"extracted_info": response.text}
            
        except Exception as e:
            print(f"Error extracting information: {e}")
            return {"extracted_info": "Unable to extract information at this time."}

# Global instance
gemini_service = GeminiService() 