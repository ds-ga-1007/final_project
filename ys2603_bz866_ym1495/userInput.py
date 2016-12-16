import pandas as pd
import numpy as np
import sys

from loadData import *


class UserChoice:

    """
    ...
    """
    def __init__(self):
        self.pokemonId = None
        self.city = None
    


    def select_pokemon(self,pokemonList):
        lower_pokeList = ['zero']
        str = 'Please select a pokemon by its index:\n'
        for i in pokemonList.index:
            str = str + '%d %s \n'%(i,pokemonList[i])
            lower_pokeList.append(pokemonList[i].lower())
        while True:
            choice = input(str)
            try:
                choice = int(choice)
                if choice in pokemonList.index:
                    choice = choice
                    break
                else:
                    print('Please select a pokemon again, within the range of index(1-151)')
                    continue
            except ValueError:
                if choice.lower() in{'quit','q','bye'}: 
                    choice = 'Wish you luck in pokemon world. Goodbye'
                    break
                elif choice.lower() in {'nidoran'}:
                    while True:
                        second_choice = input('You want Nidoran to be Female or Male? Please answer with F or M')
                        if second_choice.lower()=='f'or 'female':
                            choice = 29
                            return choice
                        elif second_choice.lower()=='m' or 'male':
                            choice = 32
                            return choice
                        else:
                            continue
                elif choice.lower() in lower_pokeList:
                    choice = lower_pokeList.index(choice.lower())
                    break
                else:
                    print('Please select a pokemon again, by its index(integer 1-151)')
                    continue
        return choice
    
    def select_city(self, cityList):        
        lower_cityList = []
        str = 'Please select a city:\n'
        for i in range(len(cityList)):
            lower_cityList.append(cityList[i].lower())
            str = str + '%d %s \n'%(i,cityList[i])
        while True:
            choice = input(str)
            try:
                choice = int(choice)
                if choice in range(len(cityList)):
                    choice = cityList[choice]
                    break
                else:
                    print('Please select a city again, within the range of index')
                    continue
            except ValueError:
                if choice.lower() in{'quit','q','bye'}: 
                    choice = 'Wish you luck in pokemon world, goodbye'
                    break
                elif choice.lower() in lower_cityList:
                    index = lower_cityList.index(choice.lower())
                    choice = cityList[index]
                    break
                else:
                    print('Please select a city again')
                    continue
        return choice
