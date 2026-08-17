import os
import sys
from src.analysis import (
    load_sales_data, generate_summary_stats, monthly_revenue_trend,
    top_products, detect_anomalies, region_performance,
    customer_analysis, discount_impact_analysis, loss_making_subcategories,   # ← جدید
)
from src.ai_insights import build_analysis_prompt, get_ai_insights
from src.report import plot_discount_impact, plot_monthly_trend, plot_top_products, build_html_report


def check_prerequisites():
    """قبل از اجرا مطمئن میشه همه‌چیز آماده‌ست"""
    if not os.getenv("OPENAI_API_KEY"):
        # اگه dotenv لود نشده باشه هم چک می‌کنیم
        from dotenv import load_dotenv
        load_dotenv()
        if not os.getenv("OPENAI_API_KEY"):
            raise EnvironmentError(
                "❌ OPENAI_API_KEY پیدا نشد. مطمئن شو فایل .env رو ساختی و کلید رو توش گذاشتی."
            )

    from pathlib import Path
    db_path = Path("data/business.db")
    if not db_path.exists():
        raise FileNotFoundError(
            "❌ دیتابیس پیدا نشد. اول python src/db.py رو اجرا کن تا داده لود بشه."
        )


def run_pipeline():
    check_prerequisites()

    print("📥 در حال بارگذاری داده...")
    try:
        df = load_sales_data()
    except Exception as e:
        raise RuntimeError(f"خطا در خواندن داده از دیتابیس: {e}")

    if df.empty:
        raise ValueError("❌ دیتابیس خالیه. داده‌ای برای تحلیل وجود نداره.")

    print("📊 در حال تحلیل...")
    stats = generate_summary_stats(df)
    monthly = monthly_revenue_trend(df)
    top_prods = top_products(df)
    anomalies = detect_anomalies(monthly)
    region_perf = region_performance(df)
    customer_data = customer_analysis(df)
    discount_impact = discount_impact_analysis(df)
    loss_makers = loss_making_subcategories(df)

    print("🤖 در حال دریافت تحلیل از AI...")
    try:
        prompt = build_analysis_prompt(
        stats, monthly, top_prods, anomalies, region_perf,
        customer_data, discount_impact, loss_makers   # ← جدید
    )
        ai_text = get_ai_insights(prompt)
    except Exception as e:
        print(f"⚠️ اتصال به AI با خطا مواجه شد ({e}). گزارش بدون تحلیل AI ساخته میشه.")
        ai_text = "تحلیل هوش مصنوعی در دسترس نبود."

    print("📈 در حال ساخت نمودارها...")
    chart1 = plot_monthly_trend(monthly)
    chart2 = plot_top_products(top_prods)
    
    chart3 = plot_discount_impact(discount_impact)   # ← جدید

    print("📄 در حال ساخت گزارش نهایی...")
    
    
    report_path = build_html_report(
        stats, ai_text, chart1, chart2, chart3,
        region_perf, customer_data, loss_makers   # ← جدید
    )
    print(f"✅ گزارش با موفقیت ساخته شد: {report_path}")
    return report_path


if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\n🛑 اجرای پروژه متوقف شد:\n{e}")
        sys.exit(1)