import os
import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objs as go

from sqlalchemy import create_engine
import json


import datetime
from datetime import datetime as dt
import settings

pd.options.mode.chained_assignment = None

#==========================CONSTANTS==========================
DAYS_OF_THE_WEEK = ['Domingo', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
MONTHS = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
engine = create_engine(f'postgresql://{settings.DB_USER}:{settings.DB_PASS}@{settings.DB_HOST}/{settings.DB_NAME}')

tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': '#31302F',
    'font-color': '#F4FCFA',
    'font-size' : '10px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'fontWeight': 'bold',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': 'rgba(255, 255, 255, 0.637)',
    'color': 'black',
    'padding': '6px',
    'font-size' : '10px'
}

#==========================FUNCTIONS==========================
def load_crime_data(load_from_db=False):
    if (os.path.exists('data/crime.csv') and (not load_from_db)):
        df_crime = pd.read_csv('data/crime.csv', sep=',')
    else:
        df_crime = pd.read_sql("SELECT * FROM vw_crime", engine.connect() )
        df_crime.to_csv('data/crime.csv', sep=',', header=True)
    
    df_crime['barrio'] = df_crime['barrio'].apply( lambda field: field.capitalize() )
    df_crime['crimen'] = df_crime['crimen'].apply( lambda field: field.capitalize() )
    df_crime["fecha_hora"] = df_crime["fecha_hora"].apply(lambda field: dt.strptime(field, "%Y-%m-%d %H:%M:%S"))
    df_crime["date_horaampm"] = df_crime["fecha_hora"].apply(lambda x: dt.strftime(x, "%I %p"))  # Datetime -> int(hour) + AM/PM

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

    df_crimes_by_barrio = get_crimes_by_barrio( df_crime_filtered )
    df_crimes_by_crimetype_and_year = get_crimes_by_crimetype_and_year( df_crime_filtered )
    df_crimes_by_localidad = get_crimes_by_localidad( df_crime_filtered )
    df_crimes_by_localidad_and_year = get_crimes_by_localidad_and_year( df_crime_filtered )
    df_crimes_by_weekday = get_crimes_by_weekday( df_crime_filtered )
    df_crimes_by_month = get_crimes_by_month( df_crime_filtered )
    df_crimes_by_crimetype_and_localidad = get_crimetype_by_localidad( df_crime_filtered )


    return df_crime_filtered,\
           df_crimes_by_barrio,\
           df_crimes_by_crimetype_and_year,\
           df_crimes_by_crimetype_and_localidad,\
           df_crimes_by_localidad,\
           df_crimes_by_localidad_and_year,\
           df_crimes_by_weekday,\
           df_crimes_by_month

def get_crimes_by_barrio( df ):
    df = df.groupby(['barrio', 'localidad']).agg({'crimen':'count', 'total_personas':'max'}).reset_index(drop=False)
    df.columns = ['barrio', 'localidad' ,'total', 'total_personas']
    df['crime_ratio'] =  np.log(df['total']) / np.log(df['total_personas'])

    return df

def get_crimetype_by_localidad( df ): 
    df = df.groupby(['localidad', 'crimen']).agg({'barrio': 'count'}).reset_index(drop=False) 
    df.columns = ['localidad', 'crimen', 'total']
    return df


def get_crimes_by_month( df ):
    df = df.groupby(['date_month']).agg({'crimen':'count'}).reset_index(drop=False)
    df.columns = ['month', 'total']
    return df


def get_crimes_by_weekday( df ):
    df = df.groupby(['date_dow']).agg({'crimen':'count'}).reset_index(drop=False)
    df.columns = ['dia_semana', 'total']
    return df

def get_crimes_by_localidad( df ):
    df = df.groupby(['localidad']).agg({'crimen':'count'}).reset_index(drop=False)
    df.columns = ['localidad', 'total']
    return df


def get_crimes_by_crimetype_and_year( df ): 
    df['period'] = df['fecha_hora'].apply(lambda field: dt.strftime(field, '%Y-%m'))
    #df = df.groupby(['crimen', df['fecha'].dt.to_period('M')]).agg({'barrio': 'count'}).reset_index(drop=False) 
    df = df.groupby(['crimen', 'period']).agg({'barrio': 'count'}).reset_index(drop=False) 
    df.columns = ['crimen', 'period', 'total']
    return df

def get_crimes_by_localidad_and_year( df ):
    df = df.groupby(['localidad', 'period']).agg({'barrio': 'count'}).reset_index(drop=False)
    df.columns = ['localidad', 'period', 'total']
    return df

