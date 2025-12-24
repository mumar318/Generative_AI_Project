#!/bin/bash

echo "🚀 Preparing Islamic Chatbot for Streamlit Cloud Deployment"
echo "=========================================================="

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Copy secrets template
cp secrets.toml .streamlit/secrets.toml

echo "✅ Created .streamlit/secrets.toml"
echo ""
echo "📝 Next steps:"
echo "1. Edit .streamlit/secrets.toml and add your GROQ_API_KEY"
echo "2. Create GitHub repository:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Islamic Chatbot - Ready for deployment'"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/islamic-chatbot.git"
echo "   git push -u origin main"
echo ""
echo "3. Go to https://share.streamlit.io/"
echo "4. Connect your GitHub repository"
echo "5. Set main file: streamlit_app.py"
echo "6. Add GROQ_API_KEY in secrets"
echo "7. Deploy!"
echo ""
echo "🌟 Your app will be live at:"
echo "https://YOUR_USERNAME-islamic-chatbot-streamlit-app-xyz123.streamlit.app/"