import schedule
import time
from datetime import datetime
from src.pipeline import run_pipeline

def scheduled_job():
    print(f"\n⏰ اجرای زمان‌بندی‌شده — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    try:
        run_pipeline()
    except Exception as e:
        print(f"❌ اجرای خودکار با خطا مواجه شد: {e}")

schedule.every().day.at("08:00").do(scheduled_job)

if __name__ == "__main__":
    print("🔄 سرویس اتوماسیون فعال شد.")
    scheduled_job()
    while True:
        schedule.run_pending()
        time.sleep(30) 