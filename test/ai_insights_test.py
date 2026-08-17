import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
 
# test_new_analysis.py (موقتی)
from src.analysis import *

df = load_sales_data()

print("--- تحلیل مشتری ---")
cust = customer_analysis(df)
print("VIP:\n", cust["top_customers"])
print("\nAt Risk:\n", cust["at_risk_customers"])

print("\n--- تأثیر تخفیف ---")
print(discount_impact_analysis(df))

print("\n--- دسته‌های ضررده ---")
print(loss_making_subcategories(df))