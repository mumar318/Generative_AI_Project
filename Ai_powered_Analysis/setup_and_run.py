"""
Quick setup and run script for AI Data Analyst Chatbot
This script helps you get started quickly!
"""
import os
import sys

def print_banner():
    print("\n" + "="*80)
    print("🤖 AI DATA ANALYST CHATBOT - SETUP & RUN")
    print("="*80 + "\n")

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    required_packages = [
        'groq', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'plotly', 'python-dotenv'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("\n💡 Install them with:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True

def check_env_file():
    """Check if .env file exists with API key"""
    print("🔑 Checking API key...")
    
    if not os.path.exists('.env'):
        print("   ❌ .env file not found!")
        print("\n💡 Create a .env file with:")
        print('   GROQ_API_KEY="your_api_key_here"')
        return False
    
    with open('.env', 'r') as f:
        content = f.read()
        if 'GROQ_API_KEY' in content and len(content.strip()) > 20:
            print("   ✅ API key found in .env file\n")
            return True
        else:
            print("   ❌ GROQ_API_KEY not properly set in .env file")
            return False

def generate_sample_data():
    """Generate sample datasets"""
    print("🎲 Would you like to generate sample datasets for testing? (y/n): ", end='')
    choice = input().strip().lower()
    
    if choice == 'y':
        print("\n📊 Generating sample datasets...")
        try:
            from create_sample_data import create_sales_dataset, create_customer_dataset, create_employee_dataset
            
            sales_df = create_sales_dataset(500)
            sales_df.to_csv('sample_sales_data.csv', index=False)
            print("   ✅ sample_sales_data.csv created")
            
            customer_df = create_customer_dataset(300)
            customer_df.to_csv('sample_customer_data.csv', index=False)
            print("   ✅ sample_customer_data.csv created")
            
            employee_df = create_employee_dataset(200)
            employee_df.to_csv('sample_employee_data.csv', index=False)
            print("   ✅ sample_employee_data.csv created")
            
            print("\n✅ Sample datasets ready!\n")
            return True
        except Exception as e:
            print(f"   ❌ Error generating datasets: {e}")
            return False
    return False

def show_menu():
    """Show main menu"""
    print("\n" + "="*80)
    print("🚀 HOW WOULD YOU LIKE TO USE THE CHATBOT?")
    print("="*80)
    print("\n1. 📓 Open Jupyter Notebook (Recommended - Interactive)")
    print("2. 🐍 Run Python Script (Quick test)")
    print("3. 💻 Command Line Interface (Interactive terminal)")
    print("4. 📚 View Documentation")
    print("5. ❌ Exit")
    print("\nEnter your choice (1-5): ", end='')
    
    return input().strip()

def run_notebook():
    """Open Jupyter notebook"""
    print("\n📓 Opening Jupyter Notebook...")
    print("💡 If Jupyter doesn't open automatically, go to: http://localhost:8888")
    print("💡 Press Ctrl+C to stop the server\n")
    os.system('jupyter notebook Analysis.ipynb')

def run_test_script():
    """Run test script"""
    print("\n🐍 Running test script...\n")
    os.system('python test_chatbot.py')

def run_cli():
    """Run command line interface"""
    print("\n💻 Starting Command Line Interface...\n")
    os.system('python Analysis_chatbot.py')

def show_docs():
    """Show documentation"""
    print("\n📚 DOCUMENTATION")
    print("="*80)
    print("\n📄 Available documentation files:")
    print("   • README.md - Complete documentation")
    print("   • QUICKSTART.md - Quick start guide")
    print("\n💡 Open these files in your text editor or IDE")
    print("\n📊 Key files:")
    print("   • Analysis.ipynb - Interactive Jupyter notebook (START HERE!)")
    print("   • Analysis_chatbot.py - Python chatbot class")
    print("   • test_chatbot.py - Test script with examples")
    print("   • create_sample_data.py - Generate sample datasets")
    input("\nPress Enter to continue...")

def main():
    """Main function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first!")
        print("   Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # Check API key
    if not check_env_file():
        print("\n❌ Please set up your API key first!")
        sys.exit(1)
    
    # Generate sample data
    generate_sample_data()
    
    # Main loop
    while True:
        choice = show_menu()
        
        if choice == '1':
            run_notebook()
            break
        elif choice == '2':
            run_test_script()
            input("\nPress Enter to continue...")
        elif choice == '3':
            run_cli()
            break
        elif choice == '4':
            show_docs()
        elif choice == '5':
            print("\n👋 Goodbye! Happy analyzing!")
            break
        else:
            print("\n❌ Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
        sys.exit(0)
