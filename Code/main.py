import nltk
from nltk import casual_tokenize
from telegram import *
from telegram.ext import *
import Responses as R
import io
import csv
import pandas as pd

#updater.stop()

bot = Bot("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4")

updater = Updater("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4", use_context=True)
dispatcher = updater.dispatcher

inlineKeybord = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(text= "Analyze" ,callback_data = "analyze")],
            [InlineKeyboardButton(text= "Gender" ,callback_data = "gender")],
            [InlineKeyboardButton(text= "Show Graph" ,callback_data = "graph")],
            [InlineKeyboardButton(text= "Alternatives" ,callback_data = "alternative")],
        ]
)

def start_command(update, context):
    update.message.reply_text("Hello there fellow! Type /help for more info!") 

def reaction(update, context):
    bot.send_message(chat_id = update.effective_chat.id, reply_markup = inlineKeybord, text = "Acestea sunt funcțiile de care dispunem")

def send(update, context):
    #test_data = [[1, 2, 3], ["please", "follow", "me"]]
    test_data = pd.read_csv(r'C:\Users\vladi\OneDrive\Desktop\downloads\code2\gender_refine-csv.csv')

    # csv module can write data in io.StringIO buffer only
    s = io.StringIO()
    csv.writer(s).writerows(test_data.values)
    s.seek(0)

    # python-telegram-bot library can send files only from io.BytesIO buffer
    # we need to convert StringIO to BytesIO
    buf = io.BytesIO()

    # extract csv-string, convert it to bytes and write to buffer
    buf.write(s.getvalue().encode())
    buf.seek(0)

    # set a filename with file's extension
    buf.name = f'gender_refine-csv.csv'

    # send the buffer as a regular file
    context.bot.send_document(chat_id=update.message.chat_id, document=buf)

def handle_message(update, text, value=False):
    #mj = joblib.load('module.joblib')
    #mj.predict(result)
    text = str(update.message.text).lower() 
    response = R.sample_responses(text, text, value)   # py file aparte
    update.message.reply_text(response)  

def handle_message2(update):
    #mj = joblib.load('module.joblib')
    #mj.predict(result)
    text = str(update.message.text).lower() 
    response = R.analyze(text)   # py file aparte
    update.message.reply_text(response)  

def button(update: Update, _: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    query.edit_message_text(text=query.data, reply_markup=inlineKeybord)        
    if query.data == "analyze":
        bot.send_message(chat_id = update.effective_chat.id, text = "give the input")
        handle_message2(update)    

def error(update, context): 
    print(f"Update {update} cause error {context.error}")  

def hello_function(update:Update, context:CallbackContext):
    bot.send_message(chat_id=update.effective_chat.id, text = "Afisare functie")


dispatcher.add_handler(CommandHandler("start", start_command))  
dispatcher.add_handler(CommandHandler('help', reaction))
dispatcher.add_handler(CommandHandler('try', send))
updater.dispatcher.add_handler(CallbackQueryHandler(button))
dispatcher.add_handler(MessageHandler(Filters.text,handle_message))
updater.start_polling()