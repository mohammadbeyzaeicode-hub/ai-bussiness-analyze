import os

from dotenv import load_dotenv

load_dotenv()
API_KEY=os.getenv("GAP_API_KEY")
BASE_URL=os.getenv("GAP_BASE_URL")
