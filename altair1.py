#!/usr/bin/env python
# coding: utf-8

# In[120]:


import altair as alt
import pandas as pd
import numpy as np
import os


# In[107]:


df = pd.read_csv('plot-data.csv')
df['consumption(B)'] = np.round(df['consumption']/1000000000,3)
df1 = df.groupby(['Month','house','appliance','time'],as_index = False).agg({'consumption(B)':'sum','house':'last',                                       'Month':'last','appliance':'last',                                           'Weekday':'last','time':'last'})
#df_04 = df1.loc[df1.house == 4,:]
df1.Month = df1.Month.astype('category')
df1.Weekday = df1.Weekday.astype('category')
df1.time = df1.time.astype('category')

click = alt.selection_multi(encodings=['color'])
click2 = alt.selection_multi(encodings=['x'])
#selection = alt.selection_multi(fields=['time'],encodings=['color'])
color = alt.condition(click,
                      alt.Color('time:N', 
                                legend=None,
                                scale=alt.Scale(scheme='accent')),
                      alt.value('white'))


# In[108]:


weekdays = ["Monday","Tuesday","Wednesday",            "Thursday","Friday","Saturday","Sunday"]


# In[112]:


chart1 = alt.Chart(df1).mark_bar().encode(
    x=alt.X('Weekday:N',sort = weekdays),
    y='mean(consumption(B)):Q',
    color= color,
    tooltip=['mean(consumption(B)):Q','house:N']
).properties(
    width=250,
    height=250
).add_selection(
    click
).add_selection(
    click2
).transform_filter(
    click & click2
).properties(width=140,title = 'Avg Consumption by Weekday')

chart3 = alt.Chart(df1).mark_bar().encode(
    x=alt.X('appliance:N',sort = weekdays),
    y='mean(consumption(B)):Q',
    color= color,
    tooltip=['mean(consumption(B)):Q','house:N']
).properties(
    width=250,
    height=250,
).add_selection(
    click
).add_selection(
    click2
).transform_filter(
    click & click2
).properties(width=140,title = 'Avg Consumption by Weekday')

legend = alt.Chart(df1).mark_point().encode(
    y=alt.Y('time:N', axis=alt.Axis(orient='right')),
    color=color
).add_selection(
    selection
)


# In[113]:


final_chart =  chart3 | chart1 | legend


# In[116]:


final_chart = final_chart.properties(title = 'Avg Consumption'
                      ).configure_title(orient='top',anchor='middle')


# In[118]:


final_chart


# In[117]:


final_chart.save('altair.html')


# In[ ]:


os.system(f'jupyter nbconvert altair.ipynb --to python')


# In[125]:


for fname in os.listdir():
    print(fname)


# In[ ]:




