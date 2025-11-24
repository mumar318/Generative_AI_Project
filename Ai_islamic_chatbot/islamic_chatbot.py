"""
Islamic Chatbot - RAG Based Quran Tafseer
A chatbot that answers questions about Quranic verses, translations, and tafseer in Urdu
"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class IslamicChatbot:
    def __init__(self, pdf_path="Tafseer Ibn-e-Kaseer 01.pdf", persist_dir="./chroma_db"):
        """Initialize the Islamic Chatbot"""
        self.pdf_path = pdf_path
        self.persist_dir = persist_dir
        self.vectorstore = None
        self.rag_chain = None
        
        # Load environment variables
        load_dotenv()
        self.groq_api_key = os.getenv('GROQ_API_KEY')
        
        if not self.groq_api_key:
            raise ValueError("Please set GROQ_API_KEY in .env file")
        
        print("✓ Islamic Chatbot initialized")
    
    def load_and_process_pdf(self):
        """Load and process the Tafseer PDF"""
        print(f"\n📖 Loading PDF: {self.pdf_path}")
        
        # Try different PDF loaders
        try:
            from langchain_community.document_loaders import PyMuPDFLoader
            loader = PyMuPDFLoader(self.pdf_path)
            documents = loader.load()
            print(f"✓ Loaded {len(documents)} pages using PyMuPDF")
        except Exception as e:
            print(f"⚠️ PyMuPDF failed: {e}")
            print("Trying alternative loader...")
            loader = PyPDFLoader(self.pdf_path)
            documents = loader.load()
            print(f"✓ Loaded {len(documents)} pages using PyPDF")
        
        # Filter out empty pages
        documents = [doc for doc in documents if doc.page_content.strip()]
        print(f"✓ Found {len(documents)} pages with content")
        
        if not documents:
            raise ValueError("No text content found in PDF. The PDF might be image-based or encrypted.")
        
        # Split into chunks - adjusted for Urdu text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            length_function=len,
            separators=["\n\n", "\n", "۔", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"✓ Created {len(chunks)} text chunks")
        
        if not chunks:
            raise ValueError("Failed to create text chunks. Please check the PDF content.")
        
        return chunks
    
    def create_vector_store(self, chunks):
        """Create vector store from document chunks"""
        print("\n🔧 Creating embeddings and vector store...")
        
        # Use multilingual embeddings for Urdu support
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # Create Chroma vector store
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=self.persist_dir
        )
        
        print(f"✓ Vector store created with {self.vectorstore._collection.count()} vectors")
        print(f"✓ Persisted to: {self.persist_dir}")
    
    def load_existing_vector_store(self):
        """Load existing vector store"""
        print(f"\n📂 Loading existing vector store from: {self.persist_dir}")
        
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        self.vectorstore = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=embeddings
        )
        
        print(f"✓ Loaded vector store with {self.vectorstore._collection.count()} vectors")
    
    def setup_rag_chain(self):
        """Setup the RAG chain"""
        print("\n⚙️ Setting up RAG chain...")
        
        # Initialize Groq LLM
        llm = ChatGroq(
            groq_api_key=self.groq_api_key,
            model_name="llama-3.3-70b-versatile",
            temperature=0.3,
            max_tokens=2048
        )
        
        # Custom prompt for Islamic chatbot
        prompt_template = """آپ ایک اسلامی چیٹ بوٹ ہیں جو قرآن پاک کی تفسیر ابن کثیر سے سوالات کے جوابات دیتے ہیں۔

Context (سیاق و سباق):
{context}

Question (سوال): {question}

Instructions:
- دیے گئے context سے متعلقہ آیات، ترجمہ اور تفسیر فراہم کریں
- اگر context میں جواب نہیں ہے تو واضح طور پر بتائیں
- جواب اردو میں دیں
- آیات کو عربی میں بھی شامل کریں اگر دستیاب ہوں
- تفصیلی اور واضح جواب دیں

Answer (جواب):"""
        
        prompt = ChatPromptTemplate.from_template(prompt_template)
        
        # Create retriever
        retriever = self.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        # Format documents function
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        # Create RAG chain
        self.rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        
        # Store retriever for getting source documents
        self.retriever = retriever
        
        print("✓ RAG chain created successfully")
    
    def ask(self, question):
        """Ask a question to the chatbot"""
        if not self.rag_chain:
            raise ValueError("RAG chain not initialized. Run setup() first.")
        
        print(f"\n{'='*60}")
        print(f"سوال: {question}")
        print(f"{'='*60}\n")
        
        # Get answer
        answer = self.rag_chain.invoke(question)
        
        # Get source documents
        source_docs = self.retriever.invoke(question)
        
        print(f"جواب:\n{answer}")
        print(f"\n{'='*60}")
        print(f"📚 Source: {len(source_docs)} relevant chunks retrieved")
        print(f"{'='*60}\n")
        
        return {"answer": answer, "source_documents": source_docs}
    
    def setup(self, use_existing=False):
        """Complete setup of the chatbot"""
        print("\n🚀 Setting up Islamic Chatbot...")
        
        if use_existing and os.path.exists(self.persist_dir):
            self.load_existing_vector_store()
        else:
            chunks = self.load_and_process_pdf()
            self.create_vector_store(chunks)
        
        self.setup_rag_chain()
        print("\n✅ Chatbot is ready!")
    
    def chat(self):
        """Interactive chat loop"""
        print("\n" + "="*60)
        print("اسلامی چیٹ بوٹ میں خوش آمدید!")
        print("Welcome to Islamic Chatbot!")
        print("="*60)
        print("\nقرآن پاک کی آیات، ترجمہ اور تفسیر کے بارے میں سوال پوچھیں")
        print("Ask questions about Quranic verses, translations, and tafseer")
        print("\nبند کرنے کے لیے 'exit' یا 'quit' لکھیں")
        print("Type 'exit' or 'quit' to stop\n")
        
        while True:
            try:
                user_question = input("\n💬 آپ کا سوال (Your question): ")
                
                if user_question.lower() in ['exit', 'quit', 'بند']:
                    print("\n🌙 اللہ حافظ! جزاک اللہ خیر")
                    print("May Allah bless you!")
                    break
                
                if user_question.strip():
                    self.ask(user_question)
                else:
                    print("⚠️ Please enter a question")
                    
            except KeyboardInterrupt:
                print("\n\n🌙 اللہ حافظ! جزاک اللہ خیر")
                break
            except Exception as e:
                print(f"\n❌ Error: {str(e)}")


def main():
    """Main function to run the chatbot"""
    try:
        # Initialize chatbot
        chatbot = IslamicChatbot(pdf_path="Tafseer Ibn-e-Kaseer 01.pdf")
        
        # Setup (use_existing=True to load existing vector store)
        chatbot.setup(use_existing=False)
        
        # Test with sample questions
        print("\n" + "="*60)
        print("🧪 Testing with sample questions...")
        print("="*60)
        
        # Test question 1
        chatbot.ask("سورہ فاتحہ کی تفسیر بتائیں")
        
        # Start interactive chat
        chatbot.chat()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nPlease make sure:")
        print("1. GROQ_API_KEY is set in .env file")
        print("2. 'Tafseer Ibn-e-Kaseer 01.pdf' exists in the current directory")
        print("3. All required packages are installed")


if __name__ == "__main__":
    main()
