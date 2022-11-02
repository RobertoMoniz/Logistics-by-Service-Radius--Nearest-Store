from fastapi import FastAPI
from api.ml_logic.data_treatment import get_data, partition_data, get_evolution
from api.ml_logic.area_definition import define_area
from api.ml_logic.optimization import best_number_of_employees, best_areas
from api.ml_logic.demmand_forecasting import prophet_predict, predict_demmand
import numpy as np
import pandas as pd
import random
import math
import datetime as dt

app = FastAPI()

# Define a root `/` endpoint
@app.get('/optimize')
def optimize(hub,date,available_employees,work_hours=8,service_time=0.5,conversion_rate=0.2):
    
    #Transforming f rom string
    date=pd.to_datetime(date,dayfirst=True)
    available_employees=float(available_employees)
    work_hours=float(work_hours)
    service_time=float(service_time)
    conversion_rate=float(conversion_rate)
    
    print('Collecting data')
    df=get_data()

    print('Partitioning data')
    df=partition_data(df, hub)

    print('Spliting df')
    df,centers=define_area(df,hub)

    print('Predicting the demmand')
    prediction = prophet_predict(df)

    print('Predicting daily demmand')
    daily_demmand = predict_demmand(prediction, date)
    
    print('Defining the number of employees')
    n_employees = best_number_of_employees(daily_demmand,conversion_rate,work_hours,service_time)

    print('defining the best areas')
    areas = best_areas(daily_demmand,available_employees,conversion_rate,work_hours,service_time)
    areas_df = pd.DataFrame(areas)
    
    response = {'necessary_employees':n_employees,'suggested_areas':areas_df.to_dict('index'),'centers': pd.DataFrame(centers).to_dict('index')}
    
    return response


@app.get('/historic')
def get_historic_data(hub,start_date,end_date):
    print('initial statements')
    start_date = pd.to_datetime(start_date,dayfirst=True).date()
    end_date = pd.to_datetime(end_date,dayfirst=True).date()
    print('getting data')
    df = get_data()
    print('partitioning data')
    df,latitude,longitude = (get_evolution(df, hub, start_date, end_date))
    print('dropping na')
    df.dropna(inplace=True)
    print('creating response')
    response = {'data':df.to_dict('index'),'hub_latitude':latitude,'hub_longitude':longitude}
    return response
