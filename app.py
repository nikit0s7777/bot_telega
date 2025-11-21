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

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.daemon = True
    t.start()

def main():
    # Запускаем Flask сервер для поддержания активности
    keep_alive()
    
    # Создаем приложение бота
    application = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    
    # Обработчик смены языка
    application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_"))
    
    # Обработчик инлайн-кнопок (каталог услуг)
    application.add_handler(CallbackQueryHandler(handle_service_selection))
    
    # Обработчик описания заказа
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_order_description
    ))
    
    # Общий обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запускаем бота
    print("🤖 Бот запущен и готов к работе!")
    print("📍 Бот работает на Render 24/7")
    application.run_polling()

if __name__ == '__main__':
    main()
