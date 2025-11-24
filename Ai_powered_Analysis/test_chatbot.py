"""
Quick test script for the AI Data Analyst Chatbot
"""
from Analysis_chatbot import DataAnalystChatbot
import pandas as pd
import numpy as np

# Create sample dataset for testing
print("Creating sample dataset...")
np.random.seed(42)
sample_data = pd.DataFrame({
    'age': np.random.randint(18, 80, 100),
    'income': np.random.randint(20000, 150000, 100),
    'score': np.random.uniform(0, 100, 100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'satisfaction': np.random.randint(1, 6, 100)
})

# Add some missing values
sample_data.loc[np.random.choice(100, 10, replace=False), 'income'] = np.nan
sample_data.to_csv('sample_data.csv', index=False)
print("✓ Sample dataset created: sample_data.csv\n")

# Initialize chatbot
print("Initializing AI Data Analyst Chatbot...")
chatbot = DataAnalystChatbot()
print("✓ Chatbot initialized\n")

# Load dataset
print("Loading dataset...")
result = chatbot.load_dataset('sample_data.csv')
print(result)
print()

# Get summary
print("=" * 80)
print("DATASET SUMMARY")
print("=" * 80)
summary = chatbot.get_dataset_summary()
print(summary)

# Test chat functionality
print("\n" + "=" * 80)
print("TESTING CHAT FUNCTIONALITY")
print("=" * 80)

test_questions = [
    "What are the key insights from this dataset?",
    "What correlations exist between the numeric variables?",
    "How should I visualize this data?"
]

for question in test_questions:
    print(f"\n📊 Question: {question}")
    print("-" * 80)
    response = chatbot.chat(question)
    print(response)
    print()

print("\n✓ Test completed successfully!")
print("\nYou can now:")
print("1. Run 'python Analysis_chatbot.py' for interactive mode")
print("2. Open 'Analysis.ipynb' in Jupyter for notebook interface")
print("3. Use the chatbot in your own scripts")
