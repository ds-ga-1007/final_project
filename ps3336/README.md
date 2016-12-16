# Programming-for-Data-Science-Project

Team Member: Wenqing Zhu(wz1070), Xiaoyu Wang(xw1435), Peimeng Sui(ps3336)


# Project Title: Winning Eleven


## Providing Guide for English Premier League Clubs’ Managers based on transfermarkt.com Data Analysis


Every summer, English Premier League Clubs spend a lot of money on transfer market to acquire new players. We want to provide managers with a data-driven approach to optimize their transfer decision. We will use Numpy and pandas packages in Python to scrape, clean and preprocess data of player transfers and stats data. We will create some interesting metrics to quantify the return of investment on transfer market. Ideally, we will have easily understandable visualization of those metrics with the help of matlibplot. Some potential metrics we have in mind: Money spent per goal by purchased player, Club improvement of performance considering their investment, performance improvement of transfer players, etc. In order to make them easily available for our potential users, we will create some interface by using terminal or Python notebook to allow the user to interactively control the analysis and display of the data. 


Our dataset is scraped from www.transfermarkt.com, which is the most popular data provider for soccer players’ transfer records and stats. Now we have scraped all transfer records of English Premier League Clubs for summer 2016 and the corresponding real-time players’ stats in season 2016-2017. We are planning to scrape the same format of data for summer 2015 and 2014 also. Some basic variables we have for each player: transfer value, club, position, age, goals, assists, minutes, minutes per goal. We will scrape for more data if we find anything is interesting. 

## The files in this repo include:
1. A Notebook showing the process of webscraping for data: Data_Scraping.ipynb
2. cleaned dataset we were using for analysis: finaldata.csv
3. A bunch of class definition .py files
4. A driver of main program final_project.py
5. A unitest file test.py

## User Guide:

## Setup

You should have the data file finaldata.csv, all class definition .py files and final_project.py file under your working directory.

## Requirements:

- Python 3
- Pandas
- Numpy
- Matplotlib

## Running the program

This is easy! 
```bash
python final_project.py
```
After entering into the program, it will allow you to input and interact to conduct your own analysis. The main menu will allow you to choose from Year, Club and Position to start your analysis. Then you can follow the pop-up hint to input your query. Each time you want to visualize the result, you will be asked if you want to save the plots of result. If you enter 'y', then the plot will be saved to your working directory automatically. Each time you finish a analysis task or enter a wrong input, you will be braught back to the main menu and you can start all over again. You can type "quit" or use any key board interruption to quit the entire program any time you want. 

## Enjoy our tools!
