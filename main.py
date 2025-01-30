import gspread
from oauth2client.service_account import ServiceAccountCredentials

# تعریف اسکوپ‌های API
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# آدرس فایل JSON که از Google Cloud Console دانلود کردی
creds = ServiceAccountCredentials.from_json_keyfile_name("serene-broker-449408-a4-44be75670742.json", scope)

# اتصال به API
client = gspread.authorize(creds)

# باز کردن شیت
sheet = client.open("InvestoBotsIdeaChecker").sheet1  # اگر شیت چند برگه داره، از `sheet1`, `sheet2` و ... استفاده کن

# خواندن همه داده‌ها
data = sheet.get_all_records()
print("Current data in sheet:", data)

# نوشتن یک مقدار جدید در اولین ردیف خالی
new_idea = ["New Video Idea", "This is a test idea"]
sheet.append_row(new_idea)

print("✅ Data successfully written to the sheet!")
