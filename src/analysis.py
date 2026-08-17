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
    
    
# ---------- تحلیل مشتری (RFM ساده) ----------

def customer_analysis(df: pd.DataFrame, top_n: int = 5) -> dict:
    """
    خلاصه‌ای از رفتار مشتری‌ها: مشتریان VIP، تعداد خرید، و مشتریانی
    که مدتی است خرید نکرده‌اند (ریسک ریزش)
    """
    last_date = df["Order_Date"].max()

    customer_summary = df.groupby(["Customer_ID", "Customer_Name"]).agg(
        total_spent=("Sales", "sum"),
        order_count=("Order_ID", "nunique"),
        last_purchase=("Order_Date", "max"),
    ).reset_index()

    customer_summary["days_since_last_purchase"] = (
        last_date - customer_summary["last_purchase"]
    ).dt.days

    top_customers = customer_summary.sort_values("total_spent", ascending=False).head(top_n)

    # مشتریانی که بیش از ۹۰ روز خرید نکرده‌اند ولی قبلاً مشتری فعالی بودند (حداقل ۲ خرید)
    at_risk = customer_summary[
        (customer_summary["days_since_last_purchase"] > 90)
        & (customer_summary["order_count"] >= 2)
    ].sort_values("total_spent", ascending=False).head(top_n)

    return {
        "top_customers": top_customers[["Customer_Name", "total_spent", "order_count"]],
        "at_risk_customers": at_risk[["Customer_Name", "total_spent", "days_since_last_purchase"]],
        "avg_orders_per_customer": round(customer_summary["order_count"].mean(), 2),
        "total_unique_customers": len(customer_summary),
    }


# ---------- تأثیر تخفیف بر سود ----------

def discount_impact_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    رابطه بین بازه تخفیف و سود را بررسی می‌کند تا مشخص شود
    از چه درصدی به بعد، تخفیف باعث ضرر می‌شود
    """
    df = df.copy()
    bins = [-0.01, 0, 0.1, 0.2, 0.3, 0.5, 1.0]
    labels = ["0%", "1-10%", "11-20%", "21-30%", "31-50%", "50%+"]
    df["discount_band"] = pd.cut(df["Discount"], bins=bins, labels=labels)

    result = df.groupby("discount_band", observed=True).agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum"),
        avg_profit_margin=("Profit", lambda x: round((x.sum() / df.loc[x.index, "Sales"].sum()) * 100, 1)),
        order_count=("Order_ID", "nunique"),
    ).reset_index()

    return result


# ---------- محصولات/دسته‌های ضررده ----------

def loss_making_subcategories(df: pd.DataFrame) -> pd.DataFrame:
    """دسته‌های فرعی که مجموع سودشان منفی است"""
    sub_cat = df.groupby("Sub_Category").agg(
        total_sales=("Sales", "sum"),
        total_profit=("Profit", "sum"),
    ).reset_index()

    losers = sub_cat[sub_cat["total_profit"] < 0].sort_values("total_profit")
    return losers    