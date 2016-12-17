'''Plots aggregate event totals across the years.  Run with bokeh serve --show yearAggregatePlot.py'''

from bokeh.layouts import column
from bokeh.models.widgets import Select
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models.formatters import DatetimeTickFormatter
from YearlyEventAggregator import YearlyEventAggregator

def callback():
    '''Callback triggered when aggregate type is changed'''
    val = eventTypeList.value
    new_data = dict()
    new_data['x'] = list(range(1955,2017))
    new_data['y'] = agg.getAggregate(val)
    p.y_range.start = 0
    p.y_range.end = max(new_data['y'])+500
    ds.data = new_data

def main() :
    '''Creates figures, and sets up widgets'''
    global agg, eventTypeList, p, ds
    file = r'./FilteredData/filteredData.csv'
    agg = YearlyEventAggregator(file)
    # create a plot and style its properties
    p = figure(x_range=(1955,2016), y_range=(0, 10000), title="Variation From Year to Year")
    p.yaxis.axis_label = 'Counts'
    p.xaxis.axis_label = 'Year'
    r = p.line(x=[],y=[])
    ds = r.data_source

    # setup widgets
    options = agg.getKeys()
    eventTypeList = Select(title="Plot Value",value=options[0],options=options)
    widgets = [eventTypeList]
    for w in widgets :
        w.on_change('value', lambda attr, old, new: callback())
    
    curdoc().add_root(column(eventTypeList, p))
    
main()
