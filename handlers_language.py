from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from keyboards import get_main_keyboard, get_language_keyboard
from config import LANGUAGES

db = Database()

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Важно: подтверждаем callback
    
    user_id = query.from_user.id
    language = query.data.replace('lang_', '')
    
    print(f"🔄 Смена языка на: {language} для пользователя {user_id}")
    
    # Сохраняем выбор языка пользователя
    db.set_user_language(user_id, language)
    
    texts = LANGUAGES[language]
    
    await query.edit_message_text(
        texts['language_changed'],
        reply_markup=get_main_keyboard(language)
    )

async def show_language_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current_language = db.get_user_language(user_id)
    
    texts = LANGUAGES[current_language]
    
    print(f"🔄 Показываем меню языка для пользователя {user_id}")
    
    if update.message:
        await update.message.reply_text(
            texts['select_language'],
            reply_markup=get_language_keyboard()
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            texts['select_language'],
            reply_markup=get_language_keyboard()
        )
