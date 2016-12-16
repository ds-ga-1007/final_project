'''
This is module which designed for interactions in industry level
This function will automatically return a rank of industry with different indicators

Created on Nov 27, 2016

@author: Yovela
'''
import sys
from h1b_exploring.plot_popular_industry import confirm_answer_ploting
from h1b_exploring.exception_list import wrong_option_exception, wrong_int_exception
from h1b_exploring.All_about_input import option_input

'''
popular_industry(industry_data)
'''

def popular_industry (industry_data):
    
    Flag = True
    while Flag:
        try:
            print ("================================ H1b Visa Approve Rate Exploring ================================")
            print ("")
            print ("                             Please choose ONE Rank you interested in                            ")
            print ("                              <a>  : Application Pull                                            ")
            print ("                              <b>  : Approve Rate                                                ")
            print ("                              <c>  : Average Wage                                                ")
            print ("                              <r>  : Go back to previous directory                               ")  
            print ("")
            print ("=================================================================================================")

            key = option_input()

            if key == 'a':
                user_input  = input("please input number of industries you want to show in this rank, please enter an integer between 5 and 20\n")
                try:
                    if user_input == 'quit':
                        sys.exit(1)
                    else:
                        try:
                            number = int(user_input)
                            if number<=20 and number>= 5:
                                industry_data.occupation_rank(industry_data, number, "application_pool")
                                confirm_answer_ploting(industry_data, number, "application_pool")
                                break
                            else:
                                raise wrong_int_exception
                
                        except wrong_int_exception:
                            print ("Invalid input, please reenter an integer between 5 and 20\n")   
                            
                except wrong_int_exception:
                    print ("Invalid input, please reenter an integer between 5 and 20\n")   
                except KeyboardInterrupt:
                    sys.exit(1)
                except EOFError:
                    sys.exit(1)
                    
            if key == 'b':
                user_input  = input("please input number of industries you want to show in this rank, please enter an integer between 5 and 20\n")
                try:
                    if user_input == 'quit':
                        sys.exit(1)
                    else:
                        try:
                            number = int(user_input)
                            if number<=20 and number>= 5:
                                industry_data.occupation_rank(industry_data, number, "approval_rate")
                                confirm_answer_ploting(industry_data, number, "approval_rate")
                                break
                            else:
                                raise wrong_int_exception
                
                        except wrong_int_exception:
                            print ("Invalid input, please reenter an integer between 5 and 20\n")   
                            
                except wrong_int_exception:
                    print ("Invalid input, please reenter an integer between 5 and 20\n")   
                except KeyboardInterrupt:
                    sys.exit(1)
                except EOFError:
                    sys.exit(1)
                
                
            if key == 'c':
                user_input  = input("please input number of industries you want to show in this rank, please enter an integer between 5 and 20\n")
                try:
                    if user_input == 'quit':
                        sys.exit(1)
                    else:
                        try:
                            number = int(user_input)
                            if number<=20 and number>= 5:
                                industry_data.occupation_rank(industry_data, number, "average_wage")
                                confirm_answer_ploting(industry_data, number, "average_wage")
                                break
                            else:
                                raise wrong_int_exception
                
                        except wrong_int_exception:
                            print ("Invalid input, please reenter an integer between 5 and 20\n")   
                            
                except wrong_int_exception:
                    print ("Invalid input, please reenter an integer between 5 and 20\n")   
                except KeyboardInterrupt:
                    sys.exit(1)
                except EOFError:
                    sys.exit(1)
                
                    
            if key == 'r':
                Flag = False
                
        except wrong_option_exception:
            print ("Invalid option, please reselect.")
            
            
            