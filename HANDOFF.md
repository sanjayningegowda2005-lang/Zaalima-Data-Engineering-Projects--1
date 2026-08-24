# Team Integration & Handoff Guide

## 1. Quickstart
1. Clone / Pull the latest main branch:
   git checkout main
   git pull origin main

2. Run the orchestrator script:
   python main.py

## 2. Data Outputs & Staging
- SQLite Database: pipeline_staging.db
- Execution Log: pipeline_execution.log
- Output Charts: Saved in Dashboard/

## 3. SQL Views Available
- view_product_revenue: Aggregates total revenue and sales count per product line.
- view_customer_summary: Summarizes order volumes and transaction metrics per customer.
