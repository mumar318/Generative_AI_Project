"""
AI Data Analyst Chatbot - Streamlit UI
Interactive web interface for data analysis with AI
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from Analysis_chatbot import DataAnalystChatbot
import io
import sys

# Page configuration
st.set_page_config(
    page_title="AI Data Analyst Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f5f5f5;
        border-left: 4px solid #4caf50;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chatbot' not in st.session_state:
    st.session_state.chatbot = None
if 'dataset_loaded' not in st.session_state:
    st.session_state.dataset_loaded = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_df' not in st.session_state:
    st.session_state.current_df = None
if 'show_dashboard' not in st.session_state:
    st.session_state.show_dashboard = False

# Header
st.markdown('<div class="main-header">🤖 AI Data Analyst Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Powered by Groq API (llama-3.3-70b-versatile)</div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Initialize chatbot
    if st.button("🚀 Initialize Chatbot"):
        try:
            st.session_state.chatbot = DataAnalystChatbot()
            st.success("✅ Chatbot initialized successfully!")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # File upload
    st.header("📁 Upload Dataset")
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls', 'json'],
        help="Upload CSV, Excel, or JSON file"
    )
    
    if uploaded_file is not None and st.session_state.chatbot is not None:
        if st.button("📊 Load Dataset"):
            try:
                # Save uploaded file temporarily
                with open(f"temp_{uploaded_file.name}", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Load dataset
                result = st.session_state.chatbot.load_dataset(f"temp_{uploaded_file.name}")
                st.session_state.dataset_loaded = True
                st.session_state.current_df = st.session_state.chatbot.current_dataset
                st.success(result)
            except Exception as e:
                st.error(f"❌ Error loading dataset: {str(e)}")
    
    st.divider()
    
    # Sample data
    st.header("🎲 Sample Data")
    if st.button("Generate Sample Data"):
        try:
            from create_sample_data import create_sales_dataset
            sample_df = create_sales_dataset(200)
            sample_df.to_csv('temp_sample.csv', index=False)
            
            if st.session_state.chatbot is not None:
                result = st.session_state.chatbot.load_dataset('temp_sample.csv')
                st.session_state.dataset_loaded = True
                st.session_state.current_df = st.session_state.chatbot.current_dataset
                st.success("✅ Sample data generated and loaded!")
            else:
                st.warning("⚠️ Please initialize chatbot first")
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.divider()
    
    # Actions
    st.header("🔧 Actions")
    if st.button("🔄 Reset Conversation"):
        if st.session_state.chatbot is not None:
            st.session_state.chatbot.reset_conversation()
            st.session_state.chat_history = []
            st.success("✅ Conversation reset!")
    
    if st.button("🗑️ Clear All"):
        st.session_state.chatbot = None
        st.session_state.dataset_loaded = False
        st.session_state.chat_history = []
        st.session_state.current_df = None
        st.success("✅ All cleared!")

# Main content
if st.session_state.chatbot is None:
    st.info("👈 Please initialize the chatbot from the sidebar to get started!")
    
    # Welcome message
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📊 Analyze Data")
        st.write("Upload your dataset and get instant insights")
    
    with col2:
        st.markdown("### 💬 Ask Questions")
        st.write("Chat with AI in natural language")
    
    with col3:
        st.markdown("### 📈 Visualize")
        st.write("Generate beautiful charts automatically")
    
    st.divider()
    
    st.markdown("### 🎯 Example Questions:")
    st.code("""
