import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
 

# test_ai.py (موقتی)
from src.analysis import *
from src.ai_insights import build_analysis_prompt, get_ai_insights

df = load_sales_data()
monthly = monthly_revenue_trend(df)

prompt = build_analysis_prompt(
    summary_stats=generate_summary_stats(df),
    monthly_trend=monthly,
    top_prods=top_products(df),
    anomalies=detect_anomalies(monthly),
    region_perf=region_performance(df),
)

print("--- در حال ارسال به AI ---")
result = get_ai_insights(prompt)
print(result)