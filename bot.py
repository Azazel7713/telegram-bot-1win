import logging
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, REGISTRATION_LINK, LANGUAGES, MESSAGES
import os

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# İstifadəçi məlumatlarını saxlamaq üçün
user_data = {}

def get_language_keyboard():
    """Dil seçimi üçün klaviatura"""
    keyboard = []
    row = []
    for lang_code, lang_name in LANGUAGES.items():
        row.append(InlineKeyboardButton(lang_name, callback_data=f"lang_{lang_code}"))
        if len(row) == 2:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def get_welcome_keyboard(lang):
    """Xoş gəlmisiniz səhifəsi üçün klaviatura"""
    keyboard = [
        [InlineKeyboardButton(MESSAGES[lang]['next'], callback_data="step1")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_step1_keyboard(lang):
    """Addım 1 üçün klaviatura"""
    keyboard = [
        [InlineKeyboardButton(MESSAGES[lang]['site_registration'], url=REGISTRATION_LINK)],
        [InlineKeyboardButton(MESSAGES[lang]['registration_check'], callback_data="check_registration")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_step2_keyboard(lang):
    """Addım 2 üçün klaviatura"""
    keyboard = [
        [InlineKeyboardButton(MESSAGES[lang]['deposit_check'], callback_data="check_deposit")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_waiting_keyboard(lang):
    """ID gözləyir zamanı klaviatura"""
    keyboard = [
        [InlineKeyboardButton(MESSAGES[lang]['back'], callback_data="back_to_step1")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_admin_keyboard(user_id, action):
    """Admin üçün klaviatura"""
    keyboard = [
        [
            InlineKeyboardButton("Təsdiq et", callback_data=f"admin_confirm_{action}_{user_id}"),
            InlineKeyboardButton("Rədd et", callback_data=f"admin_reject_{action}_{user_id}")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start əmri"""
    user_id = update.effective_user.id
    
    # start.jpeg şəkli ilə dil seçimi
    if os.path.exists("start.jpeg"):
        with open("start.jpeg", "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption="Please select your language:",
                reply_markup=get_language_keyboard()
            )
    else:
        await update.message.reply_text(
            "Please select your language:",
            reply_markup=get_language_keyboard()
        )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Düymə basma hadisələri"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    
    if query.data.startswith("lang_"):
        # Dil seçimi
        lang = query.data.split("_")[1]
        user_data[user_id] = {"lang": lang, "step": "welcome"}
        
        # Xoş gəlmisiniz mesajı
        if os.path.exists("start.jpeg"):
            with open("start.jpeg", "rb") as photo:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=MESSAGES[lang]['welcome']
                    ),
                    reply_markup=get_welcome_keyboard(lang)
                )
        else:
            await query.edit_message_text(
                text=MESSAGES[lang]['welcome'],
                reply_markup=get_welcome_keyboard(lang)
            )
    
    elif query.data == "step1":
        # Addım 1-yə keçid
        lang = user_data[user_id]["lang"]
        user_data[user_id]["step"] = "step1"
        
        if os.path.exists("1.jpeg"):
            with open("1.jpeg", "rb") as photo:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=f"{MESSAGES[lang]['step1_title']}\n\n{MESSAGES[lang]['step1_text']}"
                    ),
                    reply_markup=get_step1_keyboard(lang)
                )
        else:
            await query.edit_message_text(
                text=f"{MESSAGES[lang]['step1_title']}\n\n{MESSAGES[lang]['step1_text']}",
                reply_markup=get_step1_keyboard(lang)
            )
    
    elif query.data == "check_registration":
        # Qeydiyyat yoxlaması
        lang = user_data[user_id]["lang"]
        user_data[user_id]["waiting_for_id"] = True
        await query.edit_message_caption(
            caption=MESSAGES[lang]['send_id'],
            reply_markup=get_waiting_keyboard(lang)
        )
    
    elif query.data == "step2":
        # Addım 2-yə keçid - только после подтверждения регистрации
        lang = user_data[user_id]["lang"]
        
        # Проверяем, подтверждена ли регистрация
        if not user_data[user_id].get("registration_confirmed"):
            await query.answer("Сначала подтвердите регистрацию!", show_alert=True)
            return
            
        user_data[user_id]["step"] = "step2"
        
        if os.path.exists("2.jpeg"):
            with open("2.jpeg", "rb") as photo:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}"
                    ),
                    reply_markup=get_step2_keyboard(lang)
                )
        else:
            await query.edit_message_text(
                text=f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}",
                reply_markup=get_step2_keyboard(lang)
            )
    
    elif query.data == "check_deposit":
        # Depozit yoxlaması
        lang = user_data[user_id]["lang"]
        user_data[user_id]["waiting_for_deposit_id"] = True
        await query.edit_message_caption(
            caption=MESSAGES[lang]['send_id'],
            reply_markup=get_waiting_keyboard(lang)
        )
    
    elif query.data == "back_to_step1":
        # Geri qayıt
        lang = user_data[user_id]["lang"]
        user_data[user_id]["waiting_for_id"] = False
        user_data[user_id]["waiting_for_deposit_id"] = False
        
        if os.path.exists("1.jpeg"):
            with open("1.jpeg", "rb") as photo:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=f"{MESSAGES[lang]['step1_title']}\n\n{MESSAGES[lang]['step1_text']}"
                    ),
                    reply_markup=get_step1_keyboard(lang)
                )
        else:
            await query.edit_message_text(
                text=f"{MESSAGES[lang]['step1_title']}\n\n{MESSAGES[lang]['step1_text']}",
                reply_markup=get_step1_keyboard(lang)
            )
    
    elif query.data == "step2_show":
        # Addım 2-yə keçid
        lang = user_data[user_id]["lang"]
        user_data[user_id]["step"] = "step2"
        
        if os.path.exists("2.jpeg"):
            with open("2.jpeg", "rb") as photo:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=photo,
                        caption=f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}"
                    ),
                    reply_markup=get_step2_keyboard(lang)
                )
        else:
            await query.edit_message_text(
                text=f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}",
                reply_markup=get_step2_keyboard(lang)
            )
    
    elif query.data.startswith("admin_confirm_"):
        # Admin təsdiqi
        parts = query.data.split("_")
        action = parts[2]
        target_user_id = int(parts[3])
        lang = user_data[target_user_id]["lang"]
        
        if action == "registration":
            user_data[target_user_id]["registration_confirmed"] = True
            user_data[target_user_id]["waiting_for_id"] = False
            user_data[target_user_id]["step"] = "step2"
            
            # Автоматически переходим к Шагу 2
            if os.path.exists("2.jpeg"):
                with open("2.jpeg", "rb") as photo:
                    await context.bot.send_photo(
                        chat_id=target_user_id,
                        photo=photo,
                        caption=f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}",
                        reply_markup=get_step2_keyboard(lang)
                    )
            else:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}",
                    reply_markup=get_step2_keyboard(lang)
                )
        elif action == "deposit":
            user_data[target_user_id]["deposit_confirmed"] = True
            user_data[target_user_id]["waiting_for_deposit_id"] = False
            
            if os.path.exists("3.jpeg"):
                with open("3.jpeg", "rb") as photo:
                    await context.bot.send_photo(
                        chat_id=target_user_id,
                        photo=photo,
                        caption=MESSAGES[lang]['success']
                    )
            else:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=MESSAGES[lang]['success']
                )
        
        await query.edit_message_text("✅ Təsdiq edildi!")
    
    elif query.data.startswith("admin_reject_"):
        # Admin rəddi
        parts = query.data.split("_")
        action = parts[2]
        target_user_id = int(parts[3])
        lang = user_data[target_user_id]["lang"]
        
        if action == "registration":
            await context.bot.send_message(
                chat_id=target_user_id,
                text=MESSAGES[lang]['not_registered']
            )
        elif action == "deposit":
            await context.bot.send_message(
                chat_id=target_user_id,
                text=MESSAGES[lang]['no_deposit']
            )
        
        await query.edit_message_text("❌ Rədd edildi!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mesajları emal etmək"""
    user_id = update.effective_user.id
    message_text = update.message.text
    
    if user_id not in user_data:
        await update.message.reply_text("🤖 Zəhmət olmasa /start əmrini istifadə edin\n\n🚀 Botu başlatmaq üçün /start yazın!")
        return
    
    user_info = user_data[user_id]
    
    if user_info.get("waiting_for_id"):
        # Qeydiyyat ID-si göndərildi
        lang = user_info["lang"]
        user_info["waiting_for_id"] = False
        user_info["registration_id"] = message_text
        
        # Admin-ə bildiriş göndər
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🆕 Yeni qeydiyyat yoxlaması!\n\n👤 İstifadəçi ID: {user_id}\n🆔 Hesab ID: {message_text}\n\n⏰ Zaman: {update.message.date.strftime('%H:%M:%S')}",
            reply_markup=get_admin_keyboard(user_id, "registration")
        )
        
        await update.message.reply_text(MESSAGES[lang]['id_sent'])
    
    elif user_info.get("waiting_for_deposit_id"):
        # Depozit ID-si göndərildi
        lang = user_info["lang"]
        user_info["waiting_for_deposit_id"] = False
        user_info["deposit_id"] = message_text
        
        # Admin-ə bildiriş göndər
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"💰 Yeni depozit yoxlaması!\n\n👤 İstifadəçi ID: {user_id}\n🆔 Hesab ID: {message_text}\n\n⏰ Zaman: {update.message.date.strftime('%H:%M:%S')}",
            reply_markup=get_admin_keyboard(user_id, "deposit")
        )
        
        await update.message.reply_text(MESSAGES[lang]['id_sent'])

def main():
    """Əsas funksiya"""
    # Bot yaratmaq
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handler-ləri əlavə etmək
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Botu başlatmaq
    print("Bot başladıldı...")
    application.run_polling()

if __name__ == '__main__':
    main()
