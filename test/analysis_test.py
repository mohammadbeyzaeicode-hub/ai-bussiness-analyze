import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
 

# # test_analysis.py (موقتی، بعداً پاک می‌کنیم)
# from src.analysis import *

# df = load_sales_data()
# print(generate_summary_stats(df))
# print("\n--- روند ماهانه ---")
# print(monthly_revenue_trend(df).tail())
# print("\n--- محصولات پرفروش ---")
# print(top_products(df))
# print("\n--- ناهنجاری‌ها ---")
# print(detect_anomalies(monthly_revenue_trend(df)))
 
 
 
from src.analysis import load_sales_data
df = load_sales_data()
print(df.columns.tolist())