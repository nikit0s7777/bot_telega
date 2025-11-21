from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import get_main_keyboard
from config import LANGUAGES

db = Database()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id
    
    # Очищаем состояние пользователя
    context.user_data.clear()
    
    # Получаем язык пользователя
    language = db.get_user_language(user_id)
    texts = LANGUAGES[language]
    
    welcome_text = texts['welcome'].format(name=user.first_name)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=get_main_keyboard(language)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = db.get_user_language(user_id)
    texts = LANGUAGES[language]
    
    text = update.message.text
    
    print(f"📨 Получено сообщение: '{text}' от пользователя {user_id}")
    
    # Проверяем состояние пользователя
    if context.user_data.get('waiting_for_contacts'):
        from handlers_orders import handle_contact_info
        await handle_contact_info(update, context)
        return
        
    elif context.user_data.get('selected_service'):
        from handlers_orders import handle_order_description
        await handle_order_description(update, context)
        return
    
    # Обработка кнопок главного меню
    if text == texts['menu_catalog']:
        from handlers_catalog import show_services
        await show_services(update, context)
    elif text == texts['menu_contacts']:
        await update.message.reply_text(texts['contacts_info'])
    elif text == texts['menu_about']:
        await update.message.reply_text(texts['about_info'])
    elif text == texts['menu_language']:
        from handlers_language import show_language_menu
        await show_language_menu(update, context)
    elif text == texts['menu_my_orders']:
        from handlers_orders import show_user_orders
        await show_user_orders(update, context)
    else:
        await update.message.reply_text(
            "Используйте кнопки меню для навигации",
            reply_markup=get_main_keyboard(language)
        )
