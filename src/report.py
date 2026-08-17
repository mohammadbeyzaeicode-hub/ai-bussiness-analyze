import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

REPORTS_DIR = Path(__file__).parent.parent / "reports"
REPORTS_DIR.mkdir(exist_ok=True)


def plot_monthly_trend(monthly_df, save_name="monthly_trend.png") -> str:
    """نمودار روند فروش ماهانه رو می‌سازه و ذخیره می‌کنه"""
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(monthly_df["month"], monthly_df["revenue"], marker="o", color="#2563eb")
    ax.set_title("روند فروش ماهانه")
    ax.set_ylabel("درآمد ($)")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    path = REPORTS_DIR / save_name
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return save_name


def plot_top_products(top_df, save_name="top_products.png") -> str:
    """نمودار میله‌ای پرفروش‌ترین محصولات"""
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.barh(top_df["Product_Name"].str[:30], top_df["Sales"], color="#059669")
    ax.invert_yaxis()
    ax.set_title("پرفروش‌ترین محصولات")
    ax.set_xlabel("درآمد ($)")
    fig.tight_layout()

    path = REPORTS_DIR / save_name
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return save_name


def build_html_report(summary_stats: dict, ai_text: str, chart1: str, chart2: str,
                       region_perf, save_name: str = None) -> str:
    """همه‌چیز رو توی یک فایل HTML قابل‌ارائه ترکیب می‌کنه"""
    if save_name is None:
        save_name = f"report_{datetime.now().strftime('%Y%m%d_%H%M')}.html"

    region_table_html = region_perf.to_html(index=False, classes="table")

    # تبدیل متن AI (که با \n \n جدا شده) به پاراگراف‌های HTML
    ai_html = "".join(f"<p>{line}</p>" for line in ai_text.split("\n") if line.strip())

    html = f"""
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
    <meta charset="UTF-8">
    <title>گزارش تحلیل کسب‌وکار</title>
    <style>
        body {{ font-family: Tahoma, sans-serif; max-width: 900px; margin: 40px auto; color: #1f2937; }}
        h1 {{ color: #111827; }}
        .kpi-box {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 20px 0; }}
        .kpi {{ background: #f3f4f6; padding: 16px 20px; border-radius: 10px; flex: 1; min-width: 140px; }}
        .kpi .value {{ font-size: 22px; font-weight: bold; color: #2563eb; }}
        .kpi .label {{ font-size: 13px; color: #6b7280; }}
        .ai-box {{ background: #eff6ff; border-right: 4px solid #2563eb; padding: 16px 20px; border-radius: 8px; margin: 20px 0; }}
        table.table {{ border-collapse: collapse; width: 100%; margin: 10px 0; }}
        table.table th, table.table td {{ border: 1px solid #e5e7eb; padding: 8px 12px; text-align: right; }}
        table.table th {{ background: #f9fafb; }}
        img {{ max-width: 100%; border-radius: 8px; margin: 10px 0; }}
    </style>
    </head>
    <body>
        <h1>📊 گزارش تحلیل کسب‌وکار</h1>
        <p style="color:#6b7280">تولید شده در {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

        <div class="kpi-box">
            <div class="kpi"><div class="value">${summary_stats['total_revenue']:,.0f}</div><div class="label">درآمد کل</div></div>
            <div class="kpi"><div class="value">${summary_stats['total_profit']:,.0f}</div><div class="label">سود کل</div></div>
            <div class="kpi"><div class="value">{summary_stats['profit_margin_pct']}%</div><div class="label">حاشیه سود</div></div>
            <div class="kpi"><div class="value">{summary_stats['total_orders']:,}</div><div class="label">تعداد سفارش</div></div>
        </div>

        <h2>🤖 تحلیل هوش مصنوعی</h2>
        <div class="ai-box">{ai_html}</div>

        <h2>روند فروش ماهانه</h2>
        <img src="{chart1}" alt="روند فروش">

        <h2>پرفروش‌ترین محصولات</h2>
        <img src="{chart2}" alt="محصولات پرفروش">

        <h2>عملکرد مناطق</h2>
        {region_table_html}
    </body>
    </html>
    """

    path = REPORTS_DIR / save_name
    path.write_text(html, encoding="utf-8")
    return str(path)