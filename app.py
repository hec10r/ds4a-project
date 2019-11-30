import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from plotly import graph_objs as go
import plotly.graph_objects as go

import pandas as pd
import numpy as np

import settings
from db_functions import *
import json


tabs_styles = {
    'height': '30px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#31302F',
    'font-color': '#F4FCFA',
    'font-size' : '10px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#1f2c56',
    'color': 'white',
    'padding': '6px',
    'font-size' : '10px'
}


app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


df_crime = load_crime_data()
df_barrio = load_barrio_dane()
df_crime_type = load_crime_type(df_crime)
df_years = load_years(df_crime)
geo_json = load_baq_polyg()

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
                        html.H2("Crimenes en Barranquilla"),
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
                        dcc.Tabs(
                            id="tabs-styled-with-inline",
                            style=tabs_styles,
                            value='tab-1', 
                            children=[
                                dcc.Tab(
                                    label='Mapa', 
                                    value='tab-1',
                                    style=tab_style, 
                                    selected_style=tab_selected_style,
                                    children=[
                                        dcc.Graph(
                                            id='baq-maps'
                                        ),
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.Div(
                                                    className='column_fifty_perc',
                                                    children=[
                                                        dcc.Graph(id="histogram1")
                                                    ]
                                                ),
                                                html.Div(
                                                    className='column_fifty_perc',
                                                    children=[
                                                        dcc.Graph(id="histogram2")
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dcc.Tab(
                                    label='Más información',
                                    value='tab-2',
                                    style=tab_style, 
                                    selected_style=tab_selected_style,
                                    children=[
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.Div(
                                                    className='column_fifty_perc',
                                                    children=[
                                                        dcc.Graph(id="histogram3")
                                                    ]
                                                ),
                                                html.Div(
                                                    className='column_fifty_perc',
                                                    children=[
                                                        dcc.Graph(id="histogram4")
                                                    ]
                                                )
                                            ]
                                        ),
                                        html.Div(
                                            className='row',
                                            children=[
                                                html.Div(
                                                    className='column_fifty_perc',
                                                    children=[
                                                        dcc.Graph(id="histogram5", className="fifty_percent")
                                                    ]
                                                ),
                                                html.Div(
                                                    className='column_fifty_perc',
                                                    children=[
                                                        dcc.Graph(id="histogram6", className="fifty_percent")
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                ),
                            ]
                        ),
                        html.Div(id='tabs-content-inline'),
                    ],
                ),
            ],
        )
    ]
)
@app.callback(
    [
        dash.dependencies.Output('baq-maps', 'figure'),
        dash.dependencies.Output('histogram1', 'figure'),
        dash.dependencies.Output('histogram2', 'figure'),
    ],
    [
        dash.dependencies.Input('crimetype-dropdown', 'value'),
        dash.dependencies.Input('year-selector', 'value'),
    ]
)
def update_map(crime_type, years):
    n_of_records = 10
    df_crime_filtered = filter_crime(df_crime, crime_type, years)
    df_crime_sorted_by_ratio = df_crime_filtered.sort_values(by='crime_ratio', ascending=False)
    df_crime_sorted_by_total = df_crime_filtered.sort_values(by='total', ascending=False)
    return {
        'data': [ go.Choroplethmapbox(
                        geojson=geo_json,
                        locations=df_crime_filtered['barrio_id'],
                        z=df_crime_filtered['total'],
                        colorscale='blues',
                        colorbar_title="Indicar metrica",
                        text=df_crime_filtered['barrio']
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
    }, {
        'data': [
            {'x': df_crime_sorted_by_ratio['barrio'].head(n_of_records), 'y': df_crime_sorted_by_ratio['crime_ratio'].head(n_of_records), 'type': 'bar'}
        ],
        'layout': {
            'plot_bgcolor': '#323130',
            'paper_bgcolor':'#323130',
            'font': {
                'color': '#FFFFFF'
            },
            'title': {
                'text': 'Top 5 de Barrios - Crimen vs Población',
            }
        }
    }, {
        'data': [
            {'x': df_crime_sorted_by_total['barrio'].head(n_of_records), 'y': df_crime_sorted_by_total['total'].head(n_of_records), 'type': 'bar'}
        ],
        'layout': {
            'plot_bgcolor': '#323130',
            'paper_bgcolor':'#323130',
            'font': {
                'color': '#FFFFFF'
            },
            'title': {
                'text': 'Top 5 de Barrios - Total crimenes',
            }
        }
    }



if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0')
