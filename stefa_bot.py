#!/usr/bin/env python3
import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
SCHEDULE_URL = "https://tvorish.ru/calendar"

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

WELCOME_TEXT = (
    "\U0001f43e *\u0413\u0430\u0432! \u042f \u0421\u0442\u0435\u0444\u0430* \u2014 \u0430\u043c\u0431\u0430\u0441\u0441\u0430\u0434\u043e\u0440 \u043c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u043e\u0439 \u00ab\u0422\u044b \u0447\u043e \u0442\u0432\u043e\u0440\u0438\u0448\u044c\u00bb\n\n"
    "\u041f\u043e\u043c\u043e\u0433\u0443 \u043d\u0430\u0439\u0442\u0438 \u0432\u0441\u0451 \u043d\u0443\u0436\u043d\u043e\u0435: \u0440\u0430\u0441\u0441\u043a\u0430\u0436\u0443 \u043f\u0440\u043e \u0444\u043e\u0440\u043c\u0430\u0442\u044b, \u0443\u0437\u043d\u0430\u044e \u043f\u0440\u043e \u0442\u0432\u043e\u0451 \u0438\u0437\u0434\u0435\u043b\u0438\u0435 \u0438 \u043f\u0440\u043e\u0432\u043e\u0436\u0443 \u043a \u041a\u0430\u0442\u0435 \U0001f3a8"
)

ABOUT_TEXT = (
    "\U0001f3fa *\u041c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u0430\u044f \u00ab\u0422\u044b \u0447\u043e \u0442\u0432\u043e\u0440\u0438\u0448\u044c\u00bb*\n\n"
    "\u041a\u0440\u0435\u0430\u0442\u0438\u0432\u043d\u0430\u044f \u043c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u0430\u044f \u043a\u0435\u0440\u0430\u043c\u0438\u043a\u0438 \u0432 \u041c\u043e\u0441\u043a\u0432\u0435.\n\n"
    "\U0001f4de +7 919 770 72 89\n"
    "\U0001f310 tvorish.ru\n"
    "\U0001f4f1 t.me/u\\_cho\\_tvorish"
)

FORMATS_TEXT = (
    "\U0001f3a8 *\u0424\u043e\u0440\u043c\u0430\u0442\u044b \u043c\u0430\u0441\u0442\u0435\u0440-\u043a\u043b\u0430\u0441\u0441\u043e\u0432*\n\n"
    "\U0001f377 *\u041f\u0438\u0442\u044c \u041b\u0435\u043f\u0438\u0442\u044c* \u2014 6 500 \u20bd\n"
    "3 \u0447\u0430\u0441\u0430 \u043b\u0435\u043f\u043a\u0438 + \u0438\u0433\u0440\u0438\u0441\u0442\u043e\u0435 + \u0444\u0443\u0440\u0448\u0435\u0442 + \u043c\u0443\u0437\u044b\u043a\u0430. 18+\n\n"
    "\U0001f590 *\u0420\u0443\u043a\u0438 \u0438\u0437 \u0436\u043e\u043f\u044b* \u2014 5 000 \u20bd\n"
    "\u0420\u0443\u0447\u043d\u0430\u044f \u043b\u0435\u043f\u043a\u0430 \u0431\u0435\u0437 \u043f\u043e\u0434\u0433\u043e\u0442\u043e\u0432\u043a\u0438. 12+\n\n"
    "\U0001f46a *\u0413\u043b\u0438\u043d\u043e\u043c\u0435\u0441\u0438\u043a\u0438* \u2014 4 000 \u20bd\n"
    "\u0421\u0435\u043c\u0435\u0439\u043d\u044b\u0439/\u0434\u0435\u0442\u0441\u043a\u0438\u0439 \u041c\u041a. 3+\n\n"
    "\U0001f436 *\u041b\u0430\u043f\u044b \u043b\u0435\u043f\u044f\u0442* \u2014 6 500 \u20bd\n"
    "\u041f\u0440\u0438\u0445\u043e\u0434\u0438\u0442\u0435 \u0441 \u0441\u043e\u0431\u0430\u043a\u0430\u043c\u0438!\n\n"
    "\U0001f52e *\u041a\u0435\u0440\u0430\u043c\u0438\u0441\u0442\u0438\u043a\u0430* \u2014 7 000 \u20bd\n"
    "\u041b\u0435\u043f\u043a\u0430 + \u0442\u0430\u0440\u043e + \u0430\u0441\u0442\u0440\u043e\u043f\u0440\u043e\u0433\u043d\u043e\u0437\u044b + \u0444\u0443\u0440\u0448\u0435\u0442.\n\n"
    "\U0001f56f *\u0421\u0432\u0438\u0434\u0435\u0442\u0435\u043b\u044c\u0441\u0442\u0432\u043e \u043e \u0436\u0438\u0437\u043d\u0438* \u2014 \u043f\u043e \u0437\u0430\u043f\u0440\u043e\u0441\u0443\n\n"
    "\U0001f4c5 \u0420\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435: tvorish.ru/calendar\n"
    "_\u041f\u0435\u0440\u0435\u0434 \u043e\u043f\u043b\u0430\u0442\u043e\u0439 \u0443\u0442\u043e\u0447\u043d\u0438 \u0434\u0430\u0442\u044b: +7 919 770 72 89_"
)

