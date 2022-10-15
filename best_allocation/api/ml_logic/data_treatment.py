import pandas as pd
import glob
import os

def get_data(source='csv'):

    # Read the csv files located in data folder
    if source == 'csv':
        path = r'../best_allocation/data'
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

def partition_data(big_frame,type='HUB'):
    try:
        #Return a dictionary with the data from all the hubs, cities or districts
        partitioned_data = {}
        for i in big_frame[type]:
            partitioned_data=big_frame[big_frame[type]==i]
        return partitioned_data
    except:
        print("Only HUB, city or districts are acceptes as entries")
        return None
    
