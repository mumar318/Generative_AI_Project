import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

# Video ID (extracted from v=VGFpV3Qj4as&t=1s)
VIDEO_ID = "VGFpV3Qj4as"

def fetch_transcript(video_id):
    """Fetch YouTube transcript"""
    try:
        api = YouTubeTranscriptApi()
        result = api.fetch(video_id)
        transcript = " ".join([snippet.text for snippet in result.snippets])
        print(f"✅ Transcript fetched! Length: {len(transcript)} characters\n")
        return transcript
    except Exception as e:
        print(f"❌ Error fetching transcript: {e}")
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
    
    print(f"✅ Transcript split into {len(chunks)} chunks\n")
    return chunks

def create_chatbot(transcript_chunks):
    """Create chatbot with Groq LLM"""
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.3
    )
    return llm, transcript_chunks

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
    # Use all chunks as context (simplified approach)
    context = "\n\n".join(transcript_chunks)
    
    # Truncate context if too long (keep first 12000 chars to leave room for history)
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
    print("🎥 YouTube Chatbot - Fetching transcript...\n")
    
    # Fetch transcript
    transcript = fetch_transcript(VIDEO_ID)
    if not transcript:
        return
    
    # Split transcript
    print("📚 Splitting transcript...")
    chunks = split_transcript(transcript)
    
    # Create chatbot
    print("🤖 Initializing chatbot with Groq...\n")
    llm, transcript_chunks = create_chatbot(chunks)
    
    print("=" * 60)
    print("💬 Chatbot ready! Ask questions about the video.")
    print("Type 'quit' or 'exit' to stop.")
    print("Type 'history' to see conversation history.")
    print("=" * 60 + "\n")
    
    # Initialize chat history
    chat_history = []
    
    # Chat loop
    while True:
        question = input("You: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("\n👋 Goodbye!")
            break
        
        if question.lower() == 'history':
            if chat_history:
                print("\n📜 Chat History:")
                print("-" * 60)
                for i, entry in enumerate(chat_history, 1):
                    print(f"\n{i}. Q: {entry['question']}")
                    print(f"   A: {entry['answer'][:100]}..." if len(entry['answer']) > 100 else f"   A: {entry['answer']}")
                print("-" * 60 + "\n")
            else:
                print("\n📜 No chat history yet.\n")
            continue
        
        if not question:
            continue
        
        try:
            answer = answer_question(llm, transcript_chunks, question, chat_history)
            print(f"\n🤖 Bot: {answer}\n")
            
            # Add to chat history
            chat_history.append({
                'question': question,
                'answer': answer
            })
            
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    main()
