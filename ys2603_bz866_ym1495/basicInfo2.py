import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import *
from collections import Counter
import collections


'''
More information about pokemons in certain places
'''

def listPokemonIdsAppeared(dataframe):
    '''return a numpy array of pokemon ID number'''
    pokemonIdList = dataframe['pokemonId'].unique()
    return pokemonIdList

def getCityNames(dataframe):
    '''return a numpy array of cities'''
    cityList = dataframe['city'].unique()
    return cityList

def getContinentNames(dataframe):
    '''return a numpy array of continents'''
    continentList = dataframe['continent'].unique()
    return continentList

def pokemonwideDataframe(dataframe, pokemonId):
    '''return a dataframe of user-requested pokemon's records'''
    pokemonRecords = dataframe.loc[dataframe['pokemonId']==pokemonId]
    return pokemonRecords

def citywideDataframe(dataframe, cityName):
    '''return a dataframe of certain city's, user-requested pokemon's records '''
    citywideRecords = dataframe.loc[dataframe['city'] == cityName]
    return citywideRecords

def hasItAppearedGlobally(dataframe, pokemonId):
    '''return a boolean variable that tells the user if the requested pokemon has ever
    appeared globally'''
    return pokemonId in dataframe['pokemonId'].unique()

def city_ID_freq(dataframe, city_input):
    ''''
    input:
        city name(str)
    return:
        top ten frequencies of pokemons that appeared in the given city(Series), with pokemonId as index
    '''
    data = citywideDataframe(dataframe, city_input)
    ID_freq_count = data['pokemonId'].value_counts()
    ID_freq_count_upten = ID_freq_count[0:10]
    x_label_upten = np.array(ID_freq_count.index[0:10])

    x = np.arange(len(ID_freq_count_upten))
    plt.bar(x, ID_freq_count_upten)
    plt.xticks(x, x_label_upten, rotation=45)
    plt.ylabel('Frequency')
    plt.title('Frequencies of pokemons appear in ' + str(city_input))
    plt.savefig('Frequencies of pokemons appear in ' + str(city_input), dpi=300)
    return ID_freq_count_upten

def ID_city_freq(dataframe, ID_input):
    ''''
    input:
        pokemon ID(int)
    return:
        top ten frequencies of the given pokemons' appearances in different cities(Series), with city name as index
    '''
    data = pokemonwideDataframe(dataframe, ID_input)
    city_freq_count = data['city'].value_counts()
    city_freq_count_upten = city_freq_count[0:10]
    x_lable_upten = np.array(city_freq_count.index[0:10])

    x = np.arange(len(city_freq_count_upten))
    plt.bar(x, city_freq_count_upten)
    plt.xticks(x, x_lable_upten, rotation=45)
    plt.ylabel('Frequency')
    plt.title('Frequncy of pokemon ' + str(ID_input) + ' appears in different cities')
    plt.savefig('Frequency of pokemon ' + str(ID_input) + 'appears in different cities', dpi=300)
    return city_freq_count_upten

def appeared_incity(dataframe, ID_input, city_input):
    '''
    input:
        pokemonID(int) and city_name(str)
    return:
        **print** if the pokemon appeared in this city
    '''
    data = pokemonwideDataframe(dataframe, ID_input)
    city_freq_count = data['city'].value_counts()
    if str(city_input) in city_freq_count.index:
        return (print('Pokemon ' + str(ID_input) + ' has appeared in ' + str(city_input)+ ' before'))
    else:
        return (print('Pokemon ' + str(ID_input) + ' has not appeared in ' + str(city_input)+ ' before'))

def appeared_time(dataframe, ID_input):
    '''
    input:
        pokemonID(int)
    return:
        pie chart of this pokemon's appearance in different time priod
        '''
    data = pokemonwideDataframe(dataframe,ID_input)
    time_array = np.array(data['appearedTimeOfDay'])
    time_df = pd.DataFrame({'time':time_array})
    time_freq_count = time_df['time'].value_counts()
    #pie chart
    labels = 'night', 'morning', 'afternoon'
    pie(time_freq_count, labels =labels ,autopct='%1.1f%%')
    plt.title("Percentage of pokemon's daily appearances' periods")
    #save figure as png
    plt.savefig('pie chart of pokemon ' + str(ID_input) + ' showing up periods')
    return time_freq_count

def co_occurance (dataframe, ID_input):
    '''
    input:
        pokemonID(int)
    return:
        top five pokemons that co-occur with the user-requested pokemon' ID(list)
    '''
    data = pokemonwideDataframe(dataframe, ID_input)
    freq_list = []
    result = []
    for i in range(1,152):
        col_name = str('cooc_'+str(i))
        freq = sum(data[col_name])
        freq_list.append(freq)
    maxfive = sort(freq_list)[-5:]
    for i in range(1,6):
        a = freq_list.index(maxfive[-i])
        result.append(a)
    return result

