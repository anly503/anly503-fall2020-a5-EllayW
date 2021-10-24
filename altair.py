# -*- coding: utf-8 -*-
"""
Created on Sat Oct 23 10:11:26 2021

@author: Ella
"""

import plotly.io as pio
pio.renderers.default='browser'
import altair as alt
import pandas as pd
import numpy as np

# read the data
df = pd.read_csv('plot-data.csv')
df['consumption(B)'] = np.round(df['consumption']/1000000000,3)
df1 = df.groupby(['Month','house','appliance','time'],as_index = False).agg({'consumption(B)':'sum','house':'last',\
                                       'Month':'last','appliance':'last',\
                                           'Weekday':'last','time':'last'})
#df_04 = df1.loc[df1.house == 4,:]
df1.Month = df1.Month.astype('category')
df1.Weekday = df1.Weekday.astype('category')
df1.time = df1.time.astype('category')


## sort classes
weekdays = ["Monday","Tuesday","Wednesday",\
            "Thursday","Friday","Saturday","Sunday"]
    
## choose selector
click = alt.selection_multi(encodings=['color'])
click2 = alt.selection_multi(encodings=['x'])

## Bar plot 1
chart1 = alt.Chart(df1).mark_bar().encode(
    x=alt.X('Weekday:N',sort = weekdays),
    y=alt.Y('sum(consumption(B)):Q', stack=None),
    color= alt.Color(
            'house:N',
            scale=alt.Scale(scheme='accent'),\
        legend=alt.Legend(orient="left")),
     tooltip=['sum(consumption(B)):Q','house:N']
).properties(
    width=250,
    height=250
).add_selection(
    click
).add_selection(
    click2
).transform_filter(
    click & click2
).properties(width=140,title = 'Total Consumption by Weekday')

## Bar plot2
chart2 = alt.Chart(df1).mark_bar().encode(
    y=alt.Y('appliance:N'),
    x=alt.X('sum(consumption(B)):Q', stack=None),
    color= alt.Color(
            'house:N',
            scale=alt.Scale(scheme='accent'),\
        legend=alt.Legend(orient="left")),
).add_selection(
    click
).add_selection(
    click2
).transform_filter(
    click & click2
).properties(width=140,height = 250,title = 'Total Consumption by Appliances')

## Line plot 1
chart3 = alt.Chart(df1).mark_line(point=True).encode(
    x=alt.X('time:N'),
    y='sum(consumption(B)):Q',
    color=alt.Color('house:N',
    legend = None),
    tooltip=['sum(consumption(B)):Q','house:N']
).add_selection(
    click
).add_selection(
    click2
).transform_filter(
    click & click2
).properties(width=140,height = 250,title = 'Total Consumption by Daily Period')

    
## combined plot
final_chart =  chart2 | chart3 | chart1

final_chart.properties(title = 'Total Consumption'
                      ).configure_title(orient='top',anchor='middle')

final_chart.save('altair.html')

final_chart