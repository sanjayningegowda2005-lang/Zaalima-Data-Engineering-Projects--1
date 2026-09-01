"""
Automated Visualization & Chart Engine
Author: Sanjay (Team Lead)
Description: Queries analytical SQL views and exports visual dashboard charts.
"""
import sqlite3
import logging
from pathlib import Path
import matplotlib.pyplot as plt

def generate_dashboard_charts(db_path: Path, output_dir: Path):
    """
    Extracts aggregated data from SQLite views and exports PNG visual charts.
    """
    if not db_path.exists():
        logging.error(f"Database not found at {db_path}")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    logging.info(f"Generating visual reports in: {output_dir}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query Product Revenue View
        cursor.execute("SELECT product, total_revenue FROM view_product_revenue")
        rows = cursor.fetchall()
        
        if rows:
            products = [r[0] for r in rows]
            revenues = [r[1] for r in rows]

            plt.figure(figsize=(8, 4.5))
            plt.bar(products, revenues, color='#1f77b4', edgecolor='black')
            plt.title('Total Revenue by Product', fontsize=14, fontweight='bold')
            plt.xlabel('Product Category', fontsize=11)
            plt.ylabel('Revenue (INR)', fontsize=11)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.tight_layout()
            
            chart_file = output_dir / "product_revenue_chart.png"
            plt.savefig(chart_file, dpi=300)
            plt.close()
            logging.info(f"[PASS] Visual chart generated: {chart_file}")

        conn.close()
        return True

    except Exception as e:
        logging.error(f"Failed to generate dashboard charts: {e}")
        return False