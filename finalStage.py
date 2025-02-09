from telegram import InputMediaPhoto, Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters
import sqlite3
import asyncio

# Стадії конверсії
DATE_START, DATE_END, GUESTS, ROOM_TYPE = range(4)

# Ініціалізація бота
app = ApplicationBuilder().token("тут ваш токен").build()

# Налаштування бази даних
def setup_database():
    connection = sqlite3.connect("bot_database.db")
    cursor = connection.cursor()

    # Таблиця користувачів
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        chat_id INTEGER NOT NULL UNIQUE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    connection.commit()
    connection.close()
    print("База даних успішно налаштована.")

# Функція додавання користувача
def add_user(username, chat_id):
    connection = sqlite3.connect("bot_database.db")
    cursor = connection.cursor()
    try:
        cursor.execute("""
        INSERT OR IGNORE INTO users (username, chat_id)
        VALUES (?, ?)
        """, (username, chat_id))
        connection.commit()
        print(f"Користувач {username} успішно доданий.")
    except sqlite3.Error as e:
        print(f"Помилка при додаванні користувача: {e}")
    finally:
        connection.close()

# Отримання всіх користувачів для розсилки
def get_all_users():
    connection = sqlite3.connect("bot_database.db")
    cursor = connection.cursor()
    cursor.execute("SELECT chat_id FROM users")
    users = cursor.fetchall()
    connection.close()
    return [user[0] for user in users]

# Команда /start із збереженням користувача
async def start_command(update, context):
    username = update.effective_user.username or "NoUsername"
    chat_id = update.effective_user.id

    # Додавання користувача в базу даних
    add_user(username, chat_id)

    inline_keyboard = [
        [InlineKeyboardButton("Забронировать номер", callback_data="book")],
        [InlineKeyboardButton("Услуги", callback_data="services")],
        [InlineKeyboardButton("Контакты", callback_data="contacts")],
        [InlineKeyboardButton("Наш сайт", url="https://example.com")]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard)

    await update.message.reply_text(
        "Добро пожаловать в отель 'Dream Stay'! Выберите действие:",
        reply_markup=markup
    )

# Функція масової розсилки
async def broadcast_message(update, context):
    if not context.args:
        await update.message.reply_text("Будь ласка, вкажіть текст повідомлення після команди. Приклад: `/broadcast Доброго дня, це тестове повідомлення.`")
        return

    message_text = " ".join(context.args)
    users = get_all_users()

    successful = 0
    failed = 0

    for chat_id in users:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message_text)
            successful += 1
        except Exception as e:
            print(f"Не вдалося надіслати повідомлення користувачу {chat_id}: {e}")
            failed += 1
        await asyncio.sleep(0.1)  # Затримка для уникнення блокування API

    await update.message.reply_text(f"📢 Розсилка завершена. Надіслано: {successful}, не вдалося: {failed}.")

# Обробник кнопок
async def button_handler(update, context):
    query = update.callback_query
    await query.answer()

    if query.data == "book":
        await query.message.reply_text(
            "Для бронирования номера введите дату заезда (например, 2023-12-01):"
        )
        return DATE_START
    elif query.data == "services":
        await query.message.reply_text(
            "У нас доступны следующие услуги:\n"
            "- Завтраки\n"
            "- Бассейн и SPA\n"
            "- Трансфер из/в аэропорт"
        )
        return ConversationHandler.END

    elif query.data == "contacts":
        await query.message.reply_text(
            "Наши контактные данные:\n"
            "- Телефон: +123456789\n"
            "- Электронная почта: contact@dreamstay.com\n"
            "- Адрес: ул. Мира, 10, Киев"
        )
        return ConversationHandler.END


# Відправка фото
async def send_photos(update, context):
    photo_paths = ["photos/pic1.jpg", "photos/pic2.jpg", "photos/pic3.jpg"]
    try:
        media_group = [InputMediaPhoto(open(photo, "rb")) for photo in photo_paths]
        await update.message.reply_media_group(media_group)
    except FileNotFoundError as e:
        await update.message.reply_text(f"Помилка: файл {e.filename} не знайдено.")
    except Exception as e:
        await update.message.reply_text(f"Виникла помилка: {str(e)}")

# Ініціалізація бази даних
setup_database()

# Реєстрація обробників команд і дій
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("sendphotos", send_photos))
app.add_handler(CommandHandler("broadcast", broadcast_message))

# Обробник конверсій для бронирования
booking_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern="^(book, services, contacts)$")],
    states={
        DATE_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, date_start)],
        DATE_END: [MessageHandler(filters.TEXT & ~filters.COMMAND, date_end)],
        GUESTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, guests)],
        ROOM_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, room_type)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
app.add_handler(booking_handler)

# Запуск бота
if __name__ == "__main__":
    app.run_polling()
