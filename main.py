import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
from dotenv import load_dotenv
import time

# 🔹 بارگذاری API Key از .env
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# 🔹 تنظیم Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('serene-broker-449408-a4-44be75670742.json', scope)
client = gspread.authorize(creds)
sheet = client.open('InvestoBotsIdeaChecker').sheet1

# ✅ خواندن ایده‌ها از Google Sheets
ideas = sheet.col_values(1)  # گرفتن داده‌های ستون A (ایده‌ها)

# ✅ تابع تولید یک ایده جدید مطابق با فیلترهای مشخص‌شده
def generate_new_idea():
    model = genai.GenerativeModel("gemini-pro")
    prompt = """
    Generate a unique and engaging **YouTube video title** related to InvestoBots.com.
    The title should be **short, clear, and attention-grabbing**.
    It must be about AI trading, financial technology, or the latest trends in trading strategies.
    **Do not include any descriptions, just the title.**
    Example: "How AI is Disrupting Trading in 2024"
    **Respond ONLY with the title and nothing else.**
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# ✅ تابع بررسی یکتا بودن ایده
def is_unique_idea(idea_title, existing_ideas):
    model = genai.GenerativeModel("gemini-pro")

    prompt = (
        f"I have the following list of YouTube video titles: {existing_ideas}.\n"
        f"The new video title is: '{idea_title}'.\n"
        "Is this new title completely unique and NOT similar to any in the list?\n"
        "Reply STRICTLY with one word: 'Unique' if it is new, or 'Duplicate' if it already exists."
    )

    try:
        response = model.generate_content(prompt)
        reply = response.text.strip().lower()

        print(f"🔹 AI Response for '{idea_title}': {reply}")  # نمایش پاسخ برای دیباگ

        return "unique" in reply  # بررسی آیا جواب "Unique" هست یا نه
    except Exception as e:
        print(f"❌ Error while processing idea '{idea_title}': {e}")
        return False

# ✅ مرحله 1: اگر Google Sheets خالی باشد، یک ایده جدید تولید کند
if not ideas:
    print("⚠️ No ideas found in Google Sheets. Generating a relevant idea...")
    new_idea = generate_new_idea()
    print(f"✅ First idea generated: {new_idea}")
    sheet.append_row([new_idea, ""])  # ذخیره ایده جدید در ستون A، ستون B خالی می‌ماند
    ideas.append(new_idea)

# ✅ مرحله 2: تولید یک ایده جدید و بررسی یکتا بودن
new_idea = generate_new_idea()
while not is_unique_idea(new_idea, ideas):  # تا زمانی که ایده جدید باشد، یه ایده جدید می‌گیرد
    print(f"❌ Idea '{new_idea}' is a DUPLICATE. Generating another idea...")
    time.sleep(2)  # جلوگیری از بلاک شدن API
    new_idea = generate_new_idea()

# ✅ مرحله 3: ذخیره ایده جدید در Google Sheets (در ستون A)
print(f"✅ Saving new unique idea: {new_idea}")
sheet.append_row([new_idea, ""])  # ثبت ایده در ستون A، اما هنوز اسکریپت خالی می‌ماند
ideas.append(new_idea)

# ✅ گرفتن شماره ردیف که در آن ایده جدید ثبت شده است
new_idea_row = len(ideas)  # شماره ردیف جدید برای اسکریپت

# ✅ مرحله 4: تولید اسکریپت ویدئوی 10 دقیقه‌ای بر اساس ایده
def generate_video_script(idea_title):
    model = genai.GenerativeModel("gemini-pro")
    prompt = f"""
    Create a **detailed 10-minute YouTube video script** for the following idea:
    "{idea_title}"

    The script should include:
    - A compelling **introduction** (hook to grab audience attention).
    - Well-structured **main content** with engaging storytelling.
    - **Practical examples, data, and statistics** related to AI trading and InvestoBots.com.
    - A **strong conclusion** with a clear call-to-action.
    - **Natural dialogue** suitable for a professional YouTube video.

    Respond with the **full script only**, without additional comments.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

# ✅ دریافت اسکریپت ویدئو
print(f"📽️ Generating 10-minute video script for: {new_idea}...")
video_script = generate_video_script(new_idea)

# ✅ نمایش خروجی اسکریپت ویدئو
print("\n🎬 **Generated Video Script:**\n")
print(video_script)

# ✅ ذخیره اسکریپت در Google Sheets (در همان ردیفی که ایده ثبت شده، اما در ستون B)
sheet.update_cell(new_idea_row, 2, video_script)  # اضافه کردن اسکریپت در ستون B
print("✅ Video script saved successfully in column B!")
