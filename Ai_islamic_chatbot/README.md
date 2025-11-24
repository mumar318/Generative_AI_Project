# Islamic Chatbot - RAG Based Quran Tafseer

A RAG-based chatbot that answers questions about Quranic verses, translations (terjoma), and tafseer in Urdu using Groq API.

## Features

- 📖 Processes Tafseer Ibn-e-Kaseer PDF
- 🤖 Uses Groq API with Llama 3.1 70B model
- 🔍 RAG (Retrieval Augmented Generation) architecture
- 🌐 Multilingual support (Urdu & Arabic)
- 💾 Persistent vector store for fast reloading

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Edit the `.env` file and add your Groq API key:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from: https://console.groq.com

### 3. Prepare PDF

Make sure `Tafseer Ibn-e-Kaseer 01.pdf` is in the same directory.

## Usage

### Run the Chatbot

```bash
python islamic_chatbot.py
```

### First Run
- The chatbot will process the PDF and create a vector store
- This may take a few minutes depending on PDF size

### Subsequent Runs
- To use existing vector store (faster), modify `main()` function:
```python
chatbot.setup(use_existing=True)
```

## Example Questions

- سورہ فاتحہ کی تفسیر بتائیں
- بسم اللہ الرحمن الرحیم کا ترجمہ اور تفسیر کیا ہے؟
- آیت الکرسی کی تشریح کریں

## Architecture

```
PDF → Text Chunks → Embeddings → Vector Store (ChromaDB)
                                        ↓
User Question → Retrieval → Context + Prompt → Groq LLM → Answer
```

## Components

- **PDF Loader**: PyPDF for extracting text
- **Embeddings**: Multilingual sentence transformers
- **Vector Store**: ChromaDB for similarity search
- **LLM**: Groq API (Llama 3.1 70B)
- **Framework**: LangChain for RAG pipeline

## Customization

### Change Model
Edit in `islamic_chatbot.py`:
```python
model_name="mixtral-8x7b-32768"  # or other Groq models
```

### Adjust Chunk Size
```python
chunk_size=1000,  # Increase for more context
chunk_overlap=200  # Overlap between chunks
```

### Change Retrieval Count
```python
search_kwargs={"k": 5}  # Number of chunks to retrieve
```

## Troubleshooting

- **API Key Error**: Make sure GROQ_API_KEY is set in .env
- **PDF Not Found**: Check PDF filename and location
- **Memory Issues**: Reduce chunk_size or use smaller PDF
- **Slow Performance**: Use `use_existing=True` after first run

## License

For educational and personal use.
