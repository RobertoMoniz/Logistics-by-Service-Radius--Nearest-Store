import pandas as pd
import pickle
from sklearn.cluster import KMeans

def define_area(partitioned_data,hub):
    #for each partitioned_data, load the model for its hub and assign an area to this variable
    for data in partitioned_data:
        filename = f'../best_allocation/api/ml_logic/models/model_{hub}.sav'
        model = pickle.load(open(filename, 'rb'))

        partitioned_data['area_id']=model.predict(partitioned_data[['latitude','longitude']])

    return partitioned_data

