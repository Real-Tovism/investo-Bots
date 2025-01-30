import gspread
from oauth2client.service_account import ServiceAccountCredentials

# تنظیم دسترسی‌ها
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# خواندن اطلاعات سرویس‌اکانت از فایل JSON
creds = ServiceAccountCredentials.from_json_keyfile_name("serene-broker-449408-a4-44be75670742.json", scope)
client = gspread.authorize(creds)

# باز کردن شیت مورد نظر
spreadsheet = client.open("InvestoBots Data")  # نام فایل اکسل که توی گوگل شیت ساختی
worksheet = spreadsheet.sheet1  # اولین شیت رو انتخاب می‌کنه

# دریافت داده‌ها
data = worksheet.get_all_records()
print(data)
