'''
Created with love by Paza Anulare
'''

#Importing all libraries

from pandas.core.frame import DataFrame
from telegram.error import TelegramError
from datetime import datetime    
import random 
import nltk 
from nltk import casual_tokenize 
import requests 
import bs4 
import twint
import alghoritm
import pandas as pd
from telegram import *
from telegram.ext import *

#Setting the basic user interaction questions and answers
greetings = {"chat":[ "hi", "hey",  "how are you", "is anyone there?", "hello", "good day", "good afternoon", "good morning", ], 
        "responses": [ "Hey :-)", "Hello, thanks for visiting", "Hi there, what can I do for you?","Hi there, how can I help?" ] 
           }  

thanks  =  { "chat": ["thanks", "thank you", "that is helpful", "thanks a lot!"],
      "responses": ["Happy to help!", "Any time!", "My pleasure"] 
           }  

goodbye = { "chat": ["bye", "see you later", "goodbye","see ya", "good luck"],
      "responses": [ "See you later, thanks for visiting", "Have a nice day", "Bye! Come back again soon." ]  
          } 

jokes =  {  "chat": [ "tell me a joke", "tell me something funny", "do you know a joke?"  ],
      "responses": ["Why did the hipster burn his mouth? He drank the coffee before it was cool.", "What did the buffalo say when his son left for college? Bison."]  
         }  
random.seed()           

bot = Bot("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4")



def sample_responses(input_text: str):
    """
        The meniu function creates a the button arrangement for the response
    :param input_text: str
        The user input that needs to be handled
    :return: str
        The response to the user input
    """
    updater = Updater("1759313825:AAGevPY6RL6oqWyOkAZpQJF1B1iBzTn4VG4", use_context=True)
    user_message = str(input_text).lower()  

    #Verifying if the user message is a greeting
    if user_message  in greetings["chat"]: 
        return random.choice(greetings["responses"])   

    #Veryfying if the user input is a goodbye phrase
    if user_message  in goodbye["chat"]: 
        return random.choice(goodbye["responses"]) 

    #Veryfying if the user input is a thanking phrase
    if user_message in thanks["chat"]: 
        return random.choice(thanks["responses"])

    #Veryfying if the user input is a time question
    if  user_message in ("time?", "time","what is the time?","what is the time"): 
        now = datetime.now()
        date_time = now.strftime("The time is: %d/%m/%y, %H:%M:%S") 
    
        return(str(date_time))  

    #Veryfying if the user input is a joke request
    if user_message in jokes["chat"]: 
        return random.choice(jokes["responses"])

    #Veryfying if the user input is a weather question
    if "weather in" in user_message:
        index = user_message.find(" in ")
        city = user_message[index+4:]
        url = "https://google.com/search?q=weather+in+" + city
        request_result = requests.get( url )
        soup = bs4.BeautifulSoup( request_result.text, "html.parser" )
        temp = soup.find( "div" , class_='BNeawe' ).text
        return temp+" in "+city
    
    #Veryfying if the user input is a analysis request
    if "analyze " in user_message:
        index = user_message.find("analyze ")
        search_word = user_message[index+8:]
        result = alghoritm.start_process(search_word)
        return result

    return "Sorry, could not find an answer for your request"