import os
from dotenv import load_dotenv
from localization_ru import TEXTS as RU_TEXTS
from localization_en import TEXTS as EN_TEXTS

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_CHAT_ID = os.getenv('ADMIN_CHAT_ID')

print(f"🔧 Конфигурация: BOT_TOKEN={'установлен' if BOT_TOKEN else 'НЕТ'}, ADMIN_CHAT_ID={ADMIN_CHAT_ID}")  # Debug

# Языковые пакеты
LANGUAGES = {
    'ru': RU_TEXTS,
    'en': EN_TEXTS
}

DEFAULT_LANGUAGE = 'ru'

def get_service_prices(language='ru'):
    """Возвращает услуги на выбранном языке"""
    return LANGUAGES[language]['services']
