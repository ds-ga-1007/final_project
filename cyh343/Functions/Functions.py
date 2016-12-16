'''
The Functions file include the functions which will be use in the Main program.
@author: ChuanYa Hsu
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def stat_player(data, player_id):
         
    '''
    Function stat_player display the simple statistics for score, minutes in game, 
    fantasy score, and fantasy salary 
        
    parameters:
        data:         players database, or other database with more information
        player_id:    the player that user want to examine
        
    return:
        Tables of simple statistics 
    '''
         
    pt = data['pt'].ix[player_id] 
    minutes = data['Minutes'].ix[player_id]   
    pt_DK = data['DKP'].ix[player_id]
    pt_FD = data['FDP'].ix[player_id]
    sal_DK = data['DK.Sal'].ix[player_id]
    sal_FD = data['FD.Sal'].ix[player_id]
    player = str(np.unique(data.ix[player_id]['First.Last'])).lstrip("['").rstrip("']")
      
    print('Information of {0} : \n'.format(player))
    print('Team: ' + str(np.unique(data.ix[player_id]['Team'])).lstrip("['").rstrip("']") )
    print('Average minutes in game: {0} \n'.format(np.mean(minutes)))
         
    print('Scoring Distribution: ')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} \n'.format(np.min(pt), np.max(pt), np.mean(pt), np.std(pt)))
         
    print('Fantasy Scoring Distribution: ')
    print('Draft Kings')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} '.format(np.min(pt_DK), np.max(pt_DK), np.mean(pt_DK), np.std(pt_DK)))
    print('FanDuel')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} \n'.format(np.min(pt_FD), np.max(pt_FD), np.mean(pt_FD), np.std(pt_FD)))
         
    print('Fantasy Salary Distribution: ')
    print('Draft Kings')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} '.format(np.min(sal_DK), np.max(sal_DK), np.mean(sal_DK), np.std(sal_DK)))
    print('FanDuel')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} '.format(np.min(sal_FD), np.max(sal_FD), np.mean(sal_FD), np.std(sal_FD)))
 
 
def plot_player(data, player_id):
        
    '''
    Function plot_player display the scoring history and the fantasy salary change over time for given player.
        
    parameters:
        data:         players database, or other database with more information
        player_id:    the player that user want to examine
        
    return:
        Time series graph for the given player's scores and fantasy salary
    '''
         
    date = pd.to_datetime(data['Date'].ix[player_id], format = "%Y%m%d")
    pt = data['pt'].ix[player_id]    
    sal_DK = data['DK.Sal'].ix[player_id]
    sal_FD = data['FD.Sal'].ix[player_id]
    player = str(np.unique(data.ix[player_id]['First.Last'])).lstrip("['").rstrip("']")
      
    plt.close('all')
    plt.figure(1) 
    plt.plot(date, pt.dropna(), linestyle = '-', color = 'skyblue')  # Tried using year as index, but it seemed that the index is count begin with 1800
    plt.title('The scoring history of {0}'.format(player))
    plt.xlabel('Date')
    plt.ylabel('Score')
      
    plt.figure(2)
    plt.plot(date, sal_DK, linestyle = '-', color = 'skyblue')
    plt.plot(date, sal_FD, linestyle = '-', color = 'forestgreen')
    plt.title('The fantasy salaries of {0}'.format(player))
    plt.xlabel('Date')
    plt.ylabel('Fantasy Salary')
    plt.legend(['Draft Kings salary', 'FanDuel salary'], loc = 'upper left')
      
    plt.show()
     
# stat_player(players, 1449)
# plot_player(players, 1449)

    
def stat_team(data, team):

    '''
    Function stat_team display the simple statistics for score, average minutes in game, 
    fantasy score, and fantasy salary of players in the given team
       
    parameters:
        data:    players database, or other database with more information
        team:    the team that user want to examine
       
    return:
        Tables of simple statistics 
    '''
    data = data.groupby(['Team'])   
    g = data.get_group(team) 
    pt = g['pt']
    minutes = g['Minutes'] 
    pt_DK = g['DKP']
    pt_FD = g['FDP']
    sal_DK = g['DK.Sal']
    sal_FD = g['FD.Sal']    
     
    print('Information of {0} : \n'.format(team))
    print("Players' average minutes in game : {0} \n".format(np.mean(minutes)))
        
    print('Players Scoring Distribution: ')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} \n'.format(np.min(pt), np.max(pt), np.mean(pt), np.std(pt)))
        
    print('Players Fantasy Scoring Distribution: ')
    print('Draft Kings')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} '.format(np.min(pt_DK), np.max(pt_DK), np.mean(pt_DK), np.std(pt_DK)))
    print('FanDuel')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} \n'.format(np.min(pt_FD), np.max(pt_FD), np.mean(pt_FD), np.std(pt_FD)))
        
    print('Players Fantasy Salary Distribution: ')
    print('Draft Kings')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} '.format(np.min(sal_DK), np.max(sal_DK), np.mean(sal_DK), np.std(sal_DK)))
    print('FanDuel')
    print('Min: {0}  Max: {1}  Mean: {2}  Std: {3} '.format(np.min(sal_FD), np.max(sal_FD), np.mean(sal_FD), np.std(sal_FD)))


def plot_team(data, team):
        
    '''
    Function plot_team display the distribution of the given team points and opposite team
    points by bar chart. Also, display the time series graph for the spread of the given team. 
        
    parameters:
        data:    players database, or other database with more information
        team:    the team that user want to examine
        
    return:
        Bar Chart by date for the given and the opposite team points 
        Time series graph for the given player's scores and fantasy salary
    '''
        
    data = data.groupby(['Team'])   
    g = data.get_group(team) 
    date = pd.to_datetime(g['Date'], format = "%Y%m%d")
    pt = g['Team.pts']
    opp_pt = g['Opp.pts']
    spread = -g['Actual.Spread']
    
    plt.close('all')
    plt.figure(1).autofmt_xdate()
    plt.bar(date.values, pt, facecolor='#9999ff', edgecolor='white')    # x-axis cannot be 'TimeStamp'. As the result, using the values of Date
    plt.bar(date.values, -opp_pt, facecolor='#ff9999', edgecolor='white')
    plt.title('Bar chart of the points history for {0} and opposite team'.format(team))
    plt.xlabel('Date')
    plt.ylabel('Points: {0}(Blue) Opposite team(Red)'.format(team))
    plt.ylim(-np.maximum(np.max(pt), np.max(opp_pt))-5, np.maximum(np.max(pt), np.max(opp_pt))+5), plt.yticks([])
    
    plt.figure(2)
    plt.plot(date, spread, linestyle = '-', color = 'blue')
    plt.title('Time Series graph of the spread of {0}'.format(team))
    plt.xlabel('Date')
    plt.ylabel('Spread')
    
    plt.show()
    
# plot_team(players, 'min')    
# stat_team(players, 'min')

def multi_player(data, player_id, var2):
        
    '''
    Function multi_player display the given variable change over time for given player.
        
    parameters:
        data:         players database, or other database with more information
        player_id:    the player that user want to examine
        var2:         given variables, i.e. pt, minutes, FanPt, or FanSal 
        
    return:
        Time series graph for the given player's info
    '''
    
    var2_str = str(var2).lstrip("['").rstrip("']")     
    date = pd.to_datetime(data['Date'].ix[player_id], format = "%Y%m%d")
    var2 = data[var2].ix[player_id]    
    player = str(np.unique(data.ix[player_id]['First.Last'])).lstrip("['").rstrip("']")
      
    plt.close('all')
    plt.plot(date, var2.dropna(), linestyle = '-', color = 'skyblue')  # Tried using year as index, but it seemed that the index is count begin with 1800
    plt.title('The time series of {1} for {0}'.format(player, var2_str))
    plt.xlabel('Date')
    plt.ylabel('{0}'.format(var2_str))
    
    plt.show()
    
    
def multi_team(data, team, var2):
        
    '''
    Function multi_team display the given variable change over time for given team.
        
    parameters:
        data:    players database, or other database with more information
        team:    the team that user want to examine
        var2:    given variables, i.e. pt, minutes, FanPt, or FanSal 
        
    return:
        Bar chart for the given team's info
    '''
    
    if var2 == 'pt':
        var2 = 'Team.pts'
    else:
        var2 = var2
        
    var2_str = str(var2).lstrip("['").rstrip("']")   
    data = data.groupby(['Team'])   
    g = data.get_group(team) 
    date = np.unique(g['Date'])
    date = pd.to_datetime(date, format = "%Y%m%d")
    var2_value = g.groupby(['Date'])[var2].mean()
    
    plt.close('all')
    plt.plot(date.values, var2_value, linestyle = '-', color = 'skyblue')
    plt.title('Bar chart of the {1} of {0}'.format(team, var2_str))
    plt.xlabel('Date')
    plt.ylabel('{0}'.format(var2_str))
    
    plt.show()