'''histogramPlot of storm events served by bokeh serve --show histogramPlot'''

from bokeh.layouts import column
from bokeh.models.widgets import Slider, MultiSelect
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models.formatters import DatetimeTickFormatter

from MonthlyHistogram import MonthlyHistogram

def callback():
    '''A callback function triggered by widget value changes that updates the plotted data'''
    vals = eventTypeList.value
    new_data = dict()
    new_data['x'] = months
    new_data['top'] = histogram.getYearCounts(yearSlider.value,vals)
    p.y_range.start = 0
    p.y_range.end = max(new_data['top'])*1.5
    ds.data = new_data

def main(): 
    '''Creates our bokeh histogram plot of events vs months for a fixed year'''
    global histogram, yearSlider, eventTypeList, p, ds, months
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    file = r'./FilteredData/filteredData.csv'
    histogram = MonthlyHistogram(file)

    #Create plot
    p = figure(x_range=months, y_range=(0, 10000), title="Number of Weather Events Per Month")
    p.yaxis.axis_label = 'Counts'
    p.xaxis.axis_label = 'Months'

    r = p.vbar(x=[],top=[],width=.8)
    ds = r.data_source

    #create widgets
    events = ['Hail','Thunderstorm Wind','Tornado']
    yearSlider = Slider(start=1955,end=2016,value=1955,step=1,title="Event Year")
    eventTypeList = MultiSelect(title="Event Types",value=['Hail'],options=events)
    widgets = [yearSlider,eventTypeList]
    #setup callbacks
    for w in widgets :
        w.on_change('value', lambda attr, old, new: callback())
    #layout gui elements
    curdoc().add_root(column(yearSlider, eventTypeList, p))

#Used by bokeh server
main()
