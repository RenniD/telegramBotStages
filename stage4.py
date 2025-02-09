
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

# Стадії конверсії
DATE_START, DATE_END, GUESTS, ROOM_TYPE = range(4)

app = ApplicationBuilder().token("тут ваш токен").build()

# Команда /start с приветственным сообщением и кнопками
async def start_command(update, context):
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

# Обработчик действий с кнопок
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
    elif query.data == "contacts":
        await query.message.reply_text(
            "Наши контактные данные:\n"
            "- Телефон: +123456789\n"
            "- Электронная почта: contact@dreamstay.com\n"
            "- Адрес: ул. Мира, 10, Киев"
        )

# Сбор данных для бронирования
async def date_start(update, context):
    context.user_data['date_start'] = update.message.text
    await update.message.reply_text("Введите дату выезда (например, 2023-12-10):")
    return DATE_END

async def date_end(update, context):
    context.user_data['date_end'] = update.message.text
    await update.message.reply_text("Сколько гостей будет проживать?")
    return GUESTS

async def guests(update, context):
    context.user_data['guests'] = update.message.text
    reply_keyboard = [["Стандарт", "Люкс", "Семейный"]]
    markup = ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Выберите тип номера:", reply_markup=markup)
    return ROOM_TYPE

async def room_type(update, context):
    context.user_data['room_type'] = update.message.text
    booking_details = (
        f"Ваши данные для бронирования:\n"
        f"- Дата заезда: {context.user_data['date_start']}\n"
        f"- Дата выезда: {context.user_data['date_end']}\n"
        f"- Количество гостей: {context.user_data['guests']}\n"
        f"- Тип номера: {context.user_data['room_type']}\n"
        "Если все верно, наш администратор свяжется с вами для подтверждения."
    )
    await update.message.reply_text(booking_details, reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def cancel(update, context):
    await update.message.reply_text("Бронирование отменено. Возвращайтесь, когда будете готовы!", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# Обработчик команд
app.add_handler(CommandHandler("start", start_command))

# Добавление ConversationHandler для бронирования
booking_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(button_handler, pattern="^book$")],
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
