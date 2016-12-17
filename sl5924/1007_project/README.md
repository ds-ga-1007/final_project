## User Guide
- DS-GA-1007  Final Project: H1B VISA Approval Rate Exploring
- Team Member:
  - Yuwei Tu (yt1209)
  - Sheng Liu (sl5924)
  - Zhaopeng Liu (zl1732)


### Project Content
This project is aiming to provide information about H1B visa from historical data from 2010 to 2016. 


### Part 1: Environment Setup
1. run the following commands to download our projects
``` sh
$ git clone [git-repo-url]
$ cd 1007_project
```

2. Please don't use sample data in the repo, to run the system, please download data from the dropbox first, click [here](https://www.dropbox.com/sh/lk7ec8gjanuwnhk/AADyjXYQw-8imLqCsw3N8PZaa?dl=0)
to download.

3. After downloaded the data sets, please decompressing the file and move the folder **DataBase** into our repo 1007_project to replace the original **DataBase** folder.

4. Make sure that 'chorogrid', 'DataBase' (the one you download), 'h1b_exploring' and main_new.py are in the repo.


### Part 2 : Usage of the Application

1. Indicators
This system will generate different graphs based on 3 indicators:

    * Indicator 1: Application Pool(the total number of applications)
    * Indicator 2: Approval Rate(the total number of approved cases/the total number of applications)
    * Indicator 3: Average Wage(average wage for all application cases)

2. Dimensions
This system will analyze H1B application from 3 dimensions:

    * Dimension 1: Location(Country/State/City)
    * Dimension 2: Industry(Indicated by [SOC Groups](/http://www.bls.gov/soc/major_groups.htm))
    * Dimension 3: Company

### Part 3 : Configuration

1. Pandas to access data.
2. Numpy to perform statistical analysis.
3. Matplotlib for graphics including line plots and bar plots.
4. cloropleth maps.

### Part 4: How to run the program

In terminal, enter the command to run the program:

``` sh
$ cd 1007_project
$ python main_new.py
```

##### Main Menu:

- Enter a to go to a sub menu of Overview of H1b Data.
- Enter b to go to a sub menu of Location(National Level, State Level, and City Level).
- Enter c to go to a sub menu of Industry Level.
- Enter d to go to a sub menu of Company Level.


###### Option a: Overview
- Enter [a,b,c] to go to a summary from 2010 to 2016:
  - Enter a to go to a line chart for application pool from 2010 to 2016
  - Enter b to go to a line chart for approval rate from 2010 to 2016
  - Enter c to go to a line chart for average wage from 2010 to 2016
- Enter r: go back to previous menu.
- Enter quit: exit the program.


###### Option b: Location
- Enter [a,b,c] to go to go to different location levels
  - Enter a to go to National Level
    + Enter [a,b,c] to go to a summary from 2010 to 2016:
      * Enter a to go to a map for application pool from 2010 to 2016
      * Enter b to go to a map for approval rate from 2010 to 2016
      * Enter c to go to a map for average wage from 2010 to 2016
  - Enter b to go to State Level
    + Input a state ABBREVIATION， return line charts of application pools, approve rate, average wage
    + NOTE: close one plot will show the next plot
  - Enter c to go to City Level
    + A list of Top 20 Cities ranked by application pool will show up in terminal
    + A pdf file contained graphs of application pools, approve rate, average wage will be automatically saved in your current dictionary
- Enter r: go back to previous menu.
- Enter quit: exit the program.


###### Option c: Industry Level

- Enter a to look through popular industries
  + Enter [a,b,c] to seperately rank industries by application pools, approve rate, average wage
  + Enter an INT between [5,20] to decide how many industries to look through
  + The system will return Top n industries in terminal
  + If you enter "yes", a pdf file contained graphs of application pools, approve rate, average wage will be automatically saved in your current dictionary
- Enter B to search your interested industry
  + Input interested industry keyword
  + The system will return application pools, approved cases, approve rate, average wage and All related job titles
- Enter r: go back to previous menu.
- Enter quit: exit the program.

###### Option d: Company Level
- Enter a to look through popular companies
  + The system will return Top 10 companies with largest application pools from 2010 to 2016 in terminal
  + A pdf file contained graphs of application pools, approve rate, average wage will be automatically saved in your current dictionary
- Enter b to search your interested company
  + Input interested company fullname
  + The system will return application pools, approved cases, approve rate, and average wage in terminal
- Enter r: go back to previous menu.
- Enter quit: exit the program.



### Part 5: A commmon walk-through example
1. At the begining of the program, it will take seconds to load data and then you will see the Main Menu and options.
![Main_Menu](readme_materials/1.png?raw=true =600x)
2. For example, if you would like to see the overview of the h1b data, you should type `a`, then the line chart will pop up:
![Main_Menu](readme_materials/2.png?raw=true =600x)
3. Close the pop up window, you can type `r` to return to Main Menu. Type `b` then decide which level you are interested in. For instance, if you are interested in national level, you should type `a`, and choose the topic and year you want to see. Then you will find a **.svg** in 1007_project repo, open it with your web browser.
![Main_Menu](readme_materials/3.png?raw=true =600x)
If you are interested in city level, type `c`, you will get a table
![Main_Menu](readme_materials/4.png?raw=true =600x)
4. You can also find information about each company. For example, you can get information about the most popular companies. And find more detail in a **.pdf** in our repo, open it you will see
![Main_Menu](readme_materials/5.png?raw=true =600x)
5. You can find more information about a specific company by choosing Customized Company Inquiry and enter the company name. sometimes you may forget the complete name of the company, just type in part of the name, the system will give you a list of company names that match. For example, type `goog`, you will get
![Main_Menu](readme_materials/6.png?raw=true =600x)
6. If the company you want to see is in the list, type `yes`, you will see
![Main_Menu](readme_materials/7.png?raw=true =600x)
7. type `quit` to exit the system.


### Part 6: Test

For test, you should download complete data set from [here](https://www.dropbox.com/sh/lk7ec8gjanuwnhk/AADyjXYQw-8imLqCsw3N8PZaa?dl=0), and delete the sample data set. Go to h1b_exploring and run the test by enter
```
$ python -m unittest [unittest_something].py
```


### Acknowledgement
- Data resource from [Foreign Labor Certification Data Center](https://www.foreignlaborcert.doleta.gov/performancedata.cfm)