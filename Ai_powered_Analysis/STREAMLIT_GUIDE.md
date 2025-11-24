# 🎨 Streamlit UI Guide - AI Data Analyst Chatbot

## 🚀 Quick Start

### 1. Install Streamlit
```bash
pip install streamlit
# or
pip install -r requirements.txt
```

### 2. Run the App
```bash
streamlit run streamlit_app.py
```

The app will automatically open in your browser at `http://localhost:8501`

---

## 🎯 Features

### 📊 **Overview Tab**
- Dataset metrics (rows, columns, memory, missing values)
- Column information table
- Data types distribution chart
- AI-generated summary

### 💬 **Chat Tab**
- Interactive chat interface
- Quick question buttons
- Custom question input
- Conversation history
- Structured AI responses

### 📈 **Visualizations Tab**
- **Correlation Heatmap** - See relationships between variables
- **Distribution Plots** - Histograms and box plots
- **Scatter Plots** - Compare two variables
- **Bar Charts** - Categorical data distribution
- Interactive Plotly charts

### 📋 **Data Tab**
- View raw data
- Statistical summary
- Dataset info
- Download as CSV

---

## 🎨 User Interface

### Sidebar
```
⚙️ Configuration
├── 🚀 Initialize Chatbot
├── 📁 Upload Dataset (CSV, Excel, JSON)
├── 🎲 Generate Sample Data
└── 🔧 Actions (Reset, Clear)
```

### Main Area
```
📊 Overview    💬 Chat    📈 Visualizations    📋 Data
```

---

## 📖 How to Use

### Step 1: Initialize
1. Click **"🚀 Initialize Chatbot"** in sidebar
2. Wait for success message

### Step 2: Load Data
**Option A - Upload Your Data:**
1. Click **"Browse files"** in sidebar
2. Select CSV, Excel, or JSON file
3. Click **"📊 Load Dataset"**

**Option B - Use Sample Data:**
1. Click **"Generate Sample Data"** in sidebar
2. Sample dataset loads automatically

### Step 3: Explore
**Overview Tab:**
- View dataset metrics
- Check column information
- Get AI summary

**Chat Tab:**
- Click quick question buttons, or
- Type custom questions
- Get instant AI insights

**Visualizations Tab:**
- Select visualization type
- Choose columns
- View interactive charts

**Data Tab:**
- Browse raw data
- View statistics
- Download results

---

## 💬 Example Questions

### Quick Questions (Buttons)
- 🔍 **Key Insights** - Get main findings
- 🔗 **Correlations** - See relationships
- 📈 **Visualizations** - Get chart recommendations

### Custom Questions
```
"What patterns do you see in this data?"
"How should I handle missing values?"
"Generate code for a correlation heatmap"
"What machine learning models would work best?"
"Identify any data quality issues"
"Suggest data cleaning steps"
"What are the outliers in this dataset?"
"Explain the relationship between X and Y"
```

---

## 📊 Visualization Options

### 1. Correlation Heatmap
- Shows relationships between all numeric columns
- Color-coded (red = negative, green = positive)
- Displays correlation coefficients

### 2. Distribution Plots
- Histogram with frequency counts
- Box plot for outlier detection
- Select any numeric column

### 3. Box Plots
- Compare distributions
- Group by categorical variables
- Identify outliers visually

### 4. Scatter Plots
- Compare two numeric variables
- Color by categorical variable
- Interactive zoom and pan

### 5. Bar Charts
- Categorical data distribution
- Value counts
- Interactive tooltips

---

## 🎨 UI Features

### Interactive Elements
- ✅ Real-time chat responses
- ✅ Interactive charts (zoom, pan, hover)
- ✅ Responsive layout
- ✅ Dark/light mode support
- ✅ Mobile-friendly

### Visual Design
- 🎨 Clean, modern interface
- 📱 Responsive columns
- 🎯 Color-coded messages
- 📊 Professional charts
- ✨ Smooth animations

---

## 🔧 Configuration

### Sidebar Controls

**Initialize Chatbot**
- Connects to Groq API
- Loads AI model
- Required before use

