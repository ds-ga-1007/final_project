import numpy as np
import pandas as pd

class pokemonStats():
    '''
    This class helps present Type, Combat Power and Health Power of certain pokemon 
    '''
    def __init__(self, basicData, pokemonNumber):
        self.df = basicData
        self.df.set_index('Pokemon No.', inplace=True, drop=False)  #pandas: dataFrame.set_index
        self.pokemonNumber = pokemonNumber
        self.pokemonRecord = self.df.ix[pokemonNumber]  #pandas: dataFrame.ix()
        self.pokemonName = self.pokemonRecord['Name']
        self.pokemonMaxCP = self.pokemonRecord['Max CP']
        self.pokemonMaxHP = self.pokemonRecord['Max HP']
        self.pokemonType1 = self.pokemonRecord['Type 1']
        self.pokemonType2 = self.pokemonRecord['Type 2']
        
    def ranking(self, dataFrame):
        '''
        A base ranking function which can generate CP and HP ranking given any dataframe
        @param datafram can be overall df or df of the same type pokemons
        @return a tuple of two integers
        '''
        rankdf = dataFrame.rank(axis=0, numeric_only=True, ascending=False) #pandas: dataFrame.rank()
        rankCP = int(rankdf.get_value(self.pokemonNumber, 'Max CP'))    #pandas: dataFrame.get_value
        rankHP = int(rankdf.get_value(self.pokemonNumber, 'Max HP'))    #pandas: dataFrame.get_value
        return rankCP, rankHP
    
    def listSameTypePokemons(self):
        '''
        find the pokemons who have the same type with given pokemon
        @return a tuple of one or two dataframe
        '''
        sameType1Pokemons = self.df[(self.df["Type 1"]== self.pokemonType1) | (self.df["Type 2"]==self.pokemonType1) ]
        if pd.isnull(self.pokemonType2)==True:
            return sameType1Pokemons,
        else:
            sameType2Pokemons = self.df[(self.df["Type 1"]== self.pokemonType2) | (self.df["Type 2"]==self.pokemonType2) ]
            return sameType1Pokemons, sameType2Pokemons
    
    def countSameTypePokemons(self):
        '''
        Because pokemons could have two types together, we want to know for each type, how many friends do we have
        @return a tuple of one or two int
        '''
        if len(self.listSameTypePokemons())==1:
            return self.listSameTypePokemons()[0].count()[0],   #pandas: dataFrame.count()
        else:
            return self.listSameTypePokemons()[0].count()[0], self.listSameTypePokemons()[1].count()[0]
    
    def overallRanking(self):
        '''
        global ranking function inherited from ranking
        @return a tuple of two integers
        '''
        return self.ranking(self.df)
    
    def sameTypeRanking(self):
        '''
        rank this pokemon's power among its one or two same type group 
        @return a tuple of one or two tuples of two integers
        '''
        if len(self.listSameTypePokemons())==1:
            return self.ranking(self.listSameTypePokemons()[0]),
        else:
            return self.ranking(self.listSameTypePokemons()[0]), self.ranking(self.listSameTypePokemons()[1])
    
        
    def topPercentilePower(self, dataFrame, CPorHP):
        '''
        find the percentile of CP or HP of the pokemon among certain group
        @return a string
        '''
        str = 'Max '+ CPorHP.upper()
        if (self.pokemonRecord[str]<dataFrame.describe()[str]['25%']&self.pokemonRecord[str]>=dataFrame.describe()[str]['min']):
            ans = 'weakest'
        elif (self.pokemonRecord[str]<dataFrame.describe()[str]['50%']&self.pokemonRecord[str]>=dataFrame.describe()[str]['25%']):
            ans = 'top 75 percentile'
        elif (self.pokemonRecord[str]<dataFrame.describe()[str]['75%']&self.pokemonRecord[str]>=dataFrame.describe()[str]['50%']):
            ans = 'top 50 percentile'
        elif (self.pokemonRecord[str]<dataFrame.describe()[str]['max']&self.pokemonRecord[str]>=dataFrame.describe()[str]['75%']):
            ans = 'top 25 percentile'
        else: 
            ans = 'strongest'
        return ans
    
    def meanPower(self, dataFrame, CPorHP):
        '''
        mean of certain power among a group
        @return a double
        '''
        str = 'Max '+ CPorHP.upper()
        return dataFrame.describe()[str]['mean']
        
