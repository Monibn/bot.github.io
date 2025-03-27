import logging
import requests as req
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# تابع برای ارسال سوال به API و دریافت پاسخ
def get_response_from_api(question):
    try:
        response = req.get(f"http://5.161.91.18/chat?text={question}")
        if response.status_code == 200:
            return response.json()  # بازگشت پاسخ JSON
        else:
            return "مشکلی در پاسخ API وجود دارد."
    except Exception as e:
        return f"خطایی رخ داده است: {e}"

# تابع شروع
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! از من سوالی بپرسید.")

# تابع برای دریافت پیام و ارسال پاسخ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text.strip()  # دریافت پیام کاربر
    api_response = get_response_from_api(user_question)  # ارسال پیام به API
    await update.message.reply_text(api_response)  # ارسال پاسخ به کاربر

def main():
    # توکن ربات تلگرام
    token = "7314937475:AAFaQcpZL9tX2Xqio7odoPKQw5Hd0hzwP88"
    application = ApplicationBuilder().token(token).build()

    # تنظیم هندلرها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("ربات در حال اجراست...")
    application.run_polling()

if __name__ == "__main__":
    main()
