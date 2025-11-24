"""
Islamic Chatbot DEMO - Works with sample_tafseer.txt
"""

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


print("="*60)
print("🚀 Islamic Chatbot DEMO Starting...")
print("="*60)

# Load environment
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

if not GROQ_API_KEY:
    print("❌ Error: GROQ_API_KEY not found in .env file")
    exit(1)

print("✓ API Key loaded")

# Load sample text
print("\n📖 Loading sample tafseer...")
with open('sample_tafseer.txt', 'r', encoding='utf-8') as f:
    text = f.read()

print(f"✓ Loaded {len(text)} characters")

# Create chunks
print("\n🔧 Creating text chunks...")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
    separators=["\n\n", "\n", "۔", " "]
)

docs = [Document(page_content=text)]
chunks = text_splitter.split_documents(docs)
print(f"✓ Created {len(chunks)} chunks")

# Create embeddings
print("\n🧠 Loading embeddings model...")
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    model_kwargs={'device': 'cpu'}
)
print("✓ Embeddings ready")

# Create vector store
print("\n💾 Creating vector store...")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./demo_chroma_db"
)
print(f"✓ Vector store created with {len(chunks)} vectors")

# Setup LLM
print("\n🤖 Initializing Groq LLM...")
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0.3,
    max_tokens=2048
)
print("✓ LLM ready")

# Create RAG chain
print("\n⚙️ Building RAG chain...")
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

print("✓ RAG chain ready")

print("\n" + "="*60)
print("✅ Chatbot is ready!")
print("="*60)

# Test questions
test_questions = [
    "سورہ فاتحہ کی تفسیر بتائیں",
    "بسم اللہ الرحمن الرحیم کا کیا مطلب ہے؟",
    "آیت الکرسی کے بارے میں بتائیں"
]

print("\n🧪 Testing with sample questions...\n")

for i, question in enumerate(test_questions, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}: {question}")
    print(f"{'='*60}\n")
    
    answer = rag_chain.invoke(question)
    print(f"جواب:\n{answer}\n")

# Interactive chat
print("\n" + "="*60)
print("💬 Interactive Chat Mode")
print("="*60)
print("Type your questions in Urdu or English")
print("Type 'exit' or 'quit' to stop\n")

while True:
    try:
        user_question = input("\n💬 آپ کا سوال: ")
        
        if user_question.lower() in ['exit', 'quit', 'بند']:
            print("\n🌙 اللہ حافظ! جزاک اللہ خیر")
            break
        
        if user_question.strip():
            print(f"\n{'='*60}")
            answer = rag_chain.invoke(user_question)
            print(f"جواب:\n{answer}")
            print(f"{'='*60}\n")
            
    except KeyboardInterrupt:
        print("\n\n🌙 اللہ حافظ!")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
