async def getAdmin(update, context):
    chat_owner=await context.bot.get_chat_administrators(update.message.chat_id)
    co = [i.user.id for i in chat_owner]
    return co
    
async def get_bot_admin(update, context):
    bot_admin = await context.bot.get_chat_administrators(update.message.chat_id)
    bot_admin = [i.user.id for i in bot_admin if i.user.is_bot]
    return bot_admin