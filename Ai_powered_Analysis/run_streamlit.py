"""
Quick launcher for Streamlit UI
"""
import subprocess
import sys

print("=" * 80)
print("🎨 AI DATA ANALYST CHATBOT - STREAMLIT UI")
print("=" * 80)
print()
print("🚀 Starting Streamlit app...")
print("📱 The app will open in your browser automatically")
print()
print("💡 Tips:")
print("   • Press Ctrl+C to stop the server")
print("   • The app runs at: http://localhost:8501")
print("   • Use sidebar to upload data or generate samples")
print()
print("=" * 80)
print()

try:
    subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
except KeyboardInterrupt:
    print("\n\n👋 Streamlit app stopped. Goodbye!")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Make sure Streamlit is installed:")
    print("   pip install streamlit")
