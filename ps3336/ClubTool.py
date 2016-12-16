import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class ClubTool:
    
    def club_basic(club,save,dataset):
        data = dataset
        club_data = data[data['club'] == club]
        
        club_data_year14 = club_data[club_data['year'] == 2014]
        club_data_year15 = club_data[club_data['year'] == 2015]
        club_data_year16 = club_data[club_data['year'] == 2016]
        
        investment_out_sum14 = club_data_year14['transfer_fee_pounds_int'][club_data_year14['transfer_status'] == 'out'].sum()
        investment_in_sum14 = club_data_year14['transfer_fee_pounds_int'][club_data_year14['transfer_status'] == 'in'].sum()
        investment_out_sum15 = club_data_year15['transfer_fee_pounds_int'][club_data_year15['transfer_status'] == 'out'].sum()
        investment_in_sum15 = club_data_year15['transfer_fee_pounds_int'][club_data_year15['transfer_status'] == 'in'].sum()
        investment_out_sum16 = club_data_year16['transfer_fee_pounds_int'][club_data_year16['transfer_status'] == 'out'].sum()
        investment_in_sum16 = club_data_year16['transfer_fee_pounds_int'][club_data_year16['transfer_status'] == 'in'].sum()
        
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 6)
        bar1 = ax.bar(1.1, investment_out_sum14, 0.5, color = 'palegreen', label = 'Transfer in' )
        bar2 = ax.bar(1.65, investment_in_sum14, 0.5, color = 'dodgerblue',label = 'Transfer out')
        bar3 = ax.bar(2.65, investment_out_sum15, 0.5, color = 'palegreen' )
        bar4 = ax.bar(3.20, investment_in_sum15, 0.5, color = 'dodgerblue')
        bar5 = ax.bar(4.20, investment_out_sum16, 0.5, color = 'palegreen')
        bar6 = ax.bar(4.75, investment_in_sum16, 0.5, color = 'dodgerblue')
        
        ax.set_title('Capital Flow of ' + club + ' in 3 years')
        plt.xticks((1.60, 3.15, 4.70), ('2014', '2015','2016'))
        plt.legend()
        plt.show()
        
        if save == 'y':
            fig.savefig('Tha basic information of' + club +' over years.pdf')

    def club_investment_max_player(club, year,dataset):
        data = dataset
        club_data = data[data['club'] == club]
        club_data_year = club_data[club_data['year'] == year]
        club_data_year = club_data_year.drop_duplicates(['p_name'], keep='last')
        
        club_data_year['multiplier'] = 0
        g = club_data['transfer_fee_pounds_int'].groupby([club_data['transfer_status'],club_data['year']]) 
        club_data_year['multiplier'][club_data_year['transfer_status'] == 'in'] = club_data_year['transfer_fee_pounds_int']/g.mean()['in'][year]
               
        info = club_data_year.loc[club_data_year['multiplier'][club_data_year['transfer_status'] == 'in'].idxmax()]
        return info

    def club_investment_on_position(club, year, save,dataset):
        data = dataset
        club_data = data[data['club'] == club]
        club_data_year = club_data[club_data['year'] == year]
        
        df = club_data_year['transfer_fee_pounds_int'].groupby([club_data_year['transfer_status'],club_data_year['position']]) 
        df.sum()['in']
        
        fig = plt.figure()
        labels = 'MidField', 'Forward', 'Back'
        colors = ['yellowgreen', 'gold', 'lightskyblue']
        explode = (0, 0.1, 0)  # only "explode" the 2nd slice (i.e. 'Forward')
    
        
        plt.pie(df.sum()['in'], explode=explode, labels = labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=90)
       
        plt.axis('equal')
        ax = fig.gca()
        plt.show()
        
        if save == 'y':
            fig.savefig('Decomposition of ' + club +"'s Investment on positions.pdf")

        
    def club_investment_max_player_year(club,info,save,dataset):
        data = dataset
        fig = plt.figure()
        player14 = ClubTool.club_investment_max_player(club, 2014,dataset)
        player15 = ClubTool.club_investment_max_player(club, 2015,dataset)
        player16 = ClubTool.club_investment_max_player(club, 2016,dataset)
        
        year = ('2014: '+ player14['p_name'], 
                '2015: '+ player15['p_name'], 
                '2016: '+ player16['p_name'])
        y_pos = np.arange(len(year))
        performance = [player14[info],player15[info],player16[info]]
    
        plt.barh(y_pos, performance, align='center', alpha=0.4, color=['goldenrod','lightseagreen','blueviolet'])
        plt.yticks(y_pos, year)
        plt.xlabel('Performance')
        plt.title( info +" of each year's most expensive player" )
        plt.show()
        
        if save == 'y':
            fig.savefig('Three year comparison on' + info +' of most expensive player.pdf')

    def investment_gain_loss(year,save,dataset):
        data = dataset
        year_data = data[data['year']== year]
        grouping = year_data['transfer_fee_pounds_int'].groupby([year_data['transfer_status'], year_data['club']]) 
        grouping2 = year_data['transfer_status'].groupby(year_data['club']) 
        l_in = grouping.sum()['in']
        l_out = grouping.sum()['out']
        l_freq = grouping2.count()
        df = pd.concat([l_in, l_out, l_freq], axis=1)
        df.columns = ['in', 'out','freq']
        df= df.fillna(0)
        fig, ax = plt.subplots()
        fig.set_size_inches(10, 10)
        colors = np.random.rand(19)
        area = 5*df['freq']  
        labels = df.index.values
        X = np.log(df['in'])
        Y = np.log(df['out'])
        ax.scatter(X, Y, c=colors, s=area,alpha=0.5)
        for label, x, y in zip(labels, X, Y):
            plt.annotate(label, xy = (x, y), xytext = (-20, 20),textcoords = 'offset points' , ha = 'left', va = 'bottom',)
        
        ax.set_xlabel(r'Log Transfer Cost', fontsize=20)
        ax.set_ylabel(r'Log Transfer Profit', fontsize=20)
        ax.set_title('Club Investment Gain v.s. Loss\n Transfer frequency as size', fontsize=20)
    
        ax.grid(True)
        fig.tight_layout()
        plt.show()
        if save == 'y':
            fig.savefig('Investment Gain vs Loss of year' + year + '.pdf')