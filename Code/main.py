import nltk
from nltk import casual_tokenize
from telegram import *
from telegram.ext import *
import Responses as R
import io
import csv
import pandas as pd
import json
import alghoritm

#Bot settings

bot = Bot("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4")

updater = Updater("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4", use_context=True)
dispatcher = updater.dispatcher


#Functions for buttons

def meniu(update, context):
    keyboard = [[InlineKeyboardButton('Top', callback_data = 'top'), InlineKeyboardButton('Gender', callback_data = 'gender')],
                [InlineKeyboardButton('Trend', callback_data = 'trend'), InlineKeyboardButton('Alternative', callback_data = 'alternative')],
                [InlineKeyboardButton('Definition', callback_data = 'definition'), InlineKeyboardButton('Export Data', callback_data = 'export')]]
    markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(chat_id=update.effective_chat.id, text = 'Also you can probe other processes : ', reply_markup = markup)

def meniu_complete(update, context):
    keyboard = [[InlineKeyboardButton('Top', callback_data = 'top'), InlineKeyboardButton('Gender', callback_data = 'gender')],
                [InlineKeyboardButton('Trend', callback_data = 'trend'), InlineKeyboardButton('Alternative', callback_data = 'alternative')],
                [InlineKeyboardButton('Definition', callback_data = 'definition'), InlineKeyboardButton('Export Data', callback_data = 'export')]]
    markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(text = "The meniu is : ", reply_markup = markup)

def info(update, context):
    update.message.reply_text("This project represents a telegram bot that uses Natural Language Processing to analyze the customers' review of a product using tweets from the online platform Tweeter.")

def help(update, context):
    update.message.reply_text("IMPORTANT: \n\n To use all the funcitons like gender, trends or alternative you first need to analyze the product in this form: '/analyze *your product*' \n\n\nYou can use this commands : \n\n/info - short information about the project\n\n/help - displays all the functions that we have\n\n/meniu - gives the menu for more detailed result\n\n/analyze - function needed to start the analysis process|'/analyze *your product*'\n\n/top - gives the top positive and negative comments\n\n/gender - gives some diagrams about gender\n\n/trend - gives a graph and a map about the popularuty of the product\n\n/alternative - gives some alternatives for your product if existing\n\n/definition - gives the definition of the product if existing\n\n/export - sends you the Analysis result in a *.csv form\n\n")

def analyze(update, context):
    message = update.message.text.lower()
    search_word = message[9:]
    update.message.reply_text('Analyze : ' + search_word + '\n')
    update.message.reply_text('It might take some time\n')
    result = alghoritm.start_process(search_word)
    update.message.reply_text(result)

    meniu(update, context)

def gender(update, context):
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_comments.png', 'rb'))
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_gender_comments.png', 'rb'))
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_men_comments.png', 'rb'))
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_woman_comments.png', 'rb'))

    meniu(update, context)

def trend(update, context):
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\trend_map.png', 'rb'))
    bot.send_photo(chat_id=update.effective_chat.id, photo=open(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\plot.png', 'rb'))

    meniu(update, context)

def alternative(update, context):
    text_file = open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\alternatives.txt", "r")
    alternative_information = text_file.read()
    bot.send_message(chat_id=update.effective_chat.id, text = alternative_information )

    meniu(update, context)

def top(update, context):
    top3_information = json.load(open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\top3.txt", "r", encoding='utf8'))
    top3_final_values = ''
    i=1
    for key in top3_information:
        i=1
        top3_final_values+=str(key) + ' : '+'\n'
        for value in top3_information[key]:
            top3_final_values+=str(i) + '. ' + str(value) + '\n\n'
            i+=1
    bot.send_message(chat_id=update.effective_chat.id, text = top3_final_values)

    meniu(update, context)

def definition(update, context):
    text_file = open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\definition.txt", "r")
    alternative_information = text_file.read()
    bot.send_message(chat_id=update.effective_chat.id, text = alternative_information )

    meniu(update, context)
#Functions for work with Bot

def start_command(update, context):
    update.message.reply_text("Hello there fellow! Type /help for more info!")

def export(update, context):
    test_data = pd.read_csv(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\result.csv')

    # csv module can write data in io.StringIO buffer only
    s = io.StringIO()
    csv.writer(s).writerows(test_data.values)
    s.seek(0)

    buf = io.BytesIO()

    # extract csv-string, convert it to bytes and write to buffer
    buf.write(s.getvalue().encode())
    buf.seek(0)

    # set a filename with file's extension
    buf.name = f'Analisys result.csv'

    # send the buffer as a regular file
    bot.send_document(chat_id=update.effective_chat.id, document=buf)
    meniu(update, context)

def handle_message(update, context):
    text = str(update.message.text).lower()
    if "gender" in text:
        gender(update, context)
    elif "trend" in text:
        trend(update, context)
    elif "top" in text:
        top(update, context)
    else:
        response = R.sample_responses(text)   # py file aparte
        update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} cause error {context.error}")

def hello_function(update:Update, context:CallbackContext):
    bot.send_message(chat_id=update.effective_chat.id, text = "Afisare functie")

def callback_query_handler(update, context):
    cqd = update.callback_query.data
    if cqd == 'analyze':
        analyze(update, context)
    elif cqd == 'top':
        top(update, context)
    elif cqd == 'gender':
        gender(update, context)
    elif cqd == 'trend':
        trend(update, context)
    elif cqd == 'alternative':
        alternative(update, context)
    elif cqd == 'export':
        export(update, context)
    elif cqd == 'definition':
        definition(update, context)



#Work with Bot

dispatcher.add_handler(CommandHandler('start', start_command))
dispatcher.add_handler(CommandHandler('meniu', meniu_complete))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('info', info))
dispatcher.add_handler(CommandHandler('export', export))
dispatcher.add_handler(CommandHandler('Analyze', analyze))
dispatcher.add_handler(CommandHandler('Top', top))
dispatcher.add_handler(CommandHandler('Gender', gender))
dispatcher.add_handler(CommandHandler('Trend', trend))
dispatcher.add_handler(CommandHandler('Alternative', alternative))
dispatcher.add_handler(CommandHandler('Definition', definition))
dispatcher.add_handler(MessageHandler(Filters.text, handle_message))
dispatcher.add_handler(CallbackQueryHandler(callback_query_handler))
updater.start_polling()

updater.idle()
