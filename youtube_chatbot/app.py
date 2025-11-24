import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Page config
st.set_page_config(
    page_title="YouTube Chatbot",
    page_icon="🎥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
    }
    </style>
""", unsafe_allow_html=True)

def extract_video_id(url_or_id):
    """Extract video ID from YouTube URL or return as is"""
    if "youtube.com" in url_or_id or "youtu.be" in url_or_id:
        if "v=" in url_or_id:
            return url_or_id.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url_or_id:
            return url_or_id.split("youtu.be/")[1].split("?")[0]
    return url_or_id

@st.cache_data
def fetch_transcript(video_id):
    """Fetch YouTube transcript"""
    try:
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id)
        transcript = " ".join([snippet.text for snippet in result.snippets])
        return transcript, None
    except Exception as e:
        return None, str(e)

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

def format_chat_history(chat_history):
    """Format chat history for the prompt"""
    if not chat_history:
        return "No previous conversation."
    
    formatted = []
    for entry in chat_history[-5:]:
        formatted.append(f"User: {entry['question']}")
        formatted.append(f"Assistant: {entry['answer']}")
    return "\n".join(formatted)

def answer_question(llm, transcript_chunks, question, chat_history):
    """Answer a question using the chatbot with chat history"""
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
    
    response = llm.invoke(prompt)
    return response.content

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'transcript_loaded' not in st.session_state:
    st.session_state.transcript_loaded = False
if 'transcript_chunks' not in st.session_state:
    st.session_state.transcript_chunks = []
if 'video_id' not in st.session_state:
    st.session_state.video_id = ""

# Header
st.title("🎥 YouTube Chatbot")
st.markdown("Ask questions about any YouTube video using AI")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    video_input = st.text_input(
        "YouTube URL or Video ID",
        value="VGFpV3Qj4as",
        help="Enter a YouTube URL or video ID"
    )
    
    if st.button("Load Video", type="primary"):
        video_id = extract_video_id(video_input)
        
        with st.spinner("Fetching transcript..."):
            transcript, error = fetch_transcript(video_id)
            
            if error:
                st.error(f"❌ Error: {error}")
                st.session_state.transcript_loaded = False
            else:
                st.session_state.transcript_chunks = split_transcript(transcript)
                st.session_state.transcript_loaded = True
                st.session_state.video_id = video_id
                st.session_state.chat_history = []
                st.success(f"✅ Loaded {len(st.session_state.transcript_chunks)} chunks!")
    
    st.divider()
    
    if st.session_state.transcript_loaded:
        st.success(f"📹 Video ID: {st.session_state.video_id}")
        st.info(f"💬 Messages: {len(st.session_state.chat_history)}")
        
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    st.divider()
    st.markdown("### About")
    st.markdown("This chatbot uses Groq AI to answer questions about YouTube videos based on their transcripts.")

# Main chat interface
if not st.session_state.transcript_loaded:
    st.info("👈 Enter a YouTube URL or Video ID in the sidebar and click 'Load Video' to start chatting!")
else:
    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(message["question"])
        with st.chat_message("assistant"):
            st.write(message["answer"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about the video..."):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    llm = ChatGroq(
                        groq_api_key=GROQ_API_KEY,
                        model_name="llama-3.3-70b-versatile",
                        temperature=0.3
                    )
                    
                    answer = answer_question(
                        llm,
                        st.session_state.transcript_chunks,
                        prompt,
                        st.session_state.chat_history
                    )
                    
                    st.write(answer)
                    
                    # Add to chat history
                    st.session_state.chat_history.append({
                        'question': prompt,
                        'answer': answer
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error: {e}")
