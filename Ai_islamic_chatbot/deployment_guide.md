# 🚀 Deploy Islamic Chatbot Live

## Option 1: Streamlit Community Cloud (FREE & EASIEST)

### Steps:
1. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Islamic Chatbot - Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/islamic-chatbot.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to https://share.streamlit.io/
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file: `streamlit_app.py`
   - Add secrets (GROQ_API_KEY) in Advanced settings
   - Click "Deploy"

3. **Your app will be live at:**
   `https://YOUR_USERNAME-islamic-chatbot-streamlit-app-xyz123.streamlit.app/`

---

## Option 2: Hugging Face Spaces (FREE)

### Steps:
1. **Create account at https://huggingface.co/**
2. **Create new Space:**
   - Name: `islamic-chatbot`
   - SDK: `Streamlit`
   - Hardware: `CPU basic (free)`

3. **Upload files:**
   - `streamlit_app.py` → `app.py` (rename)
   - `requirements.txt`
   - `sample_tafseer.txt`
   - `.env` → Add GROQ_API_KEY in Space settings

4. **Your app will be live at:**
   `https://huggingface.co/spaces/YOUR_USERNAME/islamic-chatbot`

---

## Option 3: Railway (FREE TIER)

### Steps:
1. **Create account at https://railway.app/**
2. **Connect GitHub repository**
3. **Add environment variable:** `GROQ_API_KEY`
4. **Deploy automatically**

---

## Option 4: Render (FREE TIER)

### Steps:
1. **Create account at https://render.com/**
2. **Create Web Service from GitHub**
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0`
5. **Add environment variable:** `GROQ_API_KEY`

---

## 📋 Pre-deployment Checklist

- [ ] Remove API key from .env file (use platform secrets)
- [ ] Update requirements.txt
- [ ] Test locally first
- [ ] Prepare larger tafseer text file
- [ ] Add error handling

---

## 🔧 Quick Setup for Streamlit Cloud

I'll help you set this up step by step!