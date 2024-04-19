#from utils import get_mean_speed
from tabulate import tabulate
import pandas as pd
import math

width_px, height_px = 1920, 1080
width_cm, height_cm = 114, 64
px_per_cm = max(width_px/width_cm, height_px/height_cm) #on prend la plus grosse erreur

target_05 = pd.read_csv('InfiniteV_Target_AlDu00_Date19-04-2024_Time15-21-16_Target_TS0.5.csv', sep=';')
target_09 = pd.read_csv('InfiniteV_Target_AlDu00_Date19-04-2024_Time15-20-28_Target_TS0.9.csv', sep=';')
pupil_09 = pd.read_csv('Infini_Pupil_AlDu00_Date19-04-2024_Time15-20-07_Target_0.9.csv', sep=';')
pupil_05 = pd.read_csv('Infini_Pupil_AlDu00_Date19-04-2024_Time15-19-34_Target_0.5.csv', sep=';')
lens_09 = pd.read_csv('Infini_Lens_AlDu00_Date19-04-2024_Time15-18-30_Target_TS0.9.csv', sep=';')
lens_05 = pd.read_csv('Infini_Lens_AlDu00_Date19-04-2024_Time15-17-43_Target_TS0.5.csv', sep=';')


def get_mean_speed(data) :
    """
        Returns mean speed (px/s) of the moving object recorded in data('time','x', 'y')
        data(str): dataframe
    """
    data['time'] = pd.to_datetime(data['time'], unit='s')

    distances_per_second = []
    for second in pd.date_range(data['time'].min(), data['time'].max(), freq='S')  :
        second_data = data[(data['time'] >= second) & (data['time'] < second + pd.Timedelta(seconds=1))]  # Filter data for the second
        distance = math.sqrt((second_data.iloc[0]['x']-second_data.iloc[-1]['x'])**2 +(second_data.iloc[0]['y']-second_data.iloc[-1]['y'])**2) #/ px_per_cm
        distances_per_second.append(distance)
        print(second_data.iloc[0], second_data.iloc[-1])
    
    return sum(distances_per_second[:-2])/(len(distances_per_second)-1)#on exclut la dernière seconde qui peut ne pas être complète

print(tabulate([
    ['Target', '0.5', get_mean_speed(target_05), get_mean_speed(target_05)/px_per_cm],
    ['Target', '0.9', get_mean_speed(target_09), get_mean_speed(target_09)/px_per_cm ],
    ['Pupil', '0.5', get_mean_speed(pupil_05), get_mean_speed(pupil_05)/px_per_cm],
    ['Pupil', '0.9', get_mean_speed(pupil_09), get_mean_speed(pupil_09)/px_per_cm ],
    ['Lens', '0.5', get_mean_speed(lens_05), get_mean_speed(lens_05)/px_per_cm],
    ['lens', '0.9', get_mean_speed(lens_09), get_mean_speed(lens_09)/px_per_cm ]
    ],
    headers=['Type', 'TimeStep', 'px/s', 'cm/s'], tablefmt='orgtbl') )