• What are the key insights from this dataset?
• Show me the strongest correlations
• How should I handle missing values?
• Generate a correlation heatmap
• What machine learning models would work best?
• Identify any data quality issues
    """)

elif not st.session_state.dataset_loaded:
    st.warning("📁 Please upload a dataset or generate sample data from the sidebar!")
    
    st.markdown("### 📋 Supported File Formats:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("📄 CSV (.csv)")
    with col2:
        st.info("📊 Excel (.xlsx, .xls)")
    with col3:
        st.info("📋 JSON (.json)")

else:
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "💬 Chat", "📈 Visualizations", "📋 Data"])
    
    # Tab 1: Overview
    with tab1:
        st.header("📊 Dataset Overview")
        
        if st.session_state.current_df is not None:
            df = st.session_state.current_df
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📏 Rows", f"{df.shape[0]:,}")
            with col2:
                st.metric("📊 Columns", df.shape[1])
            with col3:
                st.metric("💾 Memory", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            with col4:
                st.metric("❓ Missing", df.isnull().sum().sum())
            
            st.divider()
            
            # Summary
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Column Information")
                col_info = pd.DataFrame({
                    'Column': df.columns,
                    'Type': df.dtypes.values,
                    'Missing': df.isnull().sum().values,
                    'Missing %': (df.isnull().sum() / len(df) * 100).round(2).values
                })
                st.dataframe(col_info, use_container_width=True)
            
            with col2:
                st.subheader("📊 Data Types Distribution")
                dtype_counts = df.dtypes.value_counts()
                fig = px.pie(
                    values=dtype_counts.values,
                    names=dtype_counts.index.astype(str),
                    title="Column Types"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # Get AI summary
            if st.button("🤖 Get AI Summary"):
                with st.spinner("Analyzing dataset..."):
                    summary = st.session_state.chatbot.get_dataset_summary()
                    st.text(summary)
    
    # Tab 2: Chat
    with tab2:
        st.header("💬 Chat with AI Analyst")
        
        # Display chat history
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            elif message['role'] == 'assistant':
                st.markdown(f'<div class="chat-message assistant-message"><strong>AI Analyst:</strong><br>{message["content"]}</div>', unsafe_allow_html=True)
            elif message['role'] == 'visualization':
                # Display auto-generated visualizations
                st.markdown("### 📊 Auto-Generated Visualization")
                
                df = st.session_state.current_df
                
                if message['type'] == 'correlation_heatmap':
                    fig, ax = plt.subplots(figsize=(10, 8))
                    corr_data = message['data']
                    mask = np.triu(np.ones_like(corr_data, dtype=bool))
                    sns.heatmap(corr_data, mask=mask, annot=True, cmap='RdYlGn', 
                               center=0, fmt='.2f', square=True, linewidths=1, ax=ax)
                    plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
                    st.pyplot(fig)
                    plt.close()
                
                elif message['type'] == 'distributions':
                    cols_to_show = message['columns']
                    n_cols = min(3, len(cols_to_show))
                    n_rows = (len(cols_to_show) + n_cols - 1) // n_cols
                    
                    for row in range(n_rows):
                        cols = st.columns(n_cols)
                        for col_idx in range(n_cols):
                            idx = row * n_cols + col_idx
                            if idx < len(cols_to_show):
                                col_name = cols_to_show[idx]
                                with cols[col_idx]:
                                    fig = px.histogram(df, x=col_name, marginal="box",
                                                     title=f'{col_name}')
                                    fig.update_layout(height=300)
                                    st.plotly_chart(fig, use_container_width=True)
                
                elif message['type'] == 'scatter_matrix':
                    cols_to_show = message['columns']
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                    
                    if categorical_cols:
                        fig = px.scatter_matrix(df, dimensions=cols_to_show, 
                                              color=categorical_cols[0],
                                              title="Scatter Matrix")
                    else:
                        fig = px.scatter_matrix(df, dimensions=cols_to_show,
                                              title="Scatter Matrix")
                    fig.update_layout(height=600)
                    st.plotly_chart(fig, use_container_width=True)
                
                elif message['type'] == 'boxplots':
                    cols_to_show = message['columns']
                    fig = go.Figure()
                    for col in cols_to_show:
                        fig.add_trace(go.Box(y=df[col], name=col))
                    fig.update_layout(title="Box Plots - Outlier Detection",
                                    height=500, showlegend=True)
                    st.plotly_chart(fig, use_container_width=True)
                
                elif message['type'] == 'missing_values':
                    missing_data = message['data']
                    missing_df = pd.DataFrame({
                        'Column': missing_data.index,
                        'Missing': missing_data.values,
                        'Percentage': (missing_data / len(df) * 100).round(2).values
                    })
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.dataframe(missing_df, use_container_width=True)
                    with col2:
                        fig = px.bar(missing_df, x='Column', y='Percentage',
                                   title='Missing Values (%)',
                                   color='Percentage',
                                   color_continuous_scale='Reds')
                        st.plotly_chart(fig, use_container_width=True)
                
                elif message['type'] == 'categorical':
                    cols_to_show = message['columns']
                    n_cols = min(2, len(cols_to_show))
                    n_rows = (len(cols_to_show) + n_cols - 1) // n_cols
                    
                    for row in range(n_rows):
                        cols = st.columns(n_cols)
                        for col_idx in range(n_cols):
                            idx = row * n_cols + col_idx
                            if idx < len(cols_to_show):
                                col_name = cols_to_show[idx]
                                with cols[col_idx]:
                                    value_counts = df[col_name].value_counts().head(10)
                                    fig = px.bar(x=value_counts.index, y=value_counts.values,
                                               title=f'{col_name}',
                                               labels={'x': col_name, 'y': 'Count'})
                                    fig.update_layout(height=300)
                                    st.plotly_chart(fig, use_container_width=True)
                
                elif message['type'] == 'single_distribution':
                    if 'fig' in message:
                        st.plotly_chart(message['fig'], use_container_width=True)
                    else:
                        col = message['column']
                        fig = px.histogram(df, x=col, marginal="box", title=f'Distribution of {col}')
                        st.plotly_chart(fig, use_container_width=True)
                
                elif message['type'] == 'scatter_two_cols':
                    if 'fig' in message:
                        st.plotly_chart(message['fig'], use_container_width=True)
                
                st.divider()
        
        # Chat input
        st.divider()
        
        # Quick questions
        st.subheader("⚡ Quick Questions")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🔍 Key Insights"):
                user_input = "What are the key insights from this dataset?"
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Thinking..."):
                    response = st.session_state.chatbot.chat(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
        
        with col2:
            if st.button("🔥 Show Correlation"):
                user_input = "Show me a correlation heatmap"
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Generating..."):
                    response = st.session_state.chatbot.chat(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                    # Auto-generate correlation heatmap
                    df = st.session_state.current_df
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if len(numeric_cols) > 1:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "correlation_heatmap",
                            "data": df[numeric_cols].corr()
                        })
                st.rerun()
        
        with col3:
            if st.button("📊 Show Distributions"):
                user_input = "Show me distribution plots"
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Generating..."):
                    response = st.session_state.chatbot.chat(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                    # Auto-generate distributions
                    df = st.session_state.current_df
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_cols:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "distributions",
                            "columns": numeric_cols[:6]
                        })
                st.rerun()
        
        with col4:
            if st.button("⚠️ Show Outliers"):
                user_input = "Show me outliers in the data"
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                with st.spinner("Generating..."):
                    response = st.session_state.chatbot.chat(user_input)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                    # Auto-generate boxplots
                    df = st.session_state.current_df
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_cols:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "boxplots",
                            "columns": numeric_cols[:6]
                        })
                st.rerun()
        
        # Custom question
        st.markdown("**💬 Ask anything or request visualizations:**")
        
        with st.expander("📝 Example Questions"):
            st.markdown("""
            **Request Visualizations:**
            - "Show me a correlation heatmap"
            - "Show distribution plots"
            - "Show me outliers"
            - "Show scatter plot"
            - "Show missing values"
            - "Show categorical data"
            
            **Ask Questions:**
            - "What are the key insights?"
            - "What patterns do you see?"
            - "How should I handle missing values?"
            - "What machine learning models would work?"
            """)
        
        user_input = st.text_input("💭 Your question:", placeholder="e.g., Show me a correlation heatmap")
        
        if st.button("📤 Send") and user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            with st.spinner("Thinking..."):
                response = st.session_state.chatbot.chat(user_input)
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                
                # Auto-generate visualizations based on keywords
                user_input_lower = user_input.lower()
                df = st.session_state.current_df
                
                # Check for visualization requests
                if any(keyword in user_input_lower for keyword in ['correlation', 'heatmap', 'corr']):
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if len(numeric_cols) > 1:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "correlation_heatmap",
                            "data": df[numeric_cols].corr()
                        })
                
                elif any(keyword in user_input_lower for keyword in ['distribution', 'histogram', 'dist']):
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_cols:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "distributions",
                            "columns": numeric_cols[:6]
                        })
                
                elif any(keyword in user_input_lower for keyword in ['scatter', 'relationship', 'vs']):
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if len(numeric_cols) >= 2:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "scatter_matrix",
                            "columns": numeric_cols[:4]
                        })
                
                elif any(keyword in user_input_lower for keyword in ['outlier', 'box plot', 'boxplot']):
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    if numeric_cols:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "boxplots",
                            "columns": numeric_cols[:6]
                        })
                
                elif any(keyword in user_input_lower for keyword in ['missing', 'null', 'na']):
                    missing = df.isnull().sum()
                    if missing.sum() > 0:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "missing_values",
                            "data": missing[missing > 0]
                        })
                
                elif any(keyword in user_input_lower for keyword in ['categorical', 'category', 'bar chart']):
                    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                    if categorical_cols:
                        st.session_state.chat_history.append({
                            "role": "visualization",
                            "type": "categorical",
                            "columns": categorical_cols[:4]
                        })
                
                # Check for specific column visualization requests
                elif 'plot' in user_input_lower or 'show' in user_input_lower or 'visualize' in user_input_lower:
                    # Try to find column names in the question
                    all_cols = df.columns.tolist()
                    mentioned_cols = [col for col in all_cols if col.lower() in user_input_lower]
                    
                    if len(mentioned_cols) == 1:
                        # Single column - show distribution
                        col = mentioned_cols[0]
                        if df[col].dtype in [np.number, 'int64', 'float64']:
                            fig = px.histogram(df, x=col, marginal="box", title=f'Distribution of {col}')
                            st.session_state.chat_history.append({
                                "role": "visualization",
                                "type": "single_distribution",
                                "column": col,
                                "fig": fig
                            })
                    
                    elif len(mentioned_cols) == 2:
                        # Two columns - show scatter plot
                        col1, col2 = mentioned_cols
                        if df[col1].dtype in [np.number, 'int64', 'float64'] and df[col2].dtype in [np.number, 'int64', 'float64']:
                            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
                            if categorical_cols:
                                fig = px.scatter(df, x=col1, y=col2, color=categorical_cols[0],
                                               title=f'{col2} vs {col1}')
                            else:
                                fig = px.scatter(df, x=col1, y=col2, title=f'{col2} vs {col1}')
                            
                            st.session_state.chat_history.append({
                                "role": "visualization",
                                "type": "scatter_two_cols",
                                "columns": [col1, col2],
                                "fig": fig
                            })
            
            st.rerun()
    
    # Tab 3: Visualizations
    with tab3:
        st.header("📈 Automated Visualizations & Dashboard")
        
        if st.session_state.current_df is not None:
            df = st.session_state.current_df
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # Auto-generate dashboard button
            if st.button("🚀 Generate Complete Dashboard", type="primary"):
                st.session_state.show_dashboard = True
            
            # Show automated dashboard
            if st.session_state.get('show_dashboard', False):
                st.success("✅ Automated Dashboard Generated!")
                
                # Section 1: Key Metrics
                st.subheader("📊 Key Metrics Dashboard")
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.metric("Total Rows", f"{len(df):,}")
                with col2:
                    st.metric("Total Columns", df.shape[1])
                with col3:
                    st.metric("Numeric Cols", len(numeric_cols))
                with col4:
                    st.metric("Categorical Cols", len(categorical_cols))
                with col5:
                    st.metric("Missing Values", df.isnull().sum().sum())
                
                st.divider()
                
                # Section 2: Correlation Analysis (Auto)
                if len(numeric_cols) > 1:
                    st.subheader("🔥 Correlation Analysis")
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        fig, ax = plt.subplots(figsize=(10, 8))
                        corr_matrix = df[numeric_cols].corr()
                        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
                        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='RdYlGn', 
                                   center=0, fmt='.2f', square=True, linewidths=1, ax=ax)
                        plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
                        st.pyplot(fig)
                    
                    with col2:
                        st.markdown("**Strong Correlations:**")
                        strong_corr = []
                        for i in range(len(corr_matrix.columns)):
                            for j in range(i+1, len(corr_matrix.columns)):
                                corr_val = corr_matrix.iloc[i, j]
                                if abs(corr_val) > 0.5:
                                    col1_name = corr_matrix.columns[i]
                                    col2_name = corr_matrix.columns[j]
                                    strong_corr.append((col1_name, col2_name, corr_val))
                        
                        if strong_corr:
                            for col1_name, col2_name, corr_val in sorted(strong_corr, key=lambda x: abs(x[2]), reverse=True):
                                emoji = "🔴" if corr_val < 0 else "🟢"
                                st.write(f"{emoji} **{col1_name}** ↔ **{col2_name}**: {corr_val:.3f}")
                        else:
                            st.info("No strong correlations found (|r| > 0.5)")
                
                st.divider()
                
                # Section 3: Distribution Analysis (Auto)
                if len(numeric_cols) > 0:
                    st.subheader("📊 Distribution Analysis")
                    
                    # Show up to 6 distributions
                    cols_to_show = numeric_cols[:6]
                    n_cols = min(3, len(cols_to_show))
                    n_rows = (len(cols_to_show) + n_cols - 1) // n_cols
                    
                    for row in range(n_rows):
                        cols = st.columns(n_cols)
                        for col_idx in range(n_cols):
                            idx = row * n_cols + col_idx
                            if idx < len(cols_to_show):
                                col_name = cols_to_show[idx]
                                with cols[col_idx]:
                                    fig = px.histogram(df, x=col_name, marginal="box",
                                                     title=f'{col_name}',
                                                     color_discrete_sequence=['#636EFA'])
                                    fig.update_layout(height=300, showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # Section 4: Outlier Detection (Auto)
                if len(numeric_cols) > 0:
                    st.subheader("⚠️ Outlier Detection")
                    
                    outlier_summary = []
                    for col in numeric_cols:
                        Q1 = df[col].quantile(0.25)
                        Q3 = df[col].quantile(0.75)
                        IQR = Q3 - Q1
                        outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
                        if outliers > 0:
                            outlier_summary.append({
                                'Column': col,
                                'Outliers': outliers,
                                'Percentage': f"{(outliers/len(df)*100):.2f}%"
                            })
                    
                    if outlier_summary:
                        col1, col2 = st.columns([1, 2])
                        
                        with col1:
                            outlier_df = pd.DataFrame(outlier_summary)
                            st.dataframe(outlier_df, use_container_width=True)
                        
                        with col2:
                            # Box plots for columns with outliers
                            cols_with_outliers = [item['Column'] for item in outlier_summary[:3]]
                            if cols_with_outliers:
                                fig = go.Figure()
                                for col in cols_with_outliers:
                                    fig.add_trace(go.Box(y=df[col], name=col))
                                fig.update_layout(title="Box Plots - Outlier Detection",
                                                height=400, showlegend=True)
                                st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.success("✅ No outliers detected in numeric columns!")
                
                st.divider()
                
                # Section 5: Categorical Analysis (Auto)
                if len(categorical_cols) > 0:
                    st.subheader("📊 Categorical Data Analysis")
                    
                    cols_to_show = categorical_cols[:4]
                    n_cols = min(2, len(cols_to_show))
                    n_rows = (len(cols_to_show) + n_cols - 1) // n_cols
                    
                    for row in range(n_rows):
                        cols = st.columns(n_cols)
                        for col_idx in range(n_cols):
                            idx = row * n_cols + col_idx
                            if idx < len(cols_to_show):
                                col_name = cols_to_show[idx]
                                with cols[col_idx]:
                                    value_counts = df[col_name].value_counts().head(10)
                                    fig = px.bar(x=value_counts.index, y=value_counts.values,
                                               title=f'{col_name} Distribution',
                                               labels={'x': col_name, 'y': 'Count'})
                                    fig.update_layout(height=300, showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # Section 6: Missing Values Analysis (Auto)
                missing_data = df.isnull().sum()
                if missing_data.sum() > 0:
                    st.subheader("❓ Missing Values Analysis")
                    
                    col1, col2 = st.columns([1, 2])
                    
                    with col1:
                        missing_df = pd.DataFrame({
                            'Column': missing_data[missing_data > 0].index,
                            'Missing': missing_data[missing_data > 0].values,
                            'Percentage': (missing_data[missing_data > 0] / len(df) * 100).round(2).values
                        })
                        st.dataframe(missing_df, use_container_width=True)
                    
                    with col2:
                        fig = px.bar(missing_df, x='Column', y='Percentage',
                                   title='Missing Values by Column (%)',
                                   color='Percentage',
                                   color_continuous_scale='Reds')
                        fig.update_layout(height=400)
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    st.success("✅ No missing values in the dataset!")
                
                st.divider()
                
                # Section 7: Relationship Analysis (Auto)
                if len(numeric_cols) >= 2:
                    st.subheader("🔗 Relationship Analysis")
                    
                    # Create scatter matrix for top correlated pairs
                    if len(numeric_cols) >= 2:
                        # Get top 4 numeric columns by variance
                        top_cols = df[numeric_cols].var().nlargest(4).index.tolist()
                        
                        if len(categorical_cols) > 0:
                            color_col = categorical_cols[0]
                            fig = px.scatter_matrix(df, dimensions=top_cols, color=color_col,
                                                  title="Scatter Matrix - Top Variables")
                        else:
                            fig = px.scatter_matrix(df, dimensions=top_cols,
                                                  title="Scatter Matrix - Top Variables")
                        
                        fig.update_layout(height=600)
                        st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                
                # Section 8: Statistical Summary (Auto)
                st.subheader("📈 Statistical Summary")
                st.dataframe(df.describe(), use_container_width=True)
                
                st.divider()
                
                # Section 9: AI-Generated Insights (Auto)
                st.subheader("🤖 AI-Generated Insights")
                
                if st.button("🧠 Generate AI Insights for Dashboard"):
                    with st.spinner("🤖 AI is analyzing your data..."):
                        insight_prompt = """Based on the dashboard visualizations and data analysis, provide:
