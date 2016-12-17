import pandas as pd
from yeartool import *
from PositionTool import *
from ClubTool import *
import sys
import warnings

if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    dataset = pd.read_csv("finaldata.csv")
    while(True):
        try:
            option = input("Welcome to the soccer transfer market data tool! Please enter your option to start:[Year, Club, Position] ")
            if option =="quit":
                print ("Thank you!")
                sys.exit(1)
                break
            elif option not in ["Year","Club","Position"]:
                raise ValueError
            elif option =="Year":
                while(True):
                    try: 
                        year = input("We have data available 2014-2016. Please select: ")
                        if year == 'quit':
                            print ("Thank you!")
                            sys.exit(1)
                            break
                        elif year.isdigit() and int(year) >= 2014 and int(year) <= 2016:
                            year = int(year)
                            tool = yeartool(year,dataset)
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print ('invalid input')
                    except KeyboardInterrupt:
                        print ("user quit")
                while(True):
                    try:
                        category = input("Please select from [Age, Transfer Fee, Position, Investment Return]: ")
                        if category =="quit":
                            print ("Thank you!")
                            sys.exit(1)
                            break
                        elif category in ['Age', 'Transfer Fee', 'Position', 'Investment Return']:
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print ('invalid input')
                    except KeyboardInterrupt:
                        print ("user quit")
                while(True):
                    try: 
                        save = input('Do you want to save the visualization? [y or n]: ')
                        if save in ['y', 'n']:
                            break
                        else:
                            raise ValueError
                    except ValueError:
                        print ('invalid input')
                    except KeyboardInterrupt:
                        print ("user quit")
                if category == "Age":
                    tool.income_age_dist(save)
                    tool.out_age_dist(save)
                elif category == "Transfer Fee":
                    tool.transfer_fee_amount(save)
                elif category == "Position":
                    tool.position_table()
                elif category == "Investment Return":
                    tool.investment_return(save)
            elif option == 'Position':
                while(True):
                    input_position = input('Please input the position you are interested, choose from [Forward, Back, Midfield]')
                    if input_position == 'quit':
                        print("Thank you!")
                        sys.exit(1)
                        break
                    elif input_position in dataset['position'].unique():
                        break
                    else:
                        print('Please choose from [Forward, Back, Midfield]')
                data_interested = dataset[dataset['position'] == input_position]
                while(True):
                    category = input('Please select from [Age, Transfer Fee, Number of Transfers, Investment Return]: ')
                    if category == 'quit':
                        sys.exit(1)
                    elif category in ['Age', 'Transfer Fee', 'Number of Transfers', 'Investment Return']:
                        break
                    else:
                        print('Please select from [Age, Transfer Fee, Number of Transfers, Investment Return]: ')
                while(True):
                    save = input('Do you want to save the visualization? [y or n]: ')
                    if save in ['y', 'n']:
                        break
                    else:
                        print('Please enter y or n')
                if category == 'Age':
                    PositionTool.age_distribution(data_interested, input_position, save)
                elif category == 'Transfer Fee':
                    PositionTool.transfer_fee_box(data_interested, input_position, save)
                elif category == 'Number of Transfers':
                    PositionTool.num_transfer(data_interested, input_position, save)
                elif category == 'Investment Return':
                    PositionTool.invest_on_return(data_interested, input_position, save)
        
            elif option == 'Club':
                while(True):
                    input_club = input('Please choose the club you want to explore, Please use the standard full name of the club: ')
                    if input_club == 'quit':
                        print("Thank you!")
                        sys.exit(1)
                        break
                    elif input_club in dataset['club'].unique():
                        break
                    else:
                        print(dataset['club'].unique())
                        print('Please check again you input, make sure you choose from this list above')
                
                while(True):
                    category = input('Please select a category below (Input Keywords Only): \nClub Investment Basics [basics] \nMost Expensive Player [player] \nComparison of most expensive Player over 3 years [comparison] \nInvestment Decomposition on Position [decomposition] \nInvestment Gain Loss overview [overview] \n')
                    if category == 'quit':
                        sys.exit(1)
                    elif category in ['basics', 'player', 'comparison', 'decomposition','overview']:
                        break
                    else:
                        print('Please select from a category below (Use keywords in the bracket): \nClub Investment Basics [basics] \nMost Expensive Player [player] \nComparison of most expensive Player over 3 years [comparison] \nInvestment Decomposition on Position [decomposition] \nInvestment Gain Loss overview [overview] \n')
                while(True):
                    save = input('Do you want to save the visualization? [y or n]: ')
                    if save in ['y', 'n']:
                        break
                    else:
                        print('Please enter y or n: ')
                if category == 'basics':
                    ClubTool.club_basic(input_club, save,dataset)
                
                elif category == 'overview':
                     while(True):
                        try: 
                            input_year = input('Please choose a year you want to explore: ')
                            if input_year == 'quit':
                                sys.exit(1)
                                break
                            elif input_year.isdigit() and int(input_year)>=2014 and int(input_year)<=2016:
                                ClubTool.investment_gain_loss(int(input_year),save,dataset)
                                break
                            else:
                                print()
                                raise ValueError
                        except ValueError:
                            print ('invalid input')
                        except KeyError:
                            print("No Data Available For This Year")   
                
                elif category == 'player':
                    while(True):
                        try: 
                            input_year = input('Please choose a year you want to explore: ')
                            if input_year == 'quit':
                                sys.exit(1)
                                break
                            elif input_year.isdigit() and int(input_year)>=2014 and int(input_year)<=2016:
                                print(ClubTool.club_investment_max_player(input_club, int(input_year),dataset))
                                break
                            else:
                                raise ValueError
                        except ValueError:
                            print ('invalid input')
                        except KeyError:
                            print("No Data Available For This Club This Year")
                    
                elif category == 'comparison':
                    while(True):
                        try: 
                            input_info = input('Please choose from below a statistic you want to compare \n[age,assists,goals,matches,minutes] \n')
                            if input_info == 'quit':
                                sys.exit(1)
                                break
                            elif input_info in ['age','assists','goals','matches','minutes']:
                                ClubTool.club_investment_max_player_year(input_club,input_info,save,dataset)
                                break  
                            else: 
                                raise ValueError
                        except ValueError:
                            print ('invalid input')
                        except KeyError:
                            print("No Data Available")
                                    
                
                elif category == 'decomposition':
                    while(True):
                        try: 
                            input_year = input('Please choose a year you want to explore: ')
                            if input_year == 'quit':
                                sys.exit(1)
                                break
                            elif input_year.isdigit() and int(input_year)>=2014 and int(input_year)<=2016:
                                ClubTool.club_investment_on_position(input_club, int(input_year),save,dataset)
                                break  
                            else: 
                                raise ValueError
                        except ValueError:
                            print ('invalid input')
                        except KeyError:
                            print("No Data Available")
           
                                                                             
                    
        except ValueError:
            print ('invalid input')
        except KeyboardInterrupt:
            print ("user quit")
            sys.exit(1)
