import pandas as pd
import pickle
from sklearn.cluster import KMeans

def define_area(partitioned_data,hub):

    filename = f'./api/ml_logic/models/model_{hub}.sav'
    model = pickle.load(open(filename, 'rb'))

    partitioned_data['area_id']=model.predict(partitioned_data[['latitude','longitude']])

    return partitioned_data, model.cluster_centers_

