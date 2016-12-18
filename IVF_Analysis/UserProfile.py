# -*- coding: utf-8 -*-

import PrintFunctions as pt
import InputFunctions as ip

def askAge():
    
    ''' Function to ask for user's age '''
    
    answerIsOk = False
    while answerIsOk is False:       
        try: 
            userAge = ip.delay_input("What's your age? [number]")    
            userAge = ip.wholeNumericPositiveInputParser(userAge)   
            if userAge<18:
                pt.delay_print("Whoa there! I can't accept ages below 18. Aren't you too young? \n")  
                pt.delay_print("Please, re-enter your age as a whole number between 18 and 70 \n") 
                answerIsOk = False
            elif userAge>70:
                pt.delay_print("Whoa there! I can't accept ages above 70. No data available \n")  
                pt.delay_print("Please, re-enter your age as a whole number between 18 and 70 \n") 
                answerIsOk = False
            else: 
                answerIsOk = True
                     
        except ip.negativeInput:
            pt.delay_print("Sorry, I can't accept negative numbers numbers \n")
            pt.delay_print("Please, re-enter your age as a whole number between 18 and 60 \n") 
            pass
        except ip.nonNumericInput:
            pt.delay_print("Sorry, I can only accept numbers \n")
            pt.delay_print("Please, re-enter your age as a whole number between 18 and 60 \n") 
            pass
        except ip.nonIntegerInput:  
            pt.delay_print("Sorry, I can't accept any real number, just whole numbers \n")
            pt.delay_print("Please, re-enter your age as a whole number between 18 and 60 \n")
            pass
    
    return userAge 

def askIsEggDonated():
    answerIsOk = False
    while answerIsOk is False:           
        try:
            donatedEggs = ip.delay_input("Are you using donated eggs? [y/n]")
            donatedEggs = ip.yesNoParser(donatedEggs) 
            answerIsOk = True
        except ip.yesNoParserException: 
            pt.delay_print("Sorry, I didn't get that. \n Remember, that I can understand only yes or no answers \n ")
            pass
    
    return donatedEggs
        
def askIsFresh(option):
    answerIsOk = False
    while answerIsOk is False:           
        try:
            if option is True:
                freshEggs = ip.delay_input("Are you planning to use a fresh embryo (contrary to frozen)? [y/n]")
            else: 
                freshEggs = ip.delay_input("Is your egg fresh (contrary to frozen)? [y/n]")
            freshEggs = ip.yesNoParser(freshEggs) 
            answerIsOk = True
        except ip.yesNoParserException: 
            pt.delay_print("Sorry, I didn't get that. \n Remember, that I can understand only yes or no answers \n ")
            pass    
        
    return freshEggs  

def userQuestions(instructions): 
    
    ''' General functions to ask user questions '''
    
    if instructions is True: 
        pt.delay_print("Let me start by asking some personal questions \n")
        pt.delay_print("This is only to give you the most precise statistics I have \n")
        
    age = askAge()
    isDonnated = askIsEggDonated()
    isFresh = askIsFresh(isDonnated)
    
    return age, isDonnated, isFresh


class identifier(object):
    
    def __init__(self, age, donor, fresh, state):
        self.age = age
        self.donor = donor
        self.fresh = fresh
        self.user_category = self.categorizer()
        self.age_group = self.age_grouper()   
        self.state = state.upper()     
    
    def categorizer(self):
        if self.donor == False and self.fresh == True: 
            self.user_category = (1, 'Fresh Egg Non-Donor')
        elif self.donor == False and self.fresh == False: 
            self.user_category = (2, 'Frozen Egg Non-Donor')

        elif self.donor == True and self.fresh == True: 
            self.user_category = (3, 'Fresh Embryo from Donor Egg')

        elif self.donor == True and self.fresh == False: 
            self.user_category = (4, 'Frozen Embryo from Donor Egg')
        
        return self.user_category

    def age_grouper(self):
        if self.age < 35:
            self.age_group = (1, 'under 35 years old')
            
        elif self.age >= 35 and self.age < 38:
            self.age_group = (2, 'between 35 and 37 years old')
        
        elif self.age >= 38 and self.age < 41:
            self.age_group = (3, 'between 38 and 40 years old')
        
        elif self.age >= 41 and self.age < 43:
            self.age_group = (4, 'between 41 and 42 years old')
        
        elif self.age >= 43 and self.age <= 44:
            self.age_group = (5, 'between 43 and 44 years old')
        else:
            self.age_group = (6 , '45 and older')
        
        return self.age_group  
   
    def total_cycles_plot(self):
        if self.user_category[0] == 1:   #FshND
            self.to_plot = '{var}{age}'.format(var='FshNDCycle',age=self.age_group[0])
        
        elif self.user_category[0] == 2:   #ThwND
            self.to_plot = '{var}{age}'.format(var='ThwNDTotCycles',age=self.age_group[0])

        elif self.user_category[0] == 3:  #FshDn
            self.to_plot = '{var}'.format(var='FshDnrTotCycles')

        elif self.user_category[0] == 4:    #ThwDn
            self.to_plot = '{var}'.format(var='ThwDnrTotCycles')

        return self.to_plot

    def live_births_transfer_plot(self):
        if self.user_category[0] == 1:   #FshND
            self.to_plot = '{var}{age}'.format(var='FshNDLvBirths_TransRate',age=self.age_group[0])
            
        elif self.user_category[0] == 2:   #ThwND
            self.to_plot = '{var}{age}'.format(var='ThwNDLvBirths_TransRate',age=self.age_group[0])
        
        elif self.user_category[0] == 3:  #FshDn
            self.to_plot = '{var}'.format(var='FshDnrLvBirths_TransRate')

        elif self.user_category[0] == 4:    #ThwDn
            self.to_plot = '{var}'.format(var='ThwDnrLvBirths_TransRate')

        return self.to_plot
    
    def main_variable_early(self):
        if self.user_category[0] == 1:
            for i in range(1,6):
                if self.age_group[0] == i:
                    variable = 'FshNDLvBirthsRate'+ str(i) 
                elif self.age_group[0] == 6:
                    variable = None

        elif self.user_category[0] == 2:
            for i in range(1,6):
                if self.age_group[0] == i:
                    variable = 'ThwNDLvBirthsRate'+ str(i) 
                elif self.age_group[0] == 6:
                    variable = None

     
        elif self.user_category[0] == 3:
            variable = 'FshDnrLvBirthsRate'

    
        elif self.user_category[0] == 4:
            variable = 'ThwDnrLvBirthsRate' 
        
        self.variable = variable
        return self.variable

    def main_variable_late(self):
            
        if self.user_category[0] == 1:
            for i in range(1,7):
                if self.age_group[0] == i:
                    variable = 'FshNDLvBirths_TransRate' + str(i)


        elif self.user_category[0] == 2:
            for i in range(1,7):
                if self.age_group[0] == i:
                    variable = 'ThwNDLvBirths_TransRate' + str(i) 

     
        elif self.user_category[0] == 3:
            variable = 'FshDnrLvBirths_TransRate'

        elif self.user_category[0] == 4:
            variable =  'ThwDnrLvBirths_TransRate'

        self.variable = variable
        return self.variable