import logging, random, asyncio
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler
from source import getChatAdministrator, messageContent, newUserWelcome, splitMessage, db
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("API_KEY")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[[KeyboardButton("/help")],[KeyboardButton("/info")]]
    reply_markup = ReplyKeyboardMarkup(keyboard,one_time_keyboard=True, resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Merhaba, ben Muhtar! sana nasıl yardımcı olabilirim?", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "sohbet_kurallari":
        message="Konuşmalar kibar ve saygılı olmalı 💬\ nSohbet içeriği uygun olmalı 📜\nSpam yapmak yasaktır 🚫 \nYa da keyfinize bakın amk🤪"
        await query.message.edit_text(text=message)
    elif query.data == "ben":
        await query.message.edit_text(text="Ben Muhtar! Doğan Ceylancı tarafından yapılmış bir botum.")
    elif query.data == "robot_degilim":
        time=60
        user_id = update.callback_query.from_user.id
        user_name = update.callback_query.from_user.first_name
        chat_id = update.effective_chat.id
        keyboard = [[InlineKeyboardButton("Ben robot değilim", callback_data="robot_degilim")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message=await context.bot.send_message(chat_id=update.effective_chat.id, text="Gruba hoşgeldin, {}! Lütfen {} saniye boyunca aşağıdaki butonu kullanarak robot olmadığını kanıtlar mısın?".format(user_name, time), reply_markup=reply_markup)
        await asyncio.sleep(time)
        if not await message:
            await context.bot.restrict_chat_member(chat_d=chat_id, user_id=user_id, permissions={'can_send_messages': False, 'can_send_media_messages': False, 'can_send_other_messages': False, 'can_add_web_page_previews': False}, until_date=datetime.now() + timedelta(months=1))
            await context.bot.send_message(chat_id=update.effective_chat.id, text="{} {} saniye boyunca butonu kullanmadığı için gruptan atıldı.".format(user_name, time))
        else:
            pass
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard=[[InlineKeyboardButton("ben", callback_data="ben")],[InlineKeyboardButton("Sohbet Kuralları", callback_data="sohbet_kurallari")],
          [InlineKeyboardButton("Ben", url="https://github.com/doganceylanci"), InlineKeyboardButton("Donate", url="https://www.buymeacoffee.com/dcey")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bilgi için aşağıdaki butonları kullanabilirsiniz.", reply_markup=reply_markup)

async def new_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Bu bot, @doganceylanci tarafından yapılmıştır. Botun kaynak kodlarına aşağıdaki linkten ulaşabilirsiniz. \nhttps://github.com/doganceylanci/tbot")



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.from_user.first_name
    user_id = update.message.from_user.id
    chat_owner = await getChatAdministrator.getAdmin(update, context)
    if user_id in chat_owner:
        await messageContent.restrict_user(update, context)
    else:
        #check message content
        if not await messageContent.checkBlacklist(update, context):
            await messageContent.checkGreetings(update, context)
        else:
            await messageContent.checkBlacklist(update, context)
async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    await context.bot.answer_inline_query(update.inline_query.id, results)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Üzgünüm, şu anda geliştirme aşamasında olduğum için bu komutu anlayamıyorum. Ama ileride anlayacağım, umarım. 🤖")

if __name__=="__main__":
    app = ApplicationBuilder().token(api_key).build()
    start_handler = CommandHandler('start', start)
    app.add_handler(start_handler)
    help_handler = CommandHandler('help', help)
    app.add_handler(help_handler)
    info_handler = CommandHandler('info', info)
    app.add_handler(info_handler)
    button_callback_handler = CallbackQueryHandler(button_callback, pattern='sohbet_kurallari|ben|robot_degilim')
    app.add_handler(button_callback_handler)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    app.add_handler(echo_handler)
    new_user_handler = MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_user)
    app.add_handler(new_user_handler)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    app.add_handler(unknown_handler)
    inline_caps_handler = InlineQueryHandler(inline_caps)
    app.add_handler(inline_caps_handler)
    app.run_polling()
