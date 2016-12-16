# The final project of DS-GA 1007
# NYU Center for Data Science
# Authors: Jiaming Dong (jd3405@nyu.edu)
#          Daniel Amaranto (da1933@nyu.edu)
#          Julie Cachia (jyc436@nyu.edu)
#
# The yelp user data processing class


import pandas as pd


# class for retriving data
class MyYelpUser:
    def __init__(self, user):
        self.user = user
        self._process_yelping_since()
        self._process_review_count()

    def _process_yelping_since(self):
        """transfer the yelping since into year"""
        for i in range(0, 9):
            yelp_since = []
            for j in self.user[i]['yelping_since']:
                yelp_since.append(int(j[:4]))
            self.user[i]['yelping_since'] = pd.Series(data=yelp_since).value_counts()

    def _process_review_count(self):
        """transfer the review count into value counts"""
        for i in range(0, 9):
            self.user[i]["review_count"] = self.user[i]["review_count"].value_counts()

    def get_series_range(self, data_attr, star_st, star_ed):
        """get data for the given star number and attribute"""
        index_st = int(star_st * 2 - 2)
        index_ed = int(star_ed * 2 - 2)
        ret = self.user[index_st][data_attr]
        for i in range(index_st + 1, index_ed + 1):
            for j in self.user[i][data_attr].index:
                if j in ret.index:
                    ret[j] += self.user[i][data_attr][j]
                else:
                    ret[j] = self.user[i][data_attr][j]
        return ret

    def get_data_range(self, data_attr, star_st, star_ed):
        """get data for the given star range and attribute"""
        ret = []
        index_st = int(star_st * 2 - 2)
        index_ed = int(star_ed * 2 - 2)
        for i in range(index_st, index_ed + 1):
            ret.extend(self.user[i][data_attr])
        return ret
