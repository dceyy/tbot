from source import splitMessage, db, getChatAdministrator
import time,random
karaliste =[]
with open("karaliste.txt", "r", encoding="utf-8") as f:
    for i in f:
        word=i.strip()
        karaliste.append(word.capitalize())
        karaliste.append(word.lower())
        karaliste.append(word.upper())
        karaliste.append(word.title())
bn="muhtar"
bot_names=[bn.capitalize(), bn.lower(), bn.upper(), bn.title()]
g = ['Merhaba', 'Selam', 'Merhabalar', 'Selamlar', 'Merhaba!', 'Selam!', 'Merhabalar!', 'Selamlar!', 'Merhabalar', 'Nasılsın', 'Nasılsınız', 'İyisin', 'İyisiniz','İyi günler', 'İyi geceler', 'İyi akşamlar', 'İyi sabahlar', 'İyi öğleler', 'Herkese selam', 'Herkese selamlar', 'Sana iyi geceler', 'Sizlere iyi geceler', 'Sana iyi sabahlar', 'Sizlere iyi sabahlar']
greetings = []
karsilama = ['Merhaba', 'Selam', 'Merhabalar', 'Selamlar', 'Merhaba!', 'Selam!', 'Merhabalar!', 'Selamlar!', 'Merhabalar']
for i in g:
    greetings.append(i.capitalize())
    greetings.append(i.upper())
    greetings.append(i.title())
    greetings.append(i.lower())
gruptan_at=["gruptan at", "Gruptan at", "Gruptan At", "GRUPTAN AT", "sohbetten at", "Sohbetten At", "Sohbetten at"]

async def checkBlacklist(update, context):
    message_content = splitMessage.split_message(update.message.text)
    if any(word in message_content for word in karaliste):
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
        db.warn_user(update.message.from_user.id, update.message.from_user.first_name, 1)
        await context.bot.send_message(chat_id=update.message.chat_id, text=f"⚠️ UYARI!!!  {db.view_db(update.message.from_user.id)[-1][-2]} Bu kelimeyi kullanamazsın!\nSenin uyarı sayın: {db.view_db(update.message.from_user.id)[-1][-1]}  Uyarı Sayın 3'e ulaştığında atılacaksın")
        if db.view_db(update.message.from_user.id)[-1][-1] == 3:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{update.message.from_user.first_name} 3 uyarıya ulaştı ve atıldı!")
            await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id, permissions={'can_send_messages':False, 'can_send_media_messages':False, 'can_send_other_messages':False, 'can_add_web_page_previews':False})
            db.update_db(update.message.from_user.id, 0)
        elif db.view_db(update.message.from_user.id)[-1][-1] >3:
            await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=update.message.from_user.id)
            db.update_db(update.message.from_user.id, 0)
        


async def checkGreetings(update, context):
    message_content = splitMessage.split_message(update.message.text)
    if any(word in message_content for word in bot_names):
        if any(word in message_content for word in gruptan_at):
            pass
        else:
            if any(word in message_content for word in greetings):
                await context.bot.send_message(chat_id=update.effective_chat.id, text=f"{random.choice(karsilama)}, ben Muhtar! sana nasıl yardımcı olabilirim?")
            else:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Merhaba, ben Muhtar! sana nasıl yardımcı olabilirim?")
        
async def restrict_user(update, context):
    message_content = splitMessage.split_message(update.message.text)
    message_id=update.message.message_id
    owner_id=await getChatAdministrator.getAdmin(update, context)
    user_id=update.message.reply_to_message.from_user.id
    if update.message.from_user.id in owner_id:
        if any(word in message_content for word in gruptan_at):
            if user_id in owner_id:
                await context.bot.send_message(chat_id=update.effective_chat.id, text="Adminleri gruptan atamam")
                time.sleep(3)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
                
            elif user_id == context.bot.id:
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
                time.sleep(3)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)
            else:
                time.sleep(3)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)
                await context.bot.restrict_chat_member(chat_id=update.effective_chat.id, user_id=user_id, permissions={'can_send_messages':False, 'can_send_media_messages':False, 'can_send_other_messages':False, 'can_add_web_page_previews':False})
                db.delete_db(user_id)
        
                message=await context.bot.send_message(chat_id=update.effective_chat.id, text="Kullanıcı gruptan atıldı!")
                time.sleep(3)
                await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message.message_id)