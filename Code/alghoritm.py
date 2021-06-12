'''
Created with love by Paza Anulare
'''

#Importing all libraries
from sklearn.feature_extraction.text import CountVectorizer
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import string
import nltk
import warnings
import twint
from datetime import date
import joblib
import json
import test
import requests
import bs4
from nltk import PorterStemmer


def start_process(input_text : str):
    """
        The start_process function combines these functions: twitter_sentiment_analyze, twiti, transform, Top_Comments, plot_pie.
    :param input_text: str
        The input_text that needs to be analyzed
    :return: dict
        The string with general data about the product

    """
    def twitter_sentiment_analyze(test):
        """
            The twitter_sentiment_analyze function tokenizes the input tweets
        :param test:pd.DataFrame
            The DataFrame with tweets
        :return:pd.DataFrame
            The DataFrame with the tweets gone through tokenization
        """
        global bow

        warnings.filterwarnings("ignore", category=DeprecationWarning)

        def remove_pattern(text : str, pattern : str):
            """
                The remove_pattern function removes the pattern from the text
            :param text: str
                The string to be modified
            :param pattern: str
                The string to be removed
            :return: str
                The modified string
            """
            # re.findall() finds the pattern i.e @user and puts it in a list for further task
            r = re.findall(pattern,text)

            # re.sub() removes @user from the sentences in the dataset
            for i in r:
                text = re.sub(i,"",text)

            return text

        #removing @user and other unnecessary characters from the tweets
        test['Tidy_Tweets'] = np.vectorize(remove_pattern)(test['tweet'], "@[\w]*")

        test['Tidy_Tweets'] = test['Tidy_Tweets'].str.replace("[^a-zA-Z#]", " ")

        test['Tidy_Tweets'] = test['Tidy_Tweets'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

        #creating the tokenized tweets using PorterStemmer
        tokenized_tweet = test['Tidy_Tweets'].apply(lambda x: x.split())

        ps = PorterStemmer()

        tokenized_tweet = tokenized_tweet.apply(lambda x: [ps.stem(i) for i in x])

        for i in range(len(tokenized_tweet)):
            tokenized_tweet[i] = ' '.join(tokenized_tweet[i])

        #assigning the tokenized tweets to the Tidy_Tweets column
        test['Tidy_Tweets'] = tokenized_tweet

        return test['Tidy_Tweets']

    def twiti(input_text : str):
        """
            The twiti function creates a dataframe with tweets about the input_text
        :param input_text: str
            The product-subject of the tweets
        :return: pd.DataFrame
            The DataFrame that contains tweets about the input_text
        """
        c = twint.Config()
        wanted_item = input_text
        #setting the defining limits of the tweets
        c.Limit = 500                  
        c.Links = "exclude"
        c.Lang = "en" 
        c.Min_likes = 2
        c.Min_retweets = 2
        c.Min_replies  = 2
        c.Pandas = True

        c.Search = wanted_item
        # Run
        c.Hide_output = True
        twint.run.Search(c)

        #creating a dataframe with the tweets
        df = twint.storage.panda.Tweets_df  
        
        #transfroming the values to list
        tweets_list = df['tweet'].to_list()
        lang_list = df['language'].to_list()
        likes_list = df['nlikes'].to_list()

        #creating the dataframe with id and tweet column
        postari = {}
        postari['id'] = []
        postari['tweet'] = []
        nr = 0

        #assigning the data to the postari dataframe
        for i in range(0,len(tweets_list)):
            if 'en' in lang_list[i]:
                postari['id'].append(nr)
                nr += 1
                postari['tweet'].append(tweets_list[i])

        df = pd.DataFrame(postari)
        df = df.set_index('id')

        return df


    #Reading the product input from the user
    input_user = input_text
    print(input_user)
    #finding results on twitter for the product input
    submission = twiti(input_user)


    #Reading the Sentiment Analysis module, memorized in the joblib file
    rf = joblib.load(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\SA_module.joblib')
    #Reading the Count Vectorizer module, memorized in the joblib file
    bow = joblib.load(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\bow.joblib')

    #pre-processing the twitter dataframe
    space = bow.transform(twitter_sentiment_analyze(submission))

    #predicting the results using the random forest sentiment analysis module
    test_pred = rf.predict_proba(space)

    #here we attribute to the value of test_pred_int the first column with float values of the test_pred
    test_pred_int = test_pred[:,1]


    submission['label'] = test_pred_int
    submission1 = submission
    dataframe = submission1
    #here we ttribute the gender file input to the name variable
    names = pd.read_csv(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\gender_refine-csv.csv')
    names.dropna(inplace = True)
    names = names[0 : 17198]
    dataframe['name'] = names['name']
    dataframe['name']

    vectorizer = CountVectorizer(analyzer='char')

    def transform(text : str):
        """
            The transform function defines the gender type of the user
        :param text: str
            The name of the user
        :return: str
            The gender of the user
        """
        s = ''.join(i.lower() for i in text if i.isalpha())
        x = [0 for _ in range(32)]
        X = vectorizer.fit_transform([s]).toarray()
        x[26] = ord(s[0])-97
        x[27] = ord(s[-1])-97
        x[28] = len(s)
        if s[-1] in ('a','e','i','o','u'):
            x[29] = 1
        for i in s:
            if i in ('a','e','i','o','u'):
                x[30] += 1
        x[31] = x[28] - x[30]
        count = 0
        for i in vectorizer.get_feature_names():
            x[ord(i)-97] += X[0][count]
            count += 1
        return x

    def Top_Comments(Dataframe : "pd.DataFrame", label: str = 'label' , tweet: str = 'tweet'):
        """
            The Top_Comments function creates a dict that contains statistics about the Top Comments
        :param Dataframe: pd.DataFrame
            The DataFrame to be analyzed
        :param label: str
            The name of the label in the DataFrame
        :param tweet: str
            The name of the column with tweets in DataFrame
        :return: dict
            The dict that contains the statistics about the Top Comments
        """    
        dataframe.sort_values(by=[label],inplace = True)
        positive = list(dataframe.head(n = 3)[tweet])
        negative = list(dataframe.tail(n = 3)[tweet])
        top = {'Top pozitive comments':positive, 'Top negative comments':negative}
        cls = joblib.load(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\cls.joblib')
        gender = []
        #Using the trained model it predicts the positivity of the comments
        for i in Dataframe['name']:
            gender.append(transform(i))
        dataframe['gender'] = cls.predict(gender).astype(np.int)
        for i in dataframe['gender'] :
            i = bool(i)

        dataframe.loc[dataframe.label > 0.6, 'label'] = 1
        dataframe.loc[dataframe.label <= 0.6, 'label'] = 0
        #Creates the dictionary elements with the statistics information
        top['Number of comments'] = len(dataframe)
        top['Number of positive comments'] = len(dataframe[dataframe['label'] == 0])
        top['Number of negative comments'] = len(dataframe[dataframe['label'] == 1])
        top['Positive percent of the comments'] = round((top['Number of positive comments']/len(dataframe['label']))*100, 2)
        top['Negative percent of the comments'] = (top['Number of negative comments']/len(dataframe['label']))*100

        top["Number of men's comments"] = len(dataframe[dataframe['gender'] == 1])
        top["Number of men's positive comments"] = len(dataframe[(dataframe['gender'] == 1) & (dataframe['label'] == 0)])
        top["Number of men's negative comments"] = len(dataframe[(dataframe['gender'] == 1) & (dataframe['label'] == 1)])
        top["Men's comments percentage"] = (top["Number of men's comments"] / len(dataframe['label']))*100
        top["Percentage of men's positive comments"] =( top["Number of men's positive comments"] / top["Number of men's comments"])*100
        top["Percentage of men's negative comments"] = (1 - (top["Percentage of men's positive comments"]/100))*100

        top["Number of women's comments"] = len(dataframe[dataframe['gender'] == 0])
        top["Number of women's positive comments"] = len(dataframe[(dataframe['gender'] == 0) & (dataframe['label'] == 0)])
        top["Number of women's negative comments"] = len(dataframe[(dataframe['gender'] == 0) & (dataframe['label'] == 1)])
        top["Women's comments percentage"] = (top["Number of women's comments"] / len(dataframe['label']))*100
        top["Percentage of women's positive comments"] = (top["Number of women's positive comments"] / top["Number of women's comments"])*100
        top["Percentage of women's negative comments"] = (1 - (top["Percentage of women's positive comments"]/100))*100

        return top

    resum = Top_Comments(dataframe)

    def plot_pie(resum : dict):
        """
            plot_pie function creates in the same folder 4 images with plots about general data
        :param resum: dict
            The dict with data to be used for creating the plots
        """    

        #Creating a png named Nr_men_comments.pn that contains a plot with the number of positive and negative men's comments
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        langs = ["Number of men's positive comments", "Number of men's negative comments"]
        data = [resum["Number of men's positive comments"], resum["Number of men's negative comments"]]
        ax.set_title("Men's total comments",fontsize = 25)
        ax.pie(data, labels = langs, autopct = '%1.2f%%', textprops={'fontsize': 20})
        plt.savefig(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_men_comments.png', bbox_inches='tight')

        #Creating a png named Nr_comments.png which contains a plot with the number of positive and negative comments
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        langs = ['Number of positive comments', 'Number of negative comments']
        data = [resum['Number of positive comments'], resum['Number of negative comments']]
        ax.set_title('Number of total comments', fontsize = 25)
        ax.pie(data, labels = langs, autopct = '%1.2f%%', textprops={'fontsize': 20})
        plt.savefig(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_comments.png',bbox_inches='tight')

        #Creating a png named Nr_gender_comments.png which contains a plot with the gender of the users who wrote the comments
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        langs = ["Number of men's comments", "Number of women's comments"]
        data = [resum["Number of men's comments"], resum["Number of women's comments"]]
        ax.set_title('Number of total comments', fontsize = 25)
        ax.pie(data, labels = langs, autopct = '%1.2f%%', textprops={'fontsize': 20})
        plt.savefig(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_gender_comments.png',bbox_inches='tight')

        #Creating a png named Nr_woman_comments.png which contains a plot with the number of positive and negative women's comments
        fig = plt.figure()
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('equal')
        langs = ["Number of women's positive comments", "Number of women's negative comments"]
        data = [resum["Number of women's positive comments"], resum["Number of women's negative comments"]]
        ax.set_title("Women's total comments", fontsize = 25)
        ax.pie(data, labels = langs, autopct = '%1.2f%%',textprops={'fontsize': 20})
        plt.savefig(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\Nr_woman_comments.png',bbox_inches='tight')


    #using plot_pie function to create the plot figure about the Top Comments statistics
    plot_pie(resum)

    #Assigning integer values to the prediction results
    test_pred_int[test_pred_int > 0.6] = 1
    test_pred_int[test_pred_int <= 0.6] = 0

    #Returning the result.csv with the 1/0 values
    submission['label'] = test_pred_int
    submission.to_csv(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\result.csv', index=False)
    test.trading(input_text)

    #Creating a top 3 tweets txt 
    top3_final_values = ''
    top3_values = {key: resum[key] for key in resum.keys() & {'Top pozitive comments', 'Top negative comments'}}
    json.dump(top3_values, open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\top3.txt", "w", encoding='utf8'))

    #Creating a string that contains just the number of comments; Number of positive comments; Number of negative commnets; Positivity percent of the comments
    dictionar = 'Acestea sunt datele generale despre '+input_text+' \n\n'
    intermediate = {key: resum[key] for key in resum.keys() & {'Number of comments', 'Number of positive comments', 'Number of negative comments', 'Positive percent of the comments'}}
    for key, value in intermediate.items():
        dictionar+=str(key) + ' : ' + str(value) + '\n'


    #takes the word as input
    search_word = input_text
    url = f'https://www.google.com/search?q={search_word}&hl=en'

    # Fetch the URL data using requests.get(url),
    # store it in a variable, request_result.
    request_result=requests.get( url )

    # Creating soup from the fetched request
    soup = bs4.BeautifulSoup(request_result.text, "html.parser")

    # Get the whole body tag
    tag = soup.body
    collected_strings = []

    #Filteres the information
    for string in tag.strings:
        collected_strings.append(string)

    _defenition = "Sorry, we could not find any definition for you."

    #Verifies if there is a wikipedia definition on google
    if ('Wikipedia') in collected_strings:
        alt_index = collected_strings.index('Wikipedia')
        _defenition = collected_strings[alt_index-1]

    #Saves the definition in a txt file
    string_text = _defenition
    text_file = open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\definition.txt", "wt")
    text_file.write(string_text)
    text_file.close()

    #Verifies if there are alterantives for the product on the internet
    alternatives = ''    
    if ('People also search for') in collected_strings:
        alt_index = collected_strings.index('People also search for')
        alternatives = collected_strings[alt_index+1:alt_index+7]
        if ("People also ask") in collected_strings:
            string_text = ';\n '.join(collected_strings[collected_strings.index("People also ask"):collected_strings.index("People also ask")+5])
            string_text = 'Alternatives:\n ' +';\n '.join(collected_strings[alt_index+1:alt_index+7]) + '\n\n' + string_text
    else:
        alternatives = "Sorry, we could not find any alternatives for you."
        string_text =  alternatives 

    #if there are alternatives on the internet saves the results in a txt
    text_file = open(r"F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\alternatives.txt", "wt")
    text_file.write(string_text)
    text_file.close()

    return dictionar