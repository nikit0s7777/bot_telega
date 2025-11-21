from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from config import LANGUAGES, get_service_prices

def get_main_keyboard(language='ru'):
    texts = LANGUAGES[language]
    return ReplyKeyboardMarkup([
        [texts['menu_catalog']],
        [texts['menu_my_orders'], texts['menu_about']],
        [texts['menu_contacts'], texts['menu_language']]
    ], resize_keyboard=True)

def get_services_keyboard(language='ru'):
    services = get_service_prices(language)
    keyboard = []
    services_list = list(services.keys())
    
    # Создаем кнопки по 2 в ряду
    for i in range(0, len(services_list), 2):
        row = []
        for service_key in services_list[i:i+2]:
            service = services[service_key]
            row.append(InlineKeyboardButton(service['name'], callback_data=f"service_{service_key}"))
        keyboard.append(row)
    
    texts = LANGUAGES[language]
    keyboard.append([InlineKeyboardButton(texts['back_to_main'], callback_data="back_to_main")])
    return InlineKeyboardMarkup(keyboard)

def get_order_keyboard(service_key, language='ru'):
    texts = LANGUAGES[language]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Оформить заказ" if language == 'ru' else "✅ Place Order", callback_data=f"order_{service_key}")],
        [InlineKeyboardButton(texts['back_to_services'], callback_data="back_to_services")]
    ])

def get_language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
        ]
    ])

def get_admin_order_keyboard(order_id, user_id):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📞 Написать клиенту", url=f"tg://user?id={user_id}"),
            InlineKeyboardButton("✅ Выполнено", callback_data=f"complete_{order_id}")
        ],
        [InlineKeyboardButton("📋 Детали заказа", callback_data=f"details_{order_id}")]
    ])