1. Top 3 key insights
2. Notable patterns or trends
3. Potential data quality issues
4. Recommendations for further analysis"""
                        
                        response = st.session_state.chatbot.chat(insight_prompt)
                        st.markdown(response)
                
                # Download dashboard report
                st.divider()
                st.success("✅ Dashboard Complete! You can now export your analysis.")
                
            else:
                st.info("👆 Click 'Generate Complete Dashboard' to automatically create all visualizations!")
            
            st.divider()
            
            # Manual visualization options
            st.subheader("🎨 Custom Visualizations")
            viz_type = st.selectbox(
                "Select Visualization Type",
                ["Correlation Heatmap", "Distribution Plots", "Box Plots", "Scatter Plot", "Bar Chart", "Pair Plot"]
            )
            
            if viz_type == "Correlation Heatmap" and len(numeric_cols) > 1:
                st.subheader("🔥 Correlation Heatmap")
                fig, ax = plt.subplots(figsize=(10, 8))
                corr_matrix = df[numeric_cols].corr()
                sns.heatmap(corr_matrix, annot=True, cmap='RdYlGn', center=0, fmt='.2f', ax=ax)
                plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
                st.pyplot(fig)
            
            elif viz_type == "Distribution Plots" and len(numeric_cols) > 0:
                st.subheader("📊 Distribution Plots")
                selected_col = st.selectbox("Select column", numeric_cols)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    fig, ax = plt.subplots(figsize=(8, 6))
                    df[selected_col].hist(bins=30, edgecolor='black', ax=ax)
                    ax.set_title(f'Histogram: {selected_col}')
                    ax.set_xlabel(selected_col)
                    ax.set_ylabel('Frequency')
                    st.pyplot(fig)
                
                with col2:
                    fig = px.box(df, y=selected_col, title=f'Box Plot: {selected_col}')
                    st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Box Plots" and len(numeric_cols) > 0:
                st.subheader("📦 Box Plots")
                selected_col = st.selectbox("Select column", numeric_cols)
                
                if len(categorical_cols) > 0:
                    group_by = st.selectbox("Group by (optional)", ["None"] + categorical_cols)
                    if group_by != "None":
                        fig = px.box(df, x=group_by, y=selected_col, title=f'{selected_col} by {group_by}')
                    else:
                        fig = px.box(df, y=selected_col, title=f'Box Plot: {selected_col}')
                else:
                    fig = px.box(df, y=selected_col, title=f'Box Plot: {selected_col}')
                
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Scatter Plot" and len(numeric_cols) >= 2:
                st.subheader("🔵 Scatter Plot")
                col1, col2 = st.columns(2)
                with col1:
                    x_col = st.selectbox("X-axis", numeric_cols)
                with col2:
                    y_col = st.selectbox("Y-axis", [c for c in numeric_cols if c != x_col])
                
                color_by = None
                if len(categorical_cols) > 0:
                    color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols)
                    if color_by == "None":
                        color_by = None
                
                fig = px.scatter(df, x=x_col, y=y_col, color=color_by, 
                               title=f'{y_col} vs {x_col}')
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Bar Chart" and len(categorical_cols) > 0:
                st.subheader("📊 Bar Chart")
                selected_col = st.selectbox("Select categorical column", categorical_cols)
                
                value_counts = df[selected_col].value_counts()
                fig = px.bar(x=value_counts.index, y=value_counts.values,
                           labels={'x': selected_col, 'y': 'Count'},
                           title=f'Distribution of {selected_col}')
                st.plotly_chart(fig, use_container_width=True)
            
            elif viz_type == "Pair Plot" and len(numeric_cols) >= 2:
                st.subheader("🔗 Pair Plot")
                
                # Select columns
                selected_cols = st.multiselect(
                    "Select columns (2-5 recommended)",
                    numeric_cols,
                    default=numeric_cols[:min(3, len(numeric_cols))]
                )
                
                if len(selected_cols) >= 2:
                    color_by = None
                    if len(categorical_cols) > 0:
                        color_by = st.selectbox("Color by (optional)", ["None"] + categorical_cols)
                        if color_by == "None":
                            color_by = None
                    
                    if color_by:
                        fig = px.scatter_matrix(df, dimensions=selected_cols, color=color_by,
                                              title="Pair Plot")
                    else:
                        fig = px.scatter_matrix(df, dimensions=selected_cols,
                                              title="Pair Plot")
                    
                    fig.update_layout(height=800)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Please select at least 2 columns")
    
    # Tab 4: Data
    with tab4:
        st.header("📋 Raw Data")
        
        if st.session_state.current_df is not None:
            df = st.session_state.current_df
            
            # Display options
            col1, col2, col3 = st.columns(3)
            with col1:
                show_rows = st.number_input("Rows to display", min_value=5, max_value=len(df), value=min(100, len(df)))
            with col2:
                show_stats = st.checkbox("Show Statistics", value=False)
            with col3:
                show_info = st.checkbox("Show Info", value=False)
            
            # Display data
            st.dataframe(df.head(show_rows), use_container_width=True)
            
            if show_stats:
                st.subheader("📊 Statistical Summary")
                st.dataframe(df.describe(), use_container_width=True)
            
            if show_info:
                st.subheader("ℹ️ Dataset Info")
                buffer = io.StringIO()
                df.info(buf=buffer)
                st.text(buffer.getvalue())
            
            # Download button
            st.divider()
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Dataset as CSV",
                data=csv,
                file_name="analyzed_data.csv",
                mime="text/csv"
            )

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>🤖 AI Data Analyst Chatbot | Powered by Groq API (llama-3.3-70b-versatile)</p>
    <p>Made with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
