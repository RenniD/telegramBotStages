from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Ініціалізація бота з токеном
app = ApplicationBuilder().token("тут ваш токен").build()

# Функція для команди /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome_text = (
        "Ласкаво просимо до готелю 'Dream Stay'!\n"
        "Я допоможу вам із бронюванням, розкладом та інформацією про наші послуги.\n"
        "Спробуйте наступні команди:\n"
        "/book - забронювати номер\n"
        "/services - дізнатися про наші послуги\n"
        "/contacts - наші контактні дані\n"
        "/schedule - розклад послуг"
    )
    await update.message.reply_text(welcome_text)

# Функція для команди /book
async def book_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    booking_text = (
        "Щоб забронювати номер, надішліть, будь ласка, наступну інформацію:\n"
        "- Дата заїзду\n"
        "- Дата виїзду\n"
        "- Кількість гостей\n"
        "- Тип номера (стандарт, люкс, сімейний)\n\n"
        "Наш адміністратор зв’яжеться з вами для підтвердження бронювання."
    )
    await update.message.reply_text(booking_text)

# Функція для команди /services
async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    services_text = (
        "У нас доступні такі послуги:\n"
        "- Сніданки\n"
        "- Басейн і SPA\n"
        "- Wi-Fi у всіх номерах\n"
        "- Трансфер з/до аеропорту\n"
        "- Пральня\n\n"
        "Детальніше про послуги можна дізнатися у нашого адміністратора."
    )
    await update.message.reply_text(services_text)

# Функція для команди /contacts
async def contacts_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    contacts_text = (
        "Наші контактні дані:\n"
        "- Телефон: +123456789\n"
        "- Електронна пошта: contact@dreamstay.com\n"
        "- Адреса: вул. Миру, 10, Київ\n\n"
        "Будемо раді допомогти вам!"
    )
    await update.message.reply_text(contacts_text)

# Функція для команди /schedule
async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    schedule_text = (
        "Розклад:\n"
        "- Сніданок: 7:00 - 10:00\n"
        "- Обід: 12:00 - 15:00\n"
        "- Вечеря: 18:00 - 21:00\n"
        "- Прибирання номерів: 10:00 - 14:00\n\n"
        "Будь ласка, повідомте нас, якщо вам потрібен інший час для прибирання."
    )
    await update.message.reply_text(schedule_text)

# Додавання обробників команд до бота
app.add_handler(CommandHandler("start", start_command))
app.add_handler(CommandHandler("book", book_command))
app.add_handler(CommandHandler("services", services_command))
app.add_handler(CommandHandler("contacts", contacts_command))
app.add_handler(CommandHandler("schedule", schedule_command))

# Запуск бота
if __name__ == "__main__":
    app.run_polling()
