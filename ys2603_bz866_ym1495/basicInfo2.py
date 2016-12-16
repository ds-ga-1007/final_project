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
    plt.show()
    plt.close()
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
    plt.show()
    plt.close()
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
    labels = 'night', 'morning', 'afternoon','evening'
    pie(time_freq_count, labels =labels ,autopct='%1.1f%%')
    plt.title("Percentage of pokemon's daily appearances' periods")
    #save figure as png
    plt.savefig('pie chart of pokemon ' + str(ID_input) + ' showing up periods')
    plt.show()
    plt.close()
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
    freq_list = np.array(freq_list)
    for i in range(1,6):
        item_index = np.where(freq_list==maxfive[-i])
        result.append(int(item_index[0]))
    return result

def temp_windspeed_relation(dataframe, city_input):
    '''
    input:
        city name(str)
    return:
        The scatterplot of relationship between temperature and windspeed of the given city'''
    data = dataframe.loc[dataframe['city'] == city_input]
    feature_1 = np.array(data['temperature'])
    feature_2 = np.array(data['windSpeed'])
    plt.figure(figsize = (10,8))
    plt.scatter(x = feature_1, y = feature_2)
    plt.xlabel('Temperature')
    plt.ylabel('Windspeed')
    plt.title('Relationship between temperature and windspeed of ' + str(city_input))
    plt.savefig('Relationship between temperature and windspeed of ' + str(city_input), dpi = 300)
    plt.show()
    plt.close()
    return print('The image of relationship between temperature and windspeed is saved as'
                 + 'Relationship between temperature and windspeed of ' + str(city_input))


# --- Build Map ---
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
def worldmap(dataframe):
    lats = np.array(data_origin['latitude'])
    lons = np.array(data_origin['longitude'])                                        

    eq_map = Basemap(projection='robin', resolution = 'l', area_thresh = 1000.0,
                  lat_0=0, lon_0=-130)
    eq_map.drawcoastlines()
    eq_map.drawcountries()
    eq_map.fillcontinents(color = 'gray')
    eq_map.drawmapboundary()
    eq_map.drawmeridians(np.arange(0, 360, 30))
    eq_map.drawparallels(np.arange(-90, 90, 30))

    x,y = eq_map(lons, lats)
    eq_map.plot(x, y, 'ro', markersize=6)

    plt.show()
    plt.close()
    return print('')
