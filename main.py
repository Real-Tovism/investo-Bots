import gspread
import json
import os
from oauth2client.service_account import ServiceAccountCredentials

# تنظیم دسترسی‌ها
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# خواندن JSON از متغیر محیطی
json_creds = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
creds_dict = json.loads(json_creds)

# احراز هویت با گواهی‌نامه
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# باز کردن شیت مورد نظر
spreadsheet = client.open("InvestoBots Data")  # نام شیت گوگل که ساختی
worksheet = spreadsheet.sheet1  # اولین شیت رو انتخاب می‌کنه

# دریافت داده‌ها
data = worksheet.get_all_records()
print(data)
