# 🏗️ AI Data Analyst Chatbot - Architecture

## 📐 System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Jupyter    │  │   Python     │  │  Command     │        │
│  │   Notebook   │  │   Script     │  │    Line      │        │
│  │ (Analysis.   │  │  (test_      │  │ (Analysis_   │        │
│  │  ipynb)      │  │  chatbot.py) │  │  chatbot.py) │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
│         │                 │                  │                 │
│         └─────────────────┴──────────────────┘                 │
│                           │                                     │
└───────────────────────────┼─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CHATBOT CORE CLASS                           │
│                  (DataAnalystChatbot)                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Dataset Management                                     │   │
│  │  • load_dataset()      - Load CSV/Excel/JSON          │   │
│  │  • _analyze_dataset()  - Comprehensive analysis       │   │
│  │  • get_dataset_summary() - Generate summary           │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  AI Communication                                       │   │
│  │  • chat()              - Main chat interface          │   │
│  │  • _build_context()    - Build dataset context        │   │
│  │  • conversation_history - Maintain chat history       │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌────────────────────────────────────────────────────────┐   │
│  │  Analysis Engine                                        │   │
│  │  • Statistical analysis (mean, std, correlations)     │   │
│  │  • Missing value detection                            │   │
│  │  • Outlier detection (IQR method)                     │   │
│  │  • Data type inference                                │   │
│  └────────────────────────────────────────────────────────┘   │
│                                                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SERVICES                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   Groq API   │  │    Pandas    │  │ Matplotlib/  │        │
│  │              │  │              │  │   Seaborn    │        │
│  │ llama-3.1-   │  │ Data         │  │              │        │
│  │ 70b-         │  │ Processing   │  │ Visualization│        │
│  │ versatile    │  │              │  │              │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### 1. Dataset Loading Flow
```
User Input (file path)
    │
    ▼
load_dataset()
    │
    ├─► Read file (CSV/Excel/JSON)
    │
    ├─► Store in current_dataset
    │
    └─► _analyze_dataset()
            │
            ├─► Calculate shape, dtypes
            ├─► Detect missing values
            ├─► Compute statistics
            ├─► Find correlations
            ├─► Detect outliers
            │
            └─► Store in dataset_info
```

### 2. Chat Interaction Flow
```
User Question
    │
    ▼
chat(user_message)
    │
    ├─► Add to conversation_history
    │
    ├─► _build_context()
    │       │
    │       └─► Extract dataset info
    │
    ├─► Prepare messages for API
    │       │
    │       ├─► System prompt (role definition)
    │       ├─► Dataset context
    │       └─► Conversation history (last 10)
    │
    ├─► Call Groq API
    │       │
    │       └─► llama-3.3-70b-versatile
    │
    ├─► Receive AI response
    │
    ├─► Add to conversation_history
    │
    └─► Return formatted response
            │
            ├─► 📊 Summary
            ├─► 💡 Insights
            ├─► 📈 Visualizations
            ├─► 💻 Code
            └─► 🎯 Recommendations
```

### 3. Visualization Generation Flow
```
User Request
    │
    ▼
AI Generates Code
    │
    ├─► Correlation Heatmap
    │       │
    │       └─► sns.heatmap(df.corr())
    │
    ├─► Distribution Plots
    │       │
    │       └─► df.hist() + KDE
    │
    ├─► Box Plots
    │       │
    │       └─► sns.boxplot()
    │
    └─► Custom Visualizations
            │
            └─► Based on user request
```

---

## 🧩 Component Breakdown

### Core Components

#### 1. DataAnalystChatbot Class
```python
class DataAnalystChatbot:
    - __init__()              # Initialize with API key
    - load_dataset()          # Load and validate data
    - _analyze_dataset()      # Comprehensive analysis
    - get_dataset_summary()   # Generate summary report
    - chat()                  # Main interaction method
    - _build_context()        # Prepare dataset context
    - reset_conversation()    # Clear history
```

#### 2. Dataset Analysis Module
```python
Analysis Features:
├── Basic Info
│   ├── Shape (rows × columns)
│   ├── Data types
│   ├── Memory usage
│   └── Column names
│
├── Statistical Analysis
│   ├── Descriptive statistics
│   ├── Correlation matrix
│   ├── Distribution analysis
│   └── Outlier detection
│
└── Data Quality
    ├── Missing values
    ├── Missing percentages
    ├── Duplicate detection
    └── Type validation
```

#### 3. AI Integration Module
```python
Groq API Integration:
├── Model: llama-3.3-70b-versatile
├── Temperature: 0.7
├── Max Tokens: 2500
├── Context: Last 10 messages
└── Response Format: Structured
```

---

## 📊 Data Structures

### Dataset Info Dictionary
```python
dataset_info = {
    "shape": (rows, cols),
    "columns": [col1, col2, ...],
    "dtypes": {col: dtype, ...},
    "missing_values": {col: count, ...},
    "missing_percentage": {col: pct, ...},
    "numeric_columns": [col1, col2, ...],
    "categorical_columns": [col1, col2, ...],
    "descriptive_stats": {col: {stat: value, ...}, ...},
    "correlations": {col1: {col2: corr, ...}, ...},
    "strong_correlations": [(col1, col2, corr), ...],
    "outliers": {col: count, ...},
    "memory_usage": float  # MB
}
```

