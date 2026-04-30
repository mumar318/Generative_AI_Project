"""
Islamic Chatbot - Streamlit UI
RAG-based Quran Tafseer Chatbot with beautiful UI
"""

import streamlit as st
import os
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_core.documents import Document
import time

# Page config
st.set_page_config(
    page_title="Islamic Chatbot - تفسیر ابن کثیر",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better Urdu support and Islamic theme
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    .urdu-text {
        font-family: 'Noto Nastaliq Urdu', 'Arial Unicode MS', sans-serif;
        font-size: 1.2rem;
        line-height: 1.8;
        text-align: right;
        direction: rtl;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #2E8B57;
    }
    .user-message {
        background-color: #f0f8f0;
        border-left-color: #4CAF50;
    }
    .bot-message {
        background-color: #f8f9fa;
        border-left-color: #2E8B57;
    }
    .sidebar .sidebar-content {
        background-color: #f8f9fa;
    }
    .stButton > button {
        background-color: #2E8B57;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #228B22;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot_ready' not in st.session_state:
    st.session_state.chatbot_ready = False
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

@st.cache_resource
def load_chatbot():
    """Load and initialize the chatbot"""
    try:
        # Load environment
        try:
            groq_api_key = st.secrets["GROQ_API_KEY"]
        except:
            load_dotenv()
            groq_api_key = os.getenv('GROQ_API_KEY')
        # Load sample text
        with open('sample_tafseer.txt', 'r', encoding='utf-8') as f:
            text = f.read()
        
        # Create chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n", "\n", "۔", " "]
        )
        
        docs = [Document(page_content=text)]
        chunks = text_splitter.split_documents(docs)
        
        # Create embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Create vector store
        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="./streamlit_chroma_db"
        )
        
        # Setup LLM
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2048
        )
        
        # Create RAG chain
        prompt_template = """آپ ایک اسلامی چیٹ بوٹ ہیں جو قرآن پاک کی تفسیر ابن کثیر سے سوالات کے جوابات دیتے ہیں۔

Context (سیاق و سباق):
{context}

Question (سوال): {question}

Instructions:
- دیے گئے context سے متعلقہ آیات، ترجمہ اور تفسیر فراہم کریں
- جواب اردو میں دیں
- آیات کو عربی میں بھی شامل کریں اگر دستیاب ہوں
- تفصیلی اور واضح جواب دیں

Answer (جواب):"""
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
        
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        return rag_chain, retriever
        
    except Exception as e:
        st.error(f"❌ Error loading chatbot: {str(e)}")
        return None, None

def main():
    # Header
    st.markdown('<h1 class="main-header">🕌 Islamic Chatbot - اسلامی چیٹ بوٹ</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #666; font-size: 1.1rem;">تفسیر ابن کثیر سے سوالات کے جوابات | Tafseer Ibn Kathir Q&A</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📚 About")
        st.markdown("""
        **Islamic Chatbot** uses:
        - 🤖 Groq API (Llama 3.3 70B)
        - 📖 Tafseer Ibn Kathir
        - 🔍 RAG (Retrieval Augmented Generation)
        - 🌐 Multilingual Support (Urdu/Arabic)
        """)
        
        st.markdown("### 💡 Sample Questions")
        sample_questions = [
            "سورہ فاتحہ کی تفسیر بتائیں",
            "بسم اللہ الرحمن الرحیم کا کیا مطلب ہے؟",
            "آیت الکرسی کے بارے میں بتائیں",
            "سورہ الاخلاص کی تفسیر کریں"
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(f"📝 {question}", key=f"sample_{i}"):
                st.session_state["input_value"] = question
                st.rerun()
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()
    
    # Initialize chatbot
    if not st.session_state.chatbot_ready:
        with st.spinner("🚀 Loading Islamic Chatbot..."):
            rag_chain, retriever = load_chatbot()
            if rag_chain:
                st.session_state.rag_chain = rag_chain
                st.session_state.retriever = retriever
                st.session_state.chatbot_ready = True
                st.success("✅ Chatbot loaded successfully!")
            else:
                st.error("❌ Failed to load chatbot")
                return
    
    # Chat interface
    st.markdown("### 💬 Chat Interface")
    
    # Display chat history
    for i, (question, answer) in enumerate(st.session_state.chat_history):
        # User message
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong><br>
            <div class="urdu-text">{question}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Bot message
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Islamic Chatbot:</strong><br>
            <div class="urdu-text">{answer}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Input area
    col1, col2 = st.columns([4, 1])

    with col1:
        user_input = st.text_input(
            "آپ کا سوال (Your Question):",
            placeholder="سورہ فاتحہ کی تفسیر بتائیں...",
            value=st.session_state.get("input_value", ""),
            key="user_input_box"
        )

    with col2:
        ask_button = st.button("📤 Ask", type="primary")

    # Process question
    if ask_button and user_input.strip():
        if st.session_state.chatbot_ready:
            with st.spinner("🤔 Thinking..."):
                try:
                    answer = st.session_state.rag_chain.invoke(user_input)
                    st.session_state.chat_history.append((user_input, answer))
                    st.session_state["input_value"] = ""
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
        else:
            st.error("❌ Chatbot not ready. Please wait for initialization.")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 0.9rem;">
        <p>🌙 May Allah bless you | اللہ آپ کو برکت دے</p>
        <p>Built with ❤️ using Streamlit, LangChain & Groq</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()