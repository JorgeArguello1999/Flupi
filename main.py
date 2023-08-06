# Telegram
from telegram.ext import Updater, CommandHandler
from telegram import update, ChatAction

# Database and token 
from connect import db
conn = db.connect()
import os, random 

# Date
import datetime
date = str(datetime.datetime.now())

#Commands
def start(update, context):
    """Saluda a Flupi"""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Holis, soy Flupi (☆▽☆)")

    # Envío de una imagen
    image_url = [
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/1.jpeg?raw=true",
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/2.jpeg?raw=true",
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/3.jpeg?raw=true",
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/4.jpeg?raw=true",
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/5.jpeg?raw=true",
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/6.jpeg?raw=true",
        "https://github.com/JorgeArguello1999/Flupi/blob/main/Yo/7.jpeg?raw=true",
    ]
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url[random.randint(0, 6)])

    #Debug
    print('Comando ejecutado: start')

def help(update, context):
    """Ayudanos Flupi"""
    help_doc = """
/start 'Saluda Flopi'
/help 'Este manual'
/list 'Puntaje total'
/list_total 'Lista todo el registro'
/insert 'Inserta los datos ten este ejemplo:'

1er valor = Avengers
2do valor = Quimbolitos

> /insert 1,2
_Recuerda que los registros guardan los nombres de usuario_
    """
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_doc)
    #Debug
    print('Comando ejecutado: start')

def list(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    answer = conn.list()
    answer = f"Avengers = {answer[0]}\nQuimbolitos = {answer[1]}"
    context.bot.send_message(chat_id=update.effective_chat.id, text=answer)

    #Debug
    print('Comando ejecutado: list')


def list_all(update, context):
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    
    sentences = "| ID | Vengadores | Quimbolitos | Usuario | Fecha |\n"
    for i in conn.list_all():
        sentences += f"| {i[0]} | {i[1]} | {i[2]} | {i[3]} | {i[4]} |\n"

    print(sentences)
    context.bot.send_message(chat_id=update.effective_chat.id, text=sentences)

    #Debug
    print('Comando ejecutado: start')

def insert(update, context):
    """Insertando datos"""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Usename
    user = update.effective_user
    user_name = user.username if user.username else user.full_name

    # Insert to database
    insert = (" ".join(context.args)).split(",")
    answer = [
        int(insert[0]), # Avengers
        int(insert[1]), # Quimbolitos
        user_name # Usuario
    ]
    out = conn.insert(answer)

    context.bot.send_message(chat_id=update.effective_chat.id, text=(str(out)))
    print('/insert', answer)

def rm(update, context):
    """Insertando datos"""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    id = (" ".join(context.args)).split(",")
    out = conn.remove(id[0])
    context.bot.send_message(chat_id=update.effective_chat.id, text=(str(out)))
    print('/rm', id)

#Start TelBot 
token = str(os.getenv("TELEGRAM_BOT")) 
updater = Updater(token=token, use_context=True)

#Handlers
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
list_handler = CommandHandler("list", list)
list_all_handler = CommandHandler("list_all", list_all)
insert_handler= CommandHandler("insert", insert)
rm_handler = CommandHandler("rm", rm)

#Dispatchers
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(list_handler)
updater.dispatcher.add_handler(list_all_handler)
updater.dispatcher.add_handler(insert_handler)
updater.dispatcher.add_handler(rm_handler)

updater.start_polling()