### Conversation History
```python
conversation_history = [
    {
        "role": "user",
        "content": "What are the key insights?"
    },
    {
        "role": "assistant",
        "content": "📊 Summary: ..."
    },
    ...
]
```

---

## 🔧 Configuration

### Environment Variables
```
.env file:
├── GROQ_API_KEY="your_api_key_here"
└── (Optional) GROQ_MODEL="llama-3.3-70b-versatile"
```

### Model Parameters
```python
model_config = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.7,
    "max_tokens": 2500,
    "top_p": 1.0
}
```

### Visualization Settings
```python
viz_config = {
    "style": "whitegrid",
    "palette": "husl",
    "figure_size": (12, 6),
    "font_size": 10,
    "dpi": 100
}
```

---

## 🎯 Analysis Pipeline

### Step 1: Data Ingestion
```
Input File → Validation → Pandas DataFrame → Storage
```

### Step 2: Automatic Analysis
```
DataFrame → Statistical Analysis → Pattern Detection → Storage
```

### Step 3: AI Processing
```
User Query → Context Building → API Call → Response Formatting
```

### Step 4: Visualization
```
Data + Request → Code Generation → Plot Creation → Display
```

---

## 🔐 Security Architecture

### API Key Management
```
.env file (local)
    │
    ├─► Not committed to git
    ├─► Loaded via python-dotenv
    └─► Used only for Groq API
```

### Data Privacy
```
User Data
    │
    ├─► Stored locally in memory
    ├─► Not persisted to disk (unless exported)
    ├─► Sent only to Groq API for analysis
    └─► No third-party sharing
```

---

## 📈 Performance Considerations

### Memory Management
- Dataset stored in Pandas DataFrame (efficient)
- Conversation history limited to last 10 messages
- Lazy loading of visualizations
- Garbage collection after large operations

### API Optimization
- Context limited to relevant dataset info
- Conversation history pruned
- Efficient prompt engineering
- Response caching (conversation history)

### Visualization Optimization
- Lazy rendering
- Configurable figure sizes
- Efficient plotting libraries
- Memory cleanup after display

---

## 🚀 Scalability

### Current Limitations
- Single dataset at a time
- In-memory processing
- Synchronous API calls
- Local execution only

### Future Enhancements
- Multi-dataset support
- Streaming data processing
- Async API calls
- Cloud deployment options
- Distributed computing support

---

## 🧪 Testing Architecture

### Test Components
```
test_chatbot.py
├── Sample data generation
├── Chatbot initialization
├── Dataset loading
├── Summary generation
└── Chat functionality
```

### Sample Data Generator
```
create_sample_data.py
├── Sales dataset (500 rows)
├── Customer dataset (300 rows)
└── Employee dataset (200 rows)
```

---

## 📚 Documentation Structure

```
Documentation
├── START_HERE.md          # Entry point
├── QUICKSTART.md          # 3-minute guide
├── README.md              # Complete docs
├── PROJECT_SUMMARY.md     # Overview
└── ARCHITECTURE.md        # This file
```

---

## 🎨 User Interface Options

### 1. Jupyter Notebook (Analysis.ipynb)
- **Best for**: Interactive exploration
- **Features**: 17 step-by-step cells
- **Audience**: All users

### 2. Python Script (test_chatbot.py)
- **Best for**: Quick testing
- **Features**: Automated demo
- **Audience**: Developers

### 3. Command Line (Analysis_chatbot.py)
- **Best for**: Terminal users
- **Features**: Interactive CLI
- **Audience**: Power users

### 4. Setup Script (setup_and_run.py)
- **Best for**: First-time users
- **Features**: Guided setup
- **Audience**: Beginners

---

## 🔄 Update & Maintenance

### Version Control
- Git-friendly structure
- .env excluded from commits
- Sample data optional
- Documentation versioned

### Extensibility
- Modular class design
- Easy to add new analysis methods
- Pluggable visualization types
- Customizable prompts

---

## 🎯 Design Principles

1. **Simplicity**: Easy to use, minimal setup
2. **Modularity**: Components can be used independently
3. **Extensibility**: Easy to add new features
4. **Documentation**: Comprehensive guides
5. **User-Friendly**: Multiple interfaces for different users
6. **Professional**: Production-ready code
7. **Secure**: API key management, data privacy
8. **Efficient**: Optimized for performance

---

## 📊 Technology Stack Summary

```
Frontend/Interface
├── Jupyter Notebook
├── Python CLI
└── Interactive Scripts

Core Logic
├── Python 3.8+
├── Object-Oriented Design
└── Functional Programming

Data Processing
├── Pandas (DataFrames)
├── NumPy (Numerical)
└── Python Standard Library

AI/ML
├── Groq API
├── llama-3.3-70b-versatile
└── Natural Language Processing

Visualization
├── Matplotlib (Static)
├── Seaborn (Statistical)
└── Plotly (Interactive)

Configuration
├── python-dotenv
└── Environment Variables
```

---

This architecture provides a solid foundation for AI-powered data analysis with room for future enhancements and scalability.
