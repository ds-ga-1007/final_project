import pandas as pd
import numpy as np
import plotly.plotly as py
import plotly.graph_objs as go 
import plotly 
plotly.offline.init_notebook_mode()
from plotly import tools
import matplotlib.pyplot as plt

'''
This module contains a class defined by us called plot
Class plot contains 8 functions. 
Each function returns a plot according to feature, countries, years, and graph types selected by the user.
'''
class plot():
    '''
    Initiate attributes 
    df is a dataframe of feature which is selected by the user
    country is a list of countries selected by the user
    year is a list of years selected by the user
    '''
    def __init__(self,df,country,year):
        self.df = df
        self.country = country
        self.year = year
    
    '''
    Function time_series_plot returns a time-series plot
    for one country or several countries in a selected year
    '''
    def time_series_plot(self):
        specs = [[{}]]*len(self.country)
        fig = tools.make_subplots(rows=len(self.country), cols=1, specs=specs,
                        shared_xaxes=True, shared_yaxes=True,
                        vertical_spacing=0.001)
        
        for i in range(0,len(self.country)):
            trace = go.Scatter(x=self.df.index, y=self.df[self.country[i]],name = self.country[i])
            fig.append_trace(trace, len(self.country)-i, 1)

        layout = dict(
            title = 'Time Series Plot for Countries Selected' ,
            xaxis=dict(
                rangeslider=dict(),
                type='year'
            )
            )
        fig['layout'].update(layout)
        plotly.offline.iplot(fig)
        
    '''
    Function bar_plot returns a bar plot for countries in selected years
    '''
    def bar_plot(self):
        data = []
        for i in range(0,len(self.year)):
            trace = go.Bar(
                x=self.country,
                y=self.df.loc[self.year[i]][self.country],
                name = self.year[i]
            )
            data.append(trace)
        layout = go.Layout(
            title = 'Bar Plot for Countries Selected in'+str(self.year),
            xaxis=dict(tickangle=-45),
            barmode='group',
        )

        fig = go.Figure(data=data, layout=layout)
        plotly.offline.iplot(fig)
        
    '''
    Function scatter_plot returns a scatter plot
    '''
    def scatter_plot(self):
        data = []
        for i in range(0,len(self.country)):
            trace = go.Scatter(
                x=self.df[self.country[i]],
                y=self.df.loc[self.year][self.country[i]],
                name = self.country[i],
                mode = 'markers',
                marker = dict(
                    size = 10,
                    line = dict(
                    width = 2,
                    color = 'rgb(0, 0, 0)'
                    )
                )
            )
            data.append(trace)
        layout = dict(title = 'Scatter Plot for Countries Selected in'+str(self.year),
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )

        fig = go.Figure(data = data, layout=layout)
        plotly.offline.iplot(fig)
        
    '''histogram'''
    def histogram(self):
        x0 = self.df.values.flatten()
        trace = go.Histogram(
            x=x0,
            histnorm='probability',
            opacity = 0.75
            )
        layout = dict(title = 'Histogram for Feature Selected',
              yaxis = dict(zeroline = False),
              xaxis = dict(zeroline = False)
             )
        data = [trace]
        fig = go.Figure(data=data, layout=layout)
        plotly.offline.iplot(fig)
       
    def boxplot_year(self):      
        data = []
        for i in range(0,len(self.year)):
            trace = go.Box(y=self.df.loc[self.year[i]],name = self.year[i])
            data.append(trace)
        layout = dict(
            title='Boxplot according to Years',
            )
        fig = go.Figure(data = data, layout = layout)
        plotly.offline.iplot(fig)

    '''
    Function
    '''        
    def boxplot_country(self):
        data = []
        for i in range(0,len(self.country)):
            trace = go.Box(y=self.df[self.country[i]],name = self.country[i])
            data.append(trace)
        layout = dict(
            title='Boxplot according to Countries',
            )
        fig = go.Figure(data = data, layout = layout)
        plotly.offline.iplot(fig)

    '''
    Function heatmap returns a heatmap, whose y-axis is selected years and x-axis is selected countries
    '''        
    def heatmap(self):
        z = []
        for i in range(0,len(self.year)):
            data = []
            for j in range(0,len(self.country)):
                data.append(self.df.loc[self.year[i]][self.country[j]])
            z.append(data)
        
        data1 = [
            go.Heatmap(
                z=z,
                x=self.country,
                y=self.year
            )
        ]
        layout = dict(
            title='Heatmap for Selected Countries and Years',
            )
        fig = go.Figure(data = data1, layout = layout)
        plotly.offline.iplot(fig)

    '''
    Reference: https://plot.ly/python/heatmaps/
    Function choropleth returns a heatmap of one-year feature for selected countries
    '''        
    def choropleth(self):
        layout = dict(
            title = 'Choropleth Map',
            geo = dict(
                showframe = False,
                showcoastlines = False,
                projection = dict(
                    type = 'Mercator'
                )
            )
        )

        for i in range(0,len(self.year)):
            data = []
            data = [ dict(
                    type = 'choropleth',
                    locations = self.country,
                    z = self.df.loc[self.year[0]][self.country],
                    text = self.country,
                    colorscale = [[0,"rgb(5, 10, 172)"],[0.35,"rgb(40, 60, 190)"],
                                  [0.5,"rgb(70, 100,245)"],\
                                  [0.6,"rgb(90, 120, 245)"],[0.7,"rgb(106, 137, 247)"],
                                  [1,"rgb(220, 220,220)"]],
                    autocolorscale = False,
                    reversescale = True,
                    marker = dict(
                        line = dict (
                            color = 'rgb(180,180,180)',
                            width = 0.5
                        )),
                    colorbar = dict(
                        autotick = False,
                        tickprefix = '$',
                        title = 'Selected Feature'),
                )]
            fig = dict(data=data, layout=layout )
            plotly.offline.iplot(fig, validate=False)
    def pie_chart(self):
        fig = plt.figure()
        ax = fig.gca()
        for i in range(0,len(self.year)):
            size = self.df.loc[self.year[i]][self.country]
            size[np.isnan(size) == True] = 0
            plt.pie(size,labels = self.country, autopct = '%1.1f%%', shadow = True, startangle = 90)
            plt.title('Pie Chart for Year'+ str(self.year[i]))
            plt.axis('equal')
            plt.show()
    #gives pie_plot