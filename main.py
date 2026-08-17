import sys
from src.pipeline import run_pipeline

if __name__ == "__main__":
    try:
        run_pipeline()
    except Exception as e:
        print(f"\n🛑 اجرای پروژه متوقف شد:\n{e}")
        sys.exit(1)