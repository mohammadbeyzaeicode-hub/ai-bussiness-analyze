import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from config import API_KEY,BASE_URL
load_dotenv()
client = OpenAI(api_key=API_KEY,base_url=BASE_URL)


def build_analysis_prompt(summary_stats: dict, monthly_trend, top_prods, anomalies, region_perf) -> str:
    """داده‌های تحلیل‌شده رو به یک پرامپت ساختارمند تبدیل می‌کنه"""
    return f"""
تو یک تحلیلگر ارشد کسب‌وکار (Business Analyst) هستی. داده‌های زیر خلاصه عملکرد فروش یک فروشگاه است.

### خلاصه کلی
{json.dumps(summary_stats, ensure_ascii=False, indent=2)}

### روند فروش ماهانه (۶ ماه اخیر)
{monthly_trend.tail(6).to_string(index=False)}

### پرفروش‌ترین محصولات
{top_prods.to_string(index=False)}

### ماه‌های با تغییر غیرعادی (بیش از ۲۰٪ نسبت به ماه قبل)
{anomalies.to_string(index=False) if not anomalies.empty else "موردی یافت نشد"}

### عملکرد مناطق
{region_perf.to_string(index=False)}

---
بر اساس این داده‌ها، یک گزارش تحلیلی کوتاه به فارسی بنویس شامل:
1. **خلاصه وضعیت** (۲-۳ جمله)
2. **۳ نکته کلیدی** که یک مدیر باید بدونه
3. **هشدارها یا ریسک‌ها** (اگر ناهنجاری وجود داره، دلیل احتمالی رو حدس بزن)
4. **۲ پیشنهاد عملی** برای بهبود عملکرد

لحن حرفه‌ای و مختصر باشه، مثل گزارشی که برای مدیرعامل نوشته میشه.
"""


def get_ai_insights(prompt: str, model: str = "gpt-4o-mini") -> str:
    """پرامپت رو به OpenAI می‌فرسته و پاسخ رو برمی‌گردونه"""
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "تو یک تحلیلگر داده و کسب‌وکار حرفه‌ای هستی که گزارش‌های دقیق و کاربردی می‌نویسی."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,  # پایین نگهش می‌داریم چون تحلیل دادست، نه خلاقیت آزاد
    )
    return response.choices[0].message.content