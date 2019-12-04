import os
import pandas as pd
from sqlalchemy import create_engine
import json

import settings

engine = create_engine(f'postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}')

def load_crime_data(load_from_db=False):
    if (os.path.exists('data/crime.csv') and (not load_from_db)):
        df_crime = pd.read_csv('data/crime.csv', sep=',')
    else:
        df_crime = pd.read_sql("SELECT * FROM vw_crime", engine.connect() )
        df_crime.to_csv('data/crime.csv', sep=',', header=True)
    return df_crime

def load_barrio_dane():
    if os.path.exists('data/barrio.csv'):
        df_barrio = pd.read_csv('data/barrio.csv', sep=',', dtype={'setu_ccnct':str})
    else:
        df_barrio = pd.read_sql("SELECT * FROM barrio_dane", engine.connect(), parse_dates=('OCCURRED_ON_DATE',))
        df_barrio.to_csv('data/barrio.csv', sep=',', header=True)
    return df_barrio

def load_baq_polyg():
    with open('data/barrios_ex.json') as f:
        barrio_polyg = json.loads(f.read())
    return barrio_polyg

def load_years(df_crime):
    return df_crime['date_year'].drop_duplicates().reset_index(drop=False).sort_values(by='date_year', ascending=True)

def load_crime_type(df_crime):
    return df_crime['crimen'].drop_duplicates().reset_index(drop=False)

def load_localidad(df_crime):
    return df_crime['localidad'].drop_duplicates().reset_index(drop=False).sort_values(by='localidad', ascending=True)

def filter_crime(df_crime, crime_type, years, borough):
    if years is None: 
        years = []
    if crime_type is None:
        crime_type = []
    if borough is None:
        borough = []
    
    df_crime_filtered = df_crime.copy()
    
    filter = ( df_crime_filtered['date_year'].isin(years) | (len(years) == 0) ) &\
             ((df_crime_filtered['crimen'].isin(crime_type)) | (len(crime_type) == 0) ) &\
             ((df_crime_filtered['localidad'].isin(borough)) | (len(borough) == 0))

    df_crime_filtered = df_crime_filtered[filter]
    
    #print(df_crime_filtered.head())
    df_crimes_by_barrio = get_crimes_by_barrio( df_crime_filtered )
    df_crimes_by_crimetype_and_year = get_crimes_by_crimetype_and_year( df_crime_filtered )
    df_crimes_by_localidad = get_crimes_by_localidad( df_crime_filtered )
    df_crimes_by_localidad_and_year = get_crimes_by_localidad_and_year( df_crime_filtered )
    df_crimes_by_localidad_and_weekday = get_crimes_by_localidad_and_weekday( df_crime_filtered )

    return df_crime_filtered, df_crimes_by_barrio, df_crimes_by_crimetype_and_year, df_crimes_by_localidad, df_crimes_by_localidad_and_year, df_crimes_by_localidad_and_weekday

def get_crimes_by_barrio( df ):
    df = df.groupby(['barrio_id', 'barrio']).agg({'crimen':'count', 'total_personas':'max'}).reset_index(drop=False)
    df.columns = ['barrio_id', 'barrio', 'total', 'total_personas']
    df['crime_ratio'] = df['total'] / df['total_personas']

    return df

def get_crimes_by_localidad_and_weekday( df ):
    df = df.groupby(['localidad', 'date_dow']).agg({'crimen':'count'}).reset_index(drop=False)
    df.columns = ['localidad', 'dia_semana', 'total']
    return df

def get_crimes_by_localidad( df ):
    df = df.groupby(['localidad']).agg({'crimen':'count'}).reset_index(drop=False)
    df.columns = ['localidad', 'total']
    return df


def get_crimes_by_crimetype_and_year( df ): 
    df = df.groupby(['crimen', 'date_year']).agg({'barrio': 'count'}).reset_index(drop=False)
    df.columns = ['crimen', 'year', 'total']
    return df

def get_crimes_by_localidad_and_year( df ):
    df = df.groupby(['localidad', 'date_year']).agg({'barrio': 'count'}).reset_index(drop=False)
    df.columns = ['localidad', 'year', 'total']
    return df

def get_color(impact):
    thresholds = [3, 5, 7, 9, 11]
    colors = ["#21c7ef", "#76f2ff", "#76f2ff", "#ff6969", "#ff1717"]
    for threshold, color in zip(thresholds, colors):
        if impact < threshold:
            return color
    #return a defalut color if impact value is not in thresholds
    return "#21c7ef" 