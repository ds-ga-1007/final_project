import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Functions.Functions import *
from CheckInput import *


# Import original database:
# Since it is better that the dataset can be import automatically, we set a changeable root
PATH = "C:\\Users\\NYU\\Dropbox\\2016Fall\\ProgrammingforDS\\FinalProject\\cyh343\\"
players = pd.read_excel(PATH + "players_w_spreads.xlsx", index_col = 2) # The index of the dataset is player id 
# print(players.head())

data = players # The data use in main program

def main():
    
    """
    main program to run by user, input 'Q' to quit program.
     
    There are two main steps, first, user chooses what action he/she want. There are four
    options:
        S:    Single Variable,
        M:    Multiple Variables,
        A:    Adding New Database, or
        Q:    Quit the program
        
    After choosing one of them, the following action will occur:
        S:    Choose a variable, then display the basic information, scoring history, and
              fantasy salaries change of the given variable
        M:    Choose two variable, the first variable should be Player Name or Team; the 
              second variable can be pt, minutes, fantasy pt, or fantasy salaries. Then 
              display the time series graph of second variable for the given Player/Team
        A:    Enter the path of the new dataset, then merge the new dataset to the original
              database
    """
           
    user_input = input('Choose the action you want to operate: (S:SingleVariable M:MultipleVariables A:AddingDatabase Q:quit) \n')
       
    while user_input != 'Q':
        
        # Single Variable condition        
        while user_input == 'S':
            user_input = input('Choose a name of team (player) or enter Q to quit: \n')
            if user_input == 'Q':
                break
            
            while user_input != 'Q':
                check = Check_input(user_input)
                
                # Team case
                if check.singleteam_input(data) == user_input:
                    stat_team(data, user_input)
                    plot_team(data, user_input)
                    user_input = input('Choose a name of team (player) or enter Q to quit: \n')
            
                else:
                    # Player case
                    if check.singleplayer_input(data) == user_input:   
                        player_id = data[data['Last'] == user_input].index[0]
                        stat_player(data, player_id)
                        plot_player(data, player_id)
                        user_input = input('Choose a name of team (player) or enter Q to quit: \n')

                    else:
                        print('Invalid Player or Team')
                        user_input = input('Choose a name of team (player) or enter Q to quit: \n')
        
        # Multiple Variable condition         
        while user_input == 'M':
            user_input = input('Select two variables. Press enter to the next step or enter Q to quit:')
            if user_input == 'Q':
                break
            
            while user_input != 'Q':
                user_input1 = input('Name of team/player: ')
                user_input2 = input('Select from [pt/Minutes/FanPt/FanSal]  ')
               
                # Check if the second input is valid. If is, separate into two case: pt/Minutes and FanPt/FanSal 
                check2 = Check_input(user_input2)
                var2 = check2.multi_input(data)
                if var2 == -9999:
                    print('Invalid input. Please follow the options show below.')
                    user_input1 = input('Name of team/player: ')
                    user_input2 = input('Select from [pt/Minutes/FanPt/FanSal]  ')
                    
                else:
                    
                    # pt/Minutes case
                    if len(var2) == 1:
                        check = Check_input(user_input1)
                        # Team case
                        if check.singleteam_input(data) == user_input1:
                            team = user_input1
                            multi_team(data, team, var2)
                            user_input = input('Select two variables. Press enter to the next step or enter Q to quit:')
                            
                        else:
                            # Player case
                            if check.singleplayer_input(data) == user_input1:    
                                player_id = data[data['Last'] == user_input1].index[0]
                                multi_player(data, player_id, var2)
                                user_input = input('Select two variables. Press enter to the next step or enter Q to quit:')
                                
                            else:
                                print('Invalid name of team or player')
                                user_input1 = input('Name of team/player: ')
                                user_input2 = input('Select from [pt/Minutes/FanPt/FanSal]  ')
                
                    # FanPt/FanSal case
                    elif len(var2) == 2:
                        check = Check_input(user_input1)
                        # Team case
                        if check.singleteam_input(data) == user_input1:
                            team = user_input1
                            multi_team(data, team, var2[0])
                            multi_team(data, team, var2[1])
                            user_input = input('Select two variables. Press enter to the next step or enter Q to quit:')
                            
                        else:
                            # Player case
                            if check.singleplayer_input(data) == user_input1:    
                                player_id = data[data['Last'] == user_input1].index[0]
                                multi_player(data, player_id, var2[0])
                                multi_player(data, player_id, var2[1])
                                user_input = input('Select two variables. Press enter to the next step or enter Q to quit:')
                            
                            else:
                                print('Invalid name of team or player')
                                user_input1 = input('Name of team/player: ')
                                user_input2 = input('Select from [pt/Minutes/FanPt/FanSal]  ')

        # Adding data condition                 
        while user_input == 'A':
            user_input = input('Enter the path of the new file or enter Q to quit:\n')
            if user_input == 'Q':
                break
            # Adding .csv file 
            while user_input != 'Q':
                if user_input[-3:] == 'csv':
                    new_data = pd.read_csv(user_input) # Read the .csv file
                    new_data['GID'] = new_data.index # Set player id as index
                    temp = pd.merge(data, new_data, how = 'outer')
                    temp.to_excel('players_new.xlsx')
                    user_input = input('Enter the path of the new file or enter Q to quit:\n')
                    
                else:
                    # Adding .xlsx file
                    if user_input[-4:] =='xlsx':
                        new_data = pd.read_excel(user_input) # Read the .xlsx file
                        new_data['GID'] = new_data.index
                        temp = pd.merge(data, new_data, how = 'outer')
                        temp.to_excel('players_new.xlsx')
                        user_input = input('Enter the path of the new file or enter Q to quit:\n')
                        
                    else:
                        print('Invalid file type')
                        user_input = input('Enter the path of the new file or enter Q to quit:\n')
                    
        user_input = input('Choose the action you want to operate: (S:SingleVariable M:MultipleVariables A:AddingDatabase Q:quit) \n')
              
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by the keyboard')