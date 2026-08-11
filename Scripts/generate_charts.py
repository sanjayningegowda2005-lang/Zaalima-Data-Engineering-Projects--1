import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Ensure Dashboard folder exists
os.makedirs("Dashboard", exist_ok=True)

def generate_dashboard():
    conn = sqlite3.connect("telecom_staging.db")
    sns.set_theme(style="whitegrid")
    
    # Chart 1: Customer Status Breakdown
    df_status = pd.read_sql_query("SELECT customer_status, COUNT(*) as count FROM stg_customer_churn GROUP BY customer_status", conn)
    plt.figure(figsize=(7, 5))
    sns.barplot(data=df_status, x='customer_status', y='count', palette='Blues_d')
    plt.title("Overall Customer Status Distribution")
    plt.xlabel("Customer Status")
    plt.ylabel("Total Customers")
    plt.tight_layout()
    plt.savefig("Dashboard/customer_status_distribution.png")
    plt.close()

    # Chart 2: Top Churn Reasons
    df_reasons = pd.read_sql_query("SELECT churn_reason, COUNT(*) as count FROM stg_customer_churn WHERE customer_status = 'Churned' GROUP BY churn_reason ORDER BY count DESC LIMIT 5", conn)
    plt.figure(figsize=(9, 5))
    sns.barplot(data=df_reasons, y='churn_reason', x='count', palette='Reds_d')
    plt.title("Top 5 Reasons for Customer Churn")
    plt.xlabel("Number of Churned Customers")
    plt.ylabel("Reason")
    plt.tight_layout()
    plt.savefig("Dashboard/top_churn_reasons.png")
    plt.close()

    conn.close()
    print("Dashboard charts generated successfully in 'Dashboard/' directory.")

if __name__ == "__main__":
    generate_dashboard()