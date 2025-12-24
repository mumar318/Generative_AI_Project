# 🕌 AI Islamic Chatbot - اسلامی چیٹ بوٹ

A RAG-based Islamic chatbot that answers questions about Quranic verses, translations (terjoma), and tafseer in Urdu using Groq API and Tafseer Ibn Kathir.

## 🌟 Live Demo

**🚀 [Try the Live Chatbot Here](https://ai-islamic-chatbot.streamlit.app/)** *(Will be available after deployment)*

## ✨ Features

- 🤖 **Powered by Groq API** (Llama 3.3 70B model)
- 📖 **Tafseer Ibn Kathir** knowledge base
- 🔍 **RAG (Retrieval Augmented Generation)** for accurate answers
- 🌐 **Multilingual Support** (Urdu, Arabic, English)
- 💬 **Beautiful Streamlit UI** with Islamic theme
- 📱 **Responsive Design** works on mobile and desktop
- 🎯 **Sample Questions** for easy testing

## 🖥️ Screenshots

### Main Interface
![Islamic Chatbot Interface](https://via.placeholder.com/800x400/2E8B57/FFFFFF?text=Islamic+Chatbot+Interface)

### Chat Example
![Chat Example](https://via.placeholder.com/800x300/F0F8F0/2E8B57?text=Chat+Example+in+Urdu)

## 🚀 Quick Start

### Option 1: Try Online (Recommended)
Visit the live demo: **[AI Islamic Chatbot](https://ai-islamic-chatbot.streamlit.app/)**

### Option 2: Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/mumar318/AI_Islamic_ChatBot.git
   cd AI_Islamic_ChatBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment**
   ```bash
   # Create .env file and add your Groq API key
   echo "GROQ_API_KEY=your_groq_api_key_here" > .env
   ```

4. **Run the app**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open in browser**
   ```
   http://localhost:8501
   ```

## 🔑 Get Groq API Key

1. Visit [Groq Console](https://console.groq.com/)
2. Sign up for free account
3. Generate API key
4. Add to `.env` file or Streamlit secrets

## 💡 Sample Questions

Try asking these questions in Urdu:

- `سورہ فاتحہ کی تفسیر بتائیں`
- `بسم اللہ الرحمن الرحیم کا کیا مطلب ہے؟`
- `آیت الکرسی کے بارے میں بتائیں`
- `سورہ الاخلاص کی تفسیر کریں`

## 🏗️ Architecture

```
User Question → Streamlit UI → RAG Pipeline → Groq LLM → Urdu Answer
                                    ↓
                            Vector Database (ChromaDB)
                                    ↓
                            Tafseer Ibn Kathir Text
```

## 🛠️ Technology Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (Llama 3.3 70B)
- **Framework**: LangChain
- **Vector DB**: ChromaDB
- **Embeddings**: HuggingFace Sentence Transformers
- **Language**: Python

## 📁 Project Structure

```
AI_Islamic_ChatBot/
├── streamlit_app.py          # Main Streamlit application
├── sample_tafseer.txt        # Sample Tafseer text
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml         # API keys (for deployment)
├── islamic_chatbot.py       # Console version
├── demo_chatbot.py          # Demo script
└── README.md               # This file
```

## 🚀 Deployment

### Deploy on Streamlit Cloud (Free)

1. Fork this repository
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your GitHub account
4. Select this repository
5. Set main file: `streamlit_app.py`
6. Add `GROQ_API_KEY` in secrets
7. Deploy!

### Deploy on Hugging Face Spaces

1. Create account on [Hugging Face](https://huggingface.co/)
2. Create new Space with Streamlit SDK
3. Upload files (rename `streamlit_app.py` to `app.py`)
4. Add `GROQ_API_KEY` in Space settings
5. Your app will be live!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Tafseer Ibn Kathir** for the Islamic knowledge base
- **Groq** for providing fast LLM API
- **LangChain** for RAG framework
- **Streamlit** for the beautiful UI framework

## 📞 Contact

- **GitHub**: [@mumar318](https://github.com/mumar318)
- **Project Link**: [https://github.com/mumar318/AI_Islamic_ChatBot](https://github.com/mumar318/AI_Islamic_ChatBot)

---

<div align="center">

**🌙 May Allah bless this project and make it beneficial for the Ummah**

**اللہ اس پروجیکٹ کو برکت دے اور امت کے لیے مفید بنائے**

Made with ❤️ for the Muslim community

</div>
