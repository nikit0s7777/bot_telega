from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import get_services_keyboard, get_order_keyboard
from config import LANGUAGES, get_service_prices

db = Database()

async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    language = db.get_user_language(user_id)
    texts = LANGUAGES[language]
    
    print("🔄 Показываем каталог услуг")  # Debug
    
    if update.message:
        await update.message.reply_text(texts['catalog_title'], reply_markup=get_services_keyboard(language))
    else:
        await update.callback_query.edit_message_text(texts['catalog_title'], reply_markup=get_services_keyboard(language))

async def handle_service_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    language = db.get_user_language(user_id)
    texts = LANGUAGES[language]
    services = get_service_prices(language)
    
    data = query.data
    print(f"🔄 Обрабатываем callback: {data}")  # Debug
    
    if data == 'back_to_main':
        from handlers_start import start_command
        if query.message:
            await query.message.reply_text(
                "Главное меню:",
                reply_markup=get_main_keyboard(language)
            )
        return
        
    elif data == 'back_to_services':
        await show_services(update, context)
        return
    
    if data.startswith('service_'):
        service_key = data.replace('service_', '')
        service = services.get(service_key)
        
        if service:
            text = texts['service_template'].format(
                name=service['name'],
                description=service['description'],
                price=service['price']
            )
            await query.edit_message_text(text, reply_markup=get_order_keyboard(service_key, language))
    
    elif data.startswith('order_'):
        service_key = data.replace('order_', '')
        service = services[service_key]
        context.user_data['selected_service'] = service_key
        
        text = texts['order_prompt'].format(service_name=service['name'])
        await query.edit_message_text(text)