# ==========================HOLIDAYS GRAPHS==========================
def get_crimes_by_holiday( df ):
    df['festivo_texto'] = df.apply(lambda row: get_type_of_holiday(row), axis=1)
    df = df.groupby(['festivo_texto']).agg({'crimen':'count'}).reset_index(drop=False)
    df.columns = ['festivo', 'total']
    return df

def get_type_of_dow( row ):
    type_of_dow = np.nan

    dow = int(row['date_dow'])

    if row['festivo'] == True:
        type_of_dow = 'Festivo'
    elif ( dow == 0 or dow == 6 ):
        type_of_dow = 'Fin de semana (S-D)'
    else:
        type_of_dow = 'Laboral (L-V)'

    return type_of_dow

def get_type_of_holiday( row ):
    holiday_text = np.nan
    festividad = str(row['festividad'])

    if row['festivo'] == True:
        if festividad != 'nan':
            holiday_text = row['festividad']

    return holiday_text

# ==========================LAYOUT FUNCTIONS==========================
def get_color(impact):
    thresholds = [3, 15, 29, 37, 75]
    colors = ["#21C7EF", "#76F2FF", "#76F2FF", "#FF6969", "#FF1717"]
    for threshold, color in zip(thresholds, colors):
        if impact < threshold:
            return color
    #return a defalut color if impact value is not in thresholds
    return "#21c7ef" 

def get_layout(graph_title, margin,  xtickmode='linear', xtickangle='auto', xtickformat=None, ytickformat=None,  bar_mode=None, dtick=1):
    if xtickangle == 'auto':
        x = dict(tickmode=xtickmode, dtick=dtick, tickformat=xtickformat)
    else:
        x = dict(tickmode=xtickmode, dtick=dtick, tickangle=xtickangle, tickformat=xtickformat)
    
    y = dict(tickformat=ytickformat)
    
    return go.Layout(
                margin=margin,
                plot_bgcolor='#323130',
                paper_bgcolor='#323130',
                font_color='#FFFFFF',
                title=graph_title,
                xaxis=x,
                yaxis=y,
                barmode=bar_mode
            )

def create_heatmap(df, x_axis, y_axis, x_column_name, y_column_name,  margin, height='auto', x_index = False, y_index = False, title='', xtickangle=-45):
    df['numero_crimenes'] = 1
    
    z = np.zeros((len(y_axis), len(x_axis)))
    annotations = []

    for ind_y, y_val in enumerate(y_axis):
        if not y_index:
            filtered = df[df[y_column_name] == y_val]
        else:
            filtered = df[df[y_column_name] == ind_y]

        for ind_x, x_val in enumerate(x_axis):
            if not x_index:
                sum_of_record = filtered[filtered[x_column_name] == x_val]['numero_crimenes'].sum()
            else:
                sum_of_record = filtered[filtered[x_column_name] == ind_x]['numero_crimenes'].sum()

            z[ind_y][ind_x] = sum_of_record

            annotation_dict = dict(
                showarrow=False,
                text="<b>" + str(sum_of_record) + "<b>",
                xref="x",
                yref="y",
                x=x_val,
                y=y_val,
                font=dict(family="sans-serif"),
            )

            annotations.append(annotation_dict)

    # Heatmap
    hovertemplate = "<b> %{y}  %{x} <br><br> %{z} incidentes"

    data, layout =  get_data_and_layout_heatmap(  x_axis, y_axis, z, hovertemplate, annotations, margin, height, title, xtickangle)
    return {"data": data, "layout": layout}

def get_data_and_layout_heatmap(x_axis, y_axis, z, hovertemplate, annotations, margin, height='auto', title='', xtickangle=-45): 
    data = [
        dict(
            x=x_axis,
            y=y_axis,
            z=z,
            type="heatmap",
            name="",
            hovertemplate=hovertemplate,
            showscale=True,
            colorscale=[[0, '#CCBB37'], [0.2, '#7ED338'], [0.4, '#2EAD68'], [0.6, '#1D8177'], [0.8,'#27547C'], [0.9, '#352A6C'], [1, '#340142']]
        )
    ]

    layout = dict(
                margin=margin,
                height=height,
                title=title,
                plot_bgcolor='#323130',
                paper_bgcolor='#323130',        
                modebar={"orientation": "v"},
                font=dict(family="Open Sans", color='#FFFFFF'),
                annotations=annotations,
                xaxis=dict(
                    side="top",
                    ticks="",
                    ticklen=2,
                    tickangle=xtickangle,
                    tickfont=dict(family="sans-serif"),
                    tickcolor="#FFFFFF",
                ),
                yaxis=dict(
                    side="left", ticks="", tickfont=dict(family="sans-serif"), ticksuffix=" "
                ),
                hovermode="closest",
                showlegend=True
            )
    
    return data, layout