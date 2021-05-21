# NLPC
Natural Language Processing Camp



This GitHub repository contains all the "Paza Anulare" team's work throughout the Natural Language Processing Camp.

This project represents a telegram bot that uses Natural Language Processing to analyze the customers' review of a product using tweets from the online platform Tweeter. This bot takes a product's name as an input and gives general feedback on the product based on customers' opinion from Twitter(and soon Facebook).

In the Code file, you will find all the files necessary for the working bot. There are three important files in this project:

1)main.py;

2)Responses.py;

3)alghoritm.py;

The general purpose of the files:

In the main.py file, you will find the code that focuses on the telegram bot system. Here are the principal functions of the code which powers up all this system.

In the Responses.py file, you will find the functions that concentrate on the usual talking part with the customer, here we talk about asking about the weather in a certain place or maybe telling a joke to the user.

In the alghoritm.py file, you will find the code that focuses on the Sentiment Analysis Part of the process; here, the function start_process takes as an input the productțs name to analyze and gives as an output a dictionary with all the comments passed through the Sentiment Analysis process and saves a result.csv file at the indicated location.

Starting the code:

Code changes needed:

To start all the process works, you need to compile the main.py file, but you need to change the file path from the code before doing that. It's not a big deal; to do this, you first need to copy the folder path of your project (for those who don't know what this mean, this represents the location of your files, for example: "D:\user\development\NLP camp\final version"), then access the alghoritm.py file and paste the path on line: 116; 118; 134; 174; 212

As an example:

Let's suppose that your file path is: "D:\user\development\final version"

In this case, on line 116, that looks like this after downloading:

rf = joblib.load(*r*'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\World Map Visualization\SA_module.joblib')

The changed line should look like this:

rf = joblib.load(*r*'D:\user\development\final version\SA_module.joblib').

Needed Libraries:

Afterwards, please make sure that you have all the needed libraries to compile the code. This is a list of all the libraries used in our project and the installation command for them (for those of you who don't know, if you have already installed python on your computer, then open Command Prompt and type the commands after the vertical bar to install the libraries):

1. nltk | pip install nltk
2. telegram.ext | pip install python-telegram-bot
3. pandas | pip install pandas
4. datetime | pip install DateTime
5. requests | pip install requests
6. bs4 | pip install bs4
7. scikit-learn | pip install scikit-learn
8. NumPy | pip install numpy
9. Matplotlib | pip install matplotlib
10. Seaborn | pip install seaborn
11. joblib | pip install joblib
12. twint | pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint
13. geopandas | pip install geopandas
14. pyconutry | pip install pycountry
15. pytrends | pip install pytrends

You are ready to compile the code, so please feel free to run the main.py file. To interact with the telegram bot and to get the results from it, you will probably need the link to the telegram chatbot, so here it is:

[http://t.me/PazaAnulare_NLP_Project_bot](http://t.me/PazaAnulare_NLP_Project_bot)

After compiling the code, to start the process, we recommend you use the function "/start" to start the chatbot interaction, but here are all the chatbot possibilities that we would like you to try:

- The possiblities of the chatbot

    To analyze a particular product, type "/help", afterwards the bot will send you a text message with some buttons below it. Press the analyze button for starting the process. After that, you would get a new message that asks for input from you, and now you have to type in the name of your product. Consequently, you will get short statistics about your product, which includes: the number of comments, the number of positive comments; the number of negative comments; the positive per cent of the comments.

    Important: Keep in mind that the analysis process may take a few seconds, so don't worry about it. Usually, it takes about 15 seconds to process your input.

    We are creating more user-friendly output data for you, such as graphs and diagrams, so sooner enough, we will add new features to the code, so keep in mind to constantly check our repository for the latest updates.

    Normal interaction part:

    Our bot is also capable of everyday interaction such as finding the weather in different cities or telling jokes:

    Alternatives command: type "alternatives for **the product**" to find alternatives for a specific product as Coke.

    Joke telling command: "tell me a joke" / "tell me something funny" / "do you know a joke?"

    Weather command: "weather in **the city in which you want to find the weather*.*"

    Basic greetings: "hi" / "hey" / "hello" / "good day" / "good afternoon" / "good morning"

    Basic goodbyes: "bye" / "see you later" / "goodbye" / "see ya" / "good luck"

    Essential thanks answering: "thanks" / "thank you" / "thanks a lot!"

    Overall, these are all the possibilities of our telegram bot, but we are looking forward to developing new features.

Also, we have a beta version for our telegram chatbot, which gives as an output a graph and an earth diagram for the popularity of a particular product.

To try out this function, you shall open the [test.py](http://test.py/) file from our repository and compile it. If you have all the libraries mentioned above installed then you should run the code without any problems (Hint: don't forget to write the input in the terminal)

Here are some examples of the results for the word input "bitcoin":
