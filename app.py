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

def run_bot():
    """Запуск Telegram бота в отдельном потоке"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ BOT_TOKEN не найден!")
        return
    
    try:
        application = Application.builder().token(token).build()
        
        # 1. Обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        
        # 2. Обработчики callback-кнопок - ОЧЕНЬ ВАЖНО: в правильном порядке!
        application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_"))
        application.add_handler(CallbackQueryHandler(handle_service_selection))
        
        # 3. ОБЩИЙ обработчик текстовых сообщений - В САМОМ КОНЦЕ
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("🤖 Бот запущен и готов к работе!")
        application.run_polling()
        
    except Exception as e:
        print(f"❌ Ошибка бота: {e}")

def run_flask():
    """Запуск Flask сервера"""
    print("🚀 Flask сервер запущен на порту 10000")
    app.run(host='0.0.0.0', port=10000, debug=False)

if __name__ == '__main__':
    # Запускаем бота в отдельном потоке
    bot_thread = Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем Flask в основном потоке
    run_flask()
