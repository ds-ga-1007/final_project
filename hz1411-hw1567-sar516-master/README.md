# New York City Trip Helper

This is the final project for **DS-GA 1007 Programming for Data Science** .
## Contributors

Hezhi Wang [https://github.com/HezhiWang] (https://github.com/HezhiWang) Netid: hw1567

Han Zhao [https://github.com/hzhao16] (https://github.com/hzhao16) Netid: hz1411

Storm Avery Ross [https://github.com/sar516] (https://github.com/sar516) Netid: sar516

## Dependencies
- Python = 3.5
- [tkinter](https://docs.python.org/3/library/tk.html) == 8.5.18
- [geopy](https://pypi.python.org/pypi/geopy/1.11.0) == 1.11.0
- [gmplot](https://pypi.python.org/pypi/gmplot/1.1.1) == 1.1.1
- [seaborn](https://pypi.python.org/pypi/seaborn/) == 0.7.1
- [pillow](http://pillow.readthedocs.io/en/3.4.x/installation.html) >= 2.0.0
- [numpy](https://pypi.python.org/pypi/numpy/1.11.1) == 1.11.1
- [pandas](http://pandas.pydata.org/pandas-docs/version/0.18.1/) == 0.18.1
- [matplotlib](http://matplotlib.org/) == 1.5.3
- [sklearn](http://scikit-learn.org/stable/) == 0.18.1

if any of the packages are missing, type in your command line(MAC OS X)
```sh
$ pip install <package>
```
Or you can specify the verision:
```sh
$ pip install <package>==<version>
```

## How to run
The application runs smoothly on MAC OS X.

Switch to the directory of the application, and run on command line(MAC OS X):
```sh
$ python gui.py
```
## How to test
Switch to the directory of the application, and run on command line(MAC OS X):
```sh
$ python -m unittest discover
```

## How to use
This application allows users to,

1. **Search** for places of interest by entering their latitude and longitude and specify their preferences.

2. **Plan** a trip to NYC by selecting their preferred budget, time and schedule to access a customized trip plan including recommendations for attractions, restaurants and hotels.

3. **Overview** certain visualized stats about NYC attractions, museums, restaurants and hotels, including heat map, bar chart, pie chart etc.

4. **Quit** the application by directly closing the window or ```control + C``` on command line.

5. **Please DO NOT click the buttons too quickly.**

6. For detailed description, please see below.

## Description

This program helps you to have fun in New York City. 

It consists of 3 main functions that you can select on Home Page - `Search`, `Plan` and `Overview`. Our datasets are scraped from [Booking.com](http://www.booking.com/) for hotels, [Tripadvisor.com](https://www.tripadvisor.com/) for attractions and museums, and [Yelp.com](https://www.yelp.com/nyc) for restaurants.

Firstly, You can “`search`” nearby locations that fall in 4 categories: restaurants, hotels, attractions and museums. You need to enter your current `latitude` and `longitude`, and select what kind of locations you are interested in. Your coordinate should be within NYC or an error message will be raised. We also have specific filters for certain locations. For *restaurants*, you can choose from 12 different categories, including Italian, Chinese, Cafe & bar etc. For *hotels*, you can choose from 3 price levels based on your budget. Our program will search for all nearby locations that satisfy your filter, and sort by their rating and number of reviews. To see our recommendations for you, you can click “`show the map`” to see them marked on a Google Map. If you prefer a written version, simply click “`show the recommendations`”, and a PDF file will pop up and also be saved under “*Results*” folder. It contains the name of each recommended locations, each with a *radar chart* showing their ratings from different angles. For *museums* and *attrations*, as they are relatively more scattered, the recommendation will only be based on a combination of ratings and reviews. You can always go back to the search main page by “`Back to Search`”. Note that in our calculation your location is set as the center of a circle, so if your location is too close to the sea, our recommendations may be across the sea.

Second, you can “`plan`” a trip to New York. Just choose how many days you want to stay (from 1 day to 7 days) , how much money you could spend, and how you would arrange your time (whether you prefer a tight schedule to see as many as places of interest as possible, or you like to be more flexible and just enjoy yourself). You can reset your choice by clicking “`Back to previous page`”. And finally, click “`Build your travel plan`”. Et voilà! Now you can see your travel plan which is also saved under “*Results*” folder in rtf format. You will see our arrangement for your each day, including attractions and museums to visit, and recommendations of hotels and restaurants. Our algorithm utilizes sorting, permutation, and clustering (revised K-means algorithm that return K clusters with almost the same number of elements) by distance. So you can have incredible amount of different plans, each highlights most loved travel spots, and you won’t waste too much time on traffic. You can click “`Back to previous page`” to reset your preference and get a whole new plan.

And finally, we also provide an “`overview`” section. Here you can have a look at our visualizations of overall stats of New York restaurants, hotels, attractions and museums. Just select a type and click “`Show plots`”. Then on next page you can select what kind of plot you would like to see. We have *heatmap* on Google map, *density plot for reviews*, *pie plot by price or category*, *bar plot for ratings* with mean, variance and median. On clicking the relevant button, a figure will pop up and also be saved to ”*Results*“ folder. 

Enjoy your trip in New York!

