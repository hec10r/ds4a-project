import os
import pandas as pd
from sqlalchemy import create_engine
import json

import settings

engine = create_engine(f'postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}')

def load_crime_data():
    if os.path.exists('data/crime.csv'):
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


def filter_crime(df_crime, crime_type, years):
    if years is None: 
        years = []
    if crime_type is None:
        crime_type = []

    df_crime_filtered = df_crime.copy()
    if (len(crime_type) == 0 or len(years) == 0):
        if ( len(crime_type) == 0 and len(years) != 0):
            filter = (  df_crime_filtered['date_year'].isin(years)  )
        elif (len(crime_type) != 0 and len(years) == 0):
            filter = ( df_crime_filtered['crimen'].isin(crime_type) )
        else:
            filter = None
    else:
        filter = ( df_crime_filtered['crimen'].isin(crime_type)  ) & (df_crime_filtered['date_year'].isin(years)  )
    
    if (filter is not None):
        df_crime_filtered = df_crime_filtered[filter]

    df_crime_filtered = df_crime_filtered.groupby('barrio_id').agg({'barrio':'count'}).reset_index(drop=False).rename(columns={'barrio':'total'})

    print(df_crime_filtered)

    return df_crime_filtered