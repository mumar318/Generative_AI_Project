# 🚀 Deploy Your Islamic Chatbot Live

## Step-by-Step Deployment on Streamlit Cloud

### 1. Your GitHub Repository is Ready ✅
Repository: https://github.com/mumar318/AI_Islamic_ChatBot

### 2. Deploy on Streamlit Cloud (FREE)

1. **Go to Streamlit Cloud**
   - Visit: https://share.streamlit.io/
   - Click "Sign in with GitHub"

2. **Create New App**
   - Click "New app" button
   - Select "From existing repo"
   - Repository: `mumar318/AI_Islamic_ChatBot`
   - Branch: `main`
   - Main file path: `streamlit_app.py`

3. **Add Secrets (Important!)**
   - Click "Advanced settings"
   - In "Secrets" section, add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```

4. **Deploy**
   - Click "Deploy!"
   - Wait 2-3 minutes for deployment

5. **Your Live URL**
   - Will be something like: `https://mumar318-ai-islamic-chatbot-streamlit-app-xyz123.streamlit.app/`

### 3. Alternative: Hugging Face Spaces

1. **Create Account**
   - Go to: https://huggingface.co/
   - Sign up for free

2. **Create Space**
   - Click "Create new Space"
   - Name: `islamic-chatbot`
   - SDK: `Streamlit`
   - Hardware: `CPU basic (free)`

3. **Upload Files**
   - Rename `streamlit_app.py` to `app.py`
   - Upload: `app.py`, `requirements.txt`, `sample_tafseer.txt`

4. **Add Secret**
   - Go to Space settings
   - Add secret: `GROQ_API_KEY`

5. **Your Live URL**
   - Will be: `https://huggingface.co/spaces/mumar318/islamic-chatbot`

## 🎯 Recommended: Streamlit Cloud (Easiest)

Just follow the Streamlit Cloud steps above - it's the simplest and most reliable option!

## 📞 Need Help?

If you encounter any issues during deployment, the most common problems are:
1. **API Key not set** - Make sure to add GROQ_API_KEY in secrets
2. **File paths** - Ensure all files are in the repository
3. **Dependencies** - Check requirements.txt is complete

Your chatbot will be live and accessible worldwide! 🌍