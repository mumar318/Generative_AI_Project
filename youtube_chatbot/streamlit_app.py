import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from youtube_transcript_api import YouTubeTranscriptApi
import re

# Suppress TensorFlow warnings
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def extract_video_id(url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def fetch_transcript(video_id):
    """Fetch YouTube transcript with fallback language support"""
    st.info(f"🔍 Trying to fetch transcript for video ID: {video_id}")
    
    try:
        # Create API instance
        api = YouTubeTranscriptApi()
        
        # Try different language codes in order of preference
        language_codes = ['en', 'en-US', 'en-GB', 'hi', 'es', 'fr', 'de', 'ja', 'ko', 'zh']
        
        for lang in language_codes:
            try:
                st.info(f"Trying language: {lang}")
                result = api.fetch(video_id, languages=[lang])
                text = " ".join([snippet.text for snippet in result.snippets])
                if lang == 'en' or lang.startswith('en'):
                    st.success("✅ English transcript loaded")
                else:
                    st.warning(f"⚠️ Using {lang} transcript (English not available)")
                return text
            except Exception as e:
                st.warning(f"Language {lang} failed: {str(e)[:100]}")
                continue
        
        # If no specific language works, try getting any available transcript
        try:
            st.info("Trying to get any available transcript...")
            result = api.fetch(video_id)
            text = " ".join([snippet.text for snippet in result.snippets])
            st.warning("⚠️ Using default transcript")
            return text
        except Exception as e:
            st.error(f"Default transcript failed: {e}")
        
        st.error("❌ No transcripts available for this video")
        return None
        
    except Exception as e:
        st.error(f"❌ Error fetching transcript: {e}")
        return None

def split_transcript(transcript, chunk_size=2000):
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

def create_chatbot():
    """Create chatbot with Groq LLM"""
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not found in .env file")
        return None
    
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )
    return llm

def format_chat_history(chat_history):
    """Format chat history for the prompt"""
    if not chat_history:
        return "No previous conversation."
    
    formatted = []
    for entry in chat_history[-5:]:  # Keep last 5 exchanges
        formatted.append(f"User: {entry['question']}")
        formatted.append(f"Assistant: {entry['answer']}")
    return "\n".join(formatted)

def answer_question(llm, transcript_chunks, question, chat_history):
    """Answer a question using the chatbot with chat history"""
    # Use all chunks as context
    context = "\n\n".join(transcript_chunks)
    
    # Truncate context if too long
    if len(context) > 12000:
        context = context[:12000] + "..."
    
    # Format chat history
    history_text = format_chat_history(chat_history)
    
    # Enhanced prompt template with chat history
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
    
    response = llm.invoke(prompt)
    return response.content

def main():
    st.set_page_config(
        page_title="YouTube Chatbot",
        page_icon="🎥",
        layout="wide"
    )
    
    st.title("🎥 YouTube Video Chatbot")
    st.markdown("Ask questions about any YouTube video!")
    
    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'transcript_chunks' not in st.session_state:
        st.session_state.transcript_chunks = None
    if 'video_id' not in st.session_state:
        st.session_state.video_id = None
    if 'llm' not in st.session_state:
        st.session_state.llm = None
    
    # Sidebar for video input
    with st.sidebar:
        st.header("📹 Video Setup")
        
        # YouTube URL input
        youtube_url = st.text_input(
            "Enter YouTube URL:",
            placeholder="https://www.youtube.com/watch?v=..."
        )
        
        if st.button("Load Video", type="primary"):
            if youtube_url:
                video_id = extract_video_id(youtube_url)
                if video_id:
                    with st.spinner("Fetching transcript..."):
                        # First, show available transcripts
                        try:
                            # Try to get available languages (simplified approach)
                            api = YouTubeTranscriptApi()
                            available_langs = []
                            test_langs = ['en', 'hi', 'es', 'fr', 'de', 'ja', 'ko', 'zh']
                            for lang in test_langs:
                                try:
                                    api.fetch(video_id, languages=[lang])
                                    available_langs.append(lang)
                                except:
                                    pass
                            
                            if available_langs:
                                st.info(f"📋 Available languages: {', '.join(available_langs)}")
                        except:
                            pass
                        
                        # Then fetch the transcript
                        transcript = fetch_transcript(video_id)
                        if transcript:
                            st.session_state.transcript_chunks = split_transcript(transcript)
                            st.session_state.video_id = video_id
                            st.session_state.llm = create_chatbot()
                            st.session_state.chat_history = []  # Reset chat history
                            st.success(f"✅ Video loaded! Transcript split into {len(st.session_state.transcript_chunks)} chunks")
                        else:
                            st.error("Failed to fetch transcript")
                else:
                    st.error("Invalid YouTube URL")
            else:
                st.error("Please enter a YouTube URL")
        
        # Show current video info
        if st.session_state.video_id:
            st.success(f"📺 Current Video ID: {st.session_state.video_id}")
            st.markdown(f"[Watch on YouTube](https://www.youtube.com/watch?v={st.session_state.video_id})")
        
        # Chat history management
        st.header("💬 Chat History")
        if st.button("Clear History"):
            st.session_state.chat_history = []
            st.rerun()
        
        if st.session_state.chat_history:
            st.write(f"Messages: {len(st.session_state.chat_history)}")
    
    # Main chat interface
    if st.session_state.transcript_chunks and st.session_state.llm:
        # Display chat history
        for i, entry in enumerate(st.session_state.chat_history):
            with st.chat_message("user"):
                st.write(entry['question'])
            with st.chat_message("assistant"):
                st.write(entry['answer'])
        
        # Chat input
        if question := st.chat_input("Ask a question about the video..."):
            # Display user message
            with st.chat_message("user"):
                st.write(question)
            
            # Generate and display assistant response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        answer = answer_question(
                            st.session_state.llm,
                            st.session_state.transcript_chunks,
                            question,
                            st.session_state.chat_history
                        )
                        st.write(answer)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            'question': question,
                            'answer': answer
                        })
                    except Exception as e:
                        st.error(f"Error: {e}")
    
    else:
        st.info("👈 Please load a YouTube video from the sidebar to start chatting!")
        
        # Show example
        st.markdown("### How to use:")
        st.markdown("1. Enter a YouTube URL in the sidebar")
        st.markdown("2. Click 'Load Video' to fetch the transcript")
        st.markdown("3. Start asking questions about the video content!")
        
        st.markdown("### Example URLs:")
        st.code("https://www.youtube.com/watch?v=VGFpV3Qj4as")
        st.code("https://youtu.be/VGFpV3Qj4as")

if __name__ == "__main__":
    main()