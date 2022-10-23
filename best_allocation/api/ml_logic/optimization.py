import pandas as pd
import random
import math
import numpy as np


def best_number_of_employees(demmand,conversion_rate,work_hours=8,service_time=0.5):
    demmand = np.array(demmand['value']).sum()
    employees = math.ceil(demmand*conversion_rate*service_time/work_hours)
    return employees


def best_areas(daily_demmand,available_employees,conversion_rate=0.5,work_hours=8,service_time=0.5):
    
    daily_demmand = pd.DataFrame(daily_demmand)
    available_employees=int(math.ceil(available_employees))
    services = work_hours/service_time
    
    best_areas = {'area_id':[],'predicted_demmand':[]}
    daily_demmand['true_demmand']=daily_demmand['value'].apply(lambda x: x*conversion_rate)

    
    for i in range(available_employees):
        max_demmand = daily_demmand['true_demmand'].max()
        area = daily_demmand[daily_demmand['true_demmand']==max_demmand]['area'].values[0]
        daily_demmand['true_demmand']=daily_demmand['true_demmand'].apply(lambda x: x-services if x==max_demmand else x)
        best_areas['area_id'].append(area)
        best_areas['predicted_demmand'].append(max_demmand)    
    return best_areas

