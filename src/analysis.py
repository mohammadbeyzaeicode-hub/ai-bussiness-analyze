import pandas as pd
from src.db import get_connection


def load_sales_data() -> pd.DataFrame:
    """کل داده فروش رو از دیتابیس می‌خونه و تاریخ‌ها رو تبدیل می‌کنه"""
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM sales", conn)
    conn.close()

    # تبدیل ستون تاریخ (اسم ستون بسته به دیتاست ممکنه Order_Date باشه)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], format="%m/%d/%Y")
    return df


def monthly_revenue_trend(df: pd.DataFrame) -> pd.DataFrame:
    """روند فروش ماهانه رو محاسبه می‌کنه"""
    monthly = (
        df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"]
        .sum()
        .reset_index()
    )
    monthly["Order_Date"] = monthly["Order_Date"].astype(str)
    monthly.columns = ["month", "revenue"]

    # درصد تغییر نسبت به ماه قبل — این خیلی مهمه برای AI insight
    monthly["growth_pct"] = monthly["revenue"].pct_change().round(3) * 100
    return monthly


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """پرفروش‌ترین محصولات بر اساس درآمد"""
    return (
        df.groupby("Product_Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )


def top_categories_by_profit(df: pd.DataFrame) -> pd.DataFrame:
    """سودآورترین دسته‌بندی‌ها"""
    return (
        df.groupby("Category")[["Sales", "Profit"]]
        .sum()
        .sort_values("Profit", ascending=False)
        .reset_index()
    )


def detect_anomalies(monthly_df: pd.DataFrame, threshold: float = 20.0) -> pd.DataFrame:
    """
    ماه‌هایی که تغییر فروش‌شون نسبت به ماه قبل بیشتر از threshold درصد بوده رو پیدا می‌کنه
    (چه افت شدید چه رشد شدید)
    """
    anomalies = monthly_df[monthly_df["growth_pct"].abs() > threshold].copy()
    return anomalies


def region_performance(df: pd.DataFrame) -> pd.DataFrame:
    """عملکرد فروش و سود به تفکیک منطقه"""
    return (
        df.groupby("Region")[["Sales", "Profit"]]
        .sum()
        .sort_values("Sales", ascending=False)
        .reset_index()
    )


def generate_summary_stats(df: pd.DataFrame) -> dict:
    """یک دیکشنری خلاصه از مهم‌ترین KPIها، برای دادن مستقیم به AI"""
    return {
        "total_revenue": round(df["Sales"].sum(), 2),
        "total_profit": round(df["Profit"].sum(), 2),
        "profit_margin_pct": round((df["Profit"].sum() / df["Sales"].sum()) * 100, 2),
        "total_orders": df["Order_ID"].nunique(),
        "date_range": f"{df['Order_Date'].min().date()} to {df['Order_Date'].max().date()}",
        "avg_order_value": round(df["Sales"].sum() / df["Order_ID"].nunique(), 2),
    }