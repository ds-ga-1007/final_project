# The final project of DS-GA 1007
# NYU Center for Data Science
# Authors: Jiaming Dong (jd3405@nyu.edu)
#          Daniel Amaranto (da1933@nyu.edu)
#          Julie Cachia (jyc436@nyu.edu)
#
# The function to load user data


import json
import pandas as pd


def load_user_data(path):
    # Load user data:
    yelp_users = [json.loads(line) for line in open(path)]
    users = pd.DataFrame(yelp_users)

    # Lists for all users that average between 0-1 stars
    oneStar = users[users['average_stars'] <= 1]

    oneFans = oneStar['fans']
    oneElite = oneStar['elite']
    oneYelpingSince = oneStar['yelping_since']
    oneReviewCount = oneStar['review_count']
    oneVotes = oneStar['votes']

    # Lists for all users that average between 1-1.5 stars
    oneHalfStar = users[(users['average_stars'] > 1) & (users['average_stars'] <= 1.5)]

    oneHalfFans = oneHalfStar['fans']
    oneHalfElite = oneHalfStar['elite']
    oneHalfYelpingSince = oneHalfStar['yelping_since']
    oneHalfReviewCount = oneHalfStar['review_count']
    oneHalfVotes = oneHalfStar['votes']

    # Lists for all users that average between 1.5-2 stars
    twoStar = users[(users['average_stars'] > 1.5) & (users['average_stars'] <= 2)]

    twoFans = twoStar['fans']
    twoElite = twoStar['elite']
    twoYelpingSince = twoStar['yelping_since']
    twoReviewCount = twoStar['review_count']
    twoVotes = twoStar['votes']

    # Lists for all users that average between 2-2.5 stars
    twoHalfStar = users[(users['average_stars'] > 2) & (users['average_stars'] <= 2.5)]

    twoHalfFans = twoHalfStar['fans']
    twoHalfElite = twoHalfStar['elite']
    twoHalfYelpingSince = twoHalfStar['yelping_since']
    twoHalfReviewCount = twoHalfStar['review_count']
    twoHalfVotes = twoHalfStar['votes']

    # Lists for all users that average between 2.5-3 stars
    threeStar = users[(users['average_stars'] > 2.5) & (users['average_stars'] <= 3)]

    threeFans = threeStar['fans']
    threeElite = threeStar['elite']
    threeYelpingSince = threeStar['yelping_since']
    threeReviewCount = threeStar['review_count']
    threeVotes = threeStar['votes']

    # Lists for all users that average between 3-3.5 stars
    threeHalfStar = users[(users['average_stars'] > 3) & (users['average_stars'] <= 3.5)]

    threeHalfFans = threeHalfStar['fans']
    threeHalfElite = threeHalfStar['elite']
    threeHalfYelpingSince = threeHalfStar['yelping_since']
    threeHalfReviewCount = threeHalfStar['review_count']
    threeHalfVotes = threeHalfStar['votes']

    # Lists for all users that average between 3.5-4 stars
    fourStar = users[(users['average_stars'] > 3.5) & (users['average_stars'] <= 4)]

    fourFans = fourStar['fans']
    fourElite = fourStar['elite']
    fourYelpingSince = fourStar['yelping_since']
    fourReviewCount = fourStar['review_count']
    fourVotes = fourStar['votes']

    # Lists for all users that average between 4-4.5 stars
    fourHalfStar = users[(users['average_stars'] > 4) & (users['average_stars'] <= 4.5)]

    fourHalfFans = fourHalfStar['fans']
    fourHalfElite = fourHalfStar['elite']
    fourHalfYelpingSince = fourHalfStar['yelping_since']
    fourHalfReviewCount = fourHalfStar['review_count']
    fourHalfVotes = fourHalfStar['votes']

    # Lists for all users that average between 4.5-5 stars
    fiveStar = users[(users['average_stars'] > 4.5) & (users['average_stars'] <= 5)]

    fiveFans = fiveStar['fans']
    fiveElite = fiveStar['elite']
    fiveYelpingSince = fiveStar['yelping_since']
    fiveReviewCount = fiveStar['review_count']
    fiveVotes = fiveStar['votes']

    # 1 Star

    temp = [i.get('useful') for i in oneVotes]
    oneVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in oneVotes]
    oneVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in oneVotes]
    oneVotedCool = [i for i in temp if i is not None]

    # 1.5 Stars

    temp = [i.get('useful') for i in oneHalfVotes]
    oneHalfVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in oneHalfVotes]
    oneHalfVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in oneHalfVotes]
    oneHalfVotedCool = [i for i in temp if i is not None]

    # 2 Stars

    temp = [i.get('useful') for i in twoVotes]
    twoVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in twoVotes]
    twoVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in twoVotes]
    twoVotedCool = [i for i in temp if i is not None]

    # 2.5 Stars

    temp = [i.get('useful') for i in twoHalfVotes]
    twoHalfVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in twoHalfVotes]
    twoHalfVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in twoHalfVotes]
    twoHalfVotedCool = [i for i in temp if i is not None]

    # 3 Stars

    temp = [i.get('useful') for i in threeVotes]
    threeVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in threeVotes]
    threeVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in threeVotes]
    threeVotedCool = [i for i in temp if i is not None]

    # 3.5 Stars

    temp = [i.get('useful') for i in threeHalfVotes]
    threeHalfVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in threeHalfVotes]
    threeHalfVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in threeHalfVotes]
    threeHalfVotedCool = [i for i in temp if i is not None]

    # 4 Stars

    temp = [i.get('useful') for i in fourVotes]
    fourVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in fourVotes]
    fourVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in fourVotes]
    fourVotedCool = [i for i in temp if i is not None]

    # 4.5 Stars

    temp = [i.get('useful') for i in fourHalfVotes]
    fourHalfVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in fourHalfVotes]
    fourHalfVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in fourHalfVotes]
    fourHalfVotedCool = [i for i in temp if i is not None]

    # 5 Stars

    temp = [i.get('useful') for i in fiveVotes]
    fiveVotedUseful = [i for i in temp if i is not None]
    temp = [i.get('funny') for i in fiveVotes]
    fiveVotedFunny = [i for i in temp if i is not None]
    temp = [i.get('cool') for i in fiveVotes]
    fiveVotedCool = [i for i in temp if i is not None]

    userOne = {'average_stars': oneStar,
               'fans': oneFans,
               'elite': oneElite,
               'yelping_since': oneYelpingSince,
               'review_count': oneReviewCount,
               'votedUseful': oneVotedUseful,
               'votedFunny': oneVotedFunny,
               'votedCool': oneVotedCool}

    userOneHalf = {'average_stars': oneHalfStar,
                   'fans': oneHalfFans,
                   'elite': oneHalfElite,
                   'yelping_since': oneHalfYelpingSince,
                   'review_count': oneHalfReviewCount,
                   'votedUseful': oneHalfVotedUseful,
                   'votedFunny': oneHalfVotedFunny,
                   'votedCool': oneHalfVotedCool}

    userTwo = {'average_stars': twoStar,
               'fans': twoFans,
               'elite': twoElite,
               'yelping_since': twoYelpingSince,
               'review_count': twoReviewCount,
               'votedUseful': twoVotedUseful,
               'votedFunny': twoVotedFunny,
               'votedCool': twoVotedCool}

    userTwoHalf = {'average_stars': twoHalfStar,
                   'fans': twoHalfFans,
                   'elite': twoHalfElite,
                   'yelping_since': twoHalfYelpingSince,
                   'review_count': twoHalfReviewCount,
                   'votedUseful': twoHalfVotedUseful,
                   'votedFunny': twoHalfVotedFunny,
                   'votedCool': twoHalfVotedCool}

    userThree = {'average_stars': threeStar,
                 'fans': threeFans,
                 'elite': threeElite,
                 'yelping_since': threeYelpingSince,
                 'review_count': threeReviewCount,
                 'votedUseful': threeVotedUseful,
                 'votedFunny': threeVotedFunny,
                 'votedCool': threeVotedCool}

    userThreeHalf = {'average_stars': threeHalfStar,
                     'fans': threeHalfFans,
                     'elite': threeHalfElite,
                     'yelping_since': threeHalfYelpingSince,
                     'review_count': threeHalfReviewCount,
                     'votedUseful': threeHalfVotedUseful,
                     'votedFunny': threeHalfVotedFunny,
                     'votedCool': threeHalfVotedCool}

    userFour = {'average_stars': fourStar,
                'fans': fourFans,
                'elite': fourElite,
                'yelping_since': fourYelpingSince,
                'review_count': fourReviewCount,
                'votedUseful': fourVotedUseful,
                'votedFunny': fourVotedFunny,
                'votedCool': fourVotedCool}

    userFourHalf = {'average_stars': fourHalfStar,
                    'fans': fourHalfFans,
                    'elite': fourHalfElite,
                    'yelping_since': fourHalfYelpingSince,
                    'review_count': fourHalfReviewCount,
                    'votedUseful': fourHalfVotedUseful,
                    'votedFunny': fourHalfVotedFunny,
                    'votedCool': fourHalfVotedCool}

    userFive = {'average_stars': fiveStar,
                'fans': fiveFans,
                'elite': fiveElite,
                'yelping_since': fiveYelpingSince,
                'review_count': fiveReviewCount,
                'votedUseful': fiveVotedUseful,
                'votedFunny': fiveVotedFunny,
                'votedCool': fiveVotedCool}

    # User list of dictionries for each star level:
    usersData = [userOne, userOneHalf, userTwo, userTwoHalf, userThree,
                 userThreeHalf, userFour, userFourHalf, userFive]

    return usersData
