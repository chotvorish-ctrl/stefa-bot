#!/usr/bin/env python3
import logging, os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SCHEDULE_URL = "https://tvorish.ru/calendar"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

WELCOME_TEXT = """🐾 *Гав! Я Стефа* — амбассадор мастерской «Ты чо творишь»

Помогу найти всё нужное: расскажу про форматы, узнаю про твоё изделие и провожу к Кате 🎨"""

ABOUT_TEXT = """🏺 *Мастерская «Ты чо творишь»*

Креативная мастерская керамики в Москве. Пространство свободы, творчества и самовыражения.

Лепим посуду, предметы декора, отпечатки лапок — без навыков и без понтов.

📞 +7 919 770 72 89
🌐 tvorish.ru
📱 t.me/u\\_cho\\_tvorish"""

FORMATS_TEXT = """🎨 *Форматы мастер-классов*

🍷 *Пить Лепить* — 6 500 ₽
3 часа лепки + игристое + фуршет + музыка. 18+

🖐 *Руки из жопы* — 5 000 ₽
Ручная лепка без подготовки. 12+

👨‍👩‍👧 *Глиномесики* — 4 000 ₽
Семейный/детский МК. 3+

🐶 *Лапы лепят* — 6 500 ₽
С собаками! Отпечатки лапок и носиков.

🔮 *Керамистика* — 7 000 ₽
Лепка + таро + астропрогнозы + фуршет.

🕯 *Свидетельство о жизни* — по запросу

📅 Расписание: tvorish.ru/calendar
_Перед оплатой уточни даты: +7 919 770 72 89_"""

CORPORATE_TEXT = """🏢 *Корпоративные форматы*

• 🤝 Тимбилдинги
• 🎁 Корпоративные подарки с логотипом
• 🍽 Посуда на заказ для HoReCa
• 🏠 Интерьерные решения

От 6 до 30 человек — в мастерской или выезд.

📝 tvorish.ru
📞 @katya\\_tvorish"""

READY_TEXT = """🏺 *Узнать о своём изделии*

После мастер-класса изделие проходит:
1. 🌬 Сушка
2. ✂️ Обработка
3. 🔥 Первый обжиг
4. 🎨 Глазурь
5. 🔥 Второй обжиг

*Срок — до 3–4 недель*

Узнать статус → напиши Кате:
👉 @katya\\_tvorish
📞 +7 919 770 72 89"""

PICKUP_TEXT = """📦 *Как получить готовое изделие*

🚶 *Самовывоз* — договорись с Катей о времени
🚚 *Курьер* — доставка за твой счёт
📮 *Яндекс Маркет* — Катя отправит сама

👉 @katya\\_tvorish
📞 +7 919 770 72 89"""

CERT_TEXT = """🎁 *Подарочные сертификаты*

На все форматы мастер-классов.

Купить: tvorish.ru/certificate
Или: @katya\\_tvorish"""

CONTACTS_TEXT = """📞 *Контакты*

👩‍💼 Катя — администратор
Telegram: @katya\\_tvorish
Телефон: +7 919 770 72 89

🌐 tvorish.ru
📅 tvorish.ru/calendar"""

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
    if q.data in responses:
        text, kb = responses[q.data]
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
            "🐾 Не совсем поняла! Выбери из меню 👇",
            reply_markup=main_kb()
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