**Upload Dataset**
- Supports: CSV, Excel, JSON
- Max size: 200MB (default)
- Auto-detects format

**Generate Sample Data**
- Creates 200-row sales dataset
- Includes numeric and categorical data
- Has missing values for testing

**Reset Conversation**
- Clears chat history
- Keeps dataset loaded
- Starts fresh conversation

**Clear All**
- Resets everything
- Removes dataset
- Clears chat history

---

## 💡 Pro Tips

### 1. Quick Analysis
```
1. Generate sample data
2. Click "Key Insights"
3. View visualizations
4. Ask follow-up questions
```

### 2. Deep Dive
```
1. Upload your dataset
2. Check Overview tab
3. Ask specific questions
4. Generate custom visualizations
```

### 3. Export Results
```
1. Complete your analysis
2. Go to Data tab
3. Click "Download Dataset as CSV"
4. Copy chat responses for reports
```

### 4. Best Practices
- Start with Overview tab to understand data
- Use quick questions for common analyses
- Ask specific questions for detailed insights
- Try different visualizations
- Download results before clearing

---

## 🎯 Use Cases

### Business Analytics
```
1. Upload sales data
2. Ask: "What are the top performing products?"
3. View correlation heatmap
4. Generate insights report
```

### Data Quality Check
```
1. Load dataset
2. Ask: "Identify data quality issues"
3. Check missing values in Overview
4. Get cleaning recommendations
```

### Exploratory Analysis
```
1. Upload new dataset
2. Get AI summary
3. Ask about patterns
4. Create visualizations
5. Export findings
```

### Machine Learning Prep
```
1. Load training data
2. Ask: "What features are most important?"
3. Check correlations
4. Get preprocessing recommendations
```

---

## 🆘 Troubleshooting

### App Won't Start
```bash
# Check Streamlit installation
pip install streamlit

# Run with verbose output
streamlit run streamlit_app.py --logger.level=debug
```

### Chatbot Not Initializing
- Check `.env` file has `GROQ_API_KEY`
- Verify API key is valid
- Check internet connection

### Dataset Won't Load
- Verify file format (CSV, Excel, JSON)
- Check file size (< 200MB)
- Ensure file is not corrupted

### Visualizations Not Showing
- Check if dataset has numeric columns
- Verify column selection
- Try different visualization type

### Chat Not Responding
- Check API key is valid
- Verify internet connection
- Try resetting conversation

---

## 🎨 Customization

### Change Theme
```bash
# Light theme
streamlit run streamlit_app.py --theme.base="light"

# Dark theme
streamlit run streamlit_app.py --theme.base="dark"
```

### Modify Port
```bash
streamlit run streamlit_app.py --server.port=8502
```

### Auto-reload on Changes
```bash
streamlit run streamlit_app.py --server.runOnSave=true
```

---

## 📱 Mobile Access

### Access from Phone/Tablet
1. Run app on computer
2. Note the local IP (shown in terminal)
3. Open browser on mobile device
4. Navigate to: `http://YOUR_IP:8501`

---

## 🚀 Deployment

### Deploy to Streamlit Cloud
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect repository
4. Add secrets (GROQ_API_KEY)
5. Deploy!

### Deploy to Heroku
```bash
# Create Procfile
echo "web: streamlit run streamlit_app.py" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

---

## 📊 Performance Tips

### For Large Datasets
- Use sampling for initial exploration
- Filter data before visualization
- Use Plotly for interactive charts
- Cache results with `@st.cache_data`

### For Faster Response
- Keep questions specific
- Use quick question buttons
- Reset conversation periodically
- Clear unused data

---

## 🎉 Summary

The Streamlit UI provides:
- ✅ Beautiful, intuitive interface
- ✅ Real-time AI chat
- ✅ Interactive visualizations
- ✅ Easy data upload
- ✅ Export capabilities
- ✅ Mobile-friendly design

**Start analyzing your data with a beautiful UI!**

```bash
streamlit run streamlit_app.py
```

---

**Happy Analyzing! 📊✨**
