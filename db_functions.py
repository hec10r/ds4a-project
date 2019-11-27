import settings
from sqlalchemy import create_engine
import pandas as pd
import json
import os

engine = create_engine(f'postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}')
def load_crime_data():
    if os.path.exists('data/crime.csv'):
        df = pd.read_csv('data/crime.csv', sep=',')
    else:
        df = pd.read_sql("SELECT * FROM vw_crime", engine.connect() )
        df.to_csv('data/crime.csv', sep=',', header=True)
    return df

def load_barrio_dane():
    return pd.read_sql("SELECT * FROM barrio_dane", engine.connect(), parse_dates=('OCCURRED_ON_DATE',))

def load_baq_polyg():
    with open('data/barrios_ex.json') as f:
        geojson = json.loads(f.read())
    return geojson