CORPORATE_TEXT = (
    "\U0001f3e2 *\u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0435 \u0444\u043e\u0440\u043c\u0430\u0442\u044b*\n\n"
    "\u2022 \U0001f91d \u0422\u0438\u043c\u0431\u0438\u043b\u0434\u0438\u043d\u0433\u0438\n"
    "\u2022 \U0001f381 \u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0442\u0438\u0432\u043d\u044b\u0435 \u043f\u043e\u0434\u0430\u0440\u043a\u0438\n"
    "\u2022 \U0001f37d \u041f\u043e\u0441\u0443\u0434\u0430 \u043d\u0430 \u0437\u0430\u043a\u0430\u0437\n\n"
    "\u041e\u0442 6 \u0434\u043e 30 \u0447\u0435\u043b\u043e\u0432\u0435\u043a.\n\n"
    "\U0001f4dd tvorish.ru\n"
    "\U0001f4de @katya\\_tvorish"
)

READY_TEXT = (
    "\U0001f3fa *\u0423\u0437\u043d\u0430\u0442\u044c \u043e \u0441\u0432\u043e\u0451\u043c \u0438\u0437\u0434\u0435\u043b\u0438\u0438*\n\n"
    "\u041f\u043e\u0441\u043b\u0435 \u041c\u041a \u0438\u0437\u0434\u0435\u043b\u0438\u0435 \u043f\u0440\u043e\u0445\u043e\u0434\u0438\u0442:\n"
    "1. \U0001f32c \u0421\u0443\u0448\u043a\u0430\n"
    "2. \u2702\ufe0f \u041e\u0431\u0440\u0430\u0431\u043e\u0442\u043a\u0430\n"
    "3. \U0001f525 \u041f\u0435\u0440\u0432\u044b\u0439 \u043e\u0431\u0436\u0438\u0433\n"
    "4. \U0001f3a8 \u0413\u043b\u0430\u0437\u0443\u0440\u044c\n"
    "5. \U0001f525 \u0412\u0442\u043e\u0440\u043e\u0439 \u043e\u0431\u0436\u0438\u0433\n\n"
    "*\u0421\u0440\u043e\u043a \u2014 \u0434\u043e 3\u20134 \u043d\u0435\u0434\u0435\u043b\u044c*\n\n"
    "\u0423\u0437\u043d\u0430\u0442\u044c \u0441\u0442\u0430\u0442\u0443\u0441:\n"
    "\U0001f449 @katya\\_tvorish\n"
    "\U0001f4de +7 919 770 72 89"
)

PICKUP_TEXT = (
    "\U0001f4e6 *\u041a\u0430\u043a \u043f\u043e\u043b\u0443\u0447\u0438\u0442\u044c \u0433\u043e\u0442\u043e\u0432\u043e\u0435 \u0438\u0437\u0434\u0435\u043b\u0438\u0435*\n\n"
    "\U0001f6b6 *\u0421\u0430\u043c\u043e\u0432\u044b\u0432\u043e\u0437* \u2014 \u0434\u043e\u0433\u043e\u0432\u043e\u0440\u0438\u0441\u044c \u0441 \u041a\u0430\u0442\u0435\u0439\n"
    "\U0001f69a *\u041a\u0443\u0440\u044c\u0435\u0440* \u2014 \u0434\u043e\u0441\u0442\u0430\u0432\u043a\u0430 \u0437\u0430 \u0442\u0432\u043e\u0439 \u0441\u0447\u0451\u0442\n"
    "\U0001f4ee *\u042f\u043d\u0434\u0435\u043a\u0441 \u041c\u0430\u0440\u043a\u0435\u0442* \u2014 \u041a\u0430\u0442\u044f \u043e\u0442\u043f\u0440\u0430\u0432\u0438\u0442 \u0441\u0430\u043c\u0430\n\n"
    "\U0001f449 @katya\\_tvorish\n"
    "\U0001f4de +7 919 770 72 89"
)

CERT_TEXT = (
    "\U0001f381 *\u041f\u043e\u0434\u0430\u0440\u043e\u0447\u043d\u044b\u0435 \u0441\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u044b*\n\n"
    "\u041d\u0430 \u0432\u0441\u0435 \u0444\u043e\u0440\u043c\u0430\u0442\u044b \u043c\u0430\u0441\u0442\u0435\u0440-\u043a\u043b\u0430\u0441\u0441\u043e\u0432.\n\n"
    "\u041a\u0443\u043f\u0438\u0442\u044c: tvorish.ru/certificate\n"
    "\u0418\u043b\u0438: @katya\\_tvorish"
)

