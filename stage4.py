from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = ApplicationBuilder().token("тут ваш токен").build()

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

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    
    if query.data == "book":
        await query.message.reply_text(
            "Чтобы забронировать номер, пожалуйста, отправьте следующую информацию:\n"
            "- Дата заезда\n"
            "- Дата выезда\n"
            "- Количество гостей\n"
            "- Тип номера (стандарт, люкс, семейный)"
        )
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

app.add_handler(CommandHandler("start", start_command))
app.add_handler(CallbackQueryHandler(button_handler))

if __name__ == "__main__":
    app.run_polling()
