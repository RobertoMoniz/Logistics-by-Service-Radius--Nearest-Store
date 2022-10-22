import pandas as pd
import numpy as np
import warnings
from prophet import Prophet

warnings.filterwarnings('ignore')

def prophet_predict(df):
    #predict de demmand for each 
    df['event_date'] = pd.to_datetime(df['event_date']).dt.date    

    df = df[['event_date','area_id','user_id']].groupby(by=['event_date','area_id'],as_index=False).count()
    df = df.rename(columns={'event_date': 'ds', 'user_id': 'y'})

    max_date = df['ds'].max()

    prophet_predict = {'area': [], 'resultado': [], 'modelo': [], 'modelofuturo': []}

    areas = df['area_id'].unique()
    areas.sort()

    for area in areas:
        
        prophet = Prophet()
        area_df = df[df['area_id']==area]
        area_df.drop(columns='area_id', inplace=True)
        saida_fit = prophet.fit(area_df)
        saida_futuro = prophet.make_future_dataframe(periods=20, freq='D', include_history=True)
        saida_predict = prophet.predict(saida_futuro)
        prophet_predict['modelo'].append(prophet)
        prophet_predict['modelofuturo'].append(saida_futuro)
        prophet_predict['area'].append(area)
        prophet_predict['resultado'].append(saida_predict)    

    return prophet_predict

def predict_demmand(prophet_predict,date):
    demmand = {'area':[],'value':[]}
    
    for area in prophet_predict['area']:
        df = prophet_predict['resultado'][area]
        demmand['area'].append(area)
        try:
            demmand['value'].append(df.loc[df['ds'].dt.date==date]['yhat'].values[0])
        except:
            demmand['value'].append(0)
            
    return demmand
