'''
Created on Dec 3, 2016

@author: muriel820
'''
import unittest
import numpy as np
import pandas as pd
from basicInfo import pokemonStats

'''
This class tests methods that show fundamental characteristics of different pokemons, such as health power, combat power,
rankings among them etc.
'''
df = pd.read_csv('pokemonGO.csv')
class Test(unittest.TestCase):

    def test_Name(self):
        pok = pokemonStats(df,151)
        self.assertEqual('Mew', pok.pokemonName)
        pok = pokemonStats(df,131)
        self.assertTrue('Lapras', pok.pokemonName)

    def test_ranking(self):
        pok = pokemonStats(df, 151)
        self.assertEqual('(3, 11)', str(pok.ranking(df)))
        pok = pokemonStats(df, 130)
        self.assertTrue('(12, 13)' == str(pok.ranking(df)))

    def test_countSameTypePokemons(self):
        pok1 = pokemonStats(df, 130)
        m=pok1.countSameTypePokemons()
        self.assertEqual('(32, 19)', str(m))
        pok2 = pokemonStats(df, 30)
        m=pok2.countSameTypePokemons()
        self.assertEqual('(33,)', str(m))

    def test_overallRanking(self):
        pok = pokemonStats(df, 80)
        m=pok.overallRanking()
        self.assertEqual('(16, 13)', str(m))
        pok = pokemonStats(df, 90)
        m = pok.overallRanking()
        self.assertEqual('(133, 144)', str(m))


if __name__ == "__main__":
    unittest.main()
