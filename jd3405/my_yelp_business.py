# The final project of DS-GA 1007
# NYU Center for Data Science
# Authors: Jiaming Dong (jd3405@nyu.edu)
#          Daniel Amaranto (da1933@nyu.edu)
#          Julie Cachia (jyc436@nyu.edu)
#
# The yelp business data processing class


import pandas as pd


# class for retriving data
class MyYelpBusiness:
    def __init__(self, business):
        self.business = business
        self._preprocessing()

    def _preprocessing(self):
        """transfer the lists into value counts"""
        for i in range(0, 9):
            self.business[i]["reservations"] = pd.Series(data=self.business[i]["reservations"]).value_counts()
            self.business[i]["credit_cards"] = pd.Series(data=self.business[i]["credit_cards"]).value_counts()
            self.business[i]["delivery"] = pd.Series(data=self.business[i]["delivery"]).value_counts()

    def get_series_range(self, data_attr, star_st, star_ed):
        """get data for the given star number and attribute"""
        index_st = int(star_st * 2 - 2)
        index_ed = int(star_ed * 2 - 2)
        ret = self.business[index_st][data_attr]
        for i in range(index_st + 1, index_ed + 1):
            for j in self.business[i][data_attr].index:
                if j in ret.index:
                    ret[j] += self.business[i][data_attr][j]
                else:
                    ret[j] = self.business[i][data_attr][j]
        return ret

    def get_data_range(self, data_attr, star_st, star_ed):
        """get data for the given star range and attribute"""
        ret = []
        index_st = int(star_st * 2 - 2)
        index_ed = int(star_ed * 2 - 2)
        for i in range(index_st, index_ed + 1):
            ret.extend(self.business[i][data_attr])
        return ret
