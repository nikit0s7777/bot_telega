import os
import logging
from flask import Flask
from threading import Thread
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Импорт обработчиков
from handlers_start import start_command, handle_message
from handlers_catalog import show_services, handle_service_selection
from handlers_orders import handle_order_description, handle_contact_info, show_user_orders
from handlers_language import change_language, show_language_menu

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv()

# Создаем Flask приложение
app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Бот активен и работает 24/7!"

@app.route('/health')
def health():
    return "✅ OK"

@app.route('/ping')
def ping():
    return "🏓 PONG"

# Глобальная переменная для бота
bot_application = None

def setup_bot():
    """Настройка и запуск бота в отдельном потоке"""
    global bot_application
    
    # Проверяем наличие токена
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        return
    
    try:
        # Создаем приложение бота
        bot_application = Application.builder().token(token).build()
        print("✅ Бот инициализирован успешно")
        
        # Настраиваем обработчики
        bot_application.add_handler(CommandHandler("start", start_command))
        bot_application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_"))
        bot_application.add_handler(CallbackQueryHandler(handle_service_selection))
        bot_application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Запускаем бота
        print("🤖 Бот запущен и готов к работе!")
        bot_application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка в боте: {e}")

def run_bot():
    """Запуск бота в отдельном потоке"""
    bot_thread = Thread(target=setup_bot)
    bot_thread.daemon = True
    bot_thread.start()

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    run_bot()
    
    # Запускаем Flask на стандартном порту Render (10000)
    print("🚀 Запускаем Flask сервер на порту 10000...")
    app.run(host='0.0.0.0', port=10000, debug=False)
