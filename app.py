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

# Глобальный обработчик для ВСЕХ callback кнопок
async def handle_all_callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    print(f"🎯 ПОЙМАН CALLBACK: {query.data}")
    await query.answer()  # Обязательно отвечаем
    
    data = query.data
    
    # Перенаправляем на соответствующие обработчики
    if data.startswith('lang_'):
        await change_language(update, context)
    elif data in ['back_to_main', 'back_to_services'] or data.startswith('service_') or data.startswith('order_'):
        await handle_service_selection(update, context)
    else:
        print(f"❌ Неизвестный callback: {data}")
        await query.answer("Неизвестная команда")

def run_bot():
    """Запуск Telegram бота в отдельном потоке"""
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ BOT_TOKEN не найден!")
        return
    
    try:
        application = Application.builder().token(token).build()
        
        print("🔧 Настраиваем обработчики...")
        
        # 1. Обработчики команд
        application.add_handler(CommandHandler("start", start_command))
        print("✅ Обработчик /start добавлен")
        
        # 2. УНИВЕРСАЛЬНЫЙ обработчик ВСЕХ callback кнопок
        application.add_handler(CallbackQueryHandler(handle_all_callbacks))
        print("✅ Универсальный обработчик callback кнопок добавлен")
        
        # 3. ОБЩИЙ обработчик текстовых сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        print("✅ Обработчик текстовых сообщений добавлен")
        
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
