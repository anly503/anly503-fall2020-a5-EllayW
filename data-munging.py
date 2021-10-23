# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 20:42:55 2021

@author: Ella
"""
### import packages:
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import time
import os

### Read the datasets:
#path = os.getcwd()

## read one appliance in one house by seconds. 
## Then aggregates it by day, hour
def paths(house_num = '04', appliance_num = '01'):
    path = os.getcwd()
    new_path = path + '\\'+house_num+'\\'+appliance_num
    app_paths = os.listdir(new_path)
    df = pd.DataFrame(columns = ['consumption','date','hour'])
    for sub_path in app_paths:
        new_file_path = new_path + '\\' + sub_path
        add_df = pd.read_csv(new_file_path,header=None)
        add_df.columns = ['consumption']
        add_df = add_df.groupby(add_df.index // 3600).sum()
        add_df['date'] = sub_path.split('.')[0]
        add_df['hour'] = add_df.index + 1
        df = pd.concat([df,add_df])
    df.reset_index()
    return(df)

## use for loop to apply the function to all appliances in one house
def final(house_num = '04'):
    apps_04 = ['Fridge','Kitchen appliances',\
                       'Lamp','Stereo and laptop',\
                           'Freezer','Tablet','Entertainment','Microwave']
    apps_05 = ['Tablet','Coffee machine','Fountain','Microwave',\
               'Fridge','Entertainment','PC','Kettle']
    apps_06 = ['Lamp','Laptop','Router','Coffee machine',\
               'Entertainment','Fridge','Kettle']
    apps_num = 'apps_'+house_num
    
    df = pd.DataFrame()
    for i in range(1,len(apps_num)+1):
        app_num = '0'+str(i)
        app_name = eval(apps_num)[i-1]
        locals()[app_name] = paths(house_num,app_num)
        locals()[app_name]['appliance'] = app_name
        df = pd.concat([df,locals()[app_name]])
    df.loc[df.consumption < 0,'consumption'] = 0
    return(df)

## then generate such dataset for all the house -- 04,05,06
house_04 = final()
house_05 = final('05')
house_06 = final('06')

def time(df):
    df.loc[(df.hour>5) & (df.hour<=12),'time'] = 'Morning'
    df.loc[(df.hour>12) & (df.hour<=17),'time'] = 'Afternoon'
    df.loc[(df.hour>17) & (df.hour<=21),'time'] = 'Evening'
    df.loc[((df.hour>21) & (df.hour<=24)) | ((df.hour>0) & (df.hour<=5)),\
           'time'] = 'Night'
    df2 = df.groupby(['date','appliance','time'],as_index=False).agg({'date':'last',
                                                      'appliance':'last',
                                                    'time':'last',
                                                    'consumption':'sum'})
    return(df2)

## Now take all 3 house datasets as inputs and create the final dataset:
l0 = ['house'+'_0'+str(i) for i in [4,5,6]]
def one_set(data_list):
    df = pd.DataFrame()
    for ds in data_list:
        add = time(eval(ds))
        add['house'] = ds.split('_')[1]
        df = pd.concat([df,add])
    return(df)

plot_data = one_set(l0)
plot_data = plot_data.reset_index()


## now split the date into weekday and month
weekdays = ["Monday","Tuesday","Wednesday",\
            "Thursday","Friday","Saturday","Sunday"]
months = ['January', 'February', 'March', 'April',\
          'May', 'June', 'July', 'August', 'September',\
              'October', 'November', 'December']

convert_2_mths = lambda x:months[int(x-1)]
convert_2_wds = lambda x:weekdays[int(x)]

plot_data.date = pd.to_datetime(plot_data.date)
plot_data['Month'] = plot_data.date.dt.month
plot_data['Weekday'] = plot_data.date.dt.weekday
plot_data = plot_data.dropna()
plot_data['Weekday'] = plot_data['Weekday'].apply(convert_2_wds)
plot_data['Month'] = plot_data['Month'].apply(convert_2_mths)
plot_data['date'] = plot_data.date.dt.date

plot_data.to_csv('plot-data.csv',index=False)
