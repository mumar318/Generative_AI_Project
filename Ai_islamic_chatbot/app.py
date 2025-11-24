"""
Islamic Chatbot - Streamlit UI
Beautiful web interface for Quran Tafseer chatbot
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

# Page configuration
st.set_page_config(
    page_title="Islamic Chatbot - تفسیر ابن کثیر",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better Urdu text display
st.markdown("""
<style>
    .main {
        background-color: #f5f5f5;
    }
    .stTextInput > div > div > input {
        font-size: 18px;
        direction: rtl;
        text-align: right;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    .bot-message {
        background-color: #f1f8e9;
        border-left: 5px solid #8bc34a;
    }
    .urdu-text {
        font-size: 20px;
        line-height: 2;
        direction: rtl;
        text-align: right;
        font-family: 'Noto Nastaliq Urdu', 'Jameel Noori Nastaleeq', serif;
    }
    h1, h2, h3 {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'rag_chain' not in st.session_state:
    st.session_state.rag_chain = None
if 'retriever' not in st.session_state:
    st.session_state.retriever = None

@st.cache_resource
def initialize_chatbot():
    """Initialize the RAG chatbot"""
    try:
        # Load environment
        load_dotenv()
        GROQ_API_KEY = os.getenv('GROQ_API_KEY')
        
        if not GROQ_API_KEY:
            st.error("❌ GROQ_API_KEY not found in .env file")
            return None, None
        
        # Load text
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
            groq_api_key=GROQ_API_KEY,
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
        st.error(f"❌ Error initializing chatbot: {str(e)}")
        return None, None

# Header
st.markdown("<h1>🕌 Islamic Chatbot</h1>", unsafe_allow_html=True)
st.markdown("<h3>تفسیر ابن کثیر - Tafseer Ibn Kathir</h3>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown("### 📚 About")
    st.markdown("""
    This chatbot answers questions about:
    - Quranic verses (آیات)
    - Translations (ترجمہ)
    - Tafseer (تفسیر)
    
    Based on **Tafseer Ibn Kathir** in Urdu.
    """)
    
    st.markdown("---")
    st.markdown("### 🎯 Sample Questions")
    
    sample_questions = [
        "سورہ فاتحہ کی تفسیر بتائیں",
        "بسم اللہ الرحمن الرحیم کا کیا مطلب ہے؟",
        "آیت الکرسی کے بارے میں بتائیں",
        "سورہ الاخلاص کی تشریح کریں"
    ]
    
    for q in sample_questions:
        if st.button(q, key=q, use_container_width=True):
            st.session_state.sample_question = q
    
    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Ask questions in Urdu or English
    - Be specific about the Surah or Ayat
    - You can ask about meanings, context, or interpretations
    """)

# Initialize chatbot
if st.session_state.rag_chain is None:
    with st.spinner("🔄 Loading chatbot... Please wait..."):
        rag_chain, retriever = initialize_chatbot()
        if rag_chain:
            st.session_state.rag_chain = rag_chain
            st.session_state.retriever = retriever
            st.success("✅ Chatbot loaded successfully!")
        else:
            st.error("❌ Failed to load chatbot. Please check your configuration.")
            st.stop()

# Display chat messages
for message in st.session_state.messages:
    if message["role"] == "user":
        st.markdown(f"""
        <div class="chat-message user-message">
            <strong>👤 You:</strong>
            <div class="urdu-text">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message bot-message">
            <strong>🤖 Chatbot:</strong>
            <div class="urdu-text">{message["content"]}</div>
        </div>
        """, unsafe_allow_html=True)

# Handle sample question from sidebar
if 'sample_question' in st.session_state:
    user_input = st.session_state.sample_question
    del st.session_state.sample_question
else:
    user_input = None

# Chat input
col1, col2 = st.columns([6, 1])
with col1:
    user_question = st.text_input(
        "آپ کا سوال (Your Question):",
        value=user_input if user_input else "",
        placeholder="سوال یہاں لکھیں... (Type your question here...)",
        key="user_input"
    )
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    send_button = st.button("📤 Send", use_container_width=True)

# Process user input
if (send_button or user_input) and user_question:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_question})
    
    # Get bot response
    with st.spinner("🤔 Thinking..."):
        try:
            answer = st.session_state.rag_chain.invoke(user_question)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            error_msg = f"❌ Error: {str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🌙 May Allah bless you | اللہ آپ کو برکت دے</p>
    <p style='font-size: 12px;'>Powered by Groq AI & LangChain</p>
</div>
""", unsafe_allow_html=True)
