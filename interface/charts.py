import glob
import pandas as pd
import folium
from folium import plugins

def get_historical_data(hub,start_date,end_date):
    start_date = pd.to_datetime(start_date,dayfirst=True).date()
    end_date = pd.to_datetime(end_date,dayfirst=True).date()
    path = r'../best_allocation/data'
    filenames = glob.glob(path + "/*-demanda.csv")

    dfs = []
    for filename in filenames:
        dfs.append(pd.read_csv(filename))

    # Concatenate all data into one DataFrame
    big_frame = pd.concat(dfs, ignore_index=True)
    
    #Transform all column names into lower case
    big_frame.columns = [x.lower() for x in big_frame.columns]
    big_frame = big_frame[big_frame['hub']==hub][['event_date','latitude','longitude']]
    
    big_frame['event_date']=pd.to_datetime(big_frame['event_date'])
    big_frame['event_date']=big_frame['event_date'].dt.date
    
    big_frame=big_frame[(big_frame['event_date']>=start_date)&(big_frame['event_date']<=end_date)]
    
    return big_frame


def get_hubs_coordinates(hub):
    hubs_df = pd.read_csv('../best_allocation/data/suplementar/hubs locations.csv',sep=';')
    hubs_df = hubs_df[hubs_df['hub']==hub]
    return [hubs_df.iloc[0]['Latitude'],hubs_df.iloc[0]['Longitude']]

def show_evolution(df,hub,tiles= "cartodbpositron",min_zoom=5, zoom_start=11, max_zoom=40,radius=3,min_speed=6):

    hub_coordinates = get_hubs_coordinates(hub)

    df['date']=pd.DatetimeIndex(df['event_date']).date

    heat_df = df    [['date','latitude','longitude']]
    heat_df['weight']=1/len(heat_df)
    
    heat_df['date'] = heat_df['date'].sort_values(ascending=True)

    dates_list = heat_df['date'].unique()
    data_list = []
    for _, d in heat_df.groupby('date'):
       data_list.append([[row['latitude'], row['longitude'], row['weight']] for _, row in d.iterrows()])

    new_map = folium.Map(location=hub_coordinates, tiles=tiles,min_zoom=min_zoom, zoom_start=zoom_start, max_zoom=max_zoom)
    
    hm = plugins.HeatMapWithTime(data_list, auto_play=True,max_opacity=2,min_opacity=0.4,radius=radius,min_speed=min_speed)
    hm.add_to(new_map)
    return new_map

def show_heatmap(df,hub):

    heat_df=df[['latitude','longitude']]

    hub_coordinates = get_hubs_coordinates(hub)

    new_map = folium.Map(location=hub_coordinates,tiles= "cartodbpositron",min_zoom=5, zoom_start=11, max_zoom=40)
    hm = plugins.HeatMap(heat_df,radius=3,min_opacity=0.4,max_opacity=2,blur=4)
    hm.add_to(new_map)
    return new_map
