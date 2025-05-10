import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, CallbackQueryHandler, filters, ContextTypes

# Получаем токен и ID группы
TOKEN = os.getenv("BOT_TOKEN")
admin_id_raw = os.getenv("ADMIN_GROUP_ID")
if admin_id_raw is None:
    raise ValueError("ADMIN_GROUP_ID не задан!")
ADMIN_GROUP_ID = int(admin_id_raw)

logging.basicConfig(level=logging.INFO)

# Обработка входящих сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text:
        user = update.message.from_user
        text = update.message.text
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Ответить", callback_data=f"reply:{user.id}")]
        ])
        await context.bot.send_message(chat_id=ADMIN_GROUP_ID, text=f"Сообщение от {user.full_name}:
{text}", reply_markup=keyboard)
        await update.message.reply_text("Ваше сообщение отправлено администрации.")

# Обработка нажатий кнопок
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        if query.data.startswith("reply:"):
            user_id = int(query.data.split(":")[1])
            await context.bot.send_message(chat_id=user_id, text="Админ получил ваше сообщение и скоро ответит.")

# Основная функция
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(handle_callback))
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
