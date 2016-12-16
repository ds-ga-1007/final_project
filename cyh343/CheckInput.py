import numpy as np
from Functions.Functions import *

class Check_input():
    def __init__(self, inputstr):
        self.inputstr = inputstr
             
    def singleplayer_input(self, data):
     
        """Function singleplayer_input check whether the input player is correct"""
     
        player = self.inputstr
        if player.isalpha() == False:
            final_input = -9999
             
        else:      
     
            if player[0].isupper() == False:
                temp_input = player[0].upper() + player[1:]  
                if temp_input in str(np.unique(data['Last'])):
                    final_input = temp_input
                else:
                    final_input = -9999
            else: 
                temp_input = player  
                if temp_input in str(np.unique(data['Last'])):
                    final_input = temp_input
                else:
                    final_input = -9999
                
     
        return final_input
         
    def singleteam_input(self, data):
     
        """Function singleteam_input check whether the input team is correct"""
     
        team = self.inputstr
        if team.isalpha() == False:
            final_input = -9999
        else:      
            if len(team) != 3:
                final_input = -9999
            else:
                if team.isupper() == True:
                    final_input = team.lower()    
                else:
                    if str(np.unique(data['Team'])).find(team) == -1:
                        final_input = -9999
                    else:
                        final_input = team
                             
        return final_input
     
    def multi_input(self, data):
         
        """Function multi_input check whether the input variable is available"""
         
        input_list = ['pt','Minutes','FanPt','FanSal']
         
        multiinput = self.inputstr
        if multiinput.isalpha() == False:
            final_input = -9999
        else:    
            if multiinput in input_list:
                multiinput = multiinput
                
                if multiinput == input_list[2]:
                    final_input = ["DKP", "FDP"]
                else:
                    if multiinput == input_list[3]:
                        final_input = ["DK.Sal", "FD.Sal"]
                    else:
                        final_input = [multiinput]
            else:
                final_input = -9999
                                
        return final_input