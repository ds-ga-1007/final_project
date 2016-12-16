# Predicting Income Using Demographic Variables

Final project by Zimu Li (zl1271)

## User Guide

This program explores the relationship between income, age, education, sex, and race.

### Launch

Run 'main.py' with python from shell.

### Quit

Whenever you are prompted for answer, entering 'quit' will terminate the program.
### Use

On each step, the program will output instructions and prompt for user input. When regression models were created, a summary file with the regression formula as the title will be created in '.\Results'. When plots were predicted, the figure will be shown and saved in '.\Results\Plots'. 

1. On the first level, there are 'all' and 'explore'.
   1. Entering 'all' runs the full model (see the below section 'Background' for more details), and creates a .txt file to save the result.
   2. Entering 'explore' leads you to the second level and enables you the run varies explorations of the dataset.
2. On the second level, there are 'describe' and 'regression'.
   1. Entering 'describe' lets you see a boxplot of income of all cases ('all'), or boxplots of income's distribution across the different values of your entered variable ('sex', 'race', 'age', and 'educ').
   2. Entering 'regression' leads you to the third level.
3. On the third level, you can choose one predictor to predict income of all cases ('all'), if the predictor is continuous, a plot will be created; or choose one predictor to predict income of a specific group (e.g., all female participants, all male participants, white people, black, and others)

## Background

### Data Source

The General Social Survey (2014), retrieved from http://gss.norc.org/

> The GSS gathers data on contemporary American society in order to monitor and explain trends and constants in attitudes, behaviors, and attributes. Hundreds of trends have been tracked since 1972. In addition, since the GSS adopted questions from earlier surveys, trends can be followed for up to 70 years.
>
> The GSS contains a standard core of demographic, behavioral, and attitudinal questions, plus topics of special interest. Among the topics covered are civil liberties, crime and violence, intergroup tolerance, morality, national spending priorities, psychological well-being, social mobility, and stress and traumatic events.

### The Present Study 

The aim is to identify predictors of individual income ('conrinc': inflation-adjusted personal income). It is hypothesized that income can be predicted by sex, race, age, and years of education ('educ'). Thus, the full model includes all of the above mentioned predictors. Moreover, since the 'conrinc' variable is not exactly continuous(it is ordinal, but from 0 to 80000 was equal interval), a variable 'high_inc' is created to address the issue ('0' for smaller than 80000, '1' for higher). 

By running the full model,  this study wants to see if there are gender and/or race inequality in income, test the effect of age and education, as well as the interactions.

By running the partial models and descriptive plotting functions, this program can also provide more intuitive results. 





