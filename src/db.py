import pandas as pd
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "business.db"

def load_csv_to_db(csv_path: str, table_name: str = "sales"):
    """داده CSV رو می‌خونه و توی SQLite ذخیره می‌کنه"""
    df = pd.read_csv(csv_path, encoding="latin1")  # این دیتاست معمولاً latin1 هست
    
    # تمیزکاری اولیه اسم ستون‌ها (فاصله و کاراکترهای عجیب رو حذف می‌کنیم)
    df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]
    
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ {len(df)} ردیف با موفقیت توی جدول '{table_name}' ذخیره شد.")

def get_connection():
    return sqlite3.connect(DB_PATH)

if __name__ == "__main__":
    load_csv_to_db("Sample - Superstore.csv")  # مسیر فایل دانلودی رو اینجا بذار