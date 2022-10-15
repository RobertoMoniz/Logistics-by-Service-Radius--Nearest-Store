from fastapi import FastAPI
from api.ml_logic.optimization import best_number_of_employees, best_areas
import pandas as pd
import random
import math

app = FastAPI()

# Define a root `/` endpoint
@app.get('/optimize')
def optimize(available_employees,work_hours=8,service_time=0.5,conversion_rate=0.2):
    
    #Transforming from string
    available_employees=float(available_employees)
    work_hours=float(work_hours)
    service_time=float(service_time)
    conversion_rate=float(conversion_rate)
    
    demmand=300
        
    n_employees = best_number_of_employees(demmand,conversion_rate,work_hours,service_time)
    areas = best_areas(available_employees)
    
    response = {'necessary_employees':n_employees,'suggested_areas':areas}
    
    return response
