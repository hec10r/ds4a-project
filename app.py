import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

import geopandas as gpd

import os
import plotly.graph_objects as go

import settings
import db_functions


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


df_crime = db_functions.load_crime_data()
df = db_functions.load_barrio_dane()
df_crime_type = df_crime['crimen'].drop_duplicates().reset_index(drop=False)
df_years = df_crime['date_year'].drop_duplicates().reset_index(drop=False).sort_values(by='date_year', ascending=True)

geojson = db_functions.load_baq_polyg()


#df["Date/Time"] = pd.to_datetime(df["Date/Time"], format="%Y-%m-%d %H:%M")
#df.index = df["Date/Time"]
#df.drop("Date/Time", 1, inplace=True)
totalList = []
#for month in df.groupby(df.index.month):
#    dailyList = []
#    for day in month[1].groupby(month[1].index.day):
#        dailyList.append(day[1])
#    totalList.append(dailyList)
#totalList = np.array(totalList)

# Layout of Dash App
app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("Barranquilla - Atlántico"),
                        html.H2("Crimenes 2010 - 2019"),
                        html.P(
                            """Seleccione el año y el tipo de crimen que desea consultar"""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id='bar-selector',
                                    options=[
                                        {'label': year, 'value': year} 
                                        for year in df_years['date_year']
                                    ],
                                    multi=True,
                                    placeholder="Periodo",
                                )
                            ],
                        ),
                        # Change to side-by-side for mobile layout
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown for crime types
                                        dcc.Dropdown(
                                            id='location-dropdown',
                                            options=[
                                                {'label': crimen, 'value': crimen} 
                                                for crimen in df_crime_type['crimen']
                                            ],
                                            multi=True,
                                            placeholder="Tipo de crimen",
                                        )
                                    ],
                                ),
                                html.Div(
                                    className="div-for-dropdown",
                                    children=[
                                        # Dropdown to select times

                                    ],
                                ),
                            ],
                        ),
                        html.P(id="total-rides"),
                        html.P(id="total-rides-selection"),
                        html.P(id="date-value"),
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id='baq-maps',
                            figure={
                                'data': [
                                    go.Choroplethmapbox(
                                        geojson=geojson,
                                        locations=df['setu_ccnct'],
                                        z=df['dane_area_m2'],
                                        colorscale='Viridis',
                                        colorbar_title="Área (m2)"
                                    )
                                ],
                                'layout': 
                                    go.Layout(
                                        autosize=True,
                                        margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                                        showlegend=False,                                        
                                        paper_bgcolor='rgba(0,0,0,0)',
                                        plot_bgcolor='rgba(0,0,0,0)',                                      
                                        mapbox_style=settings.mapbox_style,
                                        mapbox_accesstoken=settings.mapbox_access_token,
                                        mapbox_zoom=10,
                                        mapbox_center = settings.BAQ_CENTER_COORD,
                                    ),
                                    
                            }

                        ),
                        html.Div(
                            className="text-padding",
                            children=[
                                "Select any of the bars on the histogram to section data by time."
                            ],
                        ),
                        #dcc.Graph(id="histogram"),
                    ],
                ),
            ],
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
