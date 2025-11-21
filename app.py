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

# Сервер для поддержания активности на Render
app = Flask('')

@app.route('/')
def home():
    return "🤖 Бот активен и работает 24/7!"

@app.route('/health')
def health():
    return "✅ OK"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

def main():
    # Проверяем наличие токена
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        print("📝 Добавь BOT_TOKEN в Environment Variables на Render")
        return
    
    # Запускаем Flask сервер для поддержания активности
    keep_alive()
    print("🚀 Flask сервер запущен на порту 8080")
    
    # Создаем приложение бота
    try:
        application = Application.builder().token(token).build()
        print("✅ Бот инициализирован успешно")
    except Exception as e:
        print(f"❌ Ошибка инициализации бота: {e}")
        return
    
    # 1. Сначала обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    
    # 2. Затем обработчики callback-кнопок (инлайн кнопки)
    application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_"))
    application.add_handler(CallbackQueryHandler(handle_service_selection))
    
    # 3. ОБЩИЙ обработчик текстовых сообщений - В САМОМ КОНЦЕ
    # Этот обработчик будет ловить ВСЕ текстовые сообщения
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_message
    ))
    
    # Запускаем бота
    print("🤖 Бот запущен и готов к работе!")
    print("📍 Бот работает на Render 24/7")
    
    try:
        application.run_polling()
    except Exception as e:
        print(f"❌ Бот упал с ошибкой: {e}")
        print("🔄 Попытка перезапуска...")

if __name__ == '__main__':
    main()
