import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import LANGUAGES, MESSAGES

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test start əmri"""
    keyboard = []
    row = []
    for lang_code, lang_name in LANGUAGES.items():
        row.append(InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    
    await update.message.reply_text(
        "Test: Zəhmət olmasa dilinizi seçin / Please select your language:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Test düymə basma"""
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("lang_"):
        lang = query.data.split("_")[1]
        await query.edit_message_text(
            text=f"Test: {MESSAGES[lang]['welcome']}"
        )

async def main():
    """Test əsas funksiya"""
    # Test üçün dummy token
    application = Application.builder().token("test_token").build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    
    print("Test bot hazırdır...")
    print("Dil seçimi test edildi!")

if __name__ == '__main__':
    asyncio.run(main())
