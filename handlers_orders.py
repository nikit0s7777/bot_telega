from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import get_main_keyboard, get_admin_order_keyboard
from config import LANGUAGES, get_service_prices, ADMIN_CHAT_ID, BOT_TOKEN

db = Database()

async def handle_order_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что это действительно описание заказа, а не кнопка меню
    user_id = update.effective_user.id
    language = db.get_user_language(user_id)
    texts = LANGUAGES[language]
    
    # Если пользователь не выбрал услугу, но пишет текст - это ошибка
    if 'selected_service' not in context.user_data:
        await update.message.reply_text(
            "Пожалуйста, сначала выберите услугу из каталога" if language == 'ru' else "Please select a service from the catalog first",
            reply_markup=get_main_keyboard(language)
        )
        return
    
    # Это действительно описание заказа
    description = update.message.text
    user = update.effective_user
    services = get_service_prices(language)
    
    service_key = context.user_data['selected_service']
    service = services[service_key]
    
    # Сохраняем описание
    context.user_data['order_description'] = description
    
    # Запрашиваем контактные данные
    await update.message.reply_text(texts['contact_prompt'])
    
    # Устанавливаем состояние ожидания контактов
    context.user_data['waiting_for_contacts'] = True

async def handle_contact_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, что мы действительно ждем контактные данные
    if not context.user_data.get('waiting_for_contacts'):
        user_id = update.effective_user.id
        language = db.get_user_language(user_id)
        await update.message.reply_text(
            "Используйте кнопки меню для навигации",
            reply_markup=get_main_keyboard(language)
        )
        return
    
    contact_info = update.message.text
    user = update.effective_user
    language = db.get_user_language(user.id)
    texts = LANGUAGES[language]
    services = get_service_prices(language)
    
    # Создаем заказ в базе данных
    order_id = db.create_order(
        user_id=user.id,
        username=user.username or 'Не указан' if language == 'ru' else 'Not specified',
        first_name=user.first_name or 'Не указано' if language == 'ru' else 'Not specified',
        service_type=context.user_data['selected_service'],
        description=context.user_data['order_description'],
        contact_info=contact_info
    )
    
    # Отправляем уведомление админу
    await send_order_to_admin(order_id, context.user_data, user, contact_info, language)
    
    # Подтверждаем пользователю
    service_name = services[context.user_data['selected_service']]['name']
    confirmation_text = texts['order_confirmed'].format(
        service_name=service_name,
        order_id=order_id
    )
    
    await update.message.reply_text(
        confirmation_text,
        reply_markup=get_main_keyboard(language)
    )
    
    # Очищаем данные пользователя
    context.user_data.clear()

async def send_order_to_admin(order_id, user_data, user, contact_info, language='ru'):
    services = get_service_prices(language)
    service = services[user_data['selected_service']]
    texts = LANGUAGES[language]
    
    order_data = db.get_user_orders(user.id)[0]
    created_at = order_data[8]
    
    message_text = texts['order_notification'].format(
        order_id=order_id,
        user_name=user.first_name or 'Не указано',
        username=user.username or 'Не указан',
        user_id=user.id,
        service_name=service['name'],
        description=user_data['order_description'],
        contact_info=contact_info,
        created_at=created_at
    )
    
    # Отправляем сообщение админу с кнопками
    from telegram import Bot
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID, 
            text=message_text,
            reply_markup=get_admin_order_keyboard(order_id, user.id)
        )
        print(f"✅ Уведомление отправлено в админ-чат для заказа #{order_id}")
    except Exception as e:
        print(f"❌ Ошибка отправки сообщения админу: {e}")

async def show_user_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    language = db.get_user_language(user.id)
    texts = LANGUAGES[language]
    services = get_service_prices(language)
    
    orders = db.get_user_orders(user.id)
    
    if not orders:
        await update.message.reply_text(texts['no_orders'])
        return
    
    text = texts['user_orders_title']
    
    for order in orders[:5]:
        order_id, _, _, _, service_type, description, contact, status, created_at = order
        service_name = services.get(service_type, {}).get('name', 'Неизвестная услуга')
        
        status_text = {
            'pending': '⏳ Ожидает' if language == 'ru' else '⏳ Pending',
            'completed': '✅ Выполнен' if language == 'ru' else '✅ Completed',
            'in_progress': '🔄 В работе' if language == 'ru' else '🔄 In Progress'
        }.get(status, status)
        
        text += f"🔹 **Заказ #{order_id}**\n" if language == 'ru' else f"🔹 **Order #{order_id}**\n"
        text += f"• Услуга: {service_name}\n" if language == 'ru' else f"• Service: {service_name}\n"
        text += f"• Статус: {status_text}\n" if language == 'ru' else f"• Status: {status_text}\n"
        text += f"• Дата: {created_at[:16]}\n\n"
    
    await update.message.reply_text(text)
