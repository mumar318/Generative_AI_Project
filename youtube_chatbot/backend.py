import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from youtube_transcript_api import YouTubeTranscriptApi
import uvicorn

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Initialize FastAPI app
app = FastAPI(
    title="YouTube Chatbot API",
    description="API for chatting with YouTube videos using AI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class VideoRequest(BaseModel):
    video_id: str

class ChatMessage(BaseModel):
    question: str
    answer: str

class ChatRequest(BaseModel):
    video_id: str
    question: str
    chat_history: Optional[List[ChatMessage]] = []

class TranscriptResponse(BaseModel):
    video_id: str
    transcript: str
    chunks_count: int
    length: int

class ChatResponse(BaseModel):
    answer: str
    video_id: str

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None

# In-memory storage (use Redis/DB in production)
transcripts_cache = {}

# Helper functions
def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from YouTube URL or return as is"""
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        if "v=" in url_or_id:
            return url_or_id.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url_or_id:
            return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id

def fetch_transcript(video_id: str) -> str:
    """Fetch YouTube transcript"""
    try:
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id)
        transcript = " ".join([snippet.text for snippet in result.snippets])
        return transcript
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch transcript: {str(e)}")

def split_transcript(transcript: str, chunk_size: int = 2000) -> List[str]:
    """Split transcript into chunks"""
    words = transcript.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_chunk.append(word)
        current_length += len(word) + 1
        
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def format_chat_history(chat_history: List[ChatMessage]) -> str:
    """Format chat history for the prompt"""
    if not chat_history:
        return "No previous conversation."
    
    formatted = []
    for entry in chat_history[-5:]:
        formatted.append(f"User: {entry.question}")
        formatted.append(f"Assistant: {entry.answer}")
    return "\n".join(formatted)

def answer_question(transcript_chunks: List[str], question: str, chat_history: List[ChatMessage]) -> str:
    """Answer a question using the chatbot"""
    context = "\n\n".join(transcript_chunks)
    
    if len(context) > 12000:
        context = context[:12000] + "..."
    
    history_text = format_chat_history(chat_history)
    
    prompt = f"""You are a helpful AI assistant that answers questions about a YouTube video based on its transcript.

VIDEO TRANSCRIPT CONTEXT:
{context}

PREVIOUS CONVERSATION:
{history_text}

CURRENT QUESTION: {question}

INSTRUCTIONS:
- Answer the question based on the video transcript context provided above
- Use information from previous conversation if relevant
- If the answer is not in the transcript, politely say so
- Be conversational and helpful
- Keep answers concise but informative

ANSWER:"""
    
    try:
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="llama-3.3-70b-versatile",
            temperature=0.3
        )
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate answer: {str(e)}")

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "YouTube Chatbot API",
        "version": "1.0.0",
        "endpoints": {
            "POST /load-video": "Load a YouTube video transcript",
            "POST /chat": "Chat with the loaded video",
            "GET /video/{video_id}": "Get cached transcript info",
            "DELETE /video/{video_id}": "Clear cached transcript"
        }
    }

@app.post("/load-video", response_model=TranscriptResponse)
async def load_video(request: VideoRequest):
    """Load and cache a YouTube video transcript"""
    video_id = extract_video_id(request.video_id)
    
    # Check cache
    if video_id in transcripts_cache:
        cached = transcripts_cache[video_id]
        return TranscriptResponse(
            video_id=video_id,
            transcript=cached["transcript"][:500] + "...",
            chunks_count=len(cached["chunks"]),
            length=len(cached["transcript"])
        )
    
    # Fetch transcript
    transcript = fetch_transcript(video_id)
    chunks = split_transcript(transcript)
    
    # Cache it
    transcripts_cache[video_id] = {
        "transcript": transcript,
        "chunks": chunks
    }
    
    return TranscriptResponse(
        video_id=video_id,
        transcript=transcript[:500] + "...",
        chunks_count=len(chunks),
        length=len(transcript)
    )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with a loaded video"""
    video_id = extract_video_id(request.video_id)
    
    # Check if video is loaded
    if video_id not in transcripts_cache:
        raise HTTPException(
            status_code=404,
            detail=f"Video {video_id} not loaded. Please load the video first using /load-video"
        )
    
    # Get transcript chunks
    chunks = transcripts_cache[video_id]["chunks"]
    
    # Generate answer
    answer = answer_question(chunks, request.question, request.chat_history)
    
    return ChatResponse(
        answer=answer,
        video_id=video_id
    )

@app.get("/video/{video_id}")
async def get_video_info(video_id: str):
    """Get cached video transcript info"""
    video_id = extract_video_id(video_id)
    
    if video_id not in transcripts_cache:
        raise HTTPException(status_code=404, detail=f"Video {video_id} not found in cache")
    
    cached = transcripts_cache[video_id]
    return {
        "video_id": video_id,
        "chunks_count": len(cached["chunks"]),
        "transcript_length": len(cached["transcript"]),
        "transcript_preview": cached["transcript"][:500] + "..."
    }

@app.delete("/video/{video_id}")
async def clear_video(video_id: str):
    """Clear cached video transcript"""
    video_id = extract_video_id(video_id)
    
    if video_id in transcripts_cache:
        del transcripts_cache[video_id]
        return {"message": f"Video {video_id} cleared from cache"}
    
    raise HTTPException(status_code=404, detail=f"Video {video_id} not found in cache")

@app.get("/cache/stats")
async def cache_stats():
    """Get cache statistics"""
    return {
        "cached_videos": len(transcripts_cache),
        "video_ids": list(transcripts_cache.keys())
    }

@app.delete("/cache/clear")
async def clear_cache():
    """Clear all cached transcripts"""
    count = len(transcripts_cache)
    transcripts_cache.clear()
    return {"message": f"Cleared {count} videos from cache"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
