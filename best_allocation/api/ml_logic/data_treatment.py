import pandas as pd
import glob
import os

def get_hub_centers(source='csv'):
    if source=='csv':
        file = r'data/suplementar/hubs locations.csv'
        hub_centers_df = pd.read_csv(file,sep=';')
        return hub_centers_df.to_dict()
    return 'format not supported yet'
        
def get_data(source='csv'):

    # Read the csv files located in data folder
    if source == 'csv':
        path = r'data'
        filenames = glob.glob(path + "/*-demanda.csv")

        dfs = []
        for filename in filenames:
            dfs.append(pd.read_csv(filename))

        # Concatenate all data into one DataFrame
        big_frame = pd.concat(dfs, ignore_index=True)
        
        #Transform all column names into lower case
        big_frame.columns = [x.lower() for x in big_frame.columns]
        return big_frame
    
    print("No Data Available for this source")
    return None

def partition_data(big_frame,value,type='hub'):
    try:
        #Return a dictionary with the data from all the hubs, cities or districts
        partitioned_data = big_frame[big_frame[type]==value]
        return partitioned_data
    except:
        print("Only hub, city or districts are acceptes as entries")
        return None
    
def get_evolution(df,hub,start_date,end_date):
    df['event_date']=pd.to_datetime(df['event_date']).dt.date
    df=df[(df['event_date']>=start_date)&(df['event_date']<=end_date)][['event_date','latitude','longitude']]
    hubs_df = pd.DataFrame(get_hub_centers())
    hubs_df = hubs_df[hubs_df['hub']==hub]
    hub_latitude = hubs_df['Latitude'].min()
    hub_longitude = hubs_df['Longitude'].min()
    df['event_date']=df['event_date'].astype(str)
    df['latitude']=df['latitude'].astype(str)
    df['longitude']=df['longitude'].astype(str)

    return df,hub_latitude,hub_longitude