CONTACTS_TEXT = (
    "\U0001f4de *\u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b*\n\n"
    "\U0001f469\u200d\U0001f4bc \u041a\u0430\u0442\u044f \u2014 \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\n"
    "Telegram: @katya\\_tvorish\n"
    "\u0422\u0435\u043b\u0435\u0444\u043e\u043d: +7 919 770 72 89\n\n"
    "\U0001f310 tvorish.ru\n"
    "\U0001f4c5 tvorish.ru/calendar"
)


def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001f3fa \u041e \u043c\u0430\u0441\u0442\u0435\u0440\u0441\u043a\u043e\u0439", callback_data="about"),
         InlineKeyboardButton("\U0001f3a8 \u0424\u043e\u0440\u043c\u0430\u0442\u044b \u041c\u041a", callback_data="formats")],
        [InlineKeyboardButton("\U0001f3e2 \u041a\u043e\u0440\u043f\u043e\u0440\u0430\u0442\u0438\u0432\u0430\u043c", callback_data="corporate"),
         InlineKeyboardButton("\U0001f381 \u0421\u0435\u0440\u0442\u0438\u0444\u0438\u043a\u0430\u0442\u044b", callback_data="cert")],
        [InlineKeyboardButton("\U0001f4e6 \u0413\u043e\u0442\u043e\u0432\u043e \u043b\u0438 \u043c\u043e\u0451 \u0438\u0437\u0434\u0435\u043b\u0438\u0435?", callback_data="ready")],
        [InlineKeyboardButton("\U0001f69a \u041a\u0430\u043a \u0437\u0430\u0431\u0440\u0430\u0442\u044c \u0440\u0430\u0431\u043e\u0442\u0443", callback_data="pickup"),
         InlineKeyboardButton("\U0001f4de \u041a\u043e\u043d\u0442\u0430\u043a\u0442\u044b", callback_data="contacts")],
        [InlineKeyboardButton("\U0001f4c5 \u0420\u0430\u0441\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u2192", url=SCHEDULE_URL)],
    ])


def back_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("\U0001f43e \u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e", callback_data="main")
    ]])


def ready_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("\U0001f69a \u041a\u0430\u043a \u0437\u0430\u0431\u0440\u0430\u0442\u044c", callback_data="pickup")],
        [InlineKeyboardButton("\u270d\ufe0f \u041d\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u041a\u0430\u0442\u0435", url="https://t.me/katya_tvorish")],
        [InlineKeyboardButton("\U0001f43e \u0413\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e", callback_data="main")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(WELCOME_TEXT, parse_mode="Markdown", reply_markup=main_kb())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
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
    if query.data in responses:
        text, kb = responses[query.data]
        await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=kb)


async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.lower()
    if any(w in text for w in ["\u0433\u043e\u0442\u043e\u0432", "\u0438\u0437\u0434\u0435\u043b", "\u0440\u0430\u0431\u043e\u0442\u0430", "\u043a\u043e\u0433\u0434\u0430", "\u043e\u0431\u0436\u0438\u0433", "\u0441\u0442\u0430\u0442\u0443\u0441"]):
        await update.message.reply_text(READY_TEXT, parse_mode="Markdown", reply_markup=ready_kb())
    elif any(w in text for w in ["\u0437\u0430\u0431\u0440", "\u0434\u043e\u0441\u0442\u0430\u0432", "\u043a\u0443\u0440\u044c\u0435\u0440", "\u043f\u043e\u043b\u0443\u0447"]):
        await update.message.reply_text(PICKUP_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["\u0444\u043e\u0440\u043c\u0430\u0442", "\u043c\u0430\u0441\u0442\u0435\u0440", "\u043c\u043a", "\u043f\u0438\u0442\u044c", "\u0440\u0443\u043a\u0438", "\u0446\u0435\u043d\u0430", "\u0441\u0442\u043e\u0438\u0442", "\u0441\u043a\u043e\u043b\u044c\u043a\u043e"]):
        await update.message.reply_text(FORMATS_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["\u043a\u043e\u0440\u043f\u043e\u0440", "\u0442\u0438\u043c\u0431\u0438\u043b\u0434", "\u0431\u0438\u0437\u043d\u0435\u0441"]):
        await update.message.reply_text(CORPORATE_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["\u0441\u0435\u0440\u0442\u0438\u0444", "\u043f\u043e\u0434\u0430\u0440\u043e\u043a"]):
        await update.message.reply_text(CERT_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    elif any(w in text for w in ["\u043a\u043e\u043d\u0442\u0430\u043a\u0442", "\u0442\u0435\u043b\u0435\u0444\u043e\u043d", "\u0430\u0434\u0440\u0435\u0441", "\u0433\u0434\u0435", "\u043a\u0430\u0442\u044f"]):
        await update.message.reply_text(CONTACTS_TEXT, parse_mode="Markdown", reply_markup=back_kb())
    else:
        await update.message.reply_text(
            "\U0001f43e \u041d\u0435 \u0441\u043e\u0432\u0441\u0435\u043c \u043f\u043e\u043d\u044f\u043b\u0430! \u0412\u044b\u0431\u0435\u0440\u0438 \u0438\u0437 \u043c\u0435\u043d\u044e \U0001f447",
            reply_markup=main_kb()
        )


def main() -> None:
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("menu", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
