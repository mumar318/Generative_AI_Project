"""
Generate sample datasets for testing the AI Data Analyst Chatbot
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_sales_dataset(n_rows=500):
    """Create a realistic sales dataset"""
    np.random.seed(42)
    
    # Generate dates
    start_date = datetime(2023, 1, 1)
    dates = [start_date + timedelta(days=i) for i in range(n_rows)]
    
    # Generate data
    data = {
        'date': dates,
        'product_id': np.random.randint(1, 21, n_rows),
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Books', 'Home'], n_rows),
        'region': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_rows),
        'sales_amount': np.random.uniform(10, 1000, n_rows).round(2),
        'quantity': np.random.randint(1, 50, n_rows),
        'customer_age': np.random.randint(18, 75, n_rows),
        'customer_satisfaction': np.random.randint(1, 6, n_rows),
        'discount_applied': np.random.choice([True, False], n_rows, p=[0.3, 0.7]),
        'shipping_cost': np.random.uniform(0, 50, n_rows).round(2)
    }
    
    df = pd.DataFrame(data)
    
    # Add some correlations
    df.loc[df['discount_applied'], 'sales_amount'] *= 0.85
    df.loc[df['category'] == 'Electronics', 'sales_amount'] *= 1.5
    df['profit'] = (df['sales_amount'] - df['shipping_cost']) * 0.3
    
    # Add missing values (realistic)
    missing_indices = np.random.choice(n_rows, int(n_rows * 0.05), replace=False)
    df.loc[missing_indices, 'customer_satisfaction'] = np.nan
    
    missing_indices = np.random.choice(n_rows, int(n_rows * 0.03), replace=False)
    df.loc[missing_indices, 'shipping_cost'] = np.nan
    
    return df

def create_customer_dataset(n_rows=300):
    """Create a customer behavior dataset"""
    np.random.seed(123)
    
    data = {
        'customer_id': range(1, n_rows + 1),
        'age': np.random.randint(18, 80, n_rows),
        'income': np.random.randint(20000, 200000, n_rows),
        'credit_score': np.random.randint(300, 850, n_rows),
        'years_customer': np.random.randint(0, 20, n_rows),
        'num_purchases': np.random.randint(0, 100, n_rows),
        'total_spent': np.random.uniform(0, 50000, n_rows).round(2),
        'loyalty_tier': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], n_rows),
        'churn_risk': np.random.choice(['Low', 'Medium', 'High'], n_rows, p=[0.6, 0.3, 0.1]),
        'email_engagement': np.random.uniform(0, 1, n_rows).round(3)
    }
    
    df = pd.DataFrame(data)
    
    # Add correlations
    df.loc[df['income'] > 100000, 'credit_score'] += 50
    df.loc[df['years_customer'] > 10, 'loyalty_tier'] = np.random.choice(['Gold', 'Platinum'], 
                                                                          sum(df['years_customer'] > 10))
    df['avg_purchase_value'] = (df['total_spent'] / (df['num_purchases'] + 1)).round(2)
    
    # Add missing values
    missing_indices = np.random.choice(n_rows, int(n_rows * 0.08), replace=False)
    df.loc[missing_indices, 'income'] = np.nan
    
    missing_indices = np.random.choice(n_rows, int(n_rows * 0.04), replace=False)
    df.loc[missing_indices, 'email_engagement'] = np.nan
    
    return df

def create_employee_dataset(n_rows=200):
    """Create an employee performance dataset"""
    np.random.seed(456)
    
    data = {
        'employee_id': range(1, n_rows + 1),
        'department': np.random.choice(['Sales', 'Engineering', 'Marketing', 'HR', 'Finance'], n_rows),
        'age': np.random.randint(22, 65, n_rows),
        'years_experience': np.random.randint(0, 40, n_rows),
        'salary': np.random.randint(30000, 150000, n_rows),
        'performance_score': np.random.uniform(1, 5, n_rows).round(2),
        'projects_completed': np.random.randint(0, 50, n_rows),
        'training_hours': np.random.randint(0, 200, n_rows),
        'satisfaction_score': np.random.randint(1, 11, n_rows),
        'remote_work_days': np.random.randint(0, 5, n_rows)
    }
    
    df = pd.DataFrame(data)
    
    # Add correlations
    df.loc[df['years_experience'] > 10, 'salary'] += 20000
    df.loc[df['department'] == 'Engineering', 'salary'] *= 1.2
    df['promotion_eligible'] = ((df['performance_score'] > 4) & 
                                (df['years_experience'] > 2)).astype(int)
    
    # Add missing values
    missing_indices = np.random.choice(n_rows, int(n_rows * 0.06), replace=False)
    df.loc[missing_indices, 'satisfaction_score'] = np.nan
    
    return df

if __name__ == "__main__":
    print("🎲 Generating Sample Datasets...\n")
    
    # Generate datasets
    print("1️⃣ Creating Sales Dataset...")
    sales_df = create_sales_dataset(500)
    sales_df.to_csv('sample_sales_data.csv', index=False)
    print(f"   ✅ Saved: sample_sales_data.csv ({sales_df.shape[0]} rows, {sales_df.shape[1]} columns)")
    
    print("\n2️⃣ Creating Customer Dataset...")
    customer_df = create_customer_dataset(300)
    customer_df.to_csv('sample_customer_data.csv', index=False)
    print(f"   ✅ Saved: sample_customer_data.csv ({customer_df.shape[0]} rows, {customer_df.shape[1]} columns)")
    
    print("\n3️⃣ Creating Employee Dataset...")
    employee_df = create_employee_dataset(200)
    employee_df.to_csv('sample_employee_data.csv', index=False)
    print(f"   ✅ Saved: sample_employee_data.csv ({employee_df.shape[0]} rows, {employee_df.shape[1]} columns)")
    
    print("\n" + "="*80)
    print("✅ All sample datasets created successfully!")
    print("="*80)
    print("\n📊 You can now use these files to test the AI Data Analyst Chatbot:")
    print("   • sample_sales_data.csv - Sales and revenue analysis")
    print("   • sample_customer_data.csv - Customer behavior and segmentation")
    print("   • sample_employee_data.csv - HR and performance analytics")
    print("\n💡 Load any of these in Analysis.ipynb or Analysis_chatbot.py")
