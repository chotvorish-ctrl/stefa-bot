#!/usr/bin/env python3
import logging, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN", "8851062670:AAGp8vON3NUE-fqjmIBngAcacsvATvW0aE8")
ADMIN_USERNAME = "@katya_tvorish"
ADMIN_PHONE = "+7 919 770 72 89"
SITE_URL = "https://tvorish.ru"
SCHEDULE_URL = "https://tvorish.ru/calendar"
SHOP_URL = "https://tvorish.ru/shop"
CERT_URL = "https://tvorish.ru/certificate"
TELEGRAM_CHANNEL = "https://t.me/u_cho_tvorish"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

WELCOME_TEXT = """🐾 *Гав! Я Стефа* — главный амбассадор мастерской «Ты чо творишь»

Помогу найти всё нужное: расскажу про форматы, узнаю про твоё изделие и провожу к Кате 🎨

Что хочешь узнать?"""

ABOUT_TEXT = """🏺 *Мастерская «Ты чо творишь»*

Мы — креативная мастерская керамики в Москве. Пространство свободы, творчества, дружбы и самовыражения.

Лепим посуду, предметы декора, отпечатки лапок — без художественных навыков и без понтов.

📞 +7 919 770 72 89
🌐 tvorish.ru
📱 t.me/u_cho_tvorish"""

FORMATS_TEXT = """🎨 *Форматы мастер-классов*

🍷 *Пить Лепить* — 6 500 ₽
3 часа лепки + игристое + фуршет + музыка. 18+

🖐 *Руки из жопы* — 5 000 ₽
Ручная лепка без подготовки. Хулиганское название — терапевтический эффект. 12+

👨‍👩‍👧 *Глиномесики* — 4 000 ₽
Семейный/детский МК. Можно с детьми или всей семьёй. 3+

🐶 *Лапы лепят* — 6 500 ₽
Приходите с собаками! Отпечатки лапок и носиков.

🔮 *Керамистика* — 7 000 ₽
Лепка + таро + астропрогнозы + фуршет.

🕯 *Свидетельство о жизни* — по запросу
Альтернативные поминки. Сохранить память через творчество.

📅 Расписание: tvorish.ru/calendar
_Перед оплатой уточни даты: +7 919 770 72 89_"""

CORPORATE_TEXT = """🏢 *Корпоративные форматы*

• 🤝 Творческие тимбилдинги
• 🎁 Корпоративные подарки с логотипом
• 🍽 Посуда на заказ для HoReCa
• 🏠 Интерьерные решения

От 6 до 30 человек — в мастерской или выезд.
Стоимость меньше, когда участников больше 😊

📝 Бриф: tvorish.ru
📞 Написать Кате: @katya_tvorish"""

READY_TEXT = """🏺 *Узнать о своём изделии*

После мастер-класса изделие проходит:
1. 🌬 Сушка
2. ✂️ Обработка перед обжигом
3. 🔥 Первый обжиг
4. 🎨 Покрытие глазурью
5. 🔥 Второй обжиг

*Срок — до 3–4 недель*

Когда работа готова — Катя напишет лично!

Узнать статус → напиши Кате:
👉 @katya_tvorish
📞 +7 919 770 72 89"""

PICKUP_TEXT = """📦 *Как получить готовое изделие*

🚶 *Самовывоз* — приезжай сама, договорись с Катей о времени

🚚 *Курьер* — организуем доставку за твой счёт

📮 *Яндекс Маркет* — Катя отправит сама, оплата при получении

Напиши Кате что удобнее:
👉 @katya_tvorish
📞 +7 919 770 72 89"""

CERT_TEXT = """🎁 *Подарочные сертификаты*

Отличный подарок на любой повод!
Сертификаты на все форматы мастер-классов.

Купить: tvorish.ru/certificate
Или напиши Кате: @katya_tvorish"""

CONTACTS_TEXT = """📞 *Контакты*

👩‍💼 Катя — администратор
Telegram: @katya_tvorish
Телефон: +7 919 770 72 89

🌐 tvorish.ru
📅 tvorish.ru/calendar
🛍 tvorish.ru/shop
📱 t.me/u_cho_tvorish"""

def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏺 О мастерской", callback_data="about"),
         InlineKeyboardButton("🎨 Форматы МК", callback_data="formats")],
        [InlineKeyboardButton("🏢 Корпоративам", callback_data="corporate"),
         InlineKeyboardButton("🎁 Сертификаты", callback_data="cert")],
        [InlineKeyboardButton("📦 Готово ли моё изделие?", callback_data="ready")],
        [InlineKeyboardButton("🚚 Как забрать работу", callback_data="pickup"),
         InlineKeyboardButton("📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton("📅 Расписание →", url=SCHEDULE_URL)],
    ])

def back_kb():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🐾 Главное меню", callback_data="main")]])

def ready_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚚 Как забрать", callback_data="pickup")],
        [InlineKeyboardButton("✍️ Написать Кате", url="https://t.me/katya_tvorish")],
        [InlineKeyboardButton("🐾 Главное меню", callback_data="main")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_TEXT, parse_mode="Markdown", reply_markup=main_kb())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    responses = {
        "main": (WELCOME_TEXT, main_kb()),
        "about": (ABOUT_TEXT, back_kb()),
        "formats": (FORMATS_TEXT, back_kb()),
        "corporate": (CORPORATE_TEXT, back_kb()),
        "cert": (CERT_TEXT, back_kb()),
        "ready": (READY_TEXT, ready_kb()),
        "pickup": (PICKUP_TEXT, back_kb()),
        "contacts": (CONTACTS_TEXT, back_kb()),
    }
    if data in responses:
        text, kb = responses[data]
        await q.edit_message_text(text=text, parse_mode="Markdown", reply_markup=kb)

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if any(w in text for w in ["готов", "изделие", "работа", "когда", "обжиг", "статус"]):
        await update.message.reply_text(READY_TEXT, parse_mode="Markdown", reply_markup=ready_kb())
    elif any(w in text for w in ["забр", "доставк", "курьер", "получ"]):
        await update.message.reply_text(PICKUP_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["формат", "мастер", "мк", "пить", "руки", "глином", "цена", "стоит", "сколько"]):
        await update.message.reply_text(FORMATS_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["корпор", "тимбилд", "бизнес", "компани"]):
        await update.message.reply_text(CORPORATE_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["сертиф", "подарок"]):
        await update.message.reply_text(CERT_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["контакт", "телефон", "адрес", "где", "катя"]):
        await update.message.reply_text(CONTACTS_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    else:
        await update.message.reply_text(
            "🐾 Не совсем поняла! Выбери из меню или напиши:\n«готово» — статус изделия\n«форматы» — все МК\n«контакты» — связь с Катей",
            parse_mode="Markdown", reply_markup=main_kb()
        )

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    app.run_polling()

if __name__ == "__main__":
    main()
