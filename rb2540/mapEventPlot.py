'''Map plot of storm events across the US run with bokeh serve --show mapEventPlot.py'''

from bokeh.sampledata import us_states
from bokeh.layouts import column
from bokeh.models.widgets import Slider, MultiSelect
from bokeh.palettes import RdYlBu3
from bokeh.plotting import figure, curdoc
from bokeh.models.formatters import DatetimeTickFormatter

from MapDataSelector import MapDataSelector

# create a callback that will add a number in a random location
def callback():
    '''Triggered by widget on value change'''
    vals = eventTypeList.value
    data = mapData.getYearData(yearSlider.value,vals)
    new_data = dict()
    new_data['x'] = data[0]
    new_data['y'] = data[1]
    ds.data = new_data

def main() :
    global eventTypeList, yearSlider, mapData, us_states, ds
    file = r'./FilteredData/filteredData.csv'
    mapData = MapDataSelector(file)
    events = ['Hail','Thunderstorm Wind','Tornado']

    #loads map data for states
    us_states = us_states.data.copy()
    del us_states["HI"]
    del us_states["AK"]
    state_xs = [us_states[code]["lons"] for code in us_states]
    state_ys = [us_states[code]["lats"] for code in us_states]

    #setup map plot
    p = figure(title="US Weather Events", toolbar_location="left",
    plot_width=1100, plot_height=700)
    p.patches(state_xs, state_ys, fill_alpha=0.0,line_color="#884444", line_width=2)
    r = p.circle_cross(x=[],y=[],size=5,color='red')
    ds = r.data_source

    # add a button widget and configure with the call back
    yearSlider = Slider(start=1955,end=2016,value=1955,step=1,title="Event Year")
    eventTypeList = MultiSelect(title="Event Types",value=events,options=events)
    widgets = [yearSlider,eventTypeList]
    for w in widgets :
        w.on_change('value', lambda attr, old, new: callback())

    curdoc().add_root(column(yearSlider,eventTypeList,p))


main()
