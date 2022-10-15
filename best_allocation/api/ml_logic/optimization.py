import pandas as pd
import random
import math

def best_number_of_employees(demmand,conversion_rate,work_hours=8,service_time=0.5):
    employees = math.ceil(demmand*conversion_rate*service_time/work_hours)
    return employees

def best_areas(available_employees):
    available_employees=int(math.ceil(available_employees))
    best_areas = {'suggested_area_id':[]}
    for i in range(available_employees):
        best_areas['suggested_area_id'].append(random.randint(0,9))
    return best_areas

