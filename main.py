import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# تعریف اسکوپ‌های API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# خواندن JSON از متغیر محیطی
json_creds = os.getenv("GOOGLE_SHEETS_CREDENTIALS")

# تبدیل JSON به دیکشنری پایتون
creds_dict = json.loads(json_creds)

# ایجاد اعتبارنامه از JSON
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

# اتصال به API
client = gspread.authorize(creds)

# باز کردن شیت
sheet = client.open("InvestoBotsIdeaChecker").sheet1

# خواندن همه داده‌ها
data = sheet.get_all_records()
print("Current data in sheet:", data)

# نوشتن یک مقدار جدید در اولین ردیف خالی
new_idea = ["New Video Idea", "This is a test idea"]
sheet.append_row(new_idea)

print("✅ Data successfully written to the sheet!")
