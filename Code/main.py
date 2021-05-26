import nltk
from nltk import casual_tokenize
from telegram import *
from telegram.ext import *
import Responses as R
import io
import csv
import pandas as pd
import json

#updater.stop()

bot = Bot("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4")

updater = Updater("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4", use_context=True)
dispatcher = updater.dispatcher

def start_command(update, context):
    update.message.reply_text("Hello there fellow! Type /help for more info!") 

def send(update, context):
    #test_data = [[1, 2, 3], ["please", "follow", "me"]]
    test_data = pd.read_csv(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\gender_refine-csv.csv')

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

def handle_message(update, context):
    #mj = joblib.load('module.joblib')
    #mj.predict(result)
    text = str(update.message.text).lower() 
    if "gender" in text:
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_comments.png', 'rb'))
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_gender_comments.png', 'rb'))
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_men_comments.png', 'rb'))
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_woman_comments.png', 'rb'))
    elif "trend" in text:
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\trend_map.png', 'rb'))
        bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\plot.png', 'rb'))
    elif "alternative" in text:
        text_file = open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\alternatives.txt", "r")
        alternative_information = text_file.read()
        bot.send_message(chat_id=update.effective_chat.id, text = alternative_information )
    elif "top" in text:
        top3_information = json.load(open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\top3.txt", "r", encoding='utf8'))
        top3_final_values = ''
        for key, value in top3_information.items():
            top3_final_values+=str(key) + ' : '+ '\n' + str(value) + '\n'
        bot.send_message(chat_id=update.effective_chat.id, text = top3_final_values)
    else:
        response = R.sample_responses(text)   # py file aparte
        update.message.reply_text(response)  

def error(update, context): 
    print(f"Update {update} cause error {context.error}")  

def hello_function(update:Update, context:CallbackContext):
    bot.send_message(chat_id=update.effective_chat.id, text = "Afisare functie")


dispatcher.add_handler(CommandHandler("start", start_command))  
dispatcher.add_handler(CommandHandler('try', send))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
updater.start_polling()