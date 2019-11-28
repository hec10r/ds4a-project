import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objs as go
import plotly.graph_objects as go

import pandas as pd
import numpy as np

import settings
import db_functions
import json


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


df_crime = db_functions.load_crime_data()
df_barrio = db_functions.load_barrio_dane()
df_crime_type = db_functions.load_crime_type(df_crime)
df_years = db_functions.load_years(df_crime)
geo_json = db_functions.load_baq_polyg()


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
                        html.H1("Barranquilla - Atlántico"),
                        html.H2("Crimenes 2010 - 2019"),
                        html.P(
                            """Seleccione el año y el tipo de crimen que desea consultar"""
                        ),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id='year-selector',
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
                                            id='crimetype-dropdown',
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
                    ],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id='baq-maps'
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
@app.callback(
    dash.dependencies.Output('baq-maps', 'figure'),
    [
        dash.dependencies.Input('crimetype-dropdown', 'value'),
        dash.dependencies.Input('year-selector', 'value'),
    ]
)
def update_map(crime_type, years):
    df_crime_filtered = db_functions.filter_crime(df_crime, crime_type, years)

    return {
        'data': [ go.Choroplethmapbox(
                        geojson=geo_json,
                        locations=df_barrio['setu_ccnct'],
                        z=df_barrio['dane_area_m2'],
                        colorscale='Viridis',
                        colorbar_title="Indicar metrica"
                    )
                ],
        'layout': go.Layout(
                        autosize=True,
                        margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                        mapbox_style=settings.mapbox_style,
                        mapbox_accesstoken=settings.mapbox_access_token,
                        mapbox_zoom=11,
                        mapbox_center = settings.BAQ_CENTER_COORD,
                    ),
    }

if __name__ == "__main__":
    app.run_server(debug=True)
