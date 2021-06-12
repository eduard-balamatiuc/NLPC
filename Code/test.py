'''
Created with love by Paza Anulare
'''

#Importing all libraries

from pytrends.request import TrendReq
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd 
import requests, json   
import datetime 
from datetime import date
import time
import geopandas as gpd
import pycountry
from mpl_toolkits.axes_grid1 import make_axes_locatable

def trading(word_input: str):
    """
        The trading function analyzes the popularity through out the years and creates a plot and a map vizualization of the popularity data
    :param word_input: str
        The input product to find data about

    """
    def clear_dict(_dict: dict):
        """
            The clear_dict function clears the input dict
        :param _dict: dict
            The input_text that needs to be analyzed
        :return: dict
            The cleared dict

        """
        c = 0
        for value in _dict.values(): 
            if value == 0:
                c = c+1
                    
        while(c):
            _dict.popitem()
            c = c - 1

    #Setting the time and date
    year = datetime.date.today().year  
    today = date.today()

    #Setting up the characteristics
    totalTrend = TrendReq(hl='en-US', tz=360) 
    kw_list = [word_input]
    _cat = 0
    _geo = ''
    _gprop = ''   
    _resolution = 'COUNTRY'  
    _inc_low_vol = False       
    _inc_geo_code = False 
    backoff_factor = 0.4   
    final_dict = dict()
        
    _history_all = pd.DataFrame()
    #Going through the information from different years
    for i in range (0,5):
        if i == 0: 
            _timeframe = f'{year}-01-01 {today.year}-{today.month}-{today.day}' 
        else:
            _timeframe  = f'{year - i}-01-01 {year - i}-12-12'  
                 
        totalTrend.build_payload(kw_list, cat=_cat, timeframe=_timeframe, geo=_geo, gprop=_gprop) 
    # Getting the interest over time
    # Capture Monthly Data for use in Normalization against Weekly
        _history = totalTrend.interest_over_time()  #pandas df
    # Plot the Interest 
        text = 'Numbers represent search interest relative to the highest point on the chart for the given region and time.\n A value of 100 is the peak popularity for the term. A value of 50 means that the term is half as popular.\n A score of 0 means there was not enough data for this term.'
        _history.plot(title=text,  figsize=(30,20))
        _history_all = pd.concat([_history_all, _history])
    # returning a dataframe with the rating of searches 
        _region= totalTrend.interest_by_region(resolution=_resolution, inc_low_vol= _inc_low_vol, inc_geo_code=_inc_geo_code)   
        _region = _region.sort_values(by=word_input).iloc[::-1] 
        _region_dict = _region[word_input].to_dict() 
        clear_dict(_region_dict) 
        final_dict.update({year-i:_region_dict})

    _history_all = _history_all.sort_values('date', ascending = False)
    current = _history_all.iloc[0].name
    old = current - datetime.timedelta(days = 366)
    _history_all.to_csv('history_trends.csv')
    _history_all = pd.read_csv('history_trends.csv')
    old_str = old.strftime('%Y-%m-%d')
    last_year = _history_all[_history_all['date'] >= old_str]
    last_year = last_year.set_index('date')
    last_year.plot(title = text, figsize = (15, 10))
    plt.savefig(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\plot.png')

    _countries = _region.drop(_region.columns[0], axis = 1)
    df_final_dict = pd.DataFrame(final_dict)
    df_final_dict.index.name = 'geoName'
    df_final_dict
    _countries = _countries.merge(df_final_dict, on = 'geoName', how = 'outer')
    _countries = _countries.fillna(0)
    _region = _countries
    #_region


    _region = _region.sort_values('geoName', ascending = True)

    _region.to_csv('data.csv')

    shapefile = r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\110m_cultural\ne_110m_admin_0_countries.shp'

    #Reading the shapefile using Geopandas
    gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

    #Renaming the columns
    gdf.columns = ['country', 'country_code', 'geometry']
    gdf = gdf.drop(gdf.index[159])

    #Reading csv file using pandas
    datafile = 'data.csv'
    df = pd.read_csv(datafile)

    df = df.drop(df.index[40])
    df = df.drop(df.index[116])

    #Adding the country code to the dataframe
    input_countries = list(df['geoName'])

    input_countries[8] = 'Antigua and Barbuda'
    input_countries[25] = 'Bolivia, Plurinational State of'
    input_countries[26] = 'Bosnia and Herzegovina'
    input_countries[31] = 'Virgin Islands, British'
    input_countries[32] = 'Brunei Darussalam'
    input_countries[39] = 'Cabo Verde'
    input_countries[49] = 'Congo'
    input_countries[50] = 'Congo, The Democratic Republic of the'
    input_countries[58] = "Côte d'Ivoire"
    input_countries[71] = "Falkland Islands (Malvinas)"
    input_countries[96] = "Heard Island and McDonald Islands"
    input_countries[103] = "Iran, Islamic Republic of"
    input_countries[118] = "Lao People's Democratic Republic"
    input_countries[140] = "Micronesia, Federated States of"
    input_countries[141] = "Moldova, Republic of"
    input_countries[148] = "Myanmar"
    input_countries[160] = "Korea, Democratic People's Republic of"
    input_countries[167] = "Palestine, State of"
    input_countries[173] = "Pitcairn"
    input_countries[179] = "Russian Federation"
    input_countries[190] = "Sint Maarten (Dutch part)"
    input_countries[196] = "South Georgia and the South Sandwich Islands"
    input_countries[197] = "Korea, Republic of"
    input_countries[201] = "Saint Barthélemy"
    input_countries[202] = "Saint Helena, Ascension and Tristan da Cunha"
    input_countries[203] = "Saint Kitts and Nevis"
    input_countries[204] = "Saint Lucia"
    input_countries[205] = "Saint Martin (French part)"
    input_countries[206] = "Saint Pierre and Miquelon"
    input_countries[207] = "Saint Vincent and the Grenadines"
    input_countries[213] = "Syrian Arab Republic"
    input_countries[214] = "Sao Tome and Principe"
    input_countries[215] = "Taiwan, Province of China"
    input_countries[217] = "Tanzania, United Republic of"
    input_countries[223] = "Trinidad and Tobago"
    input_countries[210] = "Svalbard and Jan Mayen"
    input_countries[227] = "Turks and Caicos Islands"
    input_countries[229] = "United States Minor Outlying Islands"
    input_countries[230] = "Virgin Islands, U.S."
    input_countries[239] = "Holy See (Vatican City State)"
    input_countries[240] = "Venezuela, Bolivarian Republic of"
    input_countries[241] = "Viet Nam"
    input_countries[242] = "Wallis and Futuna"

    #Setting the values for each country 
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2
    codes = [countries.get(country, 'Unknown code') for country in input_countries]
    #print(codes)

    #Add country_code to df
    df['country_code'] = codes

    #Copy columns name
    search_item = df.columns
    search_item = search_item[1:-1]

    #Reshape data using melt()
    df = df.melt(id_vars = ['geoName', 'country_code'],
                var_name = ['search_item'],
                value_name = 'search_interest')

    #df.head()

    gdf = gdf.sort_values('country', ascending = True)

    #Creating the input countries list
    input_countries = list(gdf['country'])

    input_countries[15] = 'Bolivia, Plurinational State of'
    input_countries[19] = 'Brunei Darussalam'
    input_countries[36] = 'Congo, The Democratic Republic of the'
    input_countries[40] = 'Timor-Leste'
    input_countries[48] = 'Falkland Islands (Malvinas)'
    input_countries[52] = 'French Southern Territories'
    input_countries[70] = 'Iran, Islamic Republic of'
    input_countries[75] = "Côte d'Ivoire"
    input_countries[84] = "Lao People's Democratic Republic"
    input_countries[92] = 'North Macedonia'
    input_countries[99] = 'Moldova, Republic of'
    input_countries[113] = "Korea, Democratic People's Republic of"
    input_countries[114] = 'Cyprus'
    input_countries[118] = 'Palestine, State of'
    input_countries[128] = 'Serbia'
    input_countries[129] = 'Congo'
    input_countries[131] = 'Russian Federation'
    input_countries[140] = 'Somalia'
    input_countries[142] = 'Korea, Republic of'
    input_countries[150] = 'Syrian Arab Republic'
    input_countries[151] = 'Taiwan, Province of China'
    input_countries[154] = 'Bahamas'
    input_countries[164] = 'Tanzania, United Republic of'
    input_countries[165] = 'United States'
    input_countries[169] = 'Venezuela, Bolivarian Republic of'
    input_countries[170] = 'Viet Nam'
    input_countries[175] = 'Eswatini'

    #Setting the values for each country 
    countries = {}
    for country in pycountry.countries:
        countries[country.name] = country.alpha_2
    codes = [countries.get(country, 'Unknown code') for country in input_countries]
    codes[81] = 'XK'
    gdf['country_code'] = codes

    #Creating a static choropletj map 
    df_map = df[df['search_item'] == search_item[0]]

    #Merge dataframes gdf and df_map
    merged = gdf.merge(df_map, left_on = 'country_code', 
                                right_on = 'country_code', how = 'left')

    #Setting the sizes and dimensions of the text from the trending map
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(20, 15)
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    merged.plot(column = 'search_interest', cmap = 'OrRd', legend = True, ax = ax, cax = cax) 

    #Setting the title
    ax.set_title('World relative search interest of %s in 2021' %word_input, fontdict = {'fontsize':40})
    ax.set_axis_off()
    #Saving the png file to the folder
    plt.savefig(r'F:\Eduard\Autodezvoltare\NLP camp\final version\NLPC-main\bot\Code\trend_map.png')