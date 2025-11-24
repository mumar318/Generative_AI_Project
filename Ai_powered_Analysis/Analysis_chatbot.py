import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from groq import Groq
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()

class DataAnalystChatbot:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model = "llama-3.3-70b-versatile"  # Updated to current model
        self.conversation_history = []
        self.current_dataset = None
        self.dataset_info = {}
        
    def load_dataset(self, file_path):
        """Load dataset from CSV, Excel, or JSON"""
        try:
            if file_path.endswith('.csv'):
                self.current_dataset = pd.read_csv(file_path)
            elif file_path.endswith(('.xlsx', '.xls')):
                self.current_dataset = pd.read_excel(file_path)
            elif file_path.endswith('.json'):
                self.current_dataset = pd.read_json(file_path)
            else:
                return "Unsupported file format. Please use CSV, Excel, or JSON."
            
            self._analyze_dataset()
            return f"Dataset loaded successfully! Shape: {self.current_dataset.shape}"
        except Exception as e:
            return f"Error loading dataset: {str(e)}"
    
    def _analyze_dataset(self):
        """Perform initial dataset analysis"""
        df = self.current_dataset
        
        self.dataset_info = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "dtypes": df.dtypes.to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "numeric_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "descriptive_stats": df.describe().to_dict() if not df.empty else {},
            "sample_data": df.head(5).to_dict()
        }
        
        # Calculate correlations for numeric columns
        if len(self.dataset_info["numeric_columns"]) > 1:
            self.dataset_info["correlations"] = df[self.dataset_info["numeric_columns"]].corr().to_dict()
    
    def get_dataset_summary(self):
        """Generate comprehensive dataset summary"""
        if self.current_dataset is None:
            return "No dataset loaded. Please load a dataset first."
        
        summary = f"""
=== DATASET SUMMARY ===

1. SHAPE & STRUCTURE
   - Rows: {self.dataset_info['shape'][0]}
   - Columns: {self.dataset_info['shape'][1]}

2. COLUMNS & DATA TYPES
"""
        for col, dtype in self.dataset_info['dtypes'].items():
            summary += f"   - {col}: {dtype}\n"
        
        summary += "\n3. MISSING VALUES\n"
        for col, missing in self.dataset_info['missing_values'].items():
            if missing > 0:
                pct = self.dataset_info['missing_percentage'][col]
                summary += f"   - {col}: {missing} ({pct:.2f}%)\n"
        
        summary += f"\n4. NUMERIC COLUMNS: {len(self.dataset_info['numeric_columns'])}\n"
        summary += f"5. CATEGORICAL COLUMNS: {len(self.dataset_info['categorical_columns'])}\n"
        
        return summary

    def chat(self, user_message):
        """Main chat interface with Groq API"""
        if self.current_dataset is None and "load" not in user_message.lower():
            return "Please load a dataset first using load_dataset() method."
        
        # Build context with dataset information
        context = self._build_context()
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Prepare messages for Groq API
        messages = [
            {
                "role": "system",
                "content": f"""You are an expert AI Data Analyst and Visualization Expert. 

Your responsibilities:
- Analyze datasets thoroughly
- Provide clear insights and patterns
- Suggest appropriate visualizations
- Generate Python code for analysis and visualization
- Explain results in simple, professional English

Current Dataset Context:
{context}

Always structure your answers as:
1. Summary
2. Insights
3. Visualizations (if needed)
4. Code (if applicable)
5. Recommendations

Be precise, actionable, and professional."""
            }
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-10:])  # Keep last 10 messages
        
        try:
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            assistant_message = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return assistant_message
            
        except Exception as e:
            return f"Error communicating with Groq API: {str(e)}"
    
    def _build_context(self):
        """Build context string with dataset information"""
        if not self.dataset_info:
            return "No dataset loaded."
        
        context = f"""
Dataset Shape: {self.dataset_info['shape']}
Columns: {', '.join(self.dataset_info['columns'])}
Numeric Columns: {', '.join(self.dataset_info['numeric_columns'])}
Categorical Columns: {', '.join(self.dataset_info['categorical_columns'])}
Missing Values: {sum(self.dataset_info['missing_values'].values())} total
"""
        return context
    
    def generate_visualization_code(self, viz_type, columns):
        """Generate Python code for specific visualizations"""
        code_templates = {
            "histogram": f"""
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
df[{columns}].hist(bins=30, edgecolor='black')
plt.tight_layout()
plt.show()
""",
            "scatter": f"""
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
plt.scatter(df['{columns[0]}'], df['{columns[1]}'], alpha=0.6)
plt.xlabel('{columns[0]}')
plt.ylabel('{columns[1]}')
plt.title('Scatter Plot: {columns[0]} vs {columns[1]}')
plt.show()
""",
            "correlation": """
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap')
plt.tight_layout()
plt.show()
""",
            "boxplot": f"""
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 6))
sns.boxplot(data=df[{columns}])
plt.xticks(rotation=45)
plt.title('Box Plot')
plt.tight_layout()
plt.show()
"""
        }
        
        return code_templates.get(viz_type, "Visualization type not supported.")
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        return "Conversation history cleared."


# Example usage
if __name__ == "__main__":
    # Initialize chatbot
    chatbot = DataAnalystChatbot()
    
    print("=== AI Data Analyst Chatbot ===")
    print("Powered by Groq API\n")
    
    # Interactive loop
    print("Commands:")
    print("- 'load <filepath>' to load a dataset")
    print("- 'summary' to get dataset summary")
    print("- 'quit' to exit")
    print("- Or ask any analysis question\n")
    
    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        
        if user_input.lower().startswith('load '):
            filepath = user_input[5:].strip()
            response = chatbot.load_dataset(filepath)
            print(f"\nChatbot: {response}\n")
        
        elif user_input.lower() == 'summary':
            response = chatbot.get_dataset_summary()
            print(f"\nChatbot:\n{response}\n")
        
        elif user_input.lower() == 'reset':
            response = chatbot.reset_conversation()
            print(f"\nChatbot: {response}\n")
        
        else:
            response = chatbot.chat(user_input)
            print(f"\nChatbot:\n{response}\n")
