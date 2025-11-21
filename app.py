import os
import logging
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

def main():
    # Проверяем наличие токена
    token = os.getenv('BOT_TOKEN')
    if not token:
        print("❌ ОШИБКА: BOT_TOKEN не найден!")
        print("📝 Добавь BOT_TOKEN в Environment Variables на Render")
        return
    
    # Создаем приложение бота
    try:
        application = Application.builder().token(token).build()
        print("✅ Бот инициализирован успешно")
    except Exception as e:
        print(f"❌ Ошибка инициализации бота: {e}")
        return
    
    # 1. Обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    
    # 2. Обработчики callback-кнопок (инлайн кнопки)
    application.add_handler(CallbackQueryHandler(handle_service_selection))
    application.add_handler(CallbackQueryHandler(change_language, pattern="^lang_"))
    
    # 3. ОБЩИЙ обработчик текстовых сообщений
    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, 
        handle_message
    ))
    
    # Запускаем бота
    print("🤖 Бот запущен и готов к работе!")
    print("📍 Бот работает на Render")
    
    try:
        application.run_polling()
    except Exception as e:
        print(f"❌ Бот упал с ошибкой: {e}")

if __name__ == '__main__':
    main()
