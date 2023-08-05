# Telegram
from telegram.ext import Updater, CommandHandler
from telegram import update, ChatAction

# Database and token 
from connect import db
import os

# Date
from datetime import datetime

#Commands
def start(update, context):
    """Saluda a Flupi"""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Saludo desde Flupi")

    # Envío de una imagen
    image_url = "https://github.com/JorgeArguello1999/Flupi/blob/main/logo.jpeg?raw=true"
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=image_url)

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

/update
/rm
    """
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_doc)
    #Debug
    print('Comando ejecutado: start')


def insert(update, context):
    """Insertando datos"""
    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    insert = (" ".join(context.args)).split(",")
    answer = insert
    context.bot.send_message(chat_id=update.effective_chat.id, text=(str(answer)))
    print('/insert', answer)

#Start TelBot 
token = str(os.getenv("TELEGRAM_BOT")) 
updater = Updater(token=token, use_context=True)

#Handlers
start_handler = CommandHandler("start", start)
help_handler = CommandHandler("help", help)
insert_handler= CommandHandler("insert", insert)

#Dispatchers
updater.dispatcher.add_handler(start_handler)
updater.dispatcher.add_handler(help_handler)
updater.dispatcher.add_handler(insert_handler)

updater.start_polling()
