'''
Created on Dec 15, 2016

@author: muriel820
'''
import pandas as pd
import numpy as np
import sys

from loadData import *
from userInput import *
from basicInfo import *
from basicInfo2 import *
def main():
    Data = loadData('pokemonGo.csv', 'cleanedData.csv')
    userChoice = UserChoice()
    pokemonList = Data.nameList
    cityList = Data.cityList
    basicData = Data.basicData
    largeData = Data.largeData
    while True:
        '''
        The first level input tells the program to start or quit
            '''
        main_input = input('\nPlease enter \'pokemon\' to start main program.\n'
                            'Please enter \'quit\' at anytime to quit the program.'
                           '\n>  ')
        if main_input.lower() in ['q','quit','bye']:
            break
        elif main_input.lower() in ['pokemon']:
            '''
            To start with, select a pokemon of your choice. And print basic statistics about this pokemon
            '''
            pokemon_selection = userChoice.select_pokemon(pokemonList)
            if pokemon_selection =='Wish you luck in pokemon world. Goodbye':
                return (print('\n till Next Time! Goodbye.'))
            else:
                basic_info = pokemonStats(basicData, pokemon_selection)
                print('\n You have selected No.%d %s. Its a %s and %s type pokemon.'
                    'Its Combat Power is %d and its Health Power is %d.'%(pokemon_selection, pokemonList[pokemon_selection],basic_info.pokemonType1,basic_info.pokemonType2,basic_info.pokemonMaxCP,basic_info.pokemonMaxHP))
                while True:
                    '''
                    The second menu asks user to select basic info or pokemon go info
                    '''
                    secondary_input = input('\nYou have selected No.%d %s.'
                                            '\nWhat do you want to know about it?'
                                            '\nPlease enter \'basic info\' for basic info,'
                                            '\nPlease enter \'go\' for pokemon go info,'
                                            '\nPlease enter \'back\' back to previous menu.'
                                            '\n>  '%(pokemon_selection, pokemonList[pokemon_selection]))
                    if secondary_input.lower() in ['q','quit','bye']:
                        return (print('\n till Next Time! Goodbye.'))
                    elif secondary_input.lower() in ['back']:
                        break
                    elif secondary_input.lower() in ['basic info','basicinfo','basic information','information']:                    
                        while True:
                            '''
                            The Basic Info menu asks user to select basic info function
                            '''
                            third_input = input('\nYou have selected basic info about %s'
                                            '\nPlease select a function we have here'
                                            '\nA. Show its overall CP ranking/percentile/mean' 
                                            '\nB. Show its overall HP ranking/percentile/mean'
                                            '\nC. Show the same type Pokemons with it'
                                            '\nD. Show its CP ranking/percentile/mean among the same type pokemons'
                                            '\nE. Show its HP ranking/percentile/mean among the same type pokemons'
                                            '\nType \'back\' back to previous menu'
                                            '\nType \'quit\' to quit the program'
                                            '\n>  '%(pokemonList[pokemon_selection]))
                            if third_input.lower() in ['q','quit','bye']:
                                return (print('\n till Next Time! Goodbye.'))
                            elif third_input.lower() in ['back']:
                                break
                            elif third_input.lower() in ['a','a.','1']:
                                print('\n CP of %s is %d. It ranks %d among all pokemons. Overall the mean CP is %d'%(pokemonList[pokemon_selection],basic_info.pokemonMaxCP,basic_info.overallRanking()[0],basic_info.meanPower(basicData,'cp') ))
                                continue
                            elif third_input.lower() in ['b','b.','2']:
                                print('\n HP of %s is %d. It ranks %d among all pokemons. Overall the mean HP is %d'%(pokemonList[pokemon_selection],basic_info.pokemonMaxHP,basic_info.overallRanking()[1],basic_info.meanPower(basicData,'hp') ))
                                continue
                            elif third_input.lower() in ['c','c.','3']:
                                print('\n %s is a type %s pokemon. There are %d pokemons who are also type %s.'
                                      '\n They are %s'%(pokemonList[pokemon_selection],basic_info.pokemonType1,basic_info.countSameTypePokemons()[0],basic_info.pokemonType1, basic_info.listSameTypePokemons()[0].to_string()))
                                if len(basic_info.listSameTypePokemons())> 1:
                                    print('\n %s is also a type %s pokemon. There are %d pokemons who are also type %s.'
                                          '\n They are %s'%(pokemonList[pokemon_selection],basic_info.pokemonType2,basic_info.countSameTypePokemons()[1],basic_info.pokemonType2, basic_info.listSameTypePokemons()[1].to_string()))
                                continue
                            elif third_input.lower() in ['d','d.','4']:
                                print('\n CP of %s is %d. Among %s pokemons, the mean CP is %d. And it ranks %d among them.'%(pokemonList[pokemon_selection],basic_info.pokemonMaxCP,basic_info.pokemonType1,basic_info.meanPower(basic_info.listSameTypePokemons()[0],'cp'),basic_info.sameTypeRanking()[0][0] ))
                                if len(basic_info.listSameTypePokemons())> 1:
                                    print('\n CP of %s is %d. Among %s pokemons, the mean CP is %d. And it ranks %d among them.'%(pokemonList[pokemon_selection],basic_info.pokemonMaxCP,basic_info.pokemonType2,basic_info.meanPower(basic_info.listSameTypePokemons()[1],'cp'),basic_info.sameTypeRanking()[1][0] ))
                                continue
                            elif third_input.lower() in ['e','e.','5']:
                                print('\n HP of %s is %d. Among %s pokemons, the mean HP is %d. And it ranks %d among them.'%(pokemonList[pokemon_selection],basic_info.pokemonMaxHP,basic_info.pokemonType1,basic_info.meanPower(basic_info.listSameTypePokemons()[0],'hp'),basic_info.sameTypeRanking()[0][1] ))
                                if len(basic_info.listSameTypePokemons())> 1:
                                    print('\n HP of %s is %d. Among %s pokemons, the mean HP is %d. And it ranks %d among them.'%(pokemonList[pokemon_selection],basic_info.pokemonMaxHP,basic_info.pokemonType2,basic_info.meanPower(basic_info.listSameTypePokemons()[1],'hp'),basic_info.sameTypeRanking()[1][1] ))
                                continue
                            else:
                                print('\n Sorry, Please follow the input instructions and enter a letter or back.')
                                continue
                    elif secondary_input.lower() in ['go','pokemongo','pokemon go','game info']:
                        while True:
                            '''
                            The Pokemon Go Info menu asks user to select pokemon go info function
                            Moreover, user can select a certain city for info about this city
                            '''
                            third_input = input('\nYou have selected pokemon go info about %s'
                                            '\nPlease select a function we have here'
                                            '\nA. Show whether people have seen it in pokemon go' 
                                            '\nB. Show the cities where it was often observed in histogram'
                                            '\nC. Show the pokemons whom it was often observed together with'
                                            '\nD. Show distribution of its appearance time of the day in pie chart'
                                            '\nE. Show World Map of all pokemon occurrence in basemap'
                                            '\nF. Show World Map of %s occurrence in basemap'
                                            '\nG. Show Box Plot of pokemons occurrence distance to gym'
                                            '\nH. Show Line Chart of all pokemons occurence freq vs hour of day'
                                            '\n\nType \'city\' to select a certain city for more details'
                                            '\nType \'back\' back to previous menu'
                                            '\nType \'quit\' to quit the program'
                                            '\n\n>  '%(pokemonList[pokemon_selection],pokemonList[pokemon_selection]))
                            if third_input.lower() in ['q','quit','bye']:
                                return (print('\n till Next Time! Goodbye.'))
                            elif third_input.lower() in ['back']:
                                break
                            elif third_input.lower() in ['a','a.','1']:
                                ans = hasItAppearedGlobally(largeData, pokemon_selection)
                                if ans == True:
                                    print('\n %s has appeared in Pokemon Go world'%pokemonList[pokemon_selection])
                                else:
                                    print('\n %s has not appeared in Pokemon Go world yet'%pokemonList[pokemon_selection])
                                continue
                            elif third_input.lower() in ['b','b.','2']:
                                if hasItAppearedGlobally(largeData, pokemon_selection)==True:
                                    ans = ID_city_freq(largeData, pokemon_selection)
                                    print('\n Histogram of Top 10 cities %s has appeared in is saved in: '
                                          '\n Frequency of pokemon %dappears in different cities.png'%(pokemonList[pokemon_selection],pokemon_selection))
                                else:
                                    print('\n %s has not appeared in Pokemon Go world yet.'%pokemonList[pokemon_selection])
                                continue
                            elif third_input.lower() in ['c','c.','3']:
                                if hasItAppearedGlobally(largeData, pokemon_selection)==True:
                                    ans = co_occurance(largeData, pokemon_selection)
                                    print('\n Top 5 pokemons %s has appeared together with are: ')
                                    for i in range(len(ans)):
                                        print('\n %d %s'%(pokemon_selection,pokemonList[pokemon_selection]))
                                else:
                                    print('\n %s has not appeared in Pokemon Go world yet.'%pokemonList[pokemon_selection])
                                continue
                            elif third_input.lower() in ['d','d.','4']:
                                if hasItAppearedGlobally(largeData, pokemon_selection)==True:
                                    ans = appeared_time(largeData, pokemon_selection)
                                    print('\n Percentage of %s has appearance time of the day is saved in: '
                                          '\n pie chart of pokemon %d showing up periods.png'%(pokemonList[pokemon_selection],pokemon_selection))          
                                else:
                                    print('\n %s has not appeared in Pokemon Go world yet.'%pokemonList[pokemon_selection])
                                continue
                            elif third_input.lower() in ['e','e.','5']:
                                ans = worldmap(largeData)
                                continue
                            elif third_input.lower() in ['f','f.','6']:
                                if hasItAppearedGlobally(largeData, pokemon_selection)==True:
                                    ans = worldmap(pokemonwideDataframe(largeData, pokemon_selection))
                                    continue
                                else:
                                    print('\n %s has not appeared in Pokemon Go world yet.'%pokemonList[pokemon_selection])
                                continue
                            elif third_input.lower() in ['g','g.','7']:
                                ans = boxplotGym(largeData)
                                continue
                            elif third_input.lower() in ['h','h.','8']:
                                ans = appearline_according_hour(largeData)
                                continue
                            elif third_input.lower() in ['city']:                                
                                city_selection = userChoice.select_city(cityList)
                                if city_selection == 'Wish you luck in pokemon world, goodbye':
                                    return (print('\n till Next Time! Goodbye.'))
                                else:
                                    while True:
                                        '''
                                            After selecting a city, offer functions user can use
                                            '''
                                        fourth_input = input('\nYou have selected pokemon go info about %s and %s'
                                            '\nPlease select a function we have here'
                                            '\nA. Show whether people have seen it, in %s' 
                                            '\nB. Show the pokemons which were often observed in %s in histogram'
                                            '\nC. Show the pokemons whom it was often observed together with, in %s'
                                            '\nD. Show distribution of its appearance time of the day in pie chart, in %s'
                                            '\nE. Show scatterplot of windspeed and temperature relationship, in %s'
                                            '\nType \'back\' back to previous menu'
                                            '\nType \'quit\' to quit the program'
                                            '\n>  '%(pokemonList[pokemon_selection],city_selection,city_selection, city_selection,city_selection,city_selection,city_selection))
                                        if fourth_input.lower() in ['q','quit','bye']:
                                            return (print('\n till Next Time! Goodbye.'))
                                        elif fourth_input.lower() in ['back']:
                                            break
                                        elif fourth_input.lower() in ['a','a.','1']:
                                            ans = appeared_incity(largeData, pokemon_selection, city_selection)
                                            continue
                                        elif fourth_input.lower() in ['b','b.','2']:
                                            ans = city_ID_freq(largeData, city_selection)
                                            print('\n Histogram of Top 10 pokemons appeared in %s is saved in: '
                                                      '\n Frequencies of pokemons appear in %s.png'%(city_selection,city_selection))
                                            continue
                                        elif fourth_input.lower() in ['c','c.','3']:
                                            if hasItAppearedGlobally(citywideDataframe(largeData,city_selection), pokemon_selection)==True:
                                                ans = co_occurance(citywideDataframe(largeData,city_selection), pokemon_selection)
                                                print('\n In %s, Top 5 pokemons %s has appeared together with are: '%(city_selection,pokemonList[pokemon_selection]))
                                                for i in range(len(ans)):
                                                    print('\n %d %s'%(pokemon_selection,pokemonList[pokemon_selection]))
                                            else:
                                                print('\n %s has not appeared in %s yet.'%(pokemonList[pokemon_selection],city_selection))
                                            continue
                                        elif fourth_input.lower() in ['d','d.','4']:
                                            if hasItAppearedGlobally(citywideDataframe(largeData,city_selection), pokemon_selection)==True:
                                                ans = appeared_time(citywideDataframe(largeData,city_selection), pokemon_selection)
                                                print('\n Percentage of %s has appearance time of the day in %s is saved in: '
                                                      '\n pie chart of pokemon %d showing up periods.png'%(pokemonList[pokemon_selection],city_selection,pokemon_selection))          
                                            else:
                                                print('\n %s has not appeared in %s yet.'%(pokemonList[pokemon_selection],city_selection))
                                            continue
                                        elif fourth_input.lower() in ['e','e.','5']:
                                            ans = temp_windspeed_relation(largeData, city_selection)
                                            continue
                        continue
                    else:
                        print('Sorry, Please follow the input instructions.')
                        continue
        #elif main_input.lower() in ['city']:
            #city_selection = select_city(cityList)
        else:
            print('\n Please type again, I am not sure what you are talking about.')
            continue
    return (print('\n till Next Time! Goodbye.'))
if __name__ == '__main__':
    main()
