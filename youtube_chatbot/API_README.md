# YouTube Chatbot API Documentation

## Overview
FastAPI backend for chatting with YouTube videos using AI (Groq LLM).

## Installation

```bash
pip install -r requirements.txt
```

## Running the API

```bash
python backend.py
```

Or with uvicorn:

```bash
uvicorn backend:app --reload --host 0.0.0.0 --port 8000
```

API will be available at: `http://localhost:8000`

Interactive docs: `http://localhost:8000/docs`

## API Endpoints

### 1. Root
**GET** `/`

Get API information and available endpoints.

**Response:**
```json
{
  "message": "YouTube Chatbot API",
  "version": "1.0.0",
  "endpoints": {...}
}
```

### 2. Load Video
**POST** `/load-video`

Load and cache a YouTube video transcript.

**Request Body:**
```json
{
  "video_id": "VGFpV3Qj4as"
}
```

**Response:**
```json
{
  "video_id": "VGFpV3Qj4as",
  "transcript": "First 500 chars...",
  "chunks_count": 26,
  "length": 50696
}
```

### 3. Chat
**POST** `/chat`

Ask questions about a loaded video.

**Request Body:**
```json
{
  "video_id": "VGFpV3Qj4as",
  "question": "What is this video about?",
  "chat_history": [
    {
      "question": "Previous question",
      "answer": "Previous answer"
    }
  ]
}
```

**Response:**
```json
{
  "answer": "This video is about...",
  "video_id": "VGFpV3Qj4as"
}
```

### 4. Get Video Info
**GET** `/video/{video_id}`

Get cached video transcript information.

**Response:**
```json
{
  "video_id": "VGFpV3Qj4as",
  "chunks_count": 26,
  "transcript_length": 50696,
  "transcript_preview": "First 500 chars..."
}
```

### 5. Clear Video
**DELETE** `/video/{video_id}`

Remove a video from cache.

**Response:**
```json
{
  "message": "Video VGFpV3Qj4as cleared from cache"
}
```

### 6. Cache Stats
**GET** `/cache/stats`

Get cache statistics.

**Response:**
```json
{
  "cached_videos": 1,
  "video_ids": ["VGFpV3Qj4as"]
}
```

### 7. Clear Cache
**DELETE** `/cache/clear`

Clear all cached transcripts.

**Response:**
```json
{
  "message": "Cleared 1 videos from cache"
}
```

## Testing

Run the test script:

```bash
python test_api.py
```

## Example Usage with Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Load video
response = requests.post(
    f"{BASE_URL}/load-video",
    json={"video_id": "VGFpV3Qj4as"}
)
print(response.json())

# Chat
response = requests.post(
    f"{BASE_URL}/chat",
    json={
        "video_id": "VGFpV3Qj4as",
        "question": "What is this video about?",
        "chat_history": []
    }
)
print(response.json()["answer"])
```

## Example Usage with cURL

```bash
# Load video
curl -X POST "http://localhost:8000/load-video" \
  -H "Content-Type: application/json" \
  -d '{"video_id": "VGFpV3Qj4as"}'

# Chat
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "VGFpV3Qj4as",
    "question": "What is this video about?",
    "chat_history": []
  }'
```

## Features

- ✅ Load YouTube video transcripts
- ✅ Chat with videos using Groq AI
- ✅ Conversation history support
- ✅ In-memory caching
- ✅ CORS enabled
- ✅ Interactive API docs (Swagger)
- ✅ Error handling
- ✅ Video ID extraction from URLs

## Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Notes

- Transcripts are cached in memory (use Redis/DB for production)
- CORS is enabled for all origins (configure for production)
- Default model: `llama-3.3-70b-versatile`
