# AI Data Analyst Chatbot

An intelligent data analysis assistant powered by Groq API that can analyze datasets, provide insights, and generate visualizations.

## Features

- **Automated Dataset Analysis**: Load CSV, Excel, or JSON files
- **Comprehensive Summaries**: Get shape, columns, dtypes, missing values
- **Statistical Insights**: Descriptive statistics, correlations, patterns
- **Anomaly Detection**: Identify outliers and data quality issues
- **Visualization Recommendations**: Suggest and generate visualization code
- **Interactive Chat**: Ask questions in natural language
- **Professional Reporting**: Structured answers with insights and recommendations

## Installation

```bash
pip install groq python-dotenv pandas numpy matplotlib seaborn plotly openpyxl
```

## Setup

1. Get your Groq API key from [Groq Console](https://console.groq.com)
2. Add it to your `.env` file:
```
GROQ_API_KEY="your_api_key_here"
```

## Usage

### Option 1: Streamlit Web UI (Recommended) 🎨

```bash
streamlit run streamlit_app.py
# or
python run_streamlit.py
```

**Features:**
- Beautiful web interface
- Interactive visualizations
- Real-time chat
- Easy file upload
- Export results

### Option 2: Python Script

```python
from Analysis_chatbot import DataAnalystChatbot

# Initialize chatbot
chatbot = DataAnalystChatbot()

# Load dataset
chatbot.load_dataset("your_data.csv")

# Get summary
print(chatbot.get_dataset_summary())

# Ask questions
response = chatbot.chat("What are the key insights?")
print(response)
```

### Option 2: Command Line

```bash
python Analysis_chatbot.py
```

Then use commands:
- `load <filepath>` - Load a dataset
- `summary` - Get dataset summary
- `reset` - Clear conversation history
- `quit` - Exit

### Option 3: Jupyter Notebook

Open `Analysis.ipynb` and follow the interactive cells.

## Example Questions

- "What are the key insights from this dataset?"
- "What are the strongest correlations?"
- "How should I handle missing values?"
- "Are there any anomalies or outliers?"
- "What visualizations would you recommend?"
- "Generate code for a correlation heatmap"
- "What machine learning models would work best?"
- "Identify data quality issues"

## Response Structure

Every response follows this format:

1. **Summary**: Quick overview of findings
2. **Insights**: Key patterns and discoveries
3. **Visualizations**: Recommended charts (if applicable)
4. **Code**: Python code for analysis/visualization
5. **Recommendations**: Actionable next steps

## Supported File Formats

- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)

## Model

Uses Groq's `llama-3.3-70b-versatile` model for fast, accurate analysis.

## License

MIT
