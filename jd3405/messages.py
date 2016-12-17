'''
The final project of DS-GA 1007
NYU Center for Data Science
Authors: Jiaming Dong (jd3405@nyu.edu)
         Daniel Amaranto (da1933@nyu.edu)
         Julie Cachia (jyc436@nyu.edu)

Messages for user interface:
'''


inputErrorMessage =  	"Invalid Entry.\n" + \
			"This program takes three inputs.\n 1) Choose 'user' or 'business'\n" + \
			" 2) Choose a feature from the instructions.\n" + \
			" 3) Choose a star level or a range to analyze:\n" + \
			"    1   1.5   2   2.5   3   3.5   4   4.5   5\n" + \
			" E.g. 'business prices 2.5' \n" + \
			" For a range of stars levels just include an upper bound.\n" + \
			" E.g. 'business prices 1 5'\n" + \
			"Type 'business' or 'user' for more information or type 'finish' to exit.\n"
                    
business_features = 	"For a user-defined star level or range, you can see the following business categories:\n" + \
			"  review_count - the number of reviews\n" + \
			"  states - proportion of states that comprise star-ratings of your choice\n" + \
			"  cities - proportion of cities that comprise star-ratings of your choice\n" + \
			"  prices - the numbers of businesses at each price level\n" + \
			"  reservations - proportion of businesses that accept reservations\n" + \
			"  credit_cards - proportion of businesses that accept credit cards\n" + \
			"  delivery - proportion of businesses that deliver\n" + \
			"  common_categories - the most common business categories\n"

user_features =		"For a user-defined star level or range, you can see the following user categories:\n" + \
			"  yelping_since - proportion of users that have yelped since a given year\n" + \
			"  review_count - average of reviews that users have given\n" + \
			"  votedUseful - distribution of 'Useful' votes received by users\n" + \
			"  votedFunny - distribution of 'Funny' votes received by users\n" + \
			"  votedCool - distribution of 'Cool' votes received by users\n"
