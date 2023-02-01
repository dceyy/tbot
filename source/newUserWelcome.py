import source.db as db
from datetime import datetime
import logging, random, asyncio
from emoji import emojize
from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, InlineQueryHandler, CallbackQueryHandler
import source.splitMessage as splitMessage, source.db as db, time


async def new_user(update, context, time=40):
    user_id = update.message.new_chat_members[0].id
    user_name = update.message.new_chat_members[0].first_name
    chat_id = update.effective_chat.id
    #kullanıcının robot olup olmadığını denetle
    keyboard=[[InlineKeyboardButton("Ben robot değilim", callback_data="robot_degilim")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    
