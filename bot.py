import logging
import json
import os
import asyncio
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import socket
import urllib.parse

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_ID, REGISTRATION_LINK, LANGUAGES, MESSAGES

# Webhook токен для безопасности
WEBHOOK_TOKEN = "topwinbot_secure_2024"

# Простой HTTP сервер для Render с webhook endpoints
class WebhookHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Обработка GET запросов от 1win с параметрами в URL"""
        try:
            # Парсим URL и извлекаем параметры
            path = self.path
            print(f"GET request received: {path}")
            
            # Проверяем, что это webhook запрос
            if path.startswith('/webhook/'):
                # Извлекаем параметры из URL
                params = path.split('/')[2:]  # Убираем пустые элементы
                
                if len(params) >= 1:
                    user_id = params[0]
                    amount = params[1] if len(params) > 1 else None
                    country = params[2] if len(params) > 2 else None
                    
                    print(f"Webhook params: user_id={user_id}, amount={amount}, country={country}")
                    
                    # Обрабатываем webhook
                    response = self.handle_webhook_get(user_id, amount, country)
                    
                    self.send_response(200)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps(response).encode())
                else:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Missing user_id parameter'}).encode())
            else:
                # Обычная проверка состояния
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Bot is running!')
                
        except Exception as e:
            print(f"Error processing GET request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            # Парсим JSON данные
            data = json.loads(post_data.decode('utf-8'))
            
            # Проверяем токен безопасности
            if data.get('token') != WEBHOOK_TOKEN:
                self.send_response(401)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
                return
            
            # Обрабатываем webhook
            response = self.handle_webhook(data)
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def handle_webhook(self, data):
        """Обработка webhook данных от 1win"""
        # Стандартные поля 1win webhook
        webhook_type = data.get('type') or data.get('event_type')
        user_id = data.get('user_id') or data.get('telegram_id') or data.get('user')
        account_id = data.get('account_id') or data.get('account') or data.get('id')
        
        # Дополнительные поля для логирования
        amount = data.get('amount')
        currency = data.get('currency')
        timestamp = data.get('timestamp') or data.get('time')
        
        print(f"Webhook received: type={webhook_type}, user_id={user_id}, account_id={account_id}")
        print(f"Additional data: amount={amount}, currency={currency}, timestamp={timestamp}")
        
        if not all([webhook_type, user_id, account_id]):
            print(f"Missing required fields: type={webhook_type}, user_id={user_id}, account_id={account_id}")
            return {'error': 'Missing required fields'}
        
        # Запускаем асинхронную обработку в отдельном потоке
        threading.Thread(target=self.process_webhook_async, 
                       args=(webhook_type, user_id, account_id, amount, currency), 
                       daemon=True).start()
        
        return {'status': 'processing', 'type': webhook_type, 'user_id': user_id}
    
    def handle_webhook_get(self, user_id, amount=None, country=None):
        """Обработка webhook данных от 1win через GET запрос"""
        try:
            # Определяем тип события по наличию amount
            if amount and amount != "0" and amount != "null":
                webhook_type = "deposit"
                print(f"Deposit webhook: user_id={user_id}, amount={amount}, country={country}")
            else:
                webhook_type = "registration"
                print(f"Registration webhook: user_id={user_id}, country={country}")
            
            # Запускаем асинхронную обработку в отдельном потоке
            threading.Thread(target=self.process_webhook_async, 
                           args=(webhook_type, user_id, "ACC_" + str(user_id), amount, country), 
                           daemon=True).start()
            
            return {
                'status': 'processing', 
                'type': webhook_type, 
                'user_id': user_id,
                'amount': amount,
                'country': country
            }
            
        except Exception as e:
            print(f"Error in handle_webhook_get: {e}")
            return {'error': str(e)}
    
    def process_webhook_async(self, webhook_type, user_id, account_id, amount=None, currency=None):
        """Асинхронная обработка webhook в отдельном потоке"""
        try:
            # Создаем новый event loop для асинхронных операций
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Обрабатываем различные типы событий от 1win
            if webhook_type in ['registration', 'register', 'signup', 'user_created']:
                loop.run_until_complete(self.confirm_registration(user_id, account_id))
            elif webhook_type in ['deposit', 'deposit_success', 'payment_success']:
                loop.run_until_complete(self.confirm_deposit(user_id, account_id, amount, currency))
            elif webhook_type in ['login', 'user_login']:
                print(f"User {user_id} logged in to account {account_id}")
            else:
                print(f"Unknown webhook type: {webhook_type}")
            
        except Exception as e:
            print(f"Webhook processing error: {e}")
        finally:
            loop.close()
    
    async def confirm_registration(self, user_id, account_id):
        """Подтверждение регистрации через webhook"""
        try:
            # Проверяем, существует ли пользователь
            if user_id not in user_data:
                print(f"User {user_id} not found in user_data - sending welcome message")
                # Если пользователь не найден, отправляем приветствие
                await self.send_welcome_message(user_id)
                return
            
            user_info = user_data[user_id]
            lang = user_info.get("lang", "en")
            
            # Обновляем статус
            user_data[user_id]["registration_confirmed"] = True
            user_data[user_id]["waiting_for_id"] = False
            user_data[user_id]["step"] = "step2"
            user_data[user_id]["registration_id"] = account_id
            
            # Отправляем пользователю переход к Шагу 2 через Telegram API
            await self.send_telegram_message(user_id, "step2", lang)
            print(f"Registration confirmed for user {user_id} via webhook")
            
        except Exception as e:
            print(f"Error confirming registration: {e}")
    
    async def confirm_deposit(self, user_id, account_id, amount=None, currency=None):
        """Подтверждение депозита через webhook"""
        try:
            # Проверяем, существует ли пользователь
            if user_id not in user_data:
                print(f"User {user_id} not found in user_data for deposit confirmation")
                return
            
            user_info = user_data[user_id]
            lang = user_info.get("lang", "en")
            
            # Обновляем статус
            user_data[user_id]["deposit_confirmed"] = True
            user_data[user_id]["waiting_for_deposit_id"] = False
            user_data[user_id]["deposit_id"] = account_id
            user_data[user_id]["deposit_amount"] = amount
            user_data[user_id]["deposit_currency"] = currency
            
            # Отправляем пользователю финальное сообщение через Telegram API
            await self.send_telegram_message(user_id, "success", lang)
            print(f"Deposit confirmed for user {user_id} via webhook: {amount} {currency}")
            
        except Exception as e:
            print(f"Error confirming deposit: {e}")
    
    async def send_welcome_message(self, user_id):
        """Отправка приветственного сообщения новому пользователю"""
        try:
            # Отправляем приветствие через Telegram API
            await self.send_telegram_message(user_id, "welcome", "en")
            print(f"Welcome message sent to new user {user_id}")
                
        except Exception as e:
            print(f"Error sending welcome message: {e}")
    
    async def send_telegram_message(self, user_id, message_type, lang):
        """Отправка сообщений через Telegram Bot API"""
        try:
            import aiohttp
            
            # Формируем сообщение в зависимости от типа
            if message_type == "welcome":
                caption = "🤖 Welcome to the bot!\n\n🚀 THE BEST BOT with built-in artificial intelligence!\n\n💎 Integrates special software into your account and provides stable income on the 1win site.\n\n🧠 The project is based on Reationale artificial intelligence.\n\n💰 Start earning!"
                reply_markup = self.get_language_keyboard_json()
                has_photo = True
                photo_file = "start.jpeg"
                
            elif message_type == "step2":
                caption = f"{MESSAGES[lang]['step2_title']}\n\n{MESSAGES[lang]['step2_text']}"
                reply_markup = self.get_step2_keyboard_json(lang)
                has_photo = True
                photo_file = "2.jpeg"
                
            elif message_type == "success":
                caption = MESSAGES[lang]['success']
                reply_markup = None
                has_photo = True
                photo_file = "3.jpeg"
            
            # Отправляем сообщение через Telegram API
            if has_photo and os.path.exists(photo_file):
                await self.send_photo_via_api(user_id, photo_file, caption, reply_markup)
            else:
                await self.send_text_via_api(user_id, caption, reply_markup)
                
        except Exception as e:
            print(f"Error sending Telegram message: {e}")
    
    async def send_photo_via_api(self, user_id, photo_file, caption, reply_markup=None):
        """Отправка фото через Telegram Bot API"""
        try:
            import aiohttp
            
            # Читаем файл фото
            with open(photo_file, 'rb') as f:
                photo_data = f.read()
            
            # Формируем multipart данные
            data = aiohttp.FormData()
            data.add_field('chat_id', str(user_id))
            data.add_field('photo', photo_data, filename=photo_file)
            data.add_field('caption', caption)
            
            if reply_markup:
                data.add_field('reply_markup', json.dumps(reply_markup))
            
            # Отправляем запрос к Telegram API
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                async with session.post(url, data=data) as response:
                    if response.status == 200:
                        print(f"Photo sent successfully to user {user_id}")
                    else:
                        print(f"Failed to send photo to user {user_id}: {response.status}")
                        
        except Exception as e:
            print(f"Error sending photo via API: {e}")
    
    async def send_text_via_api(self, user_id, text, reply_markup=None):
        """Отправка текста через Telegram Bot API"""
        try:
            import aiohttp
            
            # Формируем данные
            data = {
                'chat_id': user_id,
                'text': text
            }
            
            if reply_markup:
                data['reply_markup'] = json.dumps(reply_markup)
            
            # Отправляем запрос к Telegram API
            async with aiohttp.ClientSession() as session:
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        print(f"Text message sent successfully to user {user_id}")
                    else:
                        print(f"Failed to send text to user {user_id}: {response.status}")
                        
        except Exception as e:
            print(f"Error sending text via API: {e}")
    
    def get_language_keyboard_json(self):
        """Получение клавиатуры выбора языка в JSON формате"""
        keyboard = []
        row = []
        for lang_code, lang_name in LANGUAGES.items():
            row.append({"text": lang_name, "callback_data": f"lang_{lang_code}"})
            if len(row) == 2:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
        return {"inline_keyboard": keyboard}
    
    def get_step2_keyboard_json(self, lang):
        """Получение клавиатуры Шага 2 в JSON формате"""
        keyboard = [
            [{"text": MESSAGES[lang]['deposit_check'], "callback_data": "check_deposit"}]
        ]
        return {"inline_keyboard": keyboard}

def run_http_server():
    try:
        # Находим свободный порт
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        
        server = HTTPServer(('0.0.0.0', port), WebhookHTTPRequestHandler)
        print(f"Webhook server running on port {port}")
        print(f"Webhook endpoints:")
        print(f"  POST / - Registration verification")
        print(f"  POST / - Deposit verification")
        print(f"  GET / - Health check")
        server.serve_forever()
    except Exception as e:
        print(f"Webhook server error: {e}")

# Запускаем HTTP сервер в отдельном потоке
http_thread = threading.Thread(target=run_http_server, daemon=True)
http_thread.start()

# Logging konfiqurasiyası
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Обработчик ошибок для Telegram бота
def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок Telegram бота"""
    logger.error("Exception while handling an update:", exc_info=context.error)
    
    # Отправляем сообщение об ошибке пользователю
    if update and hasattr(update, 'effective_chat') and update.effective_chat:
        try:
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Произошла ошибка при обработке запроса. Попробуйте еще раз."
            )
        except Exception as e:
            logger.error(f"Error sending error message: {e}")

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

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для получения Telegram ID пользователя"""
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Unknown"
    
    await update.message.reply_text(
        f"🆔 **Ваш Telegram ID:** `{user_id}`\n"
        f"👤 **Имя:** {user_name}\n\n"
        f"📋 **Используйте этот ID в 1win для webhook интеграции!**"
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
    application.add_handler(CommandHandler("getid", get_id)) # Добавляем команду /getid
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчик ошибок
    application.add_error_handler(error_handler)
    
    # Botu başlatmaq
    print("Bot başladıldı...")
    application.run_polling()

if __name__ == '__main__':
    main